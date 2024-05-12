import time
import pyupbit
import sqlite3
import pandas as pd
from utility.static import now, strf_time, timedelta_sec, int_hms_utc, GetUpbitHogaunit, GetUpbitPgSgSp, threading_timer
from utility.setting import columns_cj, columns_tj, columns_jg, columns_td, columns_tt, ui_num, DB_TRADELIST, DICT_SET


class TraderUpbit:
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
        self.dict_set = DICT_SET

        self.upbit            = None
        self.dict_name        = {}
        self.dict_curc        = {}
        self.dict_buy         = {}
        self.dict_sell        = {}
        self.dict_buy_cancel  = {}
        self.dict_sell_cancel = {}
        self.dict_order_cc    = {}

        self.df_cj = pd.DataFrame(columns=columns_cj)
        self.df_jg = pd.DataFrame(columns=columns_jg)
        self.df_tj = pd.DataFrame(columns=columns_tj)
        self.df_td = pd.DataFrame(columns=columns_td)
        self.df_tt = pd.DataFrame(columns=columns_tt)

        self.str_today = strf_time('%Y%m%d', timedelta_sec(-32400))

        self.dict_intg = {
            '예수금': 0,
            '추정예수금': 0,
            '추정예탁자산': 0,
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
            '주문확인': curr_time,
            '잔고전송': curr_time,
            '잔고갱신및주문취소확인': curr_time
        }

        self.UpdateDictName()
        self.LoadDatabase()
        self.GetKey()
        self.GetBalances()
        self.MainLoop()

    def UpdateDictName(self):
        for dict_ticker in pyupbit.get_tickers(fiat="KRW", verbose=True):
            code = dict_ticker['market']
            name = dict_ticker['korean_name']
            if code not in self.dict_name.keys():
                dummy_time = timedelta_sec(-3600)
                self.dict_name[code] = [name, dummy_time, dummy_time, dummy_time]

        self.windowQ.put((ui_num['C로그텍스트'], '시스템 명령 실행 알림 - 코인명 수집 완료'))

    def LoadDatabase(self):
        con = sqlite3.connect(DB_TRADELIST)
        self.df_cj = pd.read_sql(f"SELECT * FROM c_chegeollist WHERE 체결시간 LIKE '{self.str_today}%'", con).set_index('index')
        self.df_td = pd.read_sql(f"SELECT * FROM c_tradelist WHERE 체결시간 LIKE '{self.str_today}%'", con).set_index('index')
        self.df_jg = pd.read_sql(f'SELECT * FROM c_jangolist', con).set_index('index')
        con.close()

        if len(self.df_cj) > 0: self.windowQ.put((ui_num['C체결목록'], self.df_cj[::-1]))
        if len(self.df_td) > 0: self.windowQ.put((ui_num['C거래목록'], self.df_td[::-1]))
        if len(self.df_jg) > 0: self.creceivQ.put(('잔고목록', tuple(self.df_jg.index)))

        self.windowQ.put((ui_num['C로그텍스트'], '시스템 명령 실행 알림 - 데이터베이스 불러오기 완료'))

    def GetKey(self):
        self.upbit = pyupbit.Upbit(self.dict_set['Access_key1'], self.dict_set['Secret_key1'])
        self.windowQ.put((ui_num['C로그텍스트'], '시스템 명령 실행 알림 - 주문 및 체결확인용 업비트 객체 생성 완료'))

    def GetBalances(self):
        cbg = self.df_jg['매입금액'].sum()
        if self.dict_set['코인모의투자']:
            con = sqlite3.connect(DB_TRADELIST)
            df = pd.read_sql('SELECT * FROM c_tradelist', con)
            con.close()
            tcg = df['수익금'].sum()
            chujeonjasan = 100000000 + tcg
        else:
            ret = self.upbit.get_balances()
            if self.CheckError(ret):
                chujeonjasan = int(float(ret[0]['balance']))
            else:
                chujeonjasan = 0

        self.dict_intg['예수금'] = int(chujeonjasan - cbg)
        self.dict_intg['추정예수금'] = self.dict_intg['예수금']
        self.dict_intg['추정예탁자산'] = chujeonjasan

        if len(self.df_td) > 0:
            self.UpdateTotaltradelist(first=True)

        self.windowQ.put((ui_num['C로그텍스트'], '시스템 명령 실행 알림 - 예수금 조회 완료'))

    def MainLoop(self):
        text = '코인 전략연산 및 트레이더를 시작하였습니다.'
        if self.dict_set['코인알림소리']: self.soundQ.put(text)
        self.teleQ.put(text)
        self.windowQ.put((ui_num['C로그텍스트'], '시스템 명령 실행 알림 - 트레이더 시작'))
        while True:
            if not self.ctraderQ.empty():
                data = self.ctraderQ.get()
                if type(data) == tuple:
                    self.UpdateTuple(data)
                elif type(data) == str:
                    self.UpdateString(data)
                if data == '프로세스종료':
                    break

            curr_time = now()
            inthmsutc = int_hms_utc()

            if curr_time > self.dict_time['주문확인']:
                self.CheckChegeol()
                self.dict_time['주문확인'] = timedelta_sec(0.3)

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

            if self.ctraderQ.empty():
                time.sleep(0.001)

        self.windowQ.put((ui_num['C로그텍스트'], '시스템 명령 실행 알림 - 트레이더 종료'))
        time.sleep(1)

    def TradeProcKill(self):
        self.dict_bool['프로세스종료'] = True
        threading_timer(180, self.ctraderQ.put, '프로세스종료')

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
                    if c != self.df_jg['현재가'][code]:
                        jg = self.df_jg['매입금액'][code]
                        jc = self.df_jg['보유수량'][code]
                        pg, sg, sp = GetUpbitPgSgSp(jg, jc * c)
                        columns = ['현재가', '수익률', '평가손익', '평가금액']
                        self.df_jg.loc[code, columns] = c, sp, sg, pg
                except:
                    pass
            if data[0] == '관심진입':
                if data[1] in self.dict_sell.keys():
                    self.CancelOrder(data[1], '매도')
            elif data[0] == '관심이탈':
                if data[1] in self.dict_buy.keys():
                    self.CancelOrder(data[1], '매수')
            elif data[0] == '설정변경':
                self.dict_set = data[1]

    def UpdateString(self, data):
        if data == '코인명갱신':
            self.UpdateDictName()
        elif data == 'C체결목록':
            self.teleQ.put(self.df_cj) if len(self.df_cj) > 0 else self.teleQ.put('현재는 코인체결목록이 없습니다.')
        elif data == 'C거래목록':
            self.teleQ.put(self.df_td) if len(self.df_td) > 0 else self.teleQ.put('현재는 코인거래목록이 없습니다.')
        elif data == 'C잔고평가':
            self.teleQ.put(('잔고목록', self.df_jg)) if len(self.df_jg) > 0 else self.teleQ.put('현재는 코인잔고목록이 없습니다.')
        elif data == 'C잔고청산':
            self.JangoCheongsan('수동')

    def CheckOrder(self, data):
        if len(data) == 6:
            og, code, op, oc, signal_time, manual = data
            ordertype = None
        else:
            og, code, op, oc, signal_time, manual, ordertype = data

        NIJ = code not in self.df_jg.index
        INB = code in self.dict_buy.keys()
        INS = code in self.dict_sell.keys()

        on = ''
        cancel = False
        curr_time = now()
        if manual:
            if NIJ:   cancel = True
            elif INS: cancel = True
        elif og == '매수':
            if self.dict_intg['추정예수금'] < oc * op:
                if curr_time > self.dict_name[code][1]:
                    self.CreateOrder('시드부족', code, op, oc, strf_time('%H%M%S%f'), signal_time, manual, 0, None)
                    self.dict_name[code][1] = timedelta_sec(180)
                cancel = True
            elif INB:
                cancel = True
        elif og == '매도':
            if NIJ or INS:
                cancel = True
        elif '취소' in og:
            df = self.GetMichegeolDF(code, og.replace('취소', ''))
            if len(df) > 0:
                mc = df['미체결수량'].iloc[-1]
                if mc > 0:
                    oc = mc
                    on = df['주문번호'].iloc[-1]
                else:
                    cancel = True
            else:
                cancel = True

            if og == '매수취소' and not INB:   cancel = True
            elif og == '매도취소' and not INS: cancel = True

        if cancel:
            if '취소' not in og:
                self.cstgQ.put((f'{og}취소', code))
        else:
            if manual and og in ('매수', '매도'):
                self.cstgQ.put((f'{og}주문', code))

            if oc > 0:
                self.CreateOrder(og, code, op, oc, on, signal_time, manual, 0, ordertype)
            else:
                self.cstgQ.put((f'{og}취소', code))

    def CreateOrder(self, og, code, op, oc, on, signal_time, manual, fixc, ordertype):
        if oc * op < 5000:
            self.windowQ.put((ui_num['C로그텍스트'], f'시스템 명령 오류 알림 - 주문금액이 5천원미만입니다.'))
            self.cstgQ.put((f'{og}취소', code))
            return

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

        self.OrderTimeLog(signal_time)
        if og == '매수':
            if self.upbit is not None:
                ret = None
                if ordertype == '시장가' or (ordertype is None and self.dict_set['코인매수주문구분'] == '시장가') or manual:
                    ret = self.upbit.buy_market_order(code, int(op * oc))
                elif ordertype == '지정가' or (ordertype is None and self.dict_set['코인매수주문구분'] == '지정가'):
                    ret = self.upbit.buy_limit_order(code, op, oc)

                if ret is not None:
                    if self.CheckError(ret):
                        dt = self.GetIndex()
                        self.dict_intg['추정예수금'] -= int(oc * op)
                        self.dict_buy[code] = [ret['uuid'], timedelta_sec(self.dict_set['코인매수취소시간초']), fixc, op, GetUpbitHogaunit(op)]
                        self.UpdateChegeollist(dt, code, og + '접수', oc, 0, oc, 0, dt[:14], op, ret['uuid'])
                        self.windowQ.put((ui_num['C로그텍스트'], f'주문 관리 시스템 알림 - [접수] {code} | {op} | {oc} | {og}'))
                else:
                    self.cstgQ.put(('매수취소', code))
                    self.windowQ.put((ui_num['C로그텍스트'], f'시스템 명령 오류 알림 - [주문 실패] {code} | {op} | {oc} | {og}'))

        elif og == '매도':
            if self.upbit is not None:
                ret = None
                if ordertype == '시장가' or self.dict_set['코인매도주문구분'] == '시장가' or manual:
                    ret = self.upbit.sell_market_order(code, oc)
                elif ordertype == '지정가' or self.dict_set['코인매도주문구분'] == '지정가':
                    ret = self.upbit.sell_limit_order(code, op, oc)

                if ret is not None:
                    if self.CheckError(ret):
                        dt = self.GetIndex()
                        self.dict_sell[code] = [ret['uuid'], timedelta_sec(self.dict_set['코인매도취소시간초']), fixc, op, GetUpbitHogaunit(op)]
                        self.UpdateChegeollist(dt, code, og + '접수', oc, 0, oc, 0, dt[:14], op, ret['uuid'])
                        self.windowQ.put((ui_num['C로그텍스트'], f'주문 관리 시스템 알림 - [접수] {code} | {op} | {oc} | {og}'))
                else:
                    self.cstgQ.put(('매도취소', code))
                    self.windowQ.put((ui_num['C로그텍스트'], f'시스템 명령 오류 알림 - [주문 실패] {code} | {op} | {oc} | {og}'))

        elif og in ('매수취소', '매도취소'):
            if self.upbit is not None:
                ret = self.upbit.cancel_order(on)
                if ret is not None:
                    if self.CheckError(ret):
                        dt = self.GetIndex()
                        if og == '매수취소':
                            self.dict_buy_cancel[code] = ret['uuid']
                        elif og == '매도취소':
                            self.dict_sell_cancel[code] = ret['uuid']
                        self.UpdateChegeollist(dt, code, og + '접수', oc, 0, oc, 0, dt[:14], 0, ret['uuid'])
                        self.windowQ.put((ui_num['C로그텍스트'], f'주문 관리 시스템 알림 - [접수] {code} | {op} | {oc} | {og}'))
                else:
                    self.windowQ.put((ui_num['C로그텍스트'], f'시스템 명령 오류 알림 - [주문 실패] {code} | {op} | {oc} | {og}'))

        self.dict_time['주문시간'] = timedelta_sec(0.3)
        self.creceivQ.put(('주문목록', self.GetOrderCodeList()))

    def CheckChegeol(self):
        if len(self.dict_buy) > 0:
            order_list = []
            for code, order in self.dict_buy.items():
                order_info = self.GetOrderInfo(code, order[0])
                if order_info is not None:
                    order_list.append(order_info)

            if len(order_list) > 0:
                for code, oc, cc, mc, cp, op, on in order_list:
                    self.UpdateChejanData('매수', code, oc, cc, mc, cp, op, on)

        if len(self.dict_sell) > 0:
            order_list = []
            for code, order in self.dict_sell.items():
                order_info = self.GetOrderInfo(code, order[0])
                if order_info is not None:
                    order_list.append(order_info)

            if len(order_list) > 0:
                for code, oc, cc, mc, cp, op, on in order_list:
                    self.UpdateChejanData('매도', code, oc, cc, mc, cp, op, on)

        if len(self.dict_buy_cancel) > 0:
            order_list = []
            for code, uuid in self.dict_buy.items():
                order_info = self.GetOrderInfo(code, uuid)
                if order_info is not None:
                    order_list.append(order_info)

            if len(order_list) > 0:
                for code, oc, cc, mc, cp, op, on in order_list:
                    self.UpdateChejanData('매수취소', code, oc, cc, mc, cp, op, on)

        if len(self.dict_sell_cancel) > 0:
            order_list = []
            for code, uuid in self.dict_buy.items():
                order_info = self.GetOrderInfo(code, uuid)
                if order_info is not None:
                    order_list.append(order_info)

            if len(order_list) > 0:
                for code, oc, cc, mc, cp, op, on in order_list:
                    self.UpdateChejanData('매도취소', code, oc, cc, mc, cp, op, on)

    def GetOrderInfo(self, code, uuid):
        time.sleep(0.07)
        order_info = None
        ret = self.upbit.get_order(uuid)
        if ret is not None and self.CheckError(ret):
            try:
                op = float(ret['price'])
            except:
                op = 0.
            try:
                oc = float(ret['volume'])
            except:
                oc = 0.
            try:
                mc = float(ret['remaining_volume'])
            except:
                mc = 0.

            cc, cp, tg = 0., 0., 0.
            if ret['trades_count'] > 0:
                trades = ret['trades']
                for i in range(len(trades)):
                    tg += float(trades[i]['funds'])
                    cc += float(trades[i]['volume'])
                if cc > 0:
                    cp = round(tg / cc, 4)
                    cc = round(cc, 8)

            if cc > 0:
                if uuid not in self.dict_order_cc.keys():
                    order_info = [code, oc, cc, mc, cp, op, uuid]
                    self.dict_order_cc[uuid] = cc
                else:
                    cc_ = round(cc - self.dict_order_cc[uuid], 8)
                    if cc_ > 0:
                        order_info = [code, oc, cc_, mc, cp, op, uuid]
                        self.dict_order_cc[uuid] = cc

                if mc == 0 and uuid in self.dict_order_cc.keys():
                    del self.dict_order_cc[uuid]

        return order_info

    def JangoCheongsan(self, gubun):
        if gubun == '수동':
            self.dict_bool['장초전략잔고청산'] = True
            self.dict_bool['장중전략잔고청산'] = True
        else:
            self.dict_bool[f'{gubun}전략잔고청산'] = True

        if len(self.dict_buy) > 0:
            for code in list(self.dict_buy.keys()):
                self.CancelOrder(code, '매수')

        if len(self.dict_sell) > 0:
            for code in list(self.dict_sell.keys()):
                self.CancelOrder(code, '매도')

        if (gubun == '수동' or self.dict_set[f'코인{gubun}잔고청산']) and len(self.df_jg) > 0:
            for code in self.df_jg.index:
                c, oc = self.df_jg['현재가'][code], self.df_jg['보유수량'][code]
                if self.dict_set['코인모의투자']:
                    self.UpdateChejanData('매도', code, oc, oc, 0, c, c, '')
                else:
                    ret = self.upbit.sell_market_order(code, oc)
                    if ret is not None:
                        if self.CheckError(ret):
                            self.dict_sell[code] = [ret['uuid'], now()]
                    else:
                        self.windowQ.put((ui_num['C로그텍스트'], f'시스템 명령 오류 알림 - [주문 실패] {code} | {c} | {oc} | 매도'))
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
                self.CreateOrder(f'{gubun}취소', code, op, mc, on, now(), False, 0, None)

    def UpdateChejanData(self, gubun, code, oc, cc, mc, cp, op, on):
        dt = self.GetIndex()

        if gubun in ('매수', '매도'):
            if gubun == '매수':
                if code in self.df_jg.index:
                    jc = round(self.df_jg['보유수량'][code] + cc, 8)
                    jg = int(self.df_jg['매입금액'][code] + cc * cp)
                    jp = round(jg / jc, 4)
                    pg, sg, sp = GetUpbitPgSgSp(jg, jc * cp)
                    columns = ['매입가', '현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량', '매수시간']
                    self.df_jg.loc[code, columns] = jp, cp, sp, sg, jg, pg, jc, dt[:14]
                else:
                    jc = cc
                    jg = int(cc * cp)
                    jp = cp
                    pg, sg, sp = GetUpbitPgSgSp(jg, jc * cp)
                    self.df_jg.loc[code] = code, jp, cp, sp, sg, jg, pg, jc, 0, 0, dt[:14]

                if mc == 0:
                    self.df_jg.loc[code, '분할매수횟수'] = self.df_jg['분할매수횟수'][code] + 1
                    if code in self.dict_buy.keys():
                        del self.dict_buy[code]

            else:
                jc = round(self.df_jg['보유수량'][code] - cc, 8)
                jp = self.df_jg['매입가'][code]
                if jc != 0:
                    jg = int(jp * jc)
                    pg, sg, sp = GetUpbitPgSgSp(jg, jc * cp)
                    columns = ['현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량']
                    self.df_jg.loc[code, columns] = cp, sp, sg, jg, pg, jc
                else:
                    self.df_jg.drop(index=code, inplace=True)

                if mc == 0:
                    if jc > 0:
                        self.df_jg.loc[code, '분할매도횟수'] = self.df_jg['분할매도횟수'][code] + 1
                    if code in self.dict_sell.keys():
                        del self.dict_sell[code]

                jg = jp * cc
                pg, sg, sp = GetUpbitPgSgSp(jg, cc * cp)
                self.UpdateTradelist(dt, code, jg, pg, cc, sp, sg, dt[:14])

                if sp < 0:
                    self.dict_name[code][3] = timedelta_sec(self.dict_set['코인매수금지손절간격초'])

            columns = ['평가손익', '매입금액', '평가금액', '분할매수횟수', '분할매도횟수']
            self.df_jg[columns] = self.df_jg[columns].astype(int)
            self.df_jg.sort_values(by=['매입금액'], ascending=False, inplace=True)
            self.cstgQ.put(('잔고목록', self.df_jg))

            if mc == 0:
                self.cstgQ.put((gubun + '완료', code))

            self.UpdateChegeollist(dt, code, gubun, oc, cc, mc, cp, dt[:14], op, on)

            if gubun == '매수':
                self.dict_intg['예수금'] -= int(cc * cp)
            else:
                self.dict_intg['예수금'] += jg + sg
                self.dict_intg['추정예수금'] += jg + sg

            self.queryQ.put(('거래디비', self.df_jg, 'c_jangolist', 'replace'))
            if self.dict_set['코인알림소리']:
                self.soundQ.put(f'{self.dict_name[code][0]}을 {gubun}하였습니다.')
            self.windowQ.put((ui_num['C로그텍스트'], f'주문 관리 시스템 알림 - [체결] {code} | {cp} | {cc} | {gubun}'))

        elif gubun == '시드부족':
            self.UpdateChegeollist(dt, code, gubun, oc, cc, mc, cp, dt[:14], op, on)

        elif gubun in ('매수취소', '매도취소'):
            df = self.GetMichegeolDF(code, gubun.replace('취소', ''))
            if len(df) > 0 and df['미체결수량'].iloc[-1] > 0:
                if df['체결수량'].iloc[-1] > 0 and code in self.df_jg.index:
                    if gubun == '매수취소':
                        self.df_jg.loc[code, '분할매수횟수'] = self.df_jg['분할매수횟수'][code] + 1
                    elif gubun == '매도취소':
                        self.df_jg.loc[code, '분할매도횟수'] = self.df_jg['분할매도횟수'][code] + 1
                    self.cstgQ.put(('잔고목록', self.df_jg))

                if gubun == '매수취소':
                    self.dict_intg['추정예수금'] += df['미체결수량'].iloc[-1] * df['주문가격'].iloc[-1]

                if gubun == '매수취소' and code in self.dict_buy.keys():
                    del self.dict_buy[code]
                elif gubun == '매도취소' and code in self.dict_sell.keys():
                    del self.dict_sell[code]

            self.cstgQ.put((gubun, code))
            self.UpdateChegeollist(dt, code, gubun, oc, cc, mc, cp, dt[:14], op, on)

            if self.dict_set['코인알림소리']:
                self.soundQ.put(f'{self.dict_name[code][0]}을 {gubun}하였습니다.')
            self.windowQ.put((ui_num['C로그텍스트'], f'주문 관리 시스템 알림 - [확인] {code} | {op} | {oc} | {gubun}'))

        self.creceivQ.put(('잔고목록', tuple(self.df_jg.index)))
        self.creceivQ.put(('주문목록', self.GetOrderCodeList()))

    def UpdateTradelist(self, index, code, jg, pg, cc, sp, sg, ct):
        self.df_td.loc[index] = code, jg, pg, cc, sp, sg, ct
        self.windowQ.put((ui_num['C거래목록'], self.df_td[::-1]))

        df = pd.DataFrame([[code, jg, pg, cc, sp, sg, ct]], columns=columns_td, index=[index])
        self.queryQ.put(('거래디비', df, 'c_tradelist', 'append'))

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

    def UpdateChegeollist(self, index, code, gubun, oc, cc, mc, cp, dt, op, on):
        self.dict_name[code][2] = timedelta_sec(self.dict_set['코인매수금지간격초'])
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
                tujagm = int(self.dict_set['코인장초투자금'] * 1_000_000)
            else:
                tujagm = int(self.dict_set['코인장중투자금'] * 1_000_000)
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
        self.df_td = pd.DataFrame(columns=columns_td)
        self.GetBalances()
        self.dict_bool['실현손익저장'] = True

    def OrderTimeLog(self, signal_time):
        gap = (now() - signal_time).total_seconds()
        self.windowQ.put((ui_num['C단순텍스트'], f'시그널 주문 시간 알림 - 발생시간과 주문시간의 차이는 [{gap:.6f}]초입니다.'))

    def CheckError(self, ret):
        if type(ret) == dict and list(ret.keys())[0] == 'error':
            self.windowQ.put((ui_num['C로그텍스트'], f"시스템 명령 오류 알림 - {ret['error']['name']} : {ret['error']['message']}"))
            return False
        return True

    def GetOrderCodeList(self):
        return tuple(self.dict_buy.keys()) + tuple(self.dict_sell.keys())

    def GetMichegeolDF(self, code, gubun):
        return self.df_cj[(self.df_cj['종목명'] == code) & ((self.df_cj['주문구분'] == gubun) | (self.df_cj['주문구분'] == f'{gubun}접수'))]

    def GetIndex(self):
        dt = strf_time('%Y%m%d%H%M%S%f', timedelta_sec(-32400))
        if dt in self.df_cj.index:
            while dt in self.df_cj.index:
                dt = str(int(dt) + 1)
        return dt
