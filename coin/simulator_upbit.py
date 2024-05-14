import pyupbit
import pandas as pd
from utility.static import now, strf_time, timedelta_sec, int_hms_utc, GetUpbitPgSgSp
from utility.setting import columns_cj, columns_tj, columns_jg, columns_td, columns_tt, ui_num, DICT_SET


class ReceiverUpbit2:
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
        self.Start()

    def Start(self):
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


class TraderUpbit2:
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
        self.df_jg = pd.DataFrame(columns=columns_jg)
        self.df_tj = pd.DataFrame(columns=columns_tj)
        self.df_td = pd.DataFrame(columns=columns_td)
        self.df_tt = pd.DataFrame(columns=columns_tt)

        self.dict_name = {}
        self.dict_curc = {}
        self.dict_buy  = {}
        self.dict_sell = {}

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
        self.UpdateDictName()
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

    def UpdateDictName(self):
        for dict_ticker in pyupbit.get_tickers(fiat="KRW", verbose=True):
            code = dict_ticker['market']
            name = dict_ticker['korean_name']
            if code not in self.dict_name.keys():
                dummy_time = timedelta_sec(-3600)
                self.dict_name[code] = [name, dummy_time, dummy_time, dummy_time]

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
                        pg, sg, sp = GetUpbitPgSgSp(jg, jc * c)
                        columns = ['현재가', '수익률', '평가손익', '평가금액']
                        self.df_jg.loc[code, columns] = c, sp, sg, pg
                except:
                    pass
            elif data[0] == '설정변경':
                self.dict_set = data[1]
            elif data[0] == '복기모드시간':
                self.test_time = data[1]

    def CheckOrder(self, og, code, op, oc):
        NIJ = code not in self.df_jg.index
        INB = code in self.dict_buy.keys()
        INS = code in self.dict_sell.keys()

        on = ''
        cancel = False
        if og == '매수':
            if INB:
                cancel = True
        elif og == '매도':
            if NIJ or INS:
                cancel = True

        if cancel:
            if '취소' not in og:
                self.cstgQ.put((f'{og}취소', code))
        else:
            if oc > 0:
                self.CreateOrder(og, code, op, oc, on)
            else:
                self.cstgQ.put((f'{og}취소', code))

    def CreateOrder(self, og, code, op, oc, on):
        ct = self.test_time
        if oc > 0:
            if self.dict_set['코인모의투자'] or og == '시드부족':
                if og == '시드부족':
                    self.UpdateChejanData(og, code, oc, 0, oc, op, 0, ct, on)
                else:
                    self.UpdateChejanData(og, code, oc, oc, 0, op, op, ct, on)

    def UpdateChejanData(self, gubun, code, oc, cc, mc, cp, op, ct, on):
        index = strf_time('%Y%m%d%H%M%S%f', timedelta_sec(-32400))
        if index in self.df_cj.index:
            while index in self.df_cj.index:
                index = str(int(index) + 1)

        if gubun in ('매수', '매도'):
            if gubun == '매수':
                if code in self.df_jg.index:
                    jc = round(self.df_jg['보유수량'][code] + cc, 8)
                    jg = int(self.df_jg['매입금액'][code] + cc * cp)
                    jp = round(jg / jc, 4)
                    pg, sg, sp = GetUpbitPgSgSp(jg, jc * cp)
                    columns = ['매입가', '현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량', '매수시간']
                    self.df_jg.loc[code, columns] = jp, cp, sp, sg, jg, pg, jc, ct
                else:
                    jc = cc
                    jg = int(cc * cp)
                    jp = cp
                    pg, sg, sp = GetUpbitPgSgSp(jg, jc * cp)
                    self.df_jg.loc[code] = code, jp, cp, sp, sg, jg, pg, jc, 0, 0, ct

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
                self.UpdateTradelist(index, code, jg, pg, cc, sp, sg, ct)

                if sp < 0:
                    self.dict_name[code][3] = timedelta_sec(self.dict_set['코인매수금지손절간격초'])

            columns = ['평가손익', '매입금액', '평가금액', '분할매수횟수', '분할매도횟수']
            self.df_jg[columns] = self.df_jg[columns].astype(int)
            self.df_jg.sort_values(by=['매입금액'], ascending=False, inplace=True)
            self.cstgQ.put(('잔고목록', self.df_jg))

            if mc == 0:
                self.cstgQ.put((gubun + '완료', code))

            self.UpdateChegeollist(index, code, gubun, oc, cc, mc, cp, ct, op, on)

            if gubun == '매수':
                self.dict_intg['예수금'] -= int(cc * cp)
            else:
                self.dict_intg['예수금'] += jg + sg
                self.dict_intg['추정예수금'] += jg + sg

            if self.dict_set['코인알림소리']:
                self.soundQ.put(f'{self.dict_name[code][0]}을 {gubun}하였습니다.')
            self.windowQ.put((ui_num['C로그텍스트'], f'주문 관리 시스템 알림 - [체결] {code} | {cp} | {cc} | {gubun}'))

        elif gubun == '시드부족':
            self.UpdateChegeollist(index, code, gubun, oc, cc, mc, cp, ct, op, on)

        self.creceivQ.put(('잔고목록', tuple(self.df_jg.index)))
        self.creceivQ.put(('주문목록', self.GetOrderCodeList()))

    def UpdateTradelist(self, index, code, jg, pg, cc, sp, sg, ct):
        self.df_td.loc[index] = code, jg, pg, cc, sp, sg, ct
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
        self.dict_name[code][2] = timedelta_sec(self.dict_set['코인매수금지간격초'])
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

    def GetOrderCodeList(self):
        return tuple(self.dict_buy.keys()) + tuple(self.dict_sell.keys())
