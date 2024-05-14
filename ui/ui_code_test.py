from traceback import print_exc
# noinspection PyUnresolvedReferences
from utility.static import now, now_utc, timedelta_sec


# noinspection PyUnusedLocal
class CodeTest:
    def __init__(self, testQ, stg, var=None, ga=False):
        self.testQ = testQ
        self.vars  = {0: []}

        error = False
        if var is None:
            self.vars = {i: 1 for i in range(200)}
        else:
            try:
                exec(compile(var, '<string>', 'exec'))
            except:
                print_exc()
                error = True

            for i, var in enumerate(list(self.vars.values())):
                if len(var) != 2:
                    print(f'self.vars[{i}]의 범위 설정 방법 오류')
                    error = True
                if not ga:
                    if len(var[0]) != 3:
                        print(f'self.vars[{i}]의 범위 설정 방법 오류')
                        error = True
                    if var[0][2] != 0 and (var[0][1] - var[0][0]) / var[0][2] + 1 > 20:
                        print(f'self.vars[{i}]의 범위 설정 갯수 20개 초과')
                        error = True
                    if (var[0][0] < var[0][1] and var[0][2] < 0) or (var[0][0] > var[0][1] and var[0][2] > 0):
                        print(f'self.vars[{i}]의 범위 간격 부호 오류')
                        error = True

        if not error:
            try:
                self.stg = compile(stg, '<string>', 'exec')
            except:
                print_exc()
                error = True

            if not error:
                if var is None:
                    self.Test()
                else:
                    self.testQ.put('전략테스트완료')

    def Buy(self, *args):
        pass

    def Sell(self, *args):
        pass

    def Test(self):
        def 현재가N(pre):
            return 1

        def 시가N(pre):
            return 1

        def 고가N(pre):
            return 1

        def 저가N(pre):
            return 1

        def 등락율N(pre):
            return 1

        def 당일거래대금N(pre):
            return 1

        def 체결강도N(pre):
            return 1

        def 거래대금증감N(pre):
            return 1

        def 전일비N(pre):
            return 1

        def 회전율N(pre):
            return 1

        def 전일동시간비N(pre):
            return 1

        def 시가총액N(pre):
            return 1

        def 라운드피겨위5호가이내N(pre):
            return 1

        def 초당매수수량N(pre):
            return 1

        def 초당매도수량N(pre):
            return 1

        def 초당거래대금N(pre):
            return 1

        def 고저평균대비등락율N(pre):
            return 1

        def 매도총잔량N(pre):
            return 1

        def 매수총잔량N(pre):
            return 1

        def 매도호가5N(pre):
            return 1

        def 매도호가4N(pre):
            return 1

        def 매도호가3N(pre):
            return 1

        def 매도호가2N(pre):
            return 1

        def 매도호가1N(pre):
            return 1

        def 매수호가1N(pre):
            return 1

        def 매수호가2N(pre):
            return 1

        def 매수호가3N(pre):
            return 1

        def 매수호가4N(pre):
            return 1

        def 매수호가5N(pre):
            return 1

        def 매도잔량5N(pre):
            return 1

        def 매도잔량4N(pre):
            return 1

        def 매도잔량3N(pre):
            return 1

        def 매도잔량2N(pre):
            return 1

        def 매도잔량1N(pre):
            return 1

        def 매수잔량1N(pre):
            return 1

        def 매수잔량2N(pre):
            return 1

        def 매수잔량3N(pre):
            return 1

        def 매수잔량4N(pre):
            return 1

        def 매수잔량5N(pre):
            return 1

        def 매도수5호가잔량합N(pre):
            return 1

        def 관심종목N(pre):
            return 1

        def 이동평균(tick, pre=0):
            return 1

        def 등락율각도(tick, pre=0):
            return 1

        def 당일거래대금각도(tick, pre=0):
            return 1

        def 전일비각도(tick, pre=0):
            return 1

        def 최고현재가(tick, pre=0):
            return 1

        def 최저현재가(tick, pre=0):
            return 1

        def 체결강도평균(tick, pre=0):
            return 1

        def 최고체결강도(tick, pre=0):
            return 1

        def 최저체결강도(tick, pre=0):
            return 1

        def 최고초당매수수량(tick, pre=0):
            return 1

        def 최고초당매도수량(tick, pre=0):
            return 1

        def 누적초당매수수량(tick, pre=0):
            return 1

        def 누적초당매도수량(tick, pre=0):
            return 1

        def 초당거래대금평균(tick, pre=0):
            return 1

        def BBU_N(pre):
            return 1

        def BBM_N(pre):
            return 1

        def BBL_N(pre):
            return 1

        def MACD_N(pre):
            return 1

        def MACDS_N(pre):
            return 1

        def MACDH_N(pre):
            return 1

        def APO_N(pre):
            return 1

        def KAMA_N(pre):
            return 1

        def RSI_N(pre):
            return 1

        def HT_SINE_N(pre):
            return 1

        def HT_LSINE_N(pre):
            return 1

        def HT_PHASE_N(pre):
            return 1

        def HT_QUDRA_N(pre):
            return 1

        def OBV_N(pre):
            return 1

        체결시간, 현재가, 시가, 고가, 저가, 등락율, 당일거래대금, 체결강도, 거래대금증감, 전일비, 회전율, 전일동시간비, 시가총액, \
            라운드피겨위5호가이내, 초당매수수량, 초당매도수량, VI해제시간, VI가격, VI호가단위, 초당거래대금, 고저평균대비등락율, 매도총잔량, 매수총잔량, \
            매도호가5, 매도호가4, 매도호가3, 매도호가2, 매도호가1, 매수호가1, 매수호가2, 매수호가3, 매수호가4, 매수호가5, \
            매도잔량5, 매도잔량4, 매도잔량3, 매도잔량2, 매도잔량1, 매수잔량1, 매수잔량2, 매수잔량3, 매수잔량4, 매수잔량5, \
            매도수5호가잔량합, 관심종목, 종목코드, 틱수신시간, 종목명 = [
                20220721090001, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
                now(), 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, '005930', now(), '삼성전자']

        BBU, BBM, BBL, MACD, MACDS, MACDH, APO, KAMA, RSI, HT_SINE, HT_LSINE,  HT_PHASE, HT_QUDRA, OBV = \
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        bhogainfo = ((매도호가1, 매도잔량1), (매도호가2, 매도잔량2), (매도호가3, 매도잔량3), (매도호가4, 매도잔량4), (매도호가5, 매도잔량5))
        shogainfo = ((매수호가1, 매수잔량1), (매수호가2, 매수잔량2), (매수호가3, 매수잔량3), (매수호가4, 매수잔량4), (매수호가5, 매수잔량5))

        시분초, VI아래5호가, 데이터길이, 호가단위, 포지션, 평균값계산틱수 = int(str(체결시간)[8:]), 1, 1800, 1, 'LONG', 30
        분봉시가, 분봉고가, 분봉저가, 분봉이평5, 분봉이평10, 분봉이평20, 분봉이평60, 분봉이평120, 분봉이평240, 분봉거래대금 = 1, 1, 1, 1., 1., 1., 1., 1., 1., 1
        일봉이평5, 일봉이평10, 일봉이평20, 일봉이평60, 일봉이평120, 일봉이평240 = 1., 1., 1., 1., 1., 1.
        수익률, 매입가, 보유수량, 매도수량, 분할매수횟수, 분할매도횟수, 매수시간, 보유시간, 최고수익률, 최저수익률 = 1, 1, 1, 1, 1, 0, now(), 0, 1, 0
        매수, 매도, BUY_LONG, SELL_LONG, SELL_SHORT, BUY_SHORT, 강제청산 = False, False, False, False, False, False, False

        try:
            exec(self.stg)
        except:
            print_exc()
        else:
            self.testQ.put('전략테스트완료')
