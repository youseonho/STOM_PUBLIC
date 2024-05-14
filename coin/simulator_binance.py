import re
import binance
import pyupbit
import pandas as pd
from utility.setting import columns_cj, columns_tj, columns_tdf, columns_jgf, columns_tt, ui_num, DICT_SET
from utility.static import now, strf_time, timedelta_sec, int_hms_utc, GetBinanceShortPgSgSp, GetBinanceLongPgSgSp


class ReceiverBinanceFuture2:
    def __init__(self, qlist):
        """
        windowQ, soundQ, queryQ, teleQ, chartQ, hogaQ, webcQ, backQ, creceivQ, ctraderQ,  cstgQ, liveQ, kimpQ, wdzservQ, totalQ
           0        1       2      3       4      5      6      7       8         9         10     11    12      13       14
        """
        self.hogaQ     = qlist[5]
        self.creceivQ  = qlist[8]
        self.ctraderQ  = qlist[9]
        self.cstgQ     = qlist[10]
        self.dict_set  = DICT_SET
        self.tuple_jang = []
        self.MainLoop()

    def MainLoop(self):
        while True:
            data = self.creceivQ.get()
            if len(data) != 2:
                self.UpdateTestMode(data)
            else:
                self.UpdateTuple(data)

    def UpdateTestMode(self, data):
        code = data[-1]
        c, o, h, low, per, _, ch, bids, asks = data[1:10]
        hogadata = data[12:34]
        self.cstgQ.put(data + (0,))
        if code in self.tuple_jang:
            self.ctraderQ.put((code, c))
        self.hogaQ.put((code, c, per, 0, 0, o, h, low))
        self.hogaQ.put((bids, ch))
        self.hogaQ.put((-asks, ch))
        self.hogaQ.put((code,) + hogadata + (0, 0))

    def UpdateTuple(self, data):
        gubun, data = data
        self.tuple_jang = data


