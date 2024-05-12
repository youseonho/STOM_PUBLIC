import re
import time
import sqlite3
import binance
import asyncio
import pyupbit
import pandas as pd
from multiprocessing import Process, Queue
from binance import AsyncClient, BinanceSocketManager
from utility.static import now, strf_time, timedelta_sec, int_hms_utc, GetBinanceShortPgSgSp, GetBinanceLongPgSgSp, \
    threading_timer
from utility.setting import columns_cj, columns_tj, columns_tdf, columns_jgf, columns_tt, ui_num, DB_TRADELIST, DICT_SET


class TraderBinanceFuture:
    def __init__(self, qlist):
        """
        windowQ, soundQ, queryQ, teleQ, chartQ, hogaQ, webcQ, backQ, creceivQ, ctraderQ,  cstgQ, liveQ, kimpQ, wdzservQ
           0        1       2      3       4      5      6      7       8         9         10     11    12      13
        """
        self.windowQ  = qlist[0]
        self.soundQ   = qlist[1]
        self.queryQ   = qlist[2]
        self.teleQ    = qlist[3]
        self.creceivQ = qlist[8]
        self.ctraderQ = qlist[9]
        self.cstgQ    = qlist[10]
        self.liveQ    = qlist[11]
        self.dict_set = DICT_SET

        self.dict_time        = {}
        self.dict_info        = {}
        self.dict_curc        = {}
        self.dict_lvrg        = {}
        self.dict_buy_long    = {}
        self.dict_sell_short  = {}
        self.dict_sell_long   = {}
        self.dict_buy_short   = {}
        self.dict_order_pos   = {}

        self.proc_webs = None

        self.df_cj = pd.DataFrame(columns=columns_cj)
        self.df_jg = pd.DataFrame(columns=columns_jgf)
        self.df_tj = pd.DataFrame(columns=columns_tj)
        self.df_td = pd.DataFrame(columns=columns_tdf)
        self.df_tt = pd.DataFrame(columns=columns_tt)

        self.str_today = strf_time('%Y%m%d', timedelta_sec(-32400))

        self.dict_intg = {
            '예수금': 0.,
            '추정예탁자산': 0.,
            '종목당투자금': 0
        }
        self.dict_bool = {
            '실현손익저장': False,
            '장초전략잔고청산': False,
            '장중전략잔고청산': False,
            '프로세스종료': False
        }
        curr_time = now()
        self.dict_time = {
            '주문시간': curr_time,
            '잔고전송': curr_time,
            '잔고갱신및주문취소확인': curr_time
        }

        self.binance = binance.Client(self.dict_set['Access_key2'], self.dict_set['Secret_key2'])
        self.UpdateDictTime()
        self.LoadDatabase()
        self.GetBalances()
        self.SetPosition()
        self.MainLoop()

    def UpdateDictTime(self):
        dict_name = {x['market'].split('-')[1]: x['korean_name'] for x in pyupbit.get_tickers(verbose=True)}
        datas = self.binance.futures_ticker()
        for data in datas:
            code = data['symbol']
            if re.search('USDT$', code) is not None and code not in self.dict_time.keys():
                dummy_time = timedelta_sec(-3600)
                dummy_name = code.replace('USDT', '')
                self.dict_time[code] = [dict_name[dummy_name] if dummy_name in dict_name.keys() else dummy_name, dummy_time, dummy_time, dummy_time]

    def LoadDatabase(self):
        con = sqlite3.connect(DB_TRADELIST)
        self.df_cj = pd.read_sql(f"SELECT * FROM c_chegeollist WHERE 체결시간 LIKE '{self.str_today}%'", con).set_index('index')
        self.df_td = pd.read_sql(f"SELECT * FROM c_tradelist_future WHERE 체결시간 LIKE '{self.str_today}%'", con).set_index('index')
        self.df_jg = pd.read_sql(f'SELECT * FROM c_jangolist_future', con).set_index('index')
        con.close()

        if len(self.df_cj) > 0: self.windowQ.put((ui_num['C체결목록'], self.df_cj[::-1]))
        if len(self.df_td) > 0: self.windowQ.put((ui_num['C거래목록'], self.df_td[::-1]))
        if len(self.df_jg) > 0: self.creceivQ.put(('잔고목록', tuple(self.df_jg.index)))

        self.windowQ.put((ui_num['C로그텍스트'], '시스템 명령 실행 알림 - 데이터베이스 불러오기 완료'))

    def GetBalances(self):
        cbg = 0
        for index in self.df_jg.index:
            cbg += self.df_jg['매입가'][index] * round(self.df_jg['보유수량'][index] / self.df_jg['레버리지'][index], 4)

        if self.dict_set['코인모의투자']:
            con = sqlite3.connect(DB_TRADELIST)
            df = pd.read_sql('SELECT * FROM c_tradelist_future', con)
            con.close()
            tcg = df['수익금'].sum()
            chujeonjasan = 100000 + tcg
        else:
            datas = self.binance.futures_account_balance()
            chujeonjasan = [float(data['balance']) for data in datas if data['asset'] == 'USDT'][0]

        self.dict_intg['예수금'] = round(chujeonjasan - cbg, 4)
        self.dict_intg['추정예탁자산'] = chujeonjasan

        if len(self.df_td) > 0:
            self.UpdateTotaltradelist(first=True)

        self.windowQ.put((ui_num['C로그텍스트'], '시스템 명령 실행 알림 - 예수금 조회 완료'))

    def SetPosition(self):
        def get_decimal_place(float_):
            float_ = str(float(float_))
            float_ = float_.split('.')[1]
            return 0 if float_ == '0' else len(float_)

        datas = self.binance.futures_exchange_info()
        codes = [x['symbol'] for x in datas['symbols'] if re.search('USDT$', x['symbol']) is not None]
        datas = [x for x in datas['symbols'] if re.search('USDT$', x['symbol']) is not None]
        self.dict_info = {x['symbol']: {'호가단위': float(x['filters'][0]['tickSize']), '소숫점자리수': get_decimal_place(x['filters'][2]['minQty'])} for x in datas}

        if self.dict_set['바이낸스선물고정레버리지']:
            self.dict_lvrg = {x: self.dict_set['바이낸스선물고정레버리지값'] for x in codes}
        else:
            self.dict_lvrg = {x: 1 for x in codes}

        self.cstgQ.put(('바낸선물단위정보', self.dict_info))
        self.windowQ.put((ui_num['C로그텍스트'], '시스템 명령 실행 알림 - 호가단위 및 소숫점자리수 조회 완료'))

        if not self.dict_set['코인모의투자']:
            for code in codes:
                try:
                    if self.dict_set['바이낸스선물고정레버리지']:
                        self.binance.futures_change_leverage(symbol=code, leverage=self.dict_set['바이낸스선물고정레버리지값'])
                    else:
                        self.binance.futures_change_leverage(symbol=code, leverage=1)
                    self.binance.futures_change_margin_type(symbol=code, marginType=self.dict_set['바이낸스선물마진타입'])
                except:
                    pass
            try:
                self.binance.futures_change_position_mode(dualSidePosition=self.dict_set['바이낸스선물포지션'])
            except:
                pass

        self.windowQ.put((ui_num['C로그텍스트'], '시스템 명령 실행 알림 - 마진타입 및 레버리지 설정 완료'))

    def MainLoop(self):
        text = '코인 전략연산 및 트레이더를 시작하였습니다.'
        if self.dict_set['코인알림소리']: self.soundQ.put(text)
        self.teleQ.put(text)
        self.windowQ.put((ui_num['C로그텍스트'], '시스템 명령 실행 알림 - 트레이더 시작'))
        wsq = Queue()
        while True:
            if self.proc_webs is None or not self.proc_webs.is_alive():
                self.WebSocketsStart(wsq)

            if not self.ctraderQ.empty():
                data = self.ctraderQ.get()
                if type(data) == tuple:
                    self.UpdateTuple(data)
                elif type(data) == str:
                    self.UpdateString(data)
                if data == '프로세스종료':
                    if self.proc_webs.is_alive(): self.proc_webs.kill()
                    break

            if not wsq.empty():
                data = wsq.get()
                if data == 'ConnectionClosedError':
                    self.windowQ.put((ui_num['C단순텍스트'], '시스템 명령 오류 알림 - 웹소켓 연결 끊김으로 다시 연결합니다.'))
                    self.WebProcessKill()
                elif data[0] == 'user':
                    data = data[1]
                    if data['e'] == 'ACCOUNT_UPDATE':
                        try:
                            data = data['a']
                            self.dict_intg['추정예탁자산'] = float(data['B'][0]['wb'])
                            self.dict_intg['예수금'] = float(data['B'][0]['cw'])
                        except Exception as e:
                            self.windowQ.put((ui_num['C단순텍스트'], f'시스템 명령 오류 알림 - 웹소켓 user {e}'))
                    elif data['e'] == 'ORDER_TRADE_UPDATE':
                        try:
                            data = data['o']
                            code = data['s']
                            p    = f"{data['S']}_{self.dict_order_pos[code]}"
                            if data['X'] == 'CANCELED':
                                p = f'{p}_CANCEL'
                            oc   = float(data['q'])
                            cc   = float(data['l'])
                            mc   = round(oc - float(data['z']), self.dict_info[code]['소숫점자리수'])
                            cp   = float(data['L'])
                            op   = float(data['p'])
                            on   = int(data['i'])
                        except:
                            print('바이낸스 홈페이지 주문은 기록되지 않습니다.')
                        else:
                            if cc > 0 or 'CANCEL' in p:
                                self.UpdateChejanData(p, code, oc, cc, mc, cp, op, on)

            curr_time = now()
            inthmsutc = int_hms_utc()

            if curr_time > self.dict_time['잔고갱신및주문취소확인']:
                self.UpdateTotaljango(inthmsutc)
                self.dict_time['잔고갱신및주문취소확인'] = timedelta_sec(1)

            if curr_time > self.dict_time['잔고전송']:
                self.cstgQ.put(('잔고목록', self.df_jg))
                self.dict_time['잔고전송'] = timedelta_sec(0.5)

            if self.dict_set['코인장초전략종료시간'] < inthmsutc < self.dict_set['코인장초전략종료시간'] + 10:
                if not self.dict_bool['장초전략잔고청산']:
                    self.JangoCheongsan('장초')
                if self.dict_set['코인장초프로세스종료'] and not self.dict_bool['프로세스종료']:
                    self.SaveTotalGetbalDelcjtd()
                    self.TradeProcKill()

            if self.dict_set['코인장중전략종료시간'] < inthmsutc < self.dict_set['코인장중전략종료시간'] + 10:
                if not self.dict_bool['장중전략잔고청산']:
                    self.JangoCheongsan('장중')
                if self.dict_set['코인장중프로세스종료'] and not self.dict_bool['프로세스종료']:
                    self.SaveTotalGetbalDelcjtd()
                    self.TradeProcKill()

            if not self.dict_set['코인장초프로세스종료'] and not self.dict_set['코인장중프로세스종료']:
                if not self.dict_bool['실현손익저장'] and inthmsutc > 235950:
                    self.SaveTotalGetbalDelcjtd()

            if self.dict_bool['실현손익저장'] and 0 < inthmsutc < 10:
                self.str_today = strf_time('%Y%m%d')
                self.dict_bool['실현손익저장'] = False
                self.dict_bool['장초전략잔고청산'] = False
                self.dict_bool['장중전략잔고청산'] = False

            if self.ctraderQ.empty() and wsq.empty():
                time.sleep(0.001)

        self.windowQ.put((ui_num['C로그텍스트'], '시스템 명령 실행 알림 - 트레이더 종료'))
        time.sleep(1)

    def TradeProcKill(self):
        self.dict_bool['프로세스종료'] = True
        threading_timer(180, self.ctraderQ.put, '프로세스종료')

    def WebSocketsStart(self, wsq):
        self.proc_webs = Process(target=WebSocketManager, args=(self.dict_set['Access_key2'], self.dict_set['Secret_key2'], wsq), daemon=True)
        self.proc_webs.start()

    def WebProcessKill(self):
        if self.proc_webs.is_alive(): self.proc_webs.kill()
        time.sleep(3)

    def UpdateTuple(self, data):
        if len(data) in (6, 7):
            self.CheckOrder(data)
        elif len(data) == 9:
            self.SendOrder(data)
        elif len(data) == 2:
            if type(data[1]) == float:
                code, c = data
                self.dict_curc[code] = c
                try:
                    if code in self.df_jg.index and c != self.df_jg['현재가'][code]:
                        jg = self.df_jg['매입금액'][code]
                        jc = self.df_jg['보유수량'][code]
                        ps = self.df_jg['포지션'][code]
                        if ps == 'LONG':
                            pg, sg, sp = GetBinanceLongPgSgSp(jg, jc * c, '시장가' in self.dict_set['코인매수주문구분'], '시장가' in self.dict_set['코인매도주문구분'])
                        else:
                            pg, sg, sp = GetBinanceShortPgSgSp(jg, jc * c, '시장가' in self.dict_set['코인매수주문구분'], '시장가' in self.dict_set['코인매도주문구분'])
                        columns = ['현재가', '수익률', '평가손익', '평가금액']
                        self.df_jg.loc[code, columns] = c, sp, sg, pg
                except:
                    pass
            elif data[0] == '저가대비고가등락율':
                self.SetLeverage(data[1])
            elif data[0] == '관심진입':
                if data[1] in self.dict_sell_long.keys():
                    self.CancelOrder(data[1], 'SELL_LONG')
                if data[1] in self.dict_buy_short.keys():
                    self.CancelOrder(data[1], 'BUY_SHORT')
            elif data[0] == '관심이탈':
                if data[1] in self.dict_buy_long.keys():
                    self.CancelOrder(data[1], 'BUY_LONG')
                if data[1] in self.dict_sell_short.keys():
                    self.CancelOrder(data[1], 'SELL_SHORT')
            elif data[0] == '설정변경':
                self.dict_set = data[1]

    def UpdateString(self, data):
        if data == '코인명갱신':
            self.UpdateDictTime()
            self.SetPosition()
        elif data == 'C체결목록':
            self.teleQ.put(self.df_cj) if len(self.df_cj) > 0 else self.teleQ.put('현재는 코인체결목록이 없습니다.')
        elif data == 'C거래목록':
            self.teleQ.put(self.df_td) if len(self.df_td) > 0 else self.teleQ.put('현재는 코인거래목록이 없습니다.')
        elif data == 'C잔고평가':
            self.teleQ.put(('잔고목록', self.df_jg)) if len(self.df_jg) > 0 else self.teleQ.put('현재는 코인잔고목록이 없습니다.')
        elif data == 'C잔고청산':
            self.JangoCheongsan('수동')

    def SetLeverage(self, dict_dlhp):
        for code in list(self.dict_info.keys()):
            try:
                leverage = self.GetLeverage(dict_dlhp[code][1])
                self.dict_lvrg[code] = leverage
                if not self.dict_set['코인모의투자']:
                    self.binance.futures_change_leverage(symbol=code, leverage=leverage)
            except:
                pass

    def GetLeverage(self, dlhp):
        leverage = 1
        for min_area, max_area, lvrg in self.dict_set['바이낸스선물변동레버리지값']:
            if min_area <= dlhp < max_area:
                leverage = lvrg
                break
        return leverage

    def CheckOrder(self, data):
        if len(data) == 6:
            og, code, op, oc, signal_time, manual = data
            ordertype = None
        else:
            og, code, op, oc, signal_time, manual, ordertype = data

        NIJ  = code not in self.df_jg.index
        INBL = code in self.dict_buy_long.keys()
        INSS = code in self.dict_sell_short.keys()
        INSL = code in self.dict_sell_long.keys()
        INBS = code in self.dict_buy_short.keys()

        on = ''
        cancel = False
        curr_time = now()
        if manual:
            if (og == 'SELL_LONG' and (NIJ or INSL)) or (og == 'BUY_SHORT' and (NIJ or INBS)):
                cancel = True
        elif og in ('BUY_LONG', 'SELL_SHORT'):
            if self.dict_intg['예수금'] < oc * op:
                if curr_time > self.dict_time[code][1]:
                    self.CreateOrder('시드부족', code, op, oc, strf_time('%H%M%S%f'), signal_time, manual, 0, None)
                    self.dict_time[code][1] = timedelta_sec(180)
                cancel = True
            elif og == 'BUY_LONG' and INBL:   cancel = True
            elif og == 'SELL_SHORT' and INSS: cancel = True
        elif og in ('SELL_LONG', 'BUY_SHORT'):
            if og == 'SELL_LONG' and (NIJ or INSL):   cancel = True
            elif og == 'BUY_SHORT' and (NIJ or INBS): cancel = True
        elif 'CANCEL' in og:
            df = self.GetMichegeolDF(code, og.replace('_CANCEL', ''))
            if len(df) > 0:
                mc = df['미체결수량'].iloc[-1]
                if mc > 0:
                    oc = mc
                    on = df['주문번호'].iloc[-1]
                else:
                    cancel = True
            else:
                cancel = True

            if og == 'BUY_LONG_CANCEL' and not INBL:     cancel = True
            elif og == 'SELL_SHORT_CANCEL' and not INSS: cancel = True
            elif og == 'SELL_LONG_CANCEL' and not INSL:  cancel = True
            elif og == 'BUY_SHORT_CANCEL' and not INBS:  cancel = True

        if cancel:
            if 'CANCEL' not in og:
                self.cstgQ.put((f'{og}_CANCEL', code))
        else:
            if manual and 'CANCEL' not in og:
                self.cstgQ.put((f'{og}_MANUAL', code))

            if oc > 0:
                self.CreateOrder(og, code, op, oc, on, signal_time, manual, 0, ordertype)
            else:
                self.cstgQ.put((f'{og}_CANCEL', code))

    def CreateOrder(self, og, code, op, oc, on, signal_time, manual, fixc, ordertype):
        if oc * op < 5:
            self.windowQ.put((ui_num['C로그텍스트'], '시스템 명령 오류 알림 - 최소주문금액 5 USDT 미만입니다.'))
            self.cstgQ.put((f'{og}_CANCEL', code))
            return

        if self.dict_set['코인모의투자']:
            if og in ('BUY_LONG', 'SELL_SHORT'):
                self.dict_intg['예수금'] -= op * oc
            elif og in ('SELL_LONG', 'BUY_SHORT'):
                self.dict_intg['예수금'] += op * round(oc / self.df_jg['레버리지'][code], self.dict_info[code]['소숫점자리수'])

        if og in ('BUY_LONG', 'SELL_SHORT'):
            oc = round(oc * self.dict_lvrg[code], self.dict_info[code]['소숫점자리수'])

        if oc > 0:
            if self.dict_set['코인모의투자'] or og == '시드부족':
                self.OrderTimeLog(signal_time)
                if og == '시드부족':
                    self.UpdateChejanData(og, code, oc, 0, oc, op, 0, '')
                else:
                    self.UpdateChejanData(og, code, oc, oc, 0, op, op, '')
            else:
                data = (og, code, op, oc, on, signal_time, manual, fixc, ordertype)
                self.SendOrder(data)

    def SendOrder(self, data):
        og, code, op, oc, on, signal_time, manual, fixc, ordertype = data
        curr_time = now()
        if curr_time < self.dict_time['주문시간']:
            next_time = (self.dict_time['주문시간'] - curr_time).total_seconds()
            data = [og, code, op, oc, on, signal_time, manual, fixc, ordertype]
            threading_timer(next_time, self.ctraderQ.put, data)
            return

        ret = None
        side, position = og.split('_')[:2]
        self.OrderTimeLog(signal_time)
        if 'CANCEL' not in og:
            try:
                if ordertype == '시장가' or (ordertype is None and self.dict_set['코인매수주문구분'] == '시장가') or manual:
                    ret = self.binance.futures_create_order(symbol=code, side=side, type='MARKET', quantity=oc)
                elif ordertype == '지정가' or (ordertype is None and self.dict_set['코인매수주문구분'] == '지정가'):
                    ret = self.binance.futures_create_order(symbol=code, side=side, type='LIMIT', price=op, timeInForce='GTC', quantity=oc)
                elif ordertype == '지정가IOC' or (ordertype is None and self.dict_set['코인매수주문구분'] == '지정가IOC'):
                    ret = self.binance.futures_create_order(symbol=code, side=side, type='LIMIT', price=op, timeInForce='IOC', quantity=oc)
                elif ordertype == '지정가FOK' or (ordertype is None and self.dict_set['코인매수주문구분'] == '지정가FOK'):
                    ret = self.binance.futures_create_order(symbol=code, side=side, type='LIMIT', price=op, timeInForce='FOK', quantity=oc)
            except Exception as e:
                self.cstgQ.put((f'{og}_CANCEL', code))
                self.windowQ.put((ui_num['C로그텍스트'], f'시스템 명령 오류 알림 - [주문 실패] {e}'))
            else:
                orderId = int(ret['orderId'])
                dt = self.GetIndex()
                if og == 'BUY_LONG':
                    self.dict_buy_long[code] = [orderId, timedelta_sec(self.dict_set['코인매수취소시간초']), fixc, op, self.dict_lvrg[code]]
                elif og == 'SELL_SHORT':
                    self.dict_sell_short[code] = [orderId, timedelta_sec(self.dict_set['코인매수취소시간초']), fixc, op, self.dict_lvrg[code]]
                elif og == 'SELL_LONG':
                    self.dict_sell_long[code] = [orderId, timedelta_sec(self.dict_set['코인매도취소시간초']), fixc, op]
                elif og == 'BUY_SHORT':
                    self.dict_buy_short[code] = [orderId, timedelta_sec(self.dict_set['코인매도취소시간초']), fixc, op]
                self.dict_order_pos[code] = position
                self.UpdateChegeollist(dt, code, f'{og}_REG', oc, 0, oc, 0, dt[:14], op, orderId)
                self.windowQ.put((ui_num['C로그텍스트'], f'주문 관리 시스템 알림 - [접수] {code} | {op} | {oc} | {og}'))
        else:
            try:
                ret = self.binance.futures_cancel_order(symbol=code, orderId=on)
            except Exception as e:
                self.windowQ.put((ui_num['C로그텍스트'], f'시스템 명령 오류 알림 - [주문 실패] {e}'))
            else:
                orderId = int(ret['orderId'])
                dt = self.GetIndex()
                self.dict_order_pos[code] = position
                self.UpdateChegeollist(dt, code, f'{og}_REG', oc, 0, oc, 0, dt[:14], 0, orderId)
                self.windowQ.put((ui_num['C로그텍스트'], f'주문 관리 시스템 알림 - [접수] {code} | {op} | {oc} | {og}'))

        self.dict_time['주문시간'] = timedelta_sec(0.1)
        self.creceivQ.put(('주문목록', self.GetOrderCodeList()))

    def JangoCheongsan(self, gubun):
        if gubun == '수동':
            self.dict_bool['장초전략잔고청산'] = True
            self.dict_bool['장중전략잔고청산'] = True
        else:
            self.dict_bool[f'{gubun}전략잔고청산'] = True

        if len(self.dict_buy_long) > 0:
            for code in list(self.dict_buy_long.keys()):
                self.CancelOrder(code, 'BUY_LONG')

        if len(self.dict_sell_short) > 0:
            for code in list(self.dict_sell_short.keys()):
                self.CancelOrder(code, 'SELL_SHORT')

        if len(self.dict_sell_long) > 0:
            for code in list(self.dict_sell_long.keys()):
                self.CancelOrder(code, 'SELL_LONG')

        if len(self.dict_buy_short) > 0:
            for code in list(self.dict_buy_short.keys()):
                self.CancelOrder(code, 'BUY_SHORT')

        if gubun == '수동' or self.dict_set[f'코인{gubun}잔고청산']:
            if len(self.df_jg) > 0:
                for code in self.df_jg.index:
                    position, c, oc = self.df_jg['포지션'][code], self.df_jg['현재가'][code], self.df_jg['보유수량'][code]
                    if self.dict_set['코인모의투자']:
                        self.UpdateChejanData('SELL_LONG' if position == 'LONG' else 'BUY_SHORT', code, oc, oc, 0, c, c, '')
                    else:
                        try:
                            if position == 'LONG':
                                ret = self.binance.futures_create_order(symbol=code, side='SELL', type='MARKET', quantity=oc)
                            else:
                                ret = self.binance.futures_create_order(symbol=code, side='BUY', type='MARKET', quantity=oc)
                        except Exception as e:
                            self.windowQ.put((ui_num['C로그텍스트'], f'시스템 명령 오류 알림 - [주문 실패] {e}'))
                        else:
                            orderId = int(ret['orderId'])
                            dt = self.GetIndex()
                            self.dict_order_pos[code] = position
                            if position == 'LONG':
                                self.UpdateChegeollist(dt, code, 'SELL_LONG_REG', oc, 0, oc, 0, dt[:14], c, orderId)
                                self.windowQ.put((ui_num['C로그텍스트'], f'주문 관리 시스템 알림 - [접수] {code} | {c} | {oc} | SELL_LONG'))
                            else:
                                self.UpdateChegeollist(dt, code, 'BUY_SHORT_REG', oc, 0, oc, 0, dt[:14], c, orderId)
                                self.windowQ.put((ui_num['C로그텍스트'], f'주문 관리 시스템 알림 - [접수] {code} | {c} | {oc} | BUY_SHORT'))
                        time.sleep(0.3)

            if self.dict_set['코인알림소리']:
                self.soundQ.put(f'코인 {gubun}전략 잔고청산 주문을 전송하였습니다.')
            self.windowQ.put((ui_num['C로그텍스트'], f'시스템 명령 실행 알림 - {gubun}전략 잔고청산 주문 완료'))

    def CancelOrder(self, code, gubun):
        df = self.GetMichegeolDF(code, gubun)
        if len(df) > 0:
            mc = df['미체결수량'].iloc[-1]
            if mc > 0:
                on, op = df['주문번호'].iloc[-1], df['주문가격'].iloc[-1]
                self.CreateOrder(f'{gubun}_CANCEL', code, op, mc, on, now(), False, 0, None)

    def UpdateChejanData(self, gubun, code, oc, cc, mc, cp, op, on):
        dt = self.GetIndex()

        if gubun in ('BUY_LONG', 'SELL_SHORT', 'SELL_LONG', 'BUY_SHORT'):
            if gubun == 'BUY_LONG':
                if code in self.df_jg.index:
                    jc = round(self.df_jg['보유수량'][code] + cc, self.dict_info[code]['소숫점자리수'])
                    jg = round(self.df_jg['매입금액'][code] + cc * cp, 4)
                    jp = round(jg / jc, 8)
                    cg = round(cp * jc, 4)
                    pg, sg, sp = GetBinanceLongPgSgSp(jg, cg, '시장가' in self.dict_set['코인매수주문구분'], '시장가' in self.dict_set['코인매도주문구분'])
                    columns = ['매입가', '현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량', '매수시간']
                    self.df_jg.loc[code, columns] = jp, cp, sp, sg, jg, pg, jc, dt[:14]
                else:
                    jg = round(cp * cc, 4)
                    lv = self.dict_set['바이낸스선물고정레버리지값'] if self.dict_set['바이낸스선물고정레버리지'] else self.dict_buy_long[code][4]
                    pg, sg, sp = GetBinanceLongPgSgSp(jg, jg, '시장가' in self.dict_set['코인매수주문구분'], '시장가' in self.dict_set['코인매도주문구분'])
                    self.df_jg.loc[code] = code, 'LONG', cp, cp, sp, sg, jg, pg, cc, lv, 0, 0, dt[:14]

                if mc == 0:
                    self.df_jg.loc[code, '분할매수횟수'] = self.df_jg['분할매수횟수'][code] + 1
                    if code in self.dict_buy_long.keys():
                        del self.dict_buy_long[code]

            elif gubun == 'SELL_SHORT':
                if code in self.df_jg.index:
                    jc = round(self.df_jg['보유수량'][code] + cc, self.dict_info[code]['소숫점자리수'])
                    jg = round(self.df_jg['매입금액'][code] + cc * cp, 4)
                    jp = round(jg / jc, 8)
                    cg = round(jc * cp, 4)
                    pg, sg, sp = GetBinanceShortPgSgSp(jg, cg, '시장가' in self.dict_set['코인매수주문구분'], '시장가' in self.dict_set['코인매도주문구분'])
                    columns = ['매입가', '현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량', '매수시간']
                    self.df_jg.loc[code, columns] = jp, cp, sp, sg, jg, pg, jc, dt[:14]
                else:
                    jg = round(cc * cp, 4)
                    lv = self.dict_set['바이낸스선물고정레버리지값'] if self.dict_set['바이낸스선물고정레버리지'] else self.dict_sell_short[code][4]
                    pg, sg, sp = GetBinanceShortPgSgSp(jg, jg, '시장가' in self.dict_set['코인매수주문구분'], '시장가' in self.dict_set['코인매도주문구분'])
                    self.df_jg.loc[code] = code, 'SHORT', cp, cp, sp, sg, jg, pg, cc, lv, 0, 0, dt[:14]

                if mc == 0:
                    self.df_jg.loc[code, '분할매수횟수'] = self.df_jg['분할매수횟수'][code] + 1
                    if code in self.dict_sell_short.keys():
                        del self.dict_sell_short[code]

            elif gubun == 'SELL_LONG':
                jc = round(self.df_jg['보유수량'][code] - cc, self.dict_info[code]['소숫점자리수'])
                jp = self.df_jg['매입가'][code]
                if jc != 0:
                    jg = round(jp * jc, 4)
                    cg = round(cp * jc, 4)
                    pg, sg, sp = GetBinanceLongPgSgSp(jg, cg, '시장가' in self.dict_set['코인매수주문구분'], '시장가' in self.dict_set['코인매도주문구분'])
                    columns = ['현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량']
                    self.df_jg.loc[code, columns] = cp, sp, sg, jg, pg, jc
                else:
                    self.df_jg.drop(index=code, inplace=True)

                if mc == 0:
                    if jc > 0:
                        self.df_jg.loc[code, '분할매도횟수'] = self.df_jg['분할매도횟수'][code] + 1
                    if code in self.dict_sell_long.keys():
                        del self.dict_sell_long[code]

                jg = round(jp * cc, 4)
                cg = round(cp * cc, 4)
                pg, sg, sp = GetBinanceLongPgSgSp(jg, cg, '시장가' in self.dict_set['코인매수주문구분'], '시장가' in self.dict_set['코인매도주문구분'])
                self.UpdateTradelist(dt, code, 'LONG', jg, pg, cc, sp, sg, dt[:14])

                if sp < 0:
                    self.dict_time[code][3] = timedelta_sec(self.dict_set['코인매수금지손절간격초'])

            else:
                jc = round(self.df_jg['보유수량'][code] - cc, self.dict_info[code]['소숫점자리수'])
                jp = self.df_jg['매입가'][code]
                if jc != 0:
                    jg = round(jp * jc, 4)
                    cg = round(cp * jc, 4)
                    pg, sg, sp = GetBinanceShortPgSgSp(jg, cg, '시장가' in self.dict_set['코인매수주문구분'], '시장가' in self.dict_set['코인매도주문구분'])
                    columns = ['현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량']
                    self.df_jg.loc[code, columns] = cp, sp, sg, jg, pg, jc
                else:
                    self.df_jg.drop(index=code, inplace=True)

                if mc == 0:
                    if jc > 0:
                        self.df_jg.loc[code, '분할매도횟수'] = self.df_jg['분할매도횟수'][code] + 1
                    if code in self.dict_buy_short.keys():
                        del self.dict_buy_short[code]

                jg = round(jp * cc, 4)
                cg = round(cp * cc, 4)
                pg, sg, sp = GetBinanceShortPgSgSp(jg, cg, '시장가' in self.dict_set['코인매수주문구분'], '시장가' in self.dict_set['코인매도주문구분'])
                self.UpdateTradelist(dt, code, 'SHORT', jg, pg, cc, sp, sg, dt[:14])

                if sp < 0:
                    self.dict_time[code][3] = timedelta_sec(self.dict_set['코인매수금지손절간격초'])

            self.df_jg.sort_values(by=['매입금액'], ascending=False, inplace=True)
            self.cstgQ.put(('잔고목록', self.df_jg))

            if mc == 0:
                self.cstgQ.put((f'{gubun}_COMPLETE', code))

            self.UpdateChegeollist(dt, code, gubun, oc, cc, mc, cp, dt[:14], op, on)

            self.queryQ.put(('거래디비', self.df_jg, 'c_jangolist_future', 'replace'))
            if self.dict_set['코인알림소리']:
                text = ''
                if gubun == 'BUY_LONG':     text = '롱포지션을 진입'
                elif gubun == 'SELL_SHORT': text = '숏포지션을 진입'
                elif gubun == 'SELL_LONG':  text = '롱포지션을 청산'
                elif gubun == 'BUY_SHORT':  text = '숏포지션을 청산'
                self.soundQ.put(f'{self.dict_time[code][0]} {text}하였습니다.')
            self.windowQ.put((ui_num['C로그텍스트'], f'주문 관리 시스템 알림 - [체결] {code} | {cp} | {cc} | {gubun}'))

        elif gubun == '시드부족':
            self.UpdateChegeollist(dt, code, gubun, oc, cc, mc, cp, dt[:14], op, on)

        elif gubun in ('BUY_LONG_CANCEL', 'SELL_SHORT_CANCEL', 'SELL_LONG_CANCEL', 'BUY_SHORT_CANCEL'):
            df = self.GetMichegeolDF(code, gubun.replace('_CANCEL', ''))
            if len(df) > 0 and df['미체결수량'].iloc[-1] > 0:
                if df['체결수량'].iloc[-1] > 0 and code in self.df_jg.index:
                    if gubun in ('BUY_LONG_CANCEL', 'SELL_SHORT_CANCEL'):
                        self.df_jg.loc[code, '분할매수횟수'] = self.df_jg['분할매수횟수'][code] + 1
                    else:
                        self.df_jg.loc[code, '분할매도횟수'] = self.df_jg['분할매도횟수'][code] + 1
                    self.cstgQ.put(('잔고목록', self.df_jg))

                if gubun == 'BUY_LONG_CANCEL' and code in self.dict_buy_long.keys():
                    del self.dict_buy_long[code]
                elif gubun == 'SELL_SHORT_CANCEL' and code in self.dict_sell_short.keys():
                    del self.dict_sell_short[code]
                elif gubun == 'SELL_LONG_CANCEL' and code in self.dict_sell_long.keys():
                    del self.dict_sell_long[code]
                elif gubun == 'BUY_SHORT_CANCEL' and code in self.dict_buy_short.keys():
                    del self.dict_buy_short[code]

            self.cstgQ.put((gubun, code))
            self.UpdateChegeollist(dt, code, gubun, oc, cc, mc, cp, dt[:14], op, on)

            if self.dict_set['코인알림소리']:
                text = ''
                if gubun == 'BUY_LONG_CANCEL':     text = '롱포지션 진입을 취소'
                elif gubun == 'SELL_SHORT_CANCEL': text = '숏포지션 진입을 취소'
                elif gubun == 'SELL_LONG_CANCEL':  text = '롱포지션 청산을 취소'
                elif gubun == 'BUY_SHORT_CANCEL':  text = '숏포지션 청산을 취소'
                self.soundQ.put(f'{self.dict_time[code][0]} {text}하였습니다.')
            self.windowQ.put((ui_num['C로그텍스트'], f'주문 관리 시스템 알림 - [확인] {code} | {op} | {oc} | {gubun}'))

        self.creceivQ.put(('잔고목록', tuple(self.df_jg.index)))
        self.creceivQ.put(('주문목록', self.GetOrderCodeList()))

    def UpdateTradelist(self, index, code, pos, jg, pg, cc, sp, sg, ct):
        self.df_td.loc[index] = code, pos, jg, pg, cc, sp, sg, ct
        self.windowQ.put((ui_num['C거래목록'], self.df_td[::-1]))

        df = pd.DataFrame([[code, pos, jg, pg, cc, sp, sg, ct]], columns=columns_tdf, index=[index])
        self.queryQ.put(('거래디비', df, 'c_tradelist_future', 'append'))

        self.UpdateTotaltradelist()

    def UpdateTotaltradelist(self, first=False):
        tdt = len(self.df_td.drop_duplicates(['종목명', '체결시간']))
        tbg = self.df_td['매수금액'].sum()
        tsg = self.df_td['매도금액'].sum()
        sig = self.df_td[self.df_td['수익금'] > 0]['수익금'].sum()
        ssg = self.df_td[self.df_td['수익금'] < 0]['수익금'].sum()
        sg  = self.df_td['수익금'].sum()
        sp  = round(sg / self.dict_intg['추정예탁자산'] * 100, 2)

        self.df_tt = pd.DataFrame([[tdt, tbg, tsg, sig, ssg, sp, sg]], columns=columns_tt, index=[self.str_today])
        self.windowQ.put((ui_num['C실현손익'], self.df_tt))

        if not first:
            self.teleQ.put(f'손익 알림 - 총매수금액 {tbg:,.0f}, 총매도금액 {tsg:,.0f}, 수익 {sig:,.0f}, 손실 {ssg:,.0f}, 수익금합계 {sg:,.0f}')

        if self.dict_set['스톰라이브']:
            sp = round(sg / tbg * 100, 2)
            df = pd.DataFrame([[tdt, tbg, tsg, sig, ssg, sp, sg]], columns=columns_tt, index=[self.str_today])
            self.liveQ.put(('코인', df))

    def UpdateChegeollist(self, index, code, gubun, oc, cc, mc, cp, dt, op, on):
        self.dict_time[code][2] = timedelta_sec(self.dict_set['코인매수금지간격초'])
        self.df_cj.loc[index] = code, gubun, oc, cc, mc, cp, dt, op, on
        self.windowQ.put((ui_num['C체결목록'], self.df_cj[::-1]))

        df = pd.DataFrame([[code, gubun, oc, cc, mc, cp, dt, op, on]], columns=columns_cj, index=[dt])
        self.queryQ.put(('거래디비', df, 'c_chegeollist', 'append'))

    def UpdateTotaljango(self, inthmsutc):
        if len(self.df_jg) > 0:
            tsg = self.df_jg['평가손익'].sum()
            tbg = self.df_jg['매입금액'].sum()
            tpg = self.df_jg['평가금액'].sum()
            bct = len(self.df_jg)
            tsp = round(tsg / tbg * 100, 2)
            if self.dict_set['코인모의투자']:
                self.dict_intg['추정예탁자산'] = self.dict_intg['예수금'] + tpg
            self.df_tj = pd.DataFrame([[self.dict_intg['추정예탁자산'], self.dict_intg['예수금'], bct, tsp, tsg, tbg, tpg]], columns=columns_tj, index=[self.str_today])
        else:
            self.df_tj = pd.DataFrame([[self.dict_intg['추정예탁자산'], self.dict_intg['예수금'], 0, 0.0, 0, 0, 0]], columns=columns_tj, index=[self.str_today])

        tsg = self.df_jg['평가손익'].sum() + self.df_td['수익금'].sum()
        if self.dict_set['코인손실중지']:
            std = self.dict_intg['추정예탁자산'] * self.dict_set['코인손실중지수익률'] / 100
            if std < -tsg: self.StrategyStop()
        if self.dict_set['코인수익중지']:
            std = self.dict_intg['추정예탁자산'] * self.dict_set['코인수익중지수익률'] / 100
            if std < tsg: self.StrategyStop()

        if self.dict_set['코인투자금고정']:
            if inthmsutc < self.dict_set['코인장초전략종료시간']:
                tujagm = int(self.dict_set['코인장초투자금'])
            else:
                tujagm = int(self.dict_set['코인장중투자금'])
        else:
            if inthmsutc < self.dict_set['코인장초전략종료시간']:
                tujagm = int(self.dict_intg['추정예탁자산'] * 0.98 / self.dict_set['코인장초최대매수종목수'])
            else:
                tujagm = int(self.dict_intg['추정예탁자산'] * 0.98 / self.dict_set['코인장중최대매수종목수'])

        if self.dict_intg['종목당투자금'] != tujagm:
            self.dict_intg['종목당투자금'] = tujagm
            self.cstgQ.put(('종목당투자금', self.dict_intg['종목당투자금']))

        self.windowQ.put((ui_num['C잔고목록'], self.df_jg))
        self.windowQ.put((ui_num['C잔고평가'], self.df_tj))

    def StrategyStop(self):
        self.cstgQ.put('매수전략중지')
        # self.cstgQ.put('매도전략중지')
        self.JangoCheongsan('수동')

    def SaveTotalGetbalDelcjtd(self):
        df = self.df_tt[['총매수금액', '총매도금액', '총수익금액', '총손실금액', '수익률', '수익금합계']]
        if len(df) > 0:
            self.queryQ.put(('거래디비', df, 'c_totaltradelist', 'append'))
        self.df_cj = pd.DataFrame(columns=columns_cj)
        self.df_td = pd.DataFrame(columns=columns_tdf)
        self.GetBalances()
        self.dict_bool['실현손익저장'] = True

    def OrderTimeLog(self, signal_time):
        gap = (now() - signal_time).total_seconds()
        self.windowQ.put((ui_num['C단순텍스트'], f'시그널 주문 시간 알림 - 발생시간과 주문시간의 차이는 [{gap:.6f}]초입니다.'))

    def GetOrderCodeList(self):
        return tuple(self.dict_buy_long.keys()) + tuple(self.dict_sell_short.keys()) + tuple(self.dict_sell_long.keys()) + tuple(self.dict_buy_short.keys())

    def GetMichegeolDF(self, code, gubun):
        return self.df_cj[(self.df_cj['종목명'] == code) & ((self.df_cj['주문구분'] == gubun) | (self.df_cj['주문구분'] == f'{gubun}_REG'))]

    def GetIndex(self):
        dt = strf_time('%Y%m%d%H%M%S%f', timedelta_sec(-32400))
        if dt in self.df_cj.index:
            while dt in self.df_cj.index:
                dt = str(int(dt) + 1)
        return dt


class WebSocketManager:
    def __init__(self, api_key, scret_key, q):
        self.api_key   = api_key
        self.scret_key = scret_key
        self.q         = q
        self.AsyncioLoop()

    async def task_user_socket(self):
        client = await AsyncClient.create(self.api_key, self.scret_key)
        bm = BinanceSocketManager(client)
        us = bm.futures_user_socket()
        async with us as user_socket:
            while True:
                try:
                    recv_data = await user_socket.recv()
                    self.q.put(('user', recv_data))
                except:
                    self.q.put('ConnectionClosedError')

    def AsyncioLoop(self):
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.task_user_socket())
        loop.run_forever()
