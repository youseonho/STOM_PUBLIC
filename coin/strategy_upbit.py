import os
import math
import time
import sqlite3
import numpy as np
import pandas as pd
from talib import stream
from traceback import print_exc
from ui.ui_pattern import get_pattern_setup
# noinspection PyUnresolvedReferences
from utility.static import now, now_utc, strp_time, int_hms_utc, timedelta_sec, GetUpbitHogaunit, GetUpbitPgSgSp, pickle_read
from utility.setting import DB_STRATEGY, DICT_SET, ui_num, columns_jg, columns_gj, dict_order_ratio, PATTERN_PATH


# noinspection PyUnusedLocal
class StrategyUpbit:
    def __init__(self, qlist):
        """
        windowQ, soundQ, queryQ, teleQ, chartQ, hogaQ, webcQ, backQ, creceivQ, ctraderQ,  cstgQ, liveQ, kimpQ, wdzservQ
           0        1       2      3       4      5      6      7       8         9         10     11    12      13
        """
        self.windowQ  = qlist[0]
        self.queryQ   = qlist[2]
        self.chartQ   = qlist[4]
        self.ctraderQ = qlist[9]
        self.cstgQ    = qlist[10]
        self.dict_set = DICT_SET

        self.buystrategy1  = None
        self.sellstrategy1 = None
        self.buystrategy2  = None
        self.sellstrategy2 = None

        self.vars          = {}
        self.vars2         = {}
        self.dict_tik_ar   = {}
        self.dict_tik_ar2  = {}
        self.dict_buyinfo  = {}
        self.dict_sgn_tik  = {}
        self.dict_buy_tik  = {}

        self.tuple_gsjm  = ()
        self.list_buy    = []
        self.list_sell   = []

        self.bhogainfo  = {}
        self.shogainfo  = {}
        self.dict_hilo  = {}

        self.indexn     = 0
        self.indexb     = 0
        self.jgrv_count = 0
        self.int_tujagm = 0
        self.stg_change = False
        self.chart_code = None
        self.df_jg      = pd.DataFrame(columns=columns_jg)
        self.df_gj      = pd.DataFrame(columns=columns_gj)

        self.pattern_buy1       = None
        self.pattern_sell1      = None
        self.dict_pattern1      = {}
        self.dict_pattern_buy1  = {}
        self.dict_pattern_sell1 = {}

        self.pattern_buy2       = None
        self.pattern_sell2      = None
        self.dict_pattern2      = {}
        self.dict_pattern_buy2  = {}
        self.dict_pattern_sell2 = {}

        self.UpdateStringategy()
        self.MainLoop()

    def UpdateStringategy(self):
        con  = sqlite3.connect(DB_STRATEGY)
        dfb  = pd.read_sql('SELECT * FROM coinbuy', con).set_index('index')
        dfs  = pd.read_sql('SELECT * FROM coinsell', con).set_index('index')
        dfob = pd.read_sql('SELECT * FROM coinoptibuy', con).set_index('index')
        dfos = pd.read_sql('SELECT * FROM coinoptisell', con).set_index('index')
        dfp  = pd.read_sql('SELECT * FROM coinpattern', con).set_index('index')
        con.close()

        if self.dict_set['코인장초매수전략'] == '':
            self.buystrategy1 = None
        elif self.dict_set['코인장초매수전략'] in dfb.index:
            self.buystrategy1 = compile(dfb['전략코드'][self.dict_set['코인장초매수전략']], '<string>', 'exec')
        elif self.dict_set['코인장초매수전략'] in dfob.index:
            self.buystrategy1 = compile(dfob['전략코드'][self.dict_set['코인장초매수전략']], '<string>', 'exec')
            self.vars = {i: var for i, var in enumerate(list(dfob.loc[self.dict_set['코인장초매수전략']])[1:]) if var != 9999.}

        if self.dict_set['코인장초매도전략'] == '':
            self.sellstrategy1 = None
        elif self.dict_set['코인장초매도전략'] in dfs.index:
            self.sellstrategy1 = compile(dfs['전략코드'][self.dict_set['코인장초매도전략']], '<string>', 'exec')
        elif self.dict_set['코인장초매도전략'] in dfos.index:
            self.sellstrategy1 = compile(dfos['전략코드'][self.dict_set['코인장초매도전략']], '<string>', 'exec')

        if self.dict_set['코인장중매수전략'] == '':
            self.buystrategy2 = None
        elif self.dict_set['코인장중매수전략'] in dfb.index:
            self.buystrategy2 = compile(dfb['전략코드'][self.dict_set['코인장중매수전략']], '<string>', 'exec')
        elif self.dict_set['코인장중매수전략'] in dfob.index:
            self.buystrategy2 = compile(dfob['전략코드'][self.dict_set['코인장중매수전략']], '<string>', 'exec')
            self.vars2 = {i: var for i, var in enumerate(list(dfob.loc[self.dict_set['코인장중매수전략']])[1:]) if var != 9999.}

        if self.dict_set['코인장중매도전략'] == '':
            self.sellstrategy2 = None
        elif self.dict_set['코인장중매도전략'] in dfs.index:
            self.sellstrategy2 = compile(dfs['전략코드'][self.dict_set['코인장중매도전략']], '<string>', 'exec')
        elif self.dict_set['코인장중매도전략'] in dfos.index:
            self.sellstrategy2 = compile(dfos['전략코드'][self.dict_set['코인장중매도전략']], '<string>', 'exec')

        if self.dict_set['코인장초패턴인식'] and self.dict_set['코인장초매수전략'] in dfp.index:
            self.dict_pattern1, self.dict_pattern_buy1, self.dict_pattern_sell1 = get_pattern_setup(dfp['패턴설정'][self.dict_set['코인장초매수전략']])
            file_name = f"{PATTERN_PATH}/pattern_coin_{self.dict_set['코인장초매수전략']}"
            if os.path.isfile(f'{file_name}_buy.pkl'):
                self.pattern_buy1  = pickle_read(f'{file_name}_buy')
            if os.path.isfile(f'{file_name}_sell.pkl'):
                self.pattern_sell1 = pickle_read(f'{file_name}_sell')

        if self.dict_set['코인장중패턴인식'] and self.dict_set['코인장중매수전략'] in dfp.index:
            self.dict_pattern2, self.dict_pattern_buy2, self.dict_pattern_sell2 = get_pattern_setup(dfp['패턴설정'][self.dict_set['코인장중매수전략']])
            file_name = f"{PATTERN_PATH}/pattern_coin_{self.dict_set['코인장중매수전략']}"
            if os.path.isfile(f'{file_name}_buy.pkl'):
                self.pattern_buy2  = pickle_read(f'{file_name}_buy')
            if os.path.isfile(f'{file_name}_sell.pkl'):
                self.pattern_sell2 = pickle_read(f'{file_name}_sell')

    def MainLoop(self):
        self.windowQ.put((ui_num['C로그텍스트'], '시스템 명령 실행 알림 - 전략 연산 시작'))
        while True:
            data = self.cstgQ.get()
            if type(data) == tuple:
                if len(data) > 3:
                    self.Strategy(data)
                elif len(data) == 2:
                    self.UpdateTuple(data)
            elif type(data) == str:
                self.UpdateString(data)
                if data == '프로세스종료':
                    break

        self.windowQ.put((ui_num['C로그텍스트'], '시스템 명령 실행 알림 - 전략연산 종료'))
        time.sleep(1)

    def UpdateTuple(self, data):
        gubun, data = data
        if gubun == '관심목록':
            self.tuple_gsjm = data
            drop_index_list = list(set(list(self.df_gj.index)) - set(self.tuple_gsjm))
            if drop_index_list: self.df_gj.drop(index=drop_index_list, inplace=True)
        elif gubun in ('매수완료', '매수취소'):
            if data in self.list_buy:
                self.list_buy.remove(data)
            if gubun == '매수완료':
                if data in self.dict_sgn_tik.keys():
                    self.dict_buy_tik[data] = self.dict_sgn_tik[data]
                else:
                    self.dict_buy_tik[data] = len(self.dict_tik_ar[data]) - 1
        elif gubun in ('매도완료', '매도취소'):
            if data in self.list_sell:
                self.list_sell.remove(data)
        elif gubun == '매수주문':
            if data not in self.list_buy:
                self.list_buy.append(data)
        elif gubun == '매도주문':
            if data not in self.list_sell:
                self.list_sell.append(data)
        elif gubun == '잔고목록':
            self.df_jg = data
            self.jgrv_count += 1
            if self.jgrv_count == 2:
                self.jgrv_count = 0
                self.PutGsjmAndDeleteHilo()
        elif gubun == '매수전략':
            if int_hms_utc() < self.dict_set['코인장초전략종료시간']:
                self.buystrategy1 = compile(data, '<string>', 'exec')
            else:
                self.buystrategy2 = compile(data, '<string>', 'exec')
        elif gubun == '매도전략':
            if int_hms_utc() < self.dict_set['코인장초전략종료시간']:
                self.sellstrategy1 = compile(data, '<string>', 'exec')
            else:
                self.sellstrategy2 = compile(data, '<string>', 'exec')
        elif gubun == '종목당투자금':
            self.int_tujagm = data
        elif gubun == '차트종목코드':
            self.chart_code = data
        elif gubun == '설정변경':
            self.dict_set = data
            self.UpdateStringategy()

    def UpdateString(self, data):
        if data == '매수전략중지':
            self.buystrategy1 = None
            self.buystrategy2 = None
        elif data == '매도전략중지':
            self.sellstrategy1 = None
            self.sellstrategy2 = None
        elif data == '복기모드종료':
            self.dict_tik_ar = {}

    def Strategy(self, data):
        체결시간, 현재가, 시가, 고가, 저가, 등락율, 당일거래대금, 체결강도, 초당매수수량, 초당매도수량, 초당거래대금, 고저평균대비등락율, 매도총잔량, 매수총잔량, \
            매도호가5, 매도호가4, 매도호가3, 매도호가2, 매도호가1, 매수호가1, 매수호가2, 매수호가3, 매수호가4, 매수호가5, \
            매도잔량5, 매도잔량4, 매도잔량3, 매도잔량2, 매도잔량1, 매수잔량1, 매수잔량2, 매수잔량3, 매수잔량4, 매수잔량5, \
            매도수5호가잔량합, 관심종목, 종목코드, 틱수신시간 = data

        def Parameter_Previous(aindex, pre):
            pindex = (self.indexn - pre) if pre != -1 else self.indexb
            return self.dict_tik_ar[종목코드][pindex, aindex]

        def 현재가N(pre):
            return Parameter_Previous(1, pre)

        def 시가N(pre):
            return Parameter_Previous(2, pre)

        def 고가N(pre):
            return Parameter_Previous(3, pre)

        def 저가N(pre):
            return Parameter_Previous(4, pre)

        def 등락율N(pre):
            return Parameter_Previous(5, pre)

        def 당일거래대금N(pre):
            return Parameter_Previous(6, pre)

        def 체결강도N(pre):
            return Parameter_Previous(7, pre)

        def 초당매수수량N(pre):
            return Parameter_Previous(8, pre)

        def 초당매도수량N(pre):
            return Parameter_Previous(9, pre)

        def 초당거래대금N(pre):
            return Parameter_Previous(10, pre)

        def 고저평균대비등락율N(pre):
            return Parameter_Previous(11, pre)

        def 매도총잔량N(pre):
            return Parameter_Previous(12, pre)

        def 매수총잔량N(pre):
            return Parameter_Previous(13, pre)

        def 매도호가5N(pre):
            return Parameter_Previous(14, pre)

        def 매도호가4N(pre):
            return Parameter_Previous(15, pre)

        def 매도호가3N(pre):
            return Parameter_Previous(16, pre)

        def 매도호가2N(pre):
            return Parameter_Previous(17, pre)

        def 매도호가1N(pre):
            return Parameter_Previous(18, pre)

        def 매수호가1N(pre):
            return Parameter_Previous(19, pre)

        def 매수호가2N(pre):
            return Parameter_Previous(20, pre)

        def 매수호가3N(pre):
            return Parameter_Previous(21, pre)

        def 매수호가4N(pre):
            return Parameter_Previous(22, pre)

        def 매수호가5N(pre):
            return Parameter_Previous(23, pre)

        def 매도잔량5N(pre):
            return Parameter_Previous(24, pre)

        def 매도잔량4N(pre):
            return Parameter_Previous(25, pre)

        def 매도잔량3N(pre):
            return Parameter_Previous(26, pre)

        def 매도잔량2N(pre):
            return Parameter_Previous(27, pre)

        def 매도잔량1N(pre):
            return Parameter_Previous(28, pre)

        def 매수잔량1N(pre):
            return Parameter_Previous(29, pre)

        def 매수잔량2N(pre):
            return Parameter_Previous(30, pre)

        def 매수잔량3N(pre):
            return Parameter_Previous(31, pre)

        def 매수잔량4N(pre):
            return Parameter_Previous(32, pre)

        def 매수잔량5N(pre):
            return Parameter_Previous(33, pre)

        def 매도수5호가잔량합N(pre):
            return Parameter_Previous(34, pre)

        def 관심종목N(pre):
            return Parameter_Previous(35, pre)

        def 이동평균(tick, pre=0):
            if tick == 60:
                return Parameter_Previous(36, pre)
            elif tick == 300:
                return Parameter_Previous(37, pre)
            elif tick == 600:
                return Parameter_Previous(38, pre)
            elif tick == 1200:
                return Parameter_Previous(39, pre)
            else:
                sindex = (self.indexn + 1 - pre - tick) if pre != -1  else self.indexb + 1 - tick
                eindex = (self.indexn + 1 - pre) if pre != -1  else self.indexb + 1
                return round(self.dict_tik_ar[종목코드][sindex:eindex, 1].mean(), 8)

        def Parameter_Area(aindex, vindex, tick, pre, gubun_):
            if tick == 평균값계산틱수:
                return Parameter_Previous(aindex, pre)
            else:
                sindex = (self.indexn + 1 - pre - tick) if pre != -1  else self.indexb + 1 - tick
                eindex = (self.indexn + 1 - pre) if pre != -1  else self.indexb + 1
                if gubun_ == 'max':
                    return self.dict_tik_ar[종목코드][sindex:eindex, vindex].max()
                elif gubun_ == 'min':
                    return self.dict_tik_ar[종목코드][sindex:eindex, vindex].min()
                elif gubun_ == 'sum':
                    return self.dict_tik_ar[종목코드][sindex:eindex, vindex].sum()
                else:
                    return self.dict_tik_ar[종목코드][sindex:eindex, vindex].mean()

        def 최고현재가(tick, pre=0):
            return Parameter_Area(40, 1, tick, pre, 'max')

        def 최저현재가(tick, pre=0):
            return Parameter_Area(41, 1, tick, pre, 'min')

        def 체결강도평균(tick, pre=0):
            return Parameter_Area(42, 7, tick, pre, 'mean')

        def 최고체결강도(tick, pre=0):
            return Parameter_Area(43, 7, tick, pre, 'max')

        def 최저체결강도(tick, pre=0):
            return Parameter_Area(44, 7, tick, pre, 'min')

        def 최고초당매수수량(tick, pre=0):
            return Parameter_Area(45, 14, tick, pre, 'max')

        def 최고초당매도수량(tick, pre=0):
            return Parameter_Area(46, 15, tick, pre, 'max')

        def 누적초당매수수량(tick, pre=0):
            return Parameter_Area(47, 14, tick, pre, 'sum')

        def 누적초당매도수량(tick, pre=0):
            return Parameter_Area(48, 15, tick, pre, 'sum')

        def 초당거래대금평균(tick, pre=0):
            return Parameter_Area(49, 19, tick, pre, 'mean')

        def Parameter_Dgree(aindex, vindex, tick, pre, cf):
            if tick == 평균값계산틱수:
                return Parameter_Previous(aindex, pre)
            else:
                sindex = (self.indexn + 1 - pre - tick) if pre != -1  else self.indexb + 1 - tick
                eindex = (self.indexn + 1 - pre) if pre != -1  else self.indexb + 1
                dmp_gap = self.dict_tik_ar[종목코드][eindex, vindex] - self.dict_tik_ar[종목코드][sindex, vindex]
                return round(math.atan2(dmp_gap * cf, tick) / (2 * math.pi) * 360, 2)

        def 등락율각도(tick, pre=0):
            return Parameter_Dgree(50, 5, tick, pre, 10)

        def 당일거래대금각도(tick, pre=0):
            return Parameter_Dgree(51, 6, tick, pre, 0.00000001)

        if self.dict_set['보조지표사용']:
            def BBU_N(pre):
                return Parameter_Previous(-14, pre)

            def BBM_N(pre):
                return Parameter_Previous(-13, pre)

            def BBL_N(pre):
                return Parameter_Previous(-12, pre)

            def MACD_N(pre):
                return Parameter_Previous(-11, pre)

            def MACDS_N(pre):
                return Parameter_Previous(-10, pre)

            def MACDH_N(pre):
                return Parameter_Previous(-9, pre)

            def APO_N(pre):
                return Parameter_Previous(-8, pre)

            def KAMA_N(pre):
                return Parameter_Previous(-7, pre)

            def RSI_N(pre):
                return Parameter_Previous(-6, pre)

            def HT_SINE_N(pre):
                return Parameter_Previous(-5, pre)

            def HT_LSINE_N(pre):
                return Parameter_Previous(-4, pre)

            def HT_PHASE_N(pre):
                return Parameter_Previous(-3, pre)

            def HT_QUDRA_N(pre):
                return Parameter_Previous(-2, pre)

            def OBV_N(pre):
                return Parameter_Previous(-1, pre)

        시분초, 호가단위 = int(str(체결시간)[8:]), GetUpbitHogaunit(현재가)
        데이터길이 = len(self.dict_tik_ar[종목코드]) + 1 if 종목코드 in self.dict_tik_ar.keys() else 1
        평균값계산틱수 = self.dict_set['코인장초평균값계산틱수'] if 시분초 < self.dict_set['코인장초전략종료시간'] else self.dict_set['코인장중평균값계산틱수']
        이동평균60_, 이동평균300_, 이동평균600_, 이동평균1200_, 최고현재가_, 최저현재가_ = 0., 0., 0., 0., 0, 0
        체결강도평균_, 최고체결강도_, 최저체결강도_, 최고초당매수수량_, 최고초당매도수량_ = 0., 0., 0., 0, 0
        누적초당매수수량_, 누적초당매도수량_, 초당거래대금평균_, 등락율각도_, 당일거래대금각도_, 전일비각도_ = 0, 0, 0., 0., 0., 0.
        BBU, BBM, BBL, MACD, MACDS, MACDH, APO, KAMA, RSI, HT_SINE, HT_LSINE, HT_PHASE, HT_QUDRA, OBV = \
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        bhogainfo = ((매도호가1, 매도잔량1), (매도호가2, 매도잔량2), (매도호가3, 매도잔량3), (매도호가4, 매도잔량4), (매도호가5, 매도잔량5))
        shogainfo = ((매수호가1, 매수잔량1), (매수호가2, 매수잔량2), (매수호가3, 매수잔량3), (매수호가4, 매수잔량4), (매수호가5, 매수잔량5))
        self.bhogainfo = bhogainfo[:self.dict_set['코인매수시장가잔량범위']]
        self.shogainfo = shogainfo[:self.dict_set['코인매도시장가잔량범위']]

        if 종목코드 in self.dict_tik_ar.keys():
            if len(self.dict_tik_ar[종목코드]) >=   59: 이동평균60_   = round((self.dict_tik_ar[종목코드][  -59:, 1].sum() + 현재가) /   60, 8)
            if len(self.dict_tik_ar[종목코드]) >=  299: 이동평균300_  = round((self.dict_tik_ar[종목코드][ -299:, 1].sum() + 현재가) /  300, 8)
            if len(self.dict_tik_ar[종목코드]) >=  599: 이동평균600_  = round((self.dict_tik_ar[종목코드][ -599:, 1].sum() + 현재가) /  600, 8)
            if len(self.dict_tik_ar[종목코드]) >= 1199: 이동평균1200_ = round((self.dict_tik_ar[종목코드][-1199:, 1].sum() + 현재가) / 1200, 8)
            if len(self.dict_tik_ar[종목코드]) >= 평균값계산틱수 - 1:
                최고현재가_      = max(self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1):, 1].max(), 현재가)
                최저현재가_      = min(self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1):, 1].min(), 현재가)
                체결강도평균_    = round((self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1):, 7].sum() + 체결강도) / 평균값계산틱수, 3)
                최고체결강도_    = max(self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1):, 7].max(), 체결강도)
                최저체결강도_    = min(self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1):, 7].min(), 체결강도)
                최고초당매수수량_ = max(self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1):, 8].max(), 초당매수수량)
                최고초당매도수량_ = min(self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1):, 9].min(), 초당매도수량)
                누적초당매수수량_ =     self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1):, 8].sum() + 초당매수수량
                누적초당매도수량_ =     self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1):, 9].sum() + 초당매도수량
                초당거래대금평균_ = int((self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1):, 10].sum() + 초당거래대금) / 평균값계산틱수)
                등락율각도_      = round(math.atan2((등락율 - self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1), 5]) * 10, 평균값계산틱수) / (2 * math.pi) * 360, 2)
                당일거래대금각도_ = round(math.atan2((당일거래대금 - self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1), 6]) / 100_000_000, 평균값계산틱수) / (2 * math.pi) * 360, 2)

            """
            체결시간, 현재가, 시가, 고가, 저가, 등락율, 당일거래대금, 체결강도, 초당매수수량, 초당매도수량, 초당거래대금, 고저평균대비등락율,
               0      1     2    3     4     5        6         7         8           9          10            11
            매도총잔량, 매수총잔량, 매도호가5, 매도호가4, 매도호가3, 매도호가2, 매도호가1, 매수호가1, 매수호가2, 매수호가3, 매수호가4, 매수호가5,
               12        13        14       15       16        17       18        19       20       21        22       23
            매도잔량5, 매도잔량4, 매도잔량3, 매도잔량2, 매도잔량1, 매수잔량1, 매수잔량2, 매수잔량3, 매수잔량4, 매수잔량5, 매도수5호가잔량합, 관심종목,
               24        25       26       27        28       29        30       31       32        33         34           35
            이동평균60_, 이동평균300_, 이동평균600_, 이동평균1200_, 최고현재가_, 최저현재가_, 체결강도평균_, 최고체결강도_, 최저체결강도_,
                36         37           38          39          40         51          42           43          44
            최고초당매수수량_, 최고초당매도수량_, 누적초당매수수량_, 누적초당매도수량_, 초당거래대금평균_, 등락율각도_, 당일거래대금각도_,
                   45            46              47              48              49           50           51
            BBU, BBM, BBL, MACD, MACDS, MACDH, APO, KAMA, RSI, HT_SINE, HT_LSINE, HT_PHASE, HT_QUDRA, OBV
            52    53  54    55    56     57    58   59     60     61       62        63        64      65
            """

            if self.dict_set['보조지표사용']:
                k = self.dict_set['보조지표설정']
                close, volume = self.dict_tik_ar[종목코드][:, 1], self.dict_tik_ar[종목코드][:, 10]
                try:    BBU, BBM, BBL      = stream.BBANDS(   close, timeperiod=k[0],  nbdevup=k[1],     nbdevdn=k[2], matype=k[3])
                except: BBU, BBM, BBL      = 0, 0, 0
                try:    MACD, MACDS, MACDH = stream.MACD(     close, fastperiod=k[4],  slowperiod=k[5],  signalperiod=k[6])
                except: MACD, MACDS, MACDH = 0, 0, 0
                try:    APO                = stream.APO(      close, fastperiod=k[7],  slowperiod=k[8],  matype=k[9])
                except: APO                = 0
                try:    KAMA               = stream.KAMA(     close, timeperiod=k[17])
                except: KAMA               = 0
                try:    RSI                = stream.RSI(      close, timeperiod=k[18])
                except: RSI                = 0
                try:    HT_SINE, HT_LSINE  = stream.HT_SINE(  close)
                except: HT_SINE, HT_LSINE  = 0, 0
                try:    HT_PHASE, HT_QUDRA = stream.HT_PHASOR(close)
                except: HT_PHASE, HT_QUDRA = 0, 0
                try:    OBV                = stream.OBV(      close, volume)
                except: OBV                = 0

        if self.dict_set['보조지표사용']:
            new_data_tick = [
                체결시간, 현재가, 시가, 고가, 저가, 등락율, 당일거래대금, 체결강도, 초당매수수량, 초당매도수량, 초당거래대금,
                고저평균대비등락율, 매도총잔량, 매수총잔량, 매도호가5, 매도호가4, 매도호가3, 매도호가2, 매도호가1, 매수호가1, 매수호가2,
                매수호가3, 매수호가4, 매수호가5, 매도잔량5, 매도잔량4, 매도잔량3, 매도잔량2, 매도잔량1, 매수잔량1, 매수잔량2, 매수잔량3,
                매수잔량4, 매수잔량5, 매도수5호가잔량합, 관심종목, 이동평균60_, 이동평균300_, 이동평균600_, 이동평균1200_, 최고현재가_,
                최저현재가_, 체결강도평균_, 최고체결강도_, 최저체결강도_, 최고초당매수수량_, 최고초당매도수량_, 누적초당매수수량_,
                누적초당매도수량_, 초당거래대금평균_, 등락율각도_, 당일거래대금각도_, BBU, BBM, BBL, MACD, MACDS, MACDH, APO, KAMA,
                RSI, HT_SINE, HT_LSINE, HT_PHASE, HT_QUDRA, OBV
            ]
        else:
            new_data_tick = [
                체결시간, 현재가, 시가, 고가, 저가, 등락율, 당일거래대금, 체결강도, 초당매수수량, 초당매도수량, 초당거래대금,
                고저평균대비등락율, 매도총잔량, 매수총잔량, 매도호가5, 매도호가4, 매도호가3, 매도호가2, 매도호가1, 매수호가1, 매수호가2,
                매수호가3, 매수호가4, 매수호가5, 매도잔량5, 매도잔량4, 매도잔량3, 매도잔량2, 매도잔량1, 매수잔량1, 매수잔량2, 매수잔량3,
                매수잔량4, 매수잔량5, 매도수5호가잔량합, 관심종목, 이동평균60_, 이동평균300_, 이동평균600_, 이동평균1200_, 최고현재가_,
                최저현재가_, 체결강도평균_, 최고체결강도_, 최저체결강도_, 최고초당매수수량_, 최고초당매도수량_, 누적초당매수수량_,
                누적초당매도수량_, 초당거래대금평균_, 등락율각도_, 당일거래대금각도_
            ]

        if 종목코드 not in self.dict_tik_ar.keys():
            self.dict_tik_ar[종목코드] = np.array([new_data_tick])
        else:
            self.dict_tik_ar[종목코드] = np.r_[self.dict_tik_ar[종목코드], np.array([new_data_tick])]
            if len(self.dict_tik_ar[종목코드]) > 1800:
                self.dict_tik_ar[종목코드] = np.delete(self.dict_tik_ar[종목코드], 0, 0)

        데이터길이 = len(self.dict_tik_ar[종목코드])
        self.indexn = 데이터길이 - 1

        if 체결강도평균_ != 0:
            if 종목코드 in self.df_jg.index:
                if 종목코드 not in self.dict_buy_tik.keys():
                    self.dict_buy_tik[종목코드] = len(self.dict_tik_ar[종목코드]) - 1
                매수틱번호 = self.dict_buy_tik[종목코드]
                매입가 = self.df_jg['매입가'][종목코드]
                보유수량 = self.df_jg['보유수량'][종목코드]
                매입금액 = self.df_jg['매입금액'][종목코드]
                분할매수횟수 = int(self.df_jg['분할매수횟수'][종목코드])
                분할매도횟수 = int(self.df_jg['분할매도횟수'][종목코드])
                _, 수익금, 수익률 = GetUpbitPgSgSp(매입금액, 보유수량 * 현재가)
                매수시간 = strp_time('%Y%m%d%H%M%S', self.df_jg['매수시간'][종목코드])
                보유시간 = (now_utc() - 매수시간).total_seconds()
                if 종목코드 not in self.dict_hilo.keys():
                    self.dict_hilo[종목코드] = [수익률, 수익률]
                else:
                    if 수익률 > self.dict_hilo[종목코드][0]:
                        self.dict_hilo[종목코드][0] = 수익률
                    elif 수익률 < self.dict_hilo[종목코드][1]:
                        self.dict_hilo[종목코드][1] = 수익률
                최고수익률, 최저수익률 = self.dict_hilo[종목코드]
            else:
                매수틱번호, 수익금, 수익률, 매입가, 보유수량, 분할매수횟수, 분할매도횟수, 매수시간, 보유시간, 최고수익률, 최저수익률 = 0, 0, 0, 0, 0, 0, 0, now_utc(), 0, 0, 0
            self.indexb = 매수틱번호

            BBT = not self.dict_set['코인매수금지시간'] or not (self.dict_set['코인매수금지시작시간'] < 시분초 < self.dict_set['코인매수금지종료시간'])
            BLK = not self.dict_set['코인매수금지블랙리스트'] or 종목코드 not in self.dict_set['코인블랙리스트']
            C20 = not self.dict_set['코인매수금지200원이하'] or 현재가 > 200
            NIB = 종목코드 not in self.list_buy
            NIS = 종목코드 not in self.list_sell

            A = 관심종목 and NIB and 매입가 == 0
            B = self.dict_set['코인매수분할시그널']
            C = NIB and 매입가 != 0 and 분할매수횟수 < self.dict_set['코인매수분할횟수']
            D = NIB and self.dict_set['코인매도취소매수시그널'] and not NIS

            if BBT and BLK and C20 and (A or (B and C) or C or D):
                매수수량 = 0

                if A or (B and C) or C:
                    oc_ratio = dict_order_ratio[self.dict_set['코인매수분할방법']][self.dict_set['코인매수분할횟수']][분할매수횟수]
                    매수수량 = round(self.int_tujagm / (현재가 if 매입가 == 0 else 매입가) * oc_ratio / 100, 8)

                if A or (B and C) or D:
                    매수 = True
                    if 시분초 < self.dict_set['코인장초전략종료시간']:
                        if self.buystrategy1 is not None:
                            try:
                                exec(self.buystrategy1)
                            except:
                                print_exc()
                                self.windowQ.put((ui_num['C단순텍스트'], '시스템 명령 오류 알림 - BuyStrategy1'))
                    elif self.dict_set['코인장초전략종료시간'] <= 시분초 < self.dict_set['코인장중전략종료시간']:
                        if self.buystrategy2 is not None:
                            if not self.stg_change:
                                self.vars = self.vars2
                                self.stg_change = True
                            try:
                                exec(self.buystrategy2)
                            except:
                                print_exc()
                                self.windowQ.put((ui_num['C단순텍스트'], '시스템 명령 오류 알림 - BuyStrategy2'))
                elif C:
                    매수 = False
                    분할매수기준수익률 = round((현재가 / self.dict_buyinfo[종목코드][9] - 1) * 100, 2) if self.dict_set['코인매수분할고정수익률'] else 수익률
                    if self.dict_set['코인매수분할하방'] and 분할매수기준수익률 < -self.dict_set['코인매수분할하방수익률']:
                        매수 = True
                    elif self.dict_set['코인매수분할상방'] and 분할매수기준수익률 > self.dict_set['코인매수분할상방수익률']:
                        매수 = True

                    if 매수:
                        self.Buy(종목코드, 현재가, 매도호가1, 매수호가1, 매수수량, 데이터길이)

            SBT = not self.dict_set['코인매도금지시간'] or not (self.dict_set['코인매도금지시작시간'] < 시분초 < self.dict_set['코인매도금지종료시간'])
            SCC = self.dict_set['코인매수분할횟수'] == 1 or not self.dict_set['코인매도금지매수횟수'] or 분할매수횟수 > self.dict_set['코인매도금지매수횟수값']
            NIB = 종목코드 not in self.list_buy

            A = NIB and NIS and SCC and 매입가 != 0 and self.dict_set['코인매도분할횟수'] == 1
            B = self.dict_set['코인매도분할시그널']
            C = NIB and NIS and SCC and 매입가 != 0 and 분할매도횟수 < self.dict_set['코인매도분할횟수']
            D = NIS and self.dict_set['코인매수취소매도시그널'] and not NIB
            E = NIB and NIS and 매입가 != 0 and self.dict_set['코인매도손절수익률청산'] and 수익률 < -self.dict_set['코인매도손절수익률']
            F = NIB and NIS and 매입가 != 0 and self.dict_set['코인매도손절수익금청산'] and 수익금 < -self.dict_set['코인매도손절수익금']

            if SBT and (A or (B and C) or C or D or E or F):
                매도 = False
                매도수량 = 0
                강제청산 = E or F

                if A or E or F:
                    매도수량 = 보유수량
                elif (B and C) or C:
                    oc_ratio = dict_order_ratio[self.dict_set['코인매도분할방법']][self.dict_set['코인매도분할횟수']][분할매도횟수]
                    매도수량 = round(self.int_tujagm / 매입가 * oc_ratio / 100, 8)
                    if 매도수량 > 보유수량 or 분할매도횟수 + 1 == self.dict_set['코인매도분할횟수']: 매도수량 = 보유수량

                if A or (B and C) or D:
                    if 시분초 < self.dict_set['코인장초전략종료시간']:
                        if self.sellstrategy1 is not None:
                            try:
                                exec(self.sellstrategy1)
                            except:
                                print_exc()
                                self.windowQ.put((ui_num['C단순텍스트'], '시스템 명령 오류 알림 - SellStrategy1'))
                    elif self.dict_set['코인장초전략종료시간'] <= 시분초 < self.dict_set['코인장중전략종료시간']:
                        if self.sellstrategy2 is not None:
                            try:
                                exec(self.sellstrategy2)
                            except:
                                print_exc()
                                self.windowQ.put((ui_num['C단순텍스트'], '시스템 명령 오류 알림 - SellStrategy2'))
                elif C or E or F:
                    if 강제청산:
                        매도 = True
                    elif C:
                        if self.dict_set['코인매도분할하방'] and 수익률 < -self.dict_set['코인매도분할하방수익률'] * (분할매도횟수 + 1):  매도 = True
                        elif self.dict_set['코인매도분할상방'] and 수익률 > self.dict_set['코인매도분할상방수익률'] * (분할매도횟수 + 1): 매도 = True

                    if 매도:
                        self.Sell(종목코드, 현재가, 매도호가1, 매수호가1, 매도수량, 강제청산)

        if 종목코드 in self.tuple_gsjm:
            self.df_gj.loc[종목코드] = 종목코드, 등락율, 고저평균대비등락율, 초당거래대금, 초당거래대금평균_, 당일거래대금, 체결강도, 체결강도평균_, 최고체결강도_

        if len(self.dict_tik_ar[종목코드]) >= 평균값계산틱수 and self.chart_code == 종목코드:
            self.windowQ.put((ui_num['실시간차트'], 종목코드, self.dict_tik_ar[종목코드]))

        if self.dict_set['코인틱데이터저장'] and 종목코드 in self.tuple_gsjm:
            if 종목코드 not in self.dict_tik_ar2.keys():
                self.dict_tik_ar2[종목코드] = np.array([new_data_tick[:36]])
            else:
                self.dict_tik_ar2[종목코드] = np.r_[self.dict_tik_ar2[종목코드], np.array([new_data_tick[:36]])]

        if 틱수신시간 != 0:
            if self.dict_tik_ar2:
                data = ('코인디비', self.dict_tik_ar2)
                self.queryQ.put(data)
                self.dict_tik_ar2 = {}

            gap = (now() - 틱수신시간).total_seconds()
            self.windowQ.put((ui_num['C단순텍스트'], f'전략스 연산 시간 알림 - 수신시간과 연산시간의 차이는 [{gap:.6f}]초입니다.'))

    def Buy(self, 종목코드, 현재가, 매도호가1, 매수호가1, 매수수량, 데이터길이):
        if self.dict_set['코인장초패턴인식'] and not self.stg_change and self.pattern_buy1 is not None:
            pattern = self.GetPattern(종목코드, '매수')
            if pattern not in self.pattern_buy1:
                return
        elif self.dict_set['코인장중패턴인식'] and self.stg_change and self.pattern_buy2 is not None:
            pattern = self.GetPattern(종목코드, '매수')
            if pattern not in self.pattern_buy2:
                return

        if '지정가' in self.dict_set['코인매수주문구분']:
            기준가격 = 현재가
            if self.dict_set['코인매수지정가기준가격'] == '매도1호가': 기준가격 = 매도호가1
            if self.dict_set['코인매수지정가기준가격'] == '매수1호가': 기준가격 = 매수호가1
            self.list_buy.append(종목코드)
            self.dict_sgn_tik[종목코드] = 데이터길이 - 1
            self.ctraderQ.put(('매수', 종목코드, 기준가격, 매수수량, now(), False))
        else:
            매수금액 = 0
            미체결수량 = 매수수량
            for 매도호가, 매도잔량 in self.bhogainfo:
                if 미체결수량 - 매도잔량 <= 0:
                    매수금액 += 매도호가 * 미체결수량
                    미체결수량 -= 매도잔량
                    break
                else:
                    매수금액 += 매도호가 * 매도잔량
                    미체결수량 -= 매도잔량
            if 미체결수량 <= 0:
                예상체결가 = round(매수금액 / 매수수량, 4) if 매수수량 != 0 else 0
                self.list_buy.append(종목코드)
                self.dict_sgn_tik[종목코드] = 데이터길이 - 1
                self.ctraderQ.put(('매수', 종목코드, 예상체결가, 매수수량, now(), False))

    def Sell(self, 종목코드, 현재가, 매도호가1, 매수호가1, 매도수량, 강제청산):
        if self.dict_set['코인장초패턴인식'] and not self.stg_change and self.pattern_sell1 is not None:
            pattern = self.GetPattern(종목코드, '매도')
            if pattern not in self.pattern_sell1:
                return
        elif self.dict_set['코인장중패턴인식'] and self.stg_change and self.pattern_sell2 is not None:
            pattern = self.GetPattern(종목코드, '매도')
            if pattern not in self.pattern_sell2:
                return

        if '지정가' in self.dict_set['코인매도주문구분'] and not 강제청산:
            기준가격 = 현재가
            if self.dict_set['코인매도지정가기준가격'] == '매도1호가': 기준가격 = 매도호가1
            if self.dict_set['코인매도지정가기준가격'] == '매수1호가': 기준가격 = 매수호가1
            self.list_sell.append(종목코드)
            self.ctraderQ.put(('매도', 종목코드, 기준가격, 매도수량, now(), False))
        else:
            매도금액 = 0
            미체결수량 = 매도수량
            for 매수호가, 매수잔량 in self.shogainfo:
                if 미체결수량 - 매수잔량 <= 0:
                    매도금액 += 매수호가 * 미체결수량
                    미체결수량 -= 매수잔량
                    break
                else:
                    매도금액 += 매수호가 * 매수잔량
                    미체결수량 -= 매수잔량
            if 미체결수량 <= 0:
                예상체결가 = round(매도금액 / 매도수량, 4) if 매도수량 != 0 else 0
                self.list_sell.append(종목코드)
                self.ctraderQ.put(('매도', 종목코드, 예상체결가, 매도수량, now(), True if 강제청산 else False))

    def PutGsjmAndDeleteHilo(self):
        self.df_gj.sort_values(by=['d_money'], ascending=False, inplace=True)
        self.windowQ.put((ui_num['C관심종목'], self.df_gj))
        for code in list(self.dict_hilo.keys()):
            if code not in self.df_jg.index:
                del self.dict_hilo[code]

    def GetPattern(self, code, gubun):
        if not self.stg_change:
            arry_tick    = self.dict_tik_ar[code][self.indexn + 1 - self.dict_pattern1['인식구간']:self.indexn + 1, :]
            dict_pattern = self.dict_pattern_buy1 if gubun == '매수' else self.dict_pattern_sell1
        else:
            arry_tick    = self.dict_tik_ar[code][self.indexn + 1 - self.dict_pattern2['인식구간']:self.indexn + 1, :]
            dict_pattern = self.dict_pattern_buy2 if gubun == '매수' else self.dict_pattern_sell2

        pattern = None
        for factor, unit in dict_pattern.items():
            pattern_ = None
            if factor == '등락율':
                pattern_ = arry_tick[:, 5]
            elif factor == '당일거래대금':
                pattern_ = arry_tick[:, 6]
            elif factor == '체결강도':
                pattern_ = arry_tick[:, 7]
            elif factor == '초당매수금액':
                bids     = arry_tick[:, 8]
                price    = arry_tick[:, 1]
                pattern_ = bids * price
            elif factor == '초당매도금액':
                asks     = arry_tick[:, 9]
                price    = arry_tick[:, 1]
                pattern_ = asks * price
            elif factor == '순매수금액':
                bids     = arry_tick[:, 8]
                asks     = arry_tick[:, 9]
                price    = arry_tick[:, 1]
                pattern_ = (bids - asks) * price
            elif factor == '초당거래대금':
                pattern_ = arry_tick[:, 10]
            elif factor == '고저평균대비등락율':
                pattern_ = arry_tick[:, 11]
            elif factor == '매도1잔량금액':
                asks1    = arry_tick[:, 28]
                price    = arry_tick[:, 18]
                pattern_ = asks1 * price
            elif factor == '매수1잔량금액':
                bids1    = arry_tick[:, 29]
                price    = arry_tick[:, 19]
                pattern_ = bids1 * price
            elif factor == '매도총잔량금액':
                tasks    = arry_tick[:, 12]
                price    = arry_tick[:, 1]
                pattern_ = tasks * price
            elif factor == '매수총잔량금액':
                tbids    = arry_tick[:, 13]
                price    = arry_tick[:, 1]
                pattern_ = tbids * price
            elif factor == '매도수5호가총금액':
                t5ab     = arry_tick[:, 34]
                price    = arry_tick[:, 1]
                pattern_ = t5ab * price
            pattern_ = pattern_ * unit
            pattern_ = pattern_.astype(int)
            if pattern is None:
                pattern = pattern_
            else:
                pattern = np.r_[pattern, pattern_]
        return pattern.tolist()