class TraderBinanceFuture2:
    def __init__(self, qlist):
        """
        windowQ, soundQ, queryQ, teleQ, chartQ, hogaQ, webcQ, backQ, creceivQ, ctraderQ,  cstgQ, liveQ, kimpQ, wdzservQ, totalQ
           0        1       2      3       4      5      6      7       8         9         10     11    12      13       14
        """
        self.windowQ  = qlist[0]
        self.soundQ   = qlist[1]
        self.creceivQ = qlist[8]
        self.ctraderQ = qlist[9]
        self.cstgQ    = qlist[10]
        self.dict_set = DICT_SET

        self.df_cj = pd.DataFrame(columns=columns_cj)
        self.df_jg = pd.DataFrame(columns=columns_jgf)
        self.df_tj = pd.DataFrame(columns=columns_tj)
        self.df_td = pd.DataFrame(columns=columns_tdf)
        self.df_tt = pd.DataFrame(columns=columns_tt)

        self.dict_info       = {}
        self.dict_curc       = {}
        self.dict_buy_long   = {}
        self.dict_sell_short = {}
        self.dict_sell_long  = {}
        self.dict_buy_short  = {}

        self.str_today = strf_time('%Y%m%d', timedelta_sec(-32400))
        self.dict_intg = {
            '예수금': 0,
            '추정예수금': 0,
            '추정예탁자산': 0,
            '종목당투자금': 0
        }
        curr_time = now()
        self.dict_time = {
            '계좌평가계산': curr_time,
            '잔고목록전송': curr_time
        }
        self.test_time = None
        self.binance = binance.Client()
        self.UpdateDictTime()
        self.GetBalances()
        self.MainLoop()

    def MainLoop(self):
        while True:
            data = self.ctraderQ.get()
            self.UpdateTuple(data)

            curr_time = now()
            if curr_time > self.dict_time['계좌평가계산']:
                inthmsutc = int_hms_utc()
                self.UpdateTotaljango(inthmsutc)
                self.dict_time['계좌평가계산'] = timedelta_sec(1)
            if curr_time > self.dict_time['잔고목록전송']:
                self.cstgQ.put(('잔고목록', self.df_jg))
                self.dict_time['잔고목록전송'] = timedelta_sec(0.5)

    def UpdateDictTime(self):
        def get_decimal_place(float_):
            float_ = str(float(float_))
            float_ = float_.split('.')[1]
            return 0 if float_ == '0' else len(float_)

        dict_name = {x['market'].split('-')[1]: x['korean_name'] for x in pyupbit.get_tickers(verbose=True)}
        datas = self.binance.futures_ticker()
        for data in datas:
            code = data['symbol']
            if re.search('USDT$', code) is not None and code not in self.dict_time.keys():
                dummy_time = timedelta_sec(-3600)
                dummy_name = code.replace('USDT', '')
                self.dict_time[code] = [dict_name[dummy_name] if dummy_name in dict_name.keys() else dummy_name, dummy_time, dummy_time, dummy_time]

        datas = self.binance.futures_exchange_info()
        datas = [x for x in datas['symbols'] if re.search('USDT$', x['symbol']) is not None]
        self.dict_info = {x['symbol']: {'호가단위': float(x['filters'][0]['tickSize']), '소숫점자리수': get_decimal_place(x['filters'][2]['minQty'])} for x in datas}

    def GetBalances(self):
        self.dict_intg['예수금'] = self.dict_intg['추정예수금'] = self.dict_intg['추정예탁자산'] = 100_000_000

    def UpdateTuple(self, data):
        if len(data) == 6:
            self.CheckOrder(data[0], data[1], data[2], data[3])
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
            elif data[0] == '설정변경':
                self.dict_set = data[1]
            elif data[0] == '복기모드시간':
                self.test_time = data[1]

    def CheckOrder(self, og, code, op, oc):
        NIJ  = code not in self.df_jg.index
        INBL = code in self.dict_buy_long.keys()
        INSS = code in self.dict_sell_short.keys()
        INSL = code in self.dict_sell_long.keys()
        INBS = code in self.dict_buy_short.keys()

        on = ''
        cancel = False
        if og in ('BUY_LONG', 'SELL_SHORT'):
            if og == 'BUY_LONG' and INBL:     cancel = True
            elif og == 'SELL_SHORT' and INSS: cancel = True
        elif og in ('SELL_LONG', 'BUY_SHORT'):
            if og == 'SELL_LONG' and (NIJ or INSL):   cancel = True
            elif og == 'BUY_SHORT' and (NIJ or INBS): cancel = True

        if cancel:
            if 'CANCEL' not in og:
                self.cstgQ.put((f'{og}_CANCEL', code))
        else:
            if oc > 0:
                self.CreateOrder(og, code, op, oc, on)
            else:
                self.cstgQ.put((f'{og}_CANCEL', code))

    def CreateOrder(self, og, code, op, oc, on):
        ct = self.test_time
        if oc * op < 5:
            self.windowQ.put((ui_num['C로그텍스트'], '시스템 명령 오류 알림 - 최소주문금액 5 USDT 미만입니다.'))
            self.cstgQ.put((f'{og}_CANCEL', code))
            return

        if og in ('BUY_LONG', 'SELL_SHORT'):
            self.dict_intg['예수금'] -= op * oc
        elif og in ('SELL_LONG', 'BUY_SHORT'):
            self.dict_intg['예수금'] += op * round(oc / self.df_jg['레버리지'][code], self.dict_info[code]['소숫점자리수'])

        if og in ('BUY_LONG', 'SELL_SHORT'):
            oc = round(oc, self.dict_info[code]['소숫점자리수'])

        if oc > 0:
            if og == '시드부족':
                self.UpdateChejanData(og, code, oc, 0, oc, op, 0, ct, on)
            else:
                if og == 'BUY_LONG':
                    self.dict_buy_long[code] = [0, timedelta_sec(self.dict_set['코인매수취소시간초']), 0, op, 1]
                elif og == 'SELL_SHORT':
                    self.dict_sell_short[code] = [0, timedelta_sec(self.dict_set['코인매수취소시간초']), 0, op, 1]
                self.UpdateChejanData(og, code, oc, oc, 0, op, op, ct, on)

    def UpdateChejanData(self, gubun, code, oc, cc, mc, cp, op, ct, on):
        index = strf_time('%Y%m%d%H%M%S%f', timedelta_sec(-32400))
        if index in self.df_cj.index:
            while index in self.df_cj.index:
                index = str(int(index) + 1)

        if gubun in ('BUY_LONG', 'SELL_SHORT', 'SELL_LONG', 'BUY_SHORT'):
            if gubun == 'BUY_LONG':
                if code in self.df_jg.index:
                    jc = round(self.df_jg['보유수량'][code] + cc, self.dict_info[code]['소숫점자리수'])
                    jg = round(self.df_jg['매입금액'][code] + cc * cp, 4)
                    jp = round(jg / jc, 8)
                    cg = round(cp * jc, 4)
                    pg, sg, sp = GetBinanceLongPgSgSp(jg, cg, '시장가' in self.dict_set['코인매수주문구분'], '시장가' in self.dict_set['코인매도주문구분'])
                    columns = ['매입가', '현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량', '매수시간']
                    self.df_jg.loc[code, columns] = jp, cp, sp, sg, jg, pg, jc, ct
                else:
                    jg = round(cp * cc, 4)
                    lv = self.dict_set['바이낸스선물고정레버리지값'] if self.dict_set['바이낸스선물고정레버리지'] else self.dict_buy_long[code][4]
                    pg, sg, sp = GetBinanceLongPgSgSp(jg, jg, '시장가' in self.dict_set['코인매수주문구분'], '시장가' in self.dict_set['코인매도주문구분'])
                    self.df_jg.loc[code] = code, 'LONG', cp, cp, sp, sg, jg, pg, cc, lv, 0, 0, ct

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
                    self.df_jg.loc[code, columns] = jp, cp, sp, sg, jg, pg, jc, ct
                else:
                    jg = round(cc * cp, 4)
                    lv = self.dict_set['바이낸스선물고정레버리지값'] if self.dict_set['바이낸스선물고정레버리지'] else self.dict_sell_short[code][4]
                    pg, sg, sp = GetBinanceShortPgSgSp(jg, jg, '시장가' in self.dict_set['코인매수주문구분'], '시장가' in self.dict_set['코인매도주문구분'])
                    self.df_jg.loc[code] = code, 'SHORT', cp, cp, sp, sg, jg, pg, cc, lv, 0, 0, ct

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
                self.UpdateTradelist(index, code, 'LONG', jg, pg, cc, sp, sg, ct)

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
                self.UpdateTradelist(index, code, 'SHORT', jg, pg, cc, sp, sg, ct)

                if sp < 0:
                    self.dict_time[code][3] = timedelta_sec(self.dict_set['코인매수금지손절간격초'])

            self.df_jg.sort_values(by=['매입금액'], ascending=False, inplace=True)
            self.cstgQ.put(('잔고목록', self.df_jg))

            if mc == 0:
                self.cstgQ.put((f'{gubun}_COMPLETE', code))

            self.UpdateChegeollist(index, code, gubun, oc, cc, mc, cp, ct, op, on)

            if self.dict_set['코인알림소리']:
                text = ''
                if gubun == 'BUY_LONG':     text = '롱포지션을 진입'
                elif gubun == 'SELL_SHORT': text = '숏포지션을 진입'
                elif gubun == 'SELL_LONG':  text = '롱포지션을 청산'
                elif gubun == 'BUY_SHORT':  text = '숏포지션을 청산'
                self.soundQ.put(f'{self.dict_time[code][0]} {text}하였습니다.')
            self.windowQ.put((ui_num['C로그텍스트'], f'주문 관리 시스템 알림 - [체결] {code} | {cp} | {cc} | {gubun}'))

        elif gubun == '시드부족':
            self.UpdateChegeollist(index, code, gubun, oc, cc, mc, cp, ct, op, on)

        self.creceivQ.put(('잔고목록', tuple(self.df_jg.index)))
        self.creceivQ.put(('주문목록', self.GetOrderCodeList()))

    def UpdateTradelist(self, index, code, pos, jg, pg, cc, sp, sg, ct):
        self.df_td.loc[index] = code, pos, jg, pg, cc, sp, sg, ct
        self.windowQ.put((ui_num['C거래목록'], self.df_td[::-1]))
        self.UpdateTotaltradelist()

    def UpdateTotaltradelist(self):
        tdt = len(self.df_td)
        tbg = self.df_td['매수금액'].sum()
        tsg = self.df_td['매도금액'].sum()
        sig = self.df_td[self.df_td['수익금'] > 0]['수익금'].sum()
        ssg = self.df_td[self.df_td['수익금'] < 0]['수익금'].sum()
        sg  = self.df_td['수익금'].sum()
        sp  = round(sg / self.dict_intg['추정예탁자산'] * 100, 2)
        self.df_tt = pd.DataFrame([[tdt, tbg, tsg, sig, ssg, sp, sg]], columns=columns_tt, index=[self.str_today])
        self.windowQ.put((ui_num['C실현손익'], self.df_tt))

    def UpdateChegeollist(self, index, code, gubun, oc, cc, mc, cp, dt, op, on):
        self.dict_time[code][2] = timedelta_sec(self.dict_set['코인매수금지간격초'])
        self.df_cj.loc[index] = code, gubun, oc, cc, mc, cp, dt, op, on
        self.windowQ.put((ui_num['C체결목록'], self.df_cj[::-1]))

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

    def GetOrderCodeList(self):
        return tuple(self.dict_buy_long.keys()) + tuple(self.dict_sell_short.keys()) + tuple(self.dict_sell_long.keys()) + tuple(self.dict_buy_short.keys())
