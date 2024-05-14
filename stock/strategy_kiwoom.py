import os
import sys
import math
import time
import sqlite3
import numpy as np
import pandas as pd
from talib import stream
from traceback import print_exc
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from ui.ui_pattern import get_pattern_setup
from utility.setting import DB_STRATEGY, DICT_SET, ui_num, columns_jg, columns_gj, DB_STOCK_TICK, PATTERN_PATH
# noinspection PyUnresolvedReferences
from utility.static import now, strf_time, strp_time, int_hms, timedelta_sec, GetUvilower5, GetKiwoomPgSgSp, GetHogaunit, pickle_read


# noinspection PyUnusedLocal
class StrategyKiwoom:
    def __init__(self, gubun, qlist):
        self.gubun    = gubun
        self.kwzservQ = qlist[0]
        self.straderQ = qlist[2]
        self.sstgQs   = qlist[3]
        self.sstgQ    = qlist[3][self.gubun]
        self.dict_set = DICT_SET

        if self.gubun == 0 and self.dict_set['전략연산프로파일링']:
            import cProfile
            self.pr = cProfile.Profile()
            self.pr.enable()

        self.buystrategy1  = None
        self.buystrategy2  = None
        self.sellstrategy1 = None
        self.sellstrategy2 = None

        self.vars          = {}
        self.vars2         = {}
        self.dict_tik_ar   = {}
        self.dict_sgn_tik  = {}
        self.dict_buy_tik  = {}

        self.UpdateStringategy()

        self.tuple_kosd = ()
        self.list_buy   = []
        self.list_sell  = []

        self.indexn     = 0
        self.indexb     = 0
        self.jgrv_count = 0
        self.int_tujagm = 0
        self.stg_change = False
        self.chart_code = None
        self.dict_stgn  = None
        self.day_start  = strp_time('%Y%m%d%H%M%S', strf_time('%Y%m%d') + '090000')
        self.df_jg      = pd.DataFrame(columns=columns_jg)
        self.df_gj      = pd.DataFrame(columns=columns_gj)

        self.bhogainfo = {}
        self.shogainfo = {}
        self.dict_hilo = {}

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

        self.Start()

    def UpdateStringategy(self):
        con  = sqlite3.connect(DB_STRATEGY)
        dfb  = pd.read_sql('SELECT * FROM stockbuy', con).set_index('index')
        dfs  = pd.read_sql('SELECT * FROM stocksell', con).set_index('index')
        dfob = pd.read_sql('SELECT * FROM stockoptibuy', con).set_index('index')
        dfos = pd.read_sql('SELECT * FROM stockoptisell', con).set_index('index')
        dfp  = pd.read_sql('SELECT * FROM stockpattern', con).set_index('index')
        con.close()

        if self.dict_set['주식장초매수전략'] == '':
            self.buystrategy1 = None
        elif self.dict_set['주식장초매수전략'] in dfb.index:
            self.buystrategy1 = compile(dfb['전략코드'][self.dict_set['주식장초매수전략']], '<string>', 'exec')
        elif self.dict_set['주식장초매수전략'] in dfob.index:
            self.buystrategy1 = compile(dfob['전략코드'][self.dict_set['주식장초매수전략']], '<string>', 'exec')
            self.vars = {i: var for i, var in enumerate(list(dfob.loc[self.dict_set['주식장초매수전략']])[1:]) if var != 9999.}

        if self.dict_set['주식장초매도전략'] == '':
            self.sellstrategy1 = None
        elif self.dict_set['주식장초매도전략'] in dfs.index:
            self.sellstrategy1 = compile(dfs['전략코드'][self.dict_set['주식장초매도전략']], '<string>', 'exec')
        elif self.dict_set['주식장초매도전략'] in dfos.index:
            self.sellstrategy1 = compile(dfos['전략코드'][self.dict_set['주식장초매도전략']], '<string>', 'exec')

        if self.dict_set['주식장중매수전략'] == '':
            self.buystrategy2 = None
        elif self.dict_set['주식장중매수전략'] in dfb.index:
            self.buystrategy2 = compile(dfb['전략코드'][self.dict_set['주식장중매수전략']], '<string>', 'exec')
        elif self.dict_set['주식장중매수전략'] in dfob.index:
            self.buystrategy2 = compile(dfob['전략코드'][self.dict_set['주식장중매수전략']], '<string>', 'exec')
            self.vars2 = {i: var for i, var in enumerate(list(dfob.loc[self.dict_set['주식장중매수전략']])[1:]) if var != 9999.}

        if self.dict_set['주식장중매도전략'] == '':
            self.sellstrategy2 = None
        elif self.dict_set['주식장중매도전략'] in dfs.index:
            self.sellstrategy2 = compile(dfs['전략코드'][self.dict_set['주식장중매도전략']], '<string>', 'exec')
        elif self.dict_set['주식장중매도전략'] in dfos.index:
            self.sellstrategy2 = compile(dfos['전략코드'][self.dict_set['주식장중매도전략']], '<string>', 'exec')

        if self.dict_set['주식장초패턴인식'] and self.dict_set['주식장초매수전략'] in dfp.index:
            self.dict_pattern1, self.dict_pattern_buy1, self.dict_pattern_sell1 = get_pattern_setup(dfp['패턴설정'][self.dict_set['주식장초매수전략']])
            file_name = f"{PATTERN_PATH}/pattern_stock_{self.dict_set['주식장초매수전략']}"
            if os.path.isfile(f'{file_name}_buy.pkl'):
                self.pattern_buy1  = pickle_read(f'{file_name}_buy')
            if os.path.isfile(f'{file_name}_sell.pkl'):
                self.pattern_sell1 = pickle_read(f'{file_name}_sell')

        if self.dict_set['주식장중패턴인식'] and self.dict_set['주식장중매수전략'] in dfp.index:
            self.dict_pattern2, self.dict_pattern_buy2, self.dict_pattern_sell2 = get_pattern_setup(dfp['패턴설정'][self.dict_set['주식장중매수전략']])
            file_name = f"{PATTERN_PATH}/pattern_stock_{self.dict_set['주식장중매수전략']}"
            if os.path.isfile(f'{file_name}_buy.pkl'):
                self.pattern_buy2  = pickle_read(f'{file_name}_buy')
            if os.path.isfile(f'{file_name}_sell.pkl'):
                self.pattern_sell2 = pickle_read(f'{file_name}_sell')

    def Start(self):
        if self.gubun == 7:
            self.kwzservQ.put(('window', (ui_num['S로그텍스트'], '시스템 명령 실행 알림 - 전략연산 시작')))

        while True:
            data = self.sstgQ.get()
            if type(data) == tuple:
                if len(data) != 2:
                    self.Strategy(data)
                elif len(data) == 2:
                    self.UpdateTuple(data)
                elif len(data) == 3:
                    self.UpdateTriple(data)
            elif type(data) == str:
                self.UpdateString(data)
                if data == '프로세스종료':
                    break

        if self.gubun == 7:
            self.kwzservQ.put(('window', (ui_num['S로그텍스트'], '시스템 명령 실행 알림 - 전략연산 종료')))
        time.sleep(1)

    def UpdateTuple(self, data):
        gubun, data = data
        if gubun == '관심목록':
            drop_index_list = list(set(list(self.df_gj.index)) - set(data))
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
            if int_hms() < self.dict_set['주식장초전략종료시간']:
                self.buystrategy1 = compile(data, '<string>', 'exec')
            else:
                self.buystrategy2 = compile(data, '<string>', 'exec')
        elif gubun == '매도전략':
            if int_hms() < self.dict_set['주식장초전략종료시간']:
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
        elif gubun == '코스닥목록':
            self.tuple_kosd = data
        elif gubun == '종목구분번호':
            self.dict_stgn = data
            self.LoadDayMinData()
        elif gubun == '틱데이터저장':
            self.SaveTickData(data)

    def LoadDayMinData(self):
        pass

    def UpdateTriple(self, data):
        pass

    def UpdateString(self, data):
        if data == '매수전략중지':
            self.buystrategy1 = None
            self.buystrategy2 = None
        elif data == '매도전략중지':
            self.sellstrategy1 = None
            self.sellstrategy2 = None
        elif data == '복기모드종료':
            self.dict_tik_ar = {}
        elif data == '프로파일링결과':
            if self.gubun == 0:
                self.pr.print_stats(sort='cumulative')

    def Strategy(self, data):
        체결시간, 현재가, 시가, 고가, 저가, 등락율, 당일거래대금, 체결강도, 거래대금증감, 전일비, 회전율, 전일동시간비, 시가총액, \
            라운드피겨위5호가이내, 초당매수수량, 초당매도수량, VI해제시간, VI가격, VI호가단위, 초당거래대금, 고저평균대비등락율, 매도총잔량, 매수총잔량, \
            매도호가5, 매도호가4, 매도호가3, 매도호가2, 매도호가1, 매수호가1, 매수호가2, 매수호가3, 매수호가4, 매수호가5, \
            매도잔량5, 매도잔량4, 매도잔량3, 매도잔량2, 매도잔량1, 매수잔량1, 매수잔량2, 매수잔량3, 매수잔량4, 매수잔량5, \
            매도수5호가잔량합, 관심종목, 종목코드, 종목명, 틱수신시간 = data

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

        def 거래대금증감N(pre):
            return Parameter_Previous(8, pre)

        def 전일비N(pre):
            return Parameter_Previous(9, pre)

        def 회전율N(pre):
            return Parameter_Previous(10, pre)

        def 전일동시간비N(pre):
            return Parameter_Previous(11, pre)

        def 시가총액N(pre):
            return Parameter_Previous(12, pre)

        def 라운드피겨위5호가이내N(pre):
            return Parameter_Previous(13, pre)

        def 초당매수수량N(pre):
            return Parameter_Previous(14, pre)

        def 초당매도수량N(pre):
            return Parameter_Previous(15, pre)

        def 초당거래대금N(pre):
            return Parameter_Previous(19, pre)

        def 고저평균대비등락율N(pre):
            return Parameter_Previous(20, pre)

        def 매도총잔량N(pre):
            return Parameter_Previous(21, pre)

        def 매수총잔량N(pre):
            return Parameter_Previous(22, pre)

        def 매도호가5N(pre):
            return Parameter_Previous(23, pre)

        def 매도호가4N(pre):
            return Parameter_Previous(24, pre)

        def 매도호가3N(pre):
            return Parameter_Previous(25, pre)

        def 매도호가2N(pre):
            return Parameter_Previous(26, pre)

        def 매도호가1N(pre):
            return Parameter_Previous(27, pre)

        def 매수호가1N(pre):
            return Parameter_Previous(28, pre)

        def 매수호가2N(pre):
            return Parameter_Previous(29, pre)

        def 매수호가3N(pre):
            return Parameter_Previous(30, pre)

        def 매수호가4N(pre):
            return Parameter_Previous(31, pre)

        def 매수호가5N(pre):
            return Parameter_Previous(32, pre)

        def 매도잔량5N(pre):
            return Parameter_Previous(33, pre)

        def 매도잔량4N(pre):
            return Parameter_Previous(34, pre)

        def 매도잔량3N(pre):
            return Parameter_Previous(35, pre)

        def 매도잔량2N(pre):
            return Parameter_Previous(36, pre)

        def 매도잔량1N(pre):
            return Parameter_Previous(37, pre)

        def 매수잔량1N(pre):
            return Parameter_Previous(38, pre)

        def 매수잔량2N(pre):
            return Parameter_Previous(39, pre)

        def 매수잔량3N(pre):
            return Parameter_Previous(40, pre)

        def 매수잔량4N(pre):
            return Parameter_Previous(41, pre)

        def 매수잔량5N(pre):
            return Parameter_Previous(42, pre)

        def 매도수5호가잔량합N(pre):
            return Parameter_Previous(43, pre)

        def 관심종목N(pre):
            return Parameter_Previous(44, pre)

        def 이동평균(tick, pre=0):
            if tick == 60:
                return Parameter_Previous(45, pre)
            elif tick == 300:
                return Parameter_Previous(46, pre)
            elif tick == 600:
                return Parameter_Previous(47, pre)
            elif tick == 1200:
                return Parameter_Previous(48, pre)
            else:
                sindex = (self.indexn + 1 - pre - tick) if pre != -1  else self.indexb + 1 - tick
                eindex = (self.indexn + 1 - pre) if pre != -1  else self.indexb + 1
                return round(self.dict_tik_ar[종목코드][sindex:eindex, 1].mean(), 3)

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
            return Parameter_Area(49, 1, tick, pre, 'max')

        def 최저현재가(tick, pre=0):
            return Parameter_Area(50, 1, tick, pre, 'min')

        def 체결강도평균(tick, pre=0):
            return Parameter_Area(51, 7, tick, pre, 'mean')

        def 최고체결강도(tick, pre=0):
            return Parameter_Area(52, 7, tick, pre, 'max')

        def 최저체결강도(tick, pre=0):
            return Parameter_Area(53, 7, tick, pre, 'min')

        def 최고초당매수수량(tick, pre=0):
            return Parameter_Area(54, 14, tick, pre, 'max')

        def 최고초당매도수량(tick, pre=0):
            return Parameter_Area(55, 15, tick, pre, 'max')

        def 누적초당매수수량(tick, pre=0):
            return Parameter_Area(56, 14, tick, pre, 'sum')

        def 누적초당매도수량(tick, pre=0):
            return Parameter_Area(57, 15, tick, pre, 'sum')

        def 초당거래대금평균(tick, pre=0):
            return Parameter_Area(58, 19, tick, pre, 'mean')

        def Parameter_Dgree(aindex, vindex, tick, pre, cf):
            if tick == 평균값계산틱수:
                return Parameter_Previous(aindex, pre)
            else:
                sindex = (self.indexn + 1 - pre - tick) if pre != -1  else self.indexb + 1 - tick
                eindex = (self.indexn + 1 - pre) if pre != -1  else self.indexb + 1
                dmp_gap = self.dict_tik_ar[종목코드][eindex, vindex] - self.dict_tik_ar[종목코드][sindex, vindex]
                return round(math.atan2(dmp_gap * cf, tick) / (2 * math.pi) * 360, 2)

        def 등락율각도(tick, pre=0):
            return Parameter_Dgree(59, 5, tick, pre, 5)

        def 당일거래대금각도(tick, pre=0):
            return Parameter_Dgree(60, 6, tick, pre, 0.01)

        def 전일비각도(tick, pre=0):
            return Parameter_Dgree(61, 9, tick, pre, 1)

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

        시분초 = int(str(체결시간)[8:])
        호가단위 = GetHogaunit(종목코드 in self.tuple_kosd, 현재가, 체결시간)
        VI아래5호가 = GetUvilower5(VI가격, VI호가단위, 체결시간)
        VI해제시간_ = int(strf_time('%Y%m%d%H%M%S', VI해제시간))
        평균값계산틱수 = self.dict_set['주식장초평균값계산틱수'] if 시분초 < self.dict_set['주식장초전략종료시간'] else self.dict_set['주식장중평균값계산틱수']
        이동평균60_, 이동평균300_, 이동평균600_, 이동평균1200_, 최고현재가_, 최저현재가_ = 0., 0., 0., 0., 0, 0
        체결강도평균_, 최고체결강도_, 최저체결강도_, 최고초당매수수량_, 최고초당매도수량_ = 0., 0., 0., 0, 0
        누적초당매수수량_, 누적초당매도수량_, 초당거래대금평균_, 등락율각도_, 당일거래대금각도_, 전일비각도_ = 0, 0, 0., 0., 0., 0.
        BBU, BBM, BBL, MACD, MACDS, MACDH, APO, KAMA, RSI, HT_SINE, HT_LSINE,  HT_PHASE, HT_QUDRA, OBV = \
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        bhogainfo = ((매도호가1, 매도잔량1), (매도호가2, 매도잔량2), (매도호가3, 매도잔량3), (매도호가4, 매도잔량4), (매도호가5, 매도잔량5))
        shogainfo = ((매수호가1, 매수잔량1), (매수호가2, 매수잔량2), (매수호가3, 매수잔량3), (매수호가4, 매수잔량4), (매수호가5, 매수잔량5))
        self.bhogainfo = bhogainfo[:self.dict_set['주식매수시장가잔량범위']]
        self.shogainfo = shogainfo[:self.dict_set['주식매도시장가잔량범위']]

        if 종목코드 in self.dict_tik_ar.keys():
            len_array = len(self.dict_tik_ar[종목코드])
            if len_array >=   59: 이동평균60_   = round((self.dict_tik_ar[종목코드][  -59:, 1].sum() + 현재가) /   60, 3)
            if len_array >=  299: 이동평균300_  = round((self.dict_tik_ar[종목코드][ -299:, 1].sum() + 현재가) /  300, 3)
            if len_array >=  599: 이동평균600_  = round((self.dict_tik_ar[종목코드][ -599:, 1].sum() + 현재가) /  600, 3)
            if len_array >= 1199: 이동평균1200_ = round((self.dict_tik_ar[종목코드][-1199:, 1].sum() + 현재가) / 1200, 3)
            if len_array >= 평균값계산틱수 - 1:
                최고현재가_      = max(self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1):, 1].max(), 현재가)
                최저현재가_      = min(self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1):, 1].min(), 현재가)
                체결강도평균_    = round((self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1):, 7].sum() + 체결강도) / 평균값계산틱수, 3)
                최고체결강도_    = max(self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1):, 7].max(), 체결강도)
                최저체결강도_    = min(self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1):, 7].min(), 체결강도)
                최고초당매수수량_ = max(self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1):, 14].max(), 초당매수수량)
                최고초당매도수량_ = min(self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1):, 15].min(), 초당매도수량)
                누적초당매수수량_ =     self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1):, 14].sum() + 초당매수수량
                누적초당매도수량_ =     self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1):, 15].sum() + 초당매도수량
                초당거래대금평균_ = int((self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1):, 19].sum() + 초당거래대금) / 평균값계산틱수)
                등락율각도_      = round(math.atan2((등락율 - self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1), 5]) * 5, 평균값계산틱수) / (2 * math.pi) * 360, 2)
                당일거래대금각도_ = round(math.atan2((당일거래대금 - self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1), 6]) / 100, 평균값계산틱수) / (2 * math.pi) * 360, 2)
                전일비각도_      = round(math.atan2(전일비 - self.dict_tik_ar[종목코드][-(평균값계산틱수 - 1), 9], 평균값계산틱수) / (2 * math.pi) * 360, 2)

            """
            체결시간, 현재가, 시가, 고가, 저가, 등락율, 당일거래대금, 체결강도, 거래대금증감, 전일비, 회전율, 전일동시간비, 시가총액, 라운드피겨위5호가이내,
               0      1     2    3    4     5         6         7         8        9      10       11        12           13
            초당매수수량, 초당매도수량, VI해제시간, VI가격, VI호가단위, 초당거래대금, 고저평균대비등락율, 매도총잔량, 매수총잔량,
                14         15          16      17       18         19            20            21        22
            매도호가5, 매도호가4, 매도호가3, 매도호가2, 매도호가1, 매수호가1, 매수호가2, 매수호가3, 매수호가4, 매수호가5,
               23       24       25        26       27        28       29        30       31        32
            매도잔량5, 매도잔량4, 매도잔량3, 매도잔량2, 매도잔량1, 매수잔량1, 매수잔량2, 매수잔량3, 매수잔량4, 매수잔량5, 매도수5호가잔량합, 관심종목
               33       34       35        36       37        38       39        40       41       42          43           44
            이동평균60_, 이동평균300_, 이동평균600_, 이동평균1200_, 최고현재가_, 최저현재가_, 체결강도평균_, 최고체결강도_, 최저체결강도,
                45         46          47           48           49         50         51           52           53
            최고초당매수수량_, 최고초당매도수량_, 누적초당매수수량_, 누적초당매도수량_, 초당거래대금평균_, 등락율각도_, 당일거래대금각도_, 전일비각도_,
                  54            55               56              57              58             59         60            61
            BBU, BBM, BBL, MACD, MACDS, MACDH, APO, KAMA, RSI, HT_SINE, HT_LSINE, HT_PHASE, HT_QUDRA, OBV
            62    63  64    65    66     67     68   69    70    71        72       73         74      75
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
                체결시간, 현재가, 시가, 고가, 저가, 등락율, 당일거래대금, 체결강도, 거래대금증감, 전일비, 회전율, 전일동시간비, 시가총액,
                라운드피겨위5호가이내, 초당매수수량, 초당매도수량, VI해제시간_, VI가격, VI호가단위, 초당거래대금, 고저평균대비등락율,
                매도총잔량, 매수총잔량, 매도호가5, 매도호가4, 매도호가3, 매도호가2, 매도호가1, 매수호가1, 매수호가2, 매수호가3, 매수호가4,
                매수호가5, 매도잔량5, 매도잔량4, 매도잔량3, 매도잔량2, 매도잔량1, 매수잔량1, 매수잔량2, 매수잔량3, 매수잔량4, 매수잔량5,
                매도수5호가잔량합, 관심종목, 이동평균60_, 이동평균300_, 이동평균600_, 이동평균1200_, 최고현재가_, 최저현재가_,
                체결강도평균_, 최고체결강도_, 최저체결강도_, 최고초당매수수량_, 최고초당매도수량_, 누적초당매수수량_, 누적초당매도수량_,
                초당거래대금평균_, 등락율각도_, 당일거래대금각도_, 전일비각도_, BBU, BBM, BBL, MACD, MACDS, MACDH, APO, KAMA, RSI,
                HT_SINE, HT_LSINE, HT_PHASE, HT_QUDRA, OBV
            ]
        else:
            new_data_tick = [
                체결시간, 현재가, 시가, 고가, 저가, 등락율, 당일거래대금, 체결강도, 거래대금증감, 전일비, 회전율, 전일동시간비, 시가총액,
                라운드피겨위5호가이내, 초당매수수량, 초당매도수량, VI해제시간_, VI가격, VI호가단위, 초당거래대금, 고저평균대비등락율,
                매도총잔량, 매수총잔량, 매도호가5, 매도호가4, 매도호가3, 매도호가2, 매도호가1, 매수호가1, 매수호가2, 매수호가3, 매수호가4,
                매수호가5, 매도잔량5, 매도잔량4, 매도잔량3, 매도잔량2, 매도잔량1, 매수잔량1, 매수잔량2, 매수잔량3, 매수잔량4, 매수잔량5,
                매도수5호가잔량합, 관심종목, 이동평균60_, 이동평균300_, 이동평균600_, 이동평균1200_, 최고현재가_, 최저현재가_,
                체결강도평균_, 최고체결강도_, 최저체결강도_, 최고초당매수수량_, 최고초당매도수량_, 누적초당매수수량_, 누적초당매도수량_,
                초당거래대금평균_, 등락율각도_, 당일거래대금각도_, 전일비각도_
            ]

        if 종목코드 not in self.dict_tik_ar.keys():
            self.dict_tik_ar[종목코드] = np.array([new_data_tick])
        else:
            self.dict_tik_ar[종목코드] = np.r_[self.dict_tik_ar[종목코드], np.array([new_data_tick])]

        데이터길이 = len(self.dict_tik_ar[종목코드])
        self.indexn = 데이터길이 - 1

        if 데이터길이 > 1800 and not self.dict_set['주식틱데이터저장']:
            self.dict_tik_ar[종목코드] = np.delete(self.dict_tik_ar[종목코드], 0, 0)

        if 체결강도평균_ != 0 and not (매수잔량5 == 0 and 매도잔량5 == 0):
            if 종목코드 in self.df_jg.index:
                if 종목코드 not in self.dict_buy_tik.keys():
                    self.dict_buy_tik[종목코드] = len(self.dict_tik_ar[종목코드]) - 1
                매수틱번호 = self.dict_buy_tik[종목코드]
                매입가 = self.df_jg['매입가'][종목코드]
                보유수량 = self.df_jg['보유수량'][종목코드]
                매입금액 = self.df_jg['매입금액'][종목코드]
                분할매수횟수 = int(self.df_jg['분할매수횟수'][종목코드])
                분할매도횟수 = int(self.df_jg['분할매도횟수'][종목코드])
                _, 수익금, 수익률 = GetKiwoomPgSgSp(매입금액, 보유수량 * 현재가)
                매수시간 = strp_time('%Y%m%d%H%M%S', self.df_jg['매수시간'][종목코드])
                보유시간 = (now() - 매수시간).total_seconds()
                if 종목코드 not in self.dict_hilo.keys():
                    self.dict_hilo[종목코드] = [수익률, 수익률]
                else:
                    if 수익률 > self.dict_hilo[종목코드][0]:
                        self.dict_hilo[종목코드][0] = 수익률
                    elif 수익률 < self.dict_hilo[종목코드][1]:
                        self.dict_hilo[종목코드][1] = 수익률
                최고수익률, 최저수익률 = self.dict_hilo[종목코드]
            else:
                매수틱번호, 수익금, 수익률, 매입가, 보유수량, 분할매수횟수, 분할매도횟수, 매수시간, 보유시간, 최고수익률, 최저수익률 = 0, 0, 0, 0, 0, 0, 0, now(), 0, 0, 0
            self.indexb = 매수틱번호

            NIB = 종목코드 not in self.list_buy
            NIS = 종목코드 not in self.list_sell
            if 관심종목 and NIB and 매입가 == 0:
                매수수량 = int(self.int_tujagm / 현재가)
                매수 = True
                if 시분초 < self.dict_set['주식장초전략종료시간']:
                    if self.buystrategy1 is not None:
                        try:
                            exec(self.buystrategy1)
                        except:
                            print_exc()
                            self.kwzservQ.put(('window', (ui_num['S단순텍스트'], '시스템 명령 오류 알림 - BuyStrategy1')))
                elif self.dict_set['주식장초전략종료시간'] <= 시분초 < self.dict_set['주식장중전략종료시간']:
                    if self.buystrategy2 is not None:
                        if not self.stg_change:
                            self.vars = self.vars2
                            self.stg_change = True
                        try:
                            exec(self.buystrategy2)
                        except:
                            print_exc()
                            self.kwzservQ.put(('window', (ui_num['S단순텍스트'], '시스템 명령 오류 알림 - BuyStrategy2')))

            NIB = 종목코드 not in self.list_buy
            if NIB and NIS and 매입가 != 0:
                매도 = False
                강제청산 = False
                매도수량 = 보유수량
                if 시분초 < self.dict_set['주식장초전략종료시간']:
                    if self.sellstrategy1 is not None:
                        try:
                            exec(self.sellstrategy1)
                        except:
                            print_exc()
                            self.kwzservQ.put(('window', (ui_num['S단순텍스트'], '시스템 명령 오류 알림 - SellStrategy1')))
                elif self.dict_set['주식장초전략종료시간'] <= 시분초 < self.dict_set['주식장중전략종료시간']:
                    if self.sellstrategy2 is not None:
                        try:
                            exec(self.sellstrategy2)
                        except:
                            print_exc()
                            self.kwzservQ.put(('window', (ui_num['S단순텍스트'], '시스템 명령 오류 알림 - SellStrategy2')))

        if 관심종목:
            self.df_gj.loc[종목코드] = 종목명, 등락율, 고저평균대비등락율, 초당거래대금, 초당거래대금평균_, 당일거래대금, 체결강도, 체결강도평균_, 최고체결강도_

        if len(self.dict_tik_ar[종목코드]) >= 평균값계산틱수 and self.chart_code == 종목코드:
            self.kwzservQ.put(('window', (ui_num['실시간차트'], 종목명, self.dict_tik_ar[종목코드][-1800:, :])))

        if 틱수신시간 != 0:
            gap = (now() - 틱수신시간).total_seconds()
            self.kwzservQ.put(('window', (ui_num['S단순텍스트'], f'전략스 연산 시간 알림 - 수신시간과 연산시간의 차이는 [{gap:.6f}]초입니다.')))

    def Buy(self, 종목코드, 종목명, 매수수량, 현재가, 매도호가1, 매수호가1, 데이터길이):
        if '지정가' in self.dict_set['주식매수주문구분']:
            기준가격 = 현재가
            if self.dict_set['주식매수지정가기준가격'] == '매도1호가': 기준가격 = 매도호가1
            if self.dict_set['주식매수지정가기준가격'] == '매수1호가': 기준가격 = 매수호가1
            self.list_buy.append(종목코드)
            self.dict_sgn_tik[종목코드] = 데이터길이 - 1
            self.straderQ.put(('매수', 종목코드, 종목명, 기준가격, 매수수량, now(), False))
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
                예상체결가 = int(round(매수금액 / 매수수량)) if 매수수량 != 0 else 0
                self.list_buy.append(종목코드)
                self.dict_sgn_tik[종목코드] = 데이터길이 - 1
                self.straderQ.put(('매수', 종목코드, 종목명, 예상체결가, 매수수량, now(), False))

    def Sell(self, 종목코드, 종목명, 매도수량, 현재가, 매도호가1, 매수호가1, 강제청산):
        if '지정가' in self.dict_set['주식매도주문구분'] and not 강제청산:
            기준가격 = 현재가
            if self.dict_set['주식매도지정가기준가격'] == '매도1호가': 기준가격 = 매도호가1
            if self.dict_set['주식매도지정가기준가격'] == '매수1호가': 기준가격 = 매수호가1
            self.list_sell.append(종목코드)
            self.straderQ.put(('매도', 종목코드, 종목명, 기준가격, 매도수량, now(), False))
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
                예상체결가 = int(round(매도금액 / 매도수량)) if 매도수량 != 0 else 0
                self.list_sell.append(종목코드)
                self.straderQ.put(('매도', 종목코드, 종목명, 예상체결가, 매도수량, now(), True if 강제청산 else False))

    def PutGsjmAndDeleteHilo(self):
        if len(self.df_gj) > 0:
            self.kwzservQ.put(('window', (ui_num[f'S관심종목'], self.gubun, self.df_gj)))
        if len(self.dict_hilo) > 0:
            for code in list(self.dict_hilo.keys()):
                if code not in self.df_jg.index:
                    del self.dict_hilo[code]

    def SaveTickData(self, codes):
        for code in list(self.dict_tik_ar.keys()):
            if code not in codes:
                del self.dict_tik_ar[code]

        columns_ts = [
            'index', '현재가', '시가', '고가', '저가', '등락율', '당일거래대금', '체결강도', '거래대금증감', '전일비', '회전율',
            '전일동시간비', '시가총액', '라운드피겨위5호가이내', '초당매수수량', '초당매도수량', 'VI해제시간', 'VI가격', 'VI호가단위',
            '초당거래대금', '고저평균대비등락율', '매도총잔량', '매수총잔량', '매도호가5', '매도호가4', '매도호가3', '매도호가2',
            '매도호가1', '매수호가1', '매수호가2', '매수호가3', '매수호가4', '매수호가5', '매도잔량5', '매도잔량4', '매도잔량3',
            '매도잔량2', '매도잔량1', '매수잔량1', '매수잔량2', '매수잔량3', '매수잔량4', '매수잔량5', '매도수5호가잔량합', '관심종목'
        ]

        last = len(self.dict_tik_ar)
        con = sqlite3.connect(DB_STOCK_TICK)
        if last > 0:
            start = now()
            for i, code in enumerate(list(self.dict_tik_ar.keys())):
                df = pd.DataFrame(self.dict_tik_ar[code][:, :45], columns=columns_ts)
                df[['index']] = df[['index']].astype('int64')
                df.set_index('index', inplace=True)
                df.to_sql(code, con, if_exists='append', chunksize=1000)
                text = f'시스템 명령 실행 알림 - 전략연산 프로세스 틱데이터 저장 중 ... [{self.gubun + 1}]{i + 1}/{last}'
                self.kwzservQ.put(('window', (ui_num['S단순텍스트'], text)))
            save_time = (now() - start).total_seconds()
            text = f'시스템 명령 실행 알림 - 틱데이터 저장 쓰기소요시간은 [{save_time:.6f}]초입니다.'
            self.kwzservQ.put(('window', (ui_num['S단순텍스트'], text)))
        con.close()

        if self.gubun != 7:
            self.sstgQs[self.gubun + 1].put(('틱데이터저장', codes))
        else:
            for q in self.sstgQs:
                q.put('프로세스종료')
