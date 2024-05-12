import sqlite3
import operator
import numpy as np
from kiwoom import *
from multiprocessing import Queue
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, QTimer, pyqtSignal
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utility.setting import DICT_SET, DB_STOCK_TICK, ui_num
from utility.static import now, strf_time, strp_time, timedelta_sec, int_hms, roundfigure_upper5, qtest_qwait, GetVIPrice, GetSangHahanga


class Updater(QThread):
    signal = pyqtSignal(tuple)

    def __init__(self, sreceivQ):
        super().__init__()
        self.sreceivQ = sreceivQ

    def run(self):
        while True:
            data = self.sreceivQ.get()
            # noinspection PyUnresolvedReferences
            self.signal.emit(data)


class ReceiverKiwoom:
    def __init__(self, qlist):
        app = QApplication(sys.argv)

        self.kwzservQ = qlist[0]
        self.sreceivQ = qlist[1]
        self.straderQ = qlist[2]
        self.sstgQs   = qlist[3]
        self.dict_set = DICT_SET

        if self.dict_set['리시버프로파일링']:
            import cProfile
            self.pr = cProfile.Profile()
            self.pr.enable()

        self.dict_bool = {
            '리시버시작': False,
            '실시간조건검색시작': False,
            '실시간조건검색중단': False,
            '장중단타전략시작': False,
            '프로세스종료': False,
            '주식체결필드확인': False,
            '주식체결필드같음': False,
            '호가잔량필드확인': False,
            '호가잔량필드같음': False
        }
        self.dict_name = {}
        self.dict_code = {}
        self.dict_hgdt = {}
        self.dict_hgbs = {}
        self.dict_tick = {}
        self.dict_vipr = {}
        self.dict_sghg = {}
        self.dict_arry = {}
        self.dict_tm5m = {}
        self.dict_mtop = {}
        self.dict_sgbn = {}

        self.list_gsjm   = []
        self.tuple_janng = ()
        self.tuple_order = ()

        self.list_prmt  = None
        self.tuple_kosd = None
        self.list_code  = None
        self.list_cond  = None
        self.hoga_code  = None
        self.dt_mtct    = None

        self.operation  = 1
        self.str_tday   = strf_time('%Y%m%d')
        self.int_logt   = int(strf_time('%Y%m%d%H%M'))
        self.int_hgtime = int(strf_time('%Y%m%d%H%M%S'))
        self.int_jcct   = int(self.str_tday + '090000') if int_hms() < 90000 else int(strf_time('%Y%m%d%H%M%S'))

        curr_time = now()
        remaintime = (strp_time('%Y%m%d%H%M%S', self.str_tday + '090100') - curr_time).total_seconds()
        self.dict_time = {
            '휴무종료': timedelta_sec(remaintime) if remaintime > 0 else None,
            '거래대금순위기록': curr_time
        }

        self.recvservQ = Queue()

        self.kw = Kiwoom(self, 'Receiver')
        self.KiwoomLogin()

        self.updater = Updater(self.sreceivQ)
        # noinspection PyUnresolvedReferences
        self.updater.signal.connect(self.UpdateTuple)
        self.updater.start()

        self.qtimer1 = QTimer()
        self.qtimer1.setInterval(1 * 1000)
        # noinspection PyUnresolvedReferences
        self.qtimer1.timeout.connect(self.Scheduler)
        self.qtimer1.start()

        self.qtimer2 = QTimer()
        self.qtimer2.setInterval(10 * 1000)
        # noinspection PyUnresolvedReferences
        self.qtimer2.timeout.connect(self.MoneyTopSearch)

        app.exec_()

    def KiwoomLogin(self):
        self.kw.CommConnect()
        qtest_qwait(5)
        self.kw.GetConditionLoad()

        self.tuple_kosd = tuple(self.kw.GetCodeListByMarket('10'))
        list_code = self.kw.GetCodeListByMarket('0') + self.kw.GetCodeListByMarket('8') + list(self.tuple_kosd)
        self.dict_sgbn = {code: i % 8 for i, code in enumerate(list_code)}
        self.dict_name = {code: self.kw.GetMasterCodeName(code) for code in list_code}
        self.dict_code = {name: code for code, name in self.dict_name.items()}

        self.kwzservQ.put(('window', (ui_num['종목명데이터'], self.dict_name, self.dict_code, self.dict_sgbn, '더미')))
        self.straderQ.put(('종목구분번호', self.dict_sgbn))
        for q in self.sstgQs:
            q.put(('종목구분번호', self.dict_sgbn))
            q.put(('코스닥목록', self.tuple_kosd))

        df = pd.DataFrame(self.dict_name.values(), columns=['종목명'], index=list(self.dict_name.keys()))
        df['코스닥'] = [True if x in self.tuple_kosd else False for x in df.index]
        self.kwzservQ.put(('query', ('설정디비', df, 'codename', 'replace')))

        error = True
        while error:
            qtest_qwait(2)
            self.list_cond = self.kw.GetConditionNamelist()
            try:
                if self.list_cond[0][0] == 0 and self.list_cond[1][0] == 1:
                    self.kwzservQ.put(('window', (ui_num['S단순텍스트'], '시스템 명령 실행 알림 - 조건검색식 불러오기 완료')))
            except:
                print('조건검색식 불러오기 실패, 2초후 재시도합니다.')
            else:
                error = False
                self.kwzservQ.put(('window', (ui_num['S단순텍스트'], self.list_cond)))

        self.kwzservQ.put(('window', (ui_num['S단순텍스트'], '시스템 명령 실행 알림 - OpenAPI 로그인 완료')))
        text = '주식 리시버를 시작하였습니다.'
        if self.dict_set['주식알림소리']: self.kwzservQ.put(('sound', text))
        self.kwzservQ.put(('tele', text))

    def UpdateTuple(self, data):
        gubun, data = data
        if gubun == '잔고목록':
            self.tuple_janng = data
        elif gubun == '주문목록':
            self.tuple_order = data
        elif gubun == '호가종목코드':
            self.hoga_code = data
        elif gubun == '설정변경':
            self.dict_set = data
        elif gubun == '프로파일링결과':
            self.pr.print_stats(sort='cumulative')

    def Scheduler(self):
        curr_time = now()
        inthms = int_hms()
        if not self.dict_bool['리시버시작']:
            self.OperationRealreg()

        if self.operation == 1 and self.dict_time['휴무종료'] is not None and self.dict_time['휴무종료'] <= curr_time:
            if self.dict_set['휴무프로세스종료'] and not self.dict_bool['프로세스종료']:
                self.ReceiverProcKill()

        if self.operation in (2, 3):
            if not self.dict_bool['실시간조건검색시작'] and 85000 < inthms < self.dict_set['주식장초전략종료시간']:
                self.ConditionSearchStart()

            if not self.dict_bool['장중단타전략시작'] and not self.dict_bool['프로세스종료'] and self.dict_set['주식장초전략종료시간'] <= inthms:
                if self.dict_bool['실시간조건검색시작'] and not self.dict_bool['실시간조건검색중단']:
                    self.ConditionSearchStop()
                self.ReceiverProcKill() if self.dict_set['주식장초프로세스종료'] else self.StartJangjungStrategy()

            if self.dict_bool['장중단타전략시작'] and not self.dict_bool['프로세스종료'] and self.dict_set['주식장중전략종료시간'] <= inthms:
                if self.dict_set['주식장중프로세스종료']: self.ReceiverProcKill()

        if self.operation == 8 and not self.dict_bool['프로세스종료'] and 153500 <= inthms:
            self.ReceiverProcKill()

        if curr_time > self.dict_time['거래대금순위기록']:
            if len(self.list_gsjm) > 0:
                self.UpdateMoneyTop()
            self.dict_time['거래대금순위기록'] = timedelta_sec(1)

    def ReceiverProcKill(self):
        self.dict_bool['프로세스종료'] = True
        self.straderQ.put('프로세스종료')
        self.RemoveAllRealreg()
        QTimer.singleShot(180 * 1000, self.SysExit)
        if self.dict_set['주식알림소리']:
            self.kwzservQ.put(('sound', '키움증권 시스템을 3분 후 종료합니다.'))

    def RemoveAllRealreg(self):
        if self.dict_set['장중전략조건검색식사용']:
            self.kw.SendConditionStop([sn_cond, self.list_cond[2][1], self.list_cond[2][0]])
            self.kwzservQ.put(('window', (ui_num['S단순텍스트'], '시스템 명령 실행 알림 - 실시간조건검색 2번 중단 완료')))
        self.kw.SetRealRemove(['ALL', 'ALL'])
        if self.dict_set['주식알림소리']:
            self.kwzservQ.put(('sound', '조건검색 및 실시간데이터의 수신을 중단하였습니다.'))

    def OperationRealreg(self):
        self.dict_bool['리시버시작'] = True

        self.kw.SetRealReg([sn_oper, ' ', '215;20;214', 0])
        self.kwzservQ.put(('window', (ui_num['S단순텍스트'], '시스템 명령 실행 알림 - 장운영시간 등록 완료')))

        self.kw.SetRealReg([sn_oper, '001;101', '10;15;20', 1])
        self.kwzservQ.put(('window', (ui_num['S단순텍스트'], '시스템 명령 실행 알림 - 업종지수 등록 완료')))

        self.kw.Block_Request('opt10054', 시장구분='000', 장전구분='1', 종목코드='', 발동구분='1', 제외종목='000000000', 거래량구분='0', 거래대금구분='0', 발동방향='0', output='발동종목', next=0)
        self.kwzservQ.put(('window', (ui_num['S단순텍스트'], '시스템 명령 실행 알림 - VI발동해제 등록 완료')))

        self.list_code = self.kw.SendCondition([sn_cond, self.list_cond[1][1], self.list_cond[1][0], 0])

        if len(self.list_code) > 2400:
            print('조건검색식 설정이 잘못되었습니다.')
            print('감시종목수가 너무 많으니 조건검색식을 재설정하십시오.')

        k = 0
        for i in range(0, len(self.list_code), 100):
            rreg = [sn_gsjm + k, ';'.join(self.list_code[i:i + 100]), '10;12;14;30;228;41;61;71;81', 1]
            self.kw.SetRealReg(rreg)
            text = f"실시간 알림 등록 완료 - [{sn_gsjm + k}] 종목갯수 {len(rreg[1].split(';'))}"
            self.kwzservQ.put(('window', (ui_num['S단순텍스트'], text)))
            k += 1

        if k < 10:
            print('조건검색식 설정이 잘못되었습니다.')
            print('감시종목수가 너무 적으니 조건검색식을 재설정하십시오.')

        self.kwzservQ.put(('window', (ui_num['S단순텍스트'], '시스템 명령 실행 알림 - 실시간 등록 완료')))
        self.kwzservQ.put(('window', (ui_num['S단순텍스트'], '시스템 명령 실행 알림 - 리시버 시작')))

    def ConditionSearchStart(self):
        self.dict_bool['실시간조건검색시작'] = True

        codes = self.kw.SendCondition([sn_cond, self.list_cond[0][1], self.list_cond[0][0], 1])
        if len(codes) > 0:
            for code in codes:
                self.InsertGsjmlist(code)

        if len(codes) > 100:
            self.kwzservQ.put(('window', (ui_num['S단순텍스트'], '시스템 명령 오류 알림 - 조건검색식 0번이 잘못되었습니다. HTS에서 확인하십시오.')))
        self.kwzservQ.put(('window', (ui_num['S단순텍스트'], '시스템 명령 실행 알림 - 실시간조건검색 0번 등록 완료')))

    def ConditionSearchStop(self):
        self.dict_bool['실시간조건검색중단'] = True

        self.kw.SendConditionStop([sn_cond, self.list_cond[0][1], self.list_cond[0][0]])
        self.kwzservQ.put(('window', (ui_num['S단순텍스트'], '시스템 명령 실행 알림 - 실시간조건검색 0번 중단 완료')))

        if self.dict_set['장중전략조건검색식사용']:
            self.list_gsjm = []
            codes = self.kw.SendCondition([sn_cond, self.list_cond[2][1], self.list_cond[2][0], 1])
            if len(codes) > 0:
                for code in codes:
                    self.InsertGsjmlist(code)
            if len(codes) > 100:
                self.kwzservQ.put(('window', (ui_num['S단순텍스트'], '시스템 명령 오류 알림 - 조건검색식 2번이 잘못되었습니다. HTS에서 확인하십시오.')))
            self.kwzservQ.put(('window', (ui_num['S단순텍스트'], '시스템 명령 실행 알림 - 실시간조건검색 2번 등록 완료')))

    def StartJangjungStrategy(self):
        self.dict_bool['장중단타전략시작'] = True
        if not self.dict_set['장중전략조건검색식사용']:
            list_mtop = [x for x, y in sorted(self.dict_tm5m.items(), key=operator.itemgetter(1), reverse=True)[:self.dict_set['주식순위선정']]]

            insert_list = list(set(list_mtop) - set(self.list_gsjm))
            if len(insert_list) > 0:
                for code in insert_list:
                    self.InsertGsjmlist(code)

            delete_list = list(set(self.list_gsjm) - set(list_mtop))
            if len(delete_list) > 0:
                for code in delete_list:
                    self.DeleteGsjmlist(code)

            self.list_prmt = list_mtop
            self.qtimer2.start()
        self.kwzservQ.put(('window', (ui_num['S로그텍스트'], '시스템 명령 실행 알림 - 장중 단타 전략 시작')))
        if self.dict_set['주식알림소리']:
            self.kwzservQ.put(('sound', '키움증권 시스템 장중 전략을 시작합니다.'))

    def SysExit(self):
        self.dict_bool['프로세스종료'] = True
        if self.qtimer1.isActive():  self.qtimer1.stop()
        if self.qtimer2.isActive():  self.qtimer2.stop()
        if self.updater.isRunning(): self.updater.quit()
        if self.dict_set['주식틱데이터저장']:
            self.SaveTickData()
            qtest_qwait(10)
        else:
            for q in self.sstgQs:
                q.put('프로세스종료')

        self.kwzservQ.put(('window', (ui_num['S단순텍스트'], '시스템 명령 실행 알림 - 리시버 종료')))

    def SaveTickData(self):
        codes = []
        if len(self.dict_mtop) > 0:
            codes = list(set(';'.join(list(self.dict_mtop.values())[30:]).split(';')))
            con = sqlite3.connect(DB_STOCK_TICK)
            last_index = 0
            try:
                df = pd.read_sql(f'SELECT * FROM moneytop ORDER BY "index" DESC LIMIT 1', con)
                last_index = df['index'][0]
            except:
                pass
            df = {key: value for key, value in self.dict_mtop.items() if key > last_index}
            df = pd.DataFrame(df.values(), columns=['거래대금순위'], index=list(df.keys()))
            df.to_sql('moneytop', con, if_exists='append', chunksize=1000)
            con.close()
            self.kwzservQ.put(('window', (ui_num['S단순텍스트'], '시스템 명령 실행 알림 - 거래대금순위 저장 완료')))

        self.sstgQs[0].put(('틱데이터저장', codes))

    def UpdateMoneyTop(self):
        for q in self.sstgQs:
            q.put(('관심목록', tuple(self.list_gsjm)))

        list_gsjm = self.list_gsjm.copy()
        list_gsjm = ';'.join(list_gsjm)
        curr_strtime = str(self.int_jcct)
        curr_datetime = strp_time('%Y%m%d%H%M%S', curr_strtime)

        if self.dt_mtct is not None:
            gap_seconds = (curr_datetime - self.dt_mtct).total_seconds()
            while gap_seconds > 1:
                gap_seconds -= 1
                pre_time = strf_time('%Y%m%d%H%M%S', timedelta_sec(-gap_seconds, curr_datetime))
                self.dict_mtop[int(pre_time)] = list_gsjm

        if curr_datetime != self.dt_mtct:
            self.dict_mtop[int(curr_strtime)] = list_gsjm
            self.dt_mtct = curr_datetime

    def MoneyTopSearch(self):
        if len(self.dict_tm5m) > 0:
            list_mtop = [x for x, y in sorted(self.dict_tm5m.items(), key=operator.itemgetter(1), reverse=True)[:self.dict_set['주식순위선정']]]

            insert_list = list(set(list_mtop) - set(self.list_prmt))
            if len(insert_list) > 0:
                for code in insert_list:
                    self.InsertGsjmlist(code)

            delete_list = list(set(self.list_prmt) - set(list_mtop))
            if len(delete_list) > 0:
                for code in delete_list:
                    self.DeleteGsjmlist(code)

            self.list_prmt = list_mtop

    def InsertGsjmlist(self, code):
        if code not in self.list_gsjm:
            self.list_gsjm.append(code)
            if self.dict_set['주식매도취소관심진입']:
                self.straderQ.put(('관심진입', code))

    def DeleteGsjmlist(self, code):
        if code in self.list_gsjm:
            self.list_gsjm.remove(code)
            if self.dict_set['주식매수취소관심이탈']:
                self.straderQ.put(('관심이탈', code))

    # noinspection PyUnusedLocal
    def OnReceiveRealCondition(self, code, IorD, cname, cindex):
        if self.dict_bool['프로세스종료']:
            return

        if IorD == 'I':
            self.InsertGsjmlist(code)
        elif IorD == 'D':
            self.DeleteGsjmlist(code)

    def OnReceiveRealData(self, code, realtype, realdata):
        if self.dict_bool['프로세스종료']:
            return

        if realtype == '장시작시간':
            try:
                self.operation = int(self.kw.GetCommRealData(code, 215))
                current            = self.kw.GetCommRealData(code, 20)
                remain             = self.kw.GetCommRealData(code, 214)
            except:
                pass
            else:
                self.kwzservQ.put(('window', (ui_num['S단순텍스트'],
                                              f'장운영 시간 수신 알림 - {self.operation} {current[:2]}:{current[2:4]}:{current[4:]} '
                                              f'남은시간 {remain[:2]}:{remain[2:4]}:{remain[4:]}')))

        elif realtype == '업종지수':
            try:
                dt = int(self.str_tday + self.kw.GetCommRealData(code, 20))
                c  = round(abs(float(self.kw.GetCommRealData(code, 10))) / 100, 2)
            except:
                pass
            else:
                self.kwzservQ.put(('chart', ('코스피' if code == '001' else '코스닥', dt, c)))

        elif realtype == 'VI발동/해제':
            try:
                code  = self.kw.GetCommRealData(code, 9001).strip('A').strip('Q')
                gubun = self.kw.GetCommRealData(code, 9068)
                name  = self.dict_name[code]
            except Exception as e:
                self.kwzservQ.put(('window', (ui_num['S단순텍스트'], f'시스템 명령 오류 알림 - OnReceiveRealData VI발동/해제 {e}')))
            else:
                if gubun == '1' and code in self.list_code and \
                        (code not in self.dict_vipr.keys() or (self.dict_vipr[code][0] and now() > self.dict_vipr[code][1])):
                    self.UpdateViPrice(code, name)

        elif realtype == '주식체결':
            dt = self.kw.GetCommRealData(code, 20)
            if int(dt) < 85500:
                return

            try:
                if not self.dict_bool['주식체결필드확인']:
                    data = realdata.split('\t')
                    if data[0]                             == self.kw.GetCommRealData(code, 20) and \
                            abs(int(data[1]))      == abs(int(self.kw.GetCommRealData(code, 10))) and \
                            float(data[3])           == float(self.kw.GetCommRealData(code, 12)) and \
                            data[6]                        == self.kw.GetCommRealData(code, 15) and \
                            int(data[8])               == int(self.kw.GetCommRealData(code, 14)) and \
                            abs(int(data[9]))      == abs(int(self.kw.GetCommRealData(code, 16))) and \
                            abs(int(data[10]))     == abs(int(self.kw.GetCommRealData(code, 17))) and \
                            abs(int(data[11]))     == abs(int(self.kw.GetCommRealData(code, 18))) and \
                            float(data[18])          == float(self.kw.GetCommRealData(code, 228)) and \
                            int(data[14])              == int(self.kw.GetCommRealData(code, 29)) and \
                            abs(float(data[15])) == abs(float(self.kw.GetCommRealData(code, 30))) and \
                            float(data[16])          == float(self.kw.GetCommRealData(code, 31)) and \
                            float(data[25]) / 100    == float(self.kw.GetCommRealData(code, 851)) / 100 and \
                            int(data[19])              == int(self.kw.GetCommRealData(code, 311)) and \
                            int(data[4])               == int(self.kw.GetCommRealData(code, 27)) and \
                            int(data[5])               == int(self.kw.GetCommRealData(code, 28)):
                        self.dict_bool['주식체결필드같음'] = True
                        self.kwzservQ.put(('window', (ui_num['S로그텍스트'], '시스템 명령 실행 알림 - 주식체결 필드값 같음')))
                    else:
                        self.kwzservQ.put(('window', (ui_num['S로그텍스트'], '시스템 명령 오류 알림 - 주식체결 필드값이 다릅니다. 필드값 갱신요망!!')))
                    self.dict_bool['주식체결필드확인'] = True

                dt = int(self.str_tday + dt)
                if self.dict_bool['주식체결필드같음']:
                    data  = realdata.split('\t')
                    c     = abs(int(data[1]))
                    per     = float(data[3])
                    v             = data[6]
                    dm        = int(data[8])
                    o     = abs(int(data[9]))
                    h     = abs(int(data[10]))
                    low   = abs(int(data[11]))
                    ch      = float(data[18])
                    dmp       = int(data[14])
                    jvp = abs(float(data[15]))
                    vrp     = float(data[16])
                    jsvp    = float(data[25]) / 100
                    sgta      = int(data[19])
                    csp       = int(data[4])
                    cbp       = int(data[5])
                else:
                    c     = abs(int(self.kw.GetCommRealData(code, 10)))
                    per     = float(self.kw.GetCommRealData(code, 12))
                    v             = self.kw.GetCommRealData(code, 15)
                    dm        = int(self.kw.GetCommRealData(code, 14))
                    o     = abs(int(self.kw.GetCommRealData(code, 16)))
                    h     = abs(int(self.kw.GetCommRealData(code, 17)))
                    low   = abs(int(self.kw.GetCommRealData(code, 18)))
                    ch      = float(self.kw.GetCommRealData(code, 228))
                    dmp       = int(self.kw.GetCommRealData(code, 29))
                    jvp = abs(float(self.kw.GetCommRealData(code, 30)))
                    vrp     = float(self.kw.GetCommRealData(code, 31))
                    jsvp    = float(self.kw.GetCommRealData(code, 851)) / 100
                    sgta      = int(self.kw.GetCommRealData(code, 311))
                    csp       = int(self.kw.GetCommRealData(code, 27))
                    cbp       = int(self.kw.GetCommRealData(code, 28))
            except Exception as e:
                self.kwzservQ.put(('window', (ui_num['S단순텍스트'], f'시스템 명령 오류 알림 - OnReceiveRealData 주식체결 {e}')))
            else:
                self.UpdateTickData(code, dt, c, o, h, low, per, dm, v, ch, dmp, jvp, vrp, jsvp, sgta, csp, cbp)

        elif realtype == '주식호가잔량':
            dt = self.kw.GetCommRealData(code, 21)
            if int(dt) < 85500:
                return

            try:
                start = now()
                if not self.dict_bool['호가잔량필드확인']:
                    data = realdata.split('\t')
                    if int(data[61])               == int(self.kw.GetCommRealData(code, 121)) and \
                            int(data[63])          == int(self.kw.GetCommRealData(code, 125)) and \
                            abs(int(data[55])) == abs(int(self.kw.GetCommRealData(code, 50))) and \
                            abs(int(data[49])) == abs(int(self.kw.GetCommRealData(code, 49))) and \
                            abs(int(data[43])) == abs(int(self.kw.GetCommRealData(code, 48))) and \
                            abs(int(data[37])) == abs(int(self.kw.GetCommRealData(code, 47))) and \
                            abs(int(data[31])) == abs(int(self.kw.GetCommRealData(code, 46))) and \
                            abs(int(data[25])) == abs(int(self.kw.GetCommRealData(code, 45))) and \
                            abs(int(data[19])) == abs(int(self.kw.GetCommRealData(code, 44))) and \
                            abs(int(data[13])) == abs(int(self.kw.GetCommRealData(code, 43))) and \
                            abs(int(data[7]))  == abs(int(self.kw.GetCommRealData(code, 42))) and \
                            abs(int(data[1]))  == abs(int(self.kw.GetCommRealData(code, 41))) and \
                            abs(int(data[4]))  == abs(int(self.kw.GetCommRealData(code, 51))) and \
                            abs(int(data[10])) == abs(int(self.kw.GetCommRealData(code, 52))) and \
                            abs(int(data[16])) == abs(int(self.kw.GetCommRealData(code, 53))) and \
                            abs(int(data[22])) == abs(int(self.kw.GetCommRealData(code, 54))) and \
                            abs(int(data[28])) == abs(int(self.kw.GetCommRealData(code, 55))) and \
                            abs(int(data[34])) == abs(int(self.kw.GetCommRealData(code, 56))) and \
                            abs(int(data[40])) == abs(int(self.kw.GetCommRealData(code, 57))) and \
                            abs(int(data[46])) == abs(int(self.kw.GetCommRealData(code, 58))) and \
                            abs(int(data[52])) == abs(int(self.kw.GetCommRealData(code, 59))) and \
                            abs(int(data[58])) == abs(int(self.kw.GetCommRealData(code, 60))) and \
                            int(data[56])          == int(self.kw.GetCommRealData(code, 70)) and \
                            int(data[50])          == int(self.kw.GetCommRealData(code, 69)) and \
                            int(data[44])          == int(self.kw.GetCommRealData(code, 68)) and \
                            int(data[38])          == int(self.kw.GetCommRealData(code, 67)) and \
                            int(data[32])          == int(self.kw.GetCommRealData(code, 66)) and \
                            int(data[26])          == int(self.kw.GetCommRealData(code, 65)) and \
                            int(data[20])          == int(self.kw.GetCommRealData(code, 64)) and \
                            int(data[14])          == int(self.kw.GetCommRealData(code, 63)) and \
                            int(data[8])           == int(self.kw.GetCommRealData(code, 62)) and \
                            int(data[2])           == int(self.kw.GetCommRealData(code, 61)) and \
                            int(data[5])           == int(self.kw.GetCommRealData(code, 71)) and \
                            int(data[11])          == int(self.kw.GetCommRealData(code, 72)) and \
                            int(data[17])          == int(self.kw.GetCommRealData(code, 73)) and \
                            int(data[23])          == int(self.kw.GetCommRealData(code, 74)) and \
                            int(data[29])          == int(self.kw.GetCommRealData(code, 75)) and \
                            int(data[35])          == int(self.kw.GetCommRealData(code, 76)) and \
                            int(data[41])          == int(self.kw.GetCommRealData(code, 77)) and \
                            int(data[47])          == int(self.kw.GetCommRealData(code, 78)) and \
                            int(data[53])          == int(self.kw.GetCommRealData(code, 79)) and \
                            int(data[59])          == int(self.kw.GetCommRealData(code, 80)):
                        self.dict_bool['호가잔량필드같음'] = True
                        self.kwzservQ.put(('window', (ui_num['S로그텍스트'], f'시스템 명령 실행 알림 - 호가잔량 필드값 같음')))
                    else:
                        self.kwzservQ.put(('window', (ui_num['S로그텍스트'], f'시스템 명령 오류 알림 - 호가잔량 필드값이 다릅니다. 필드값 갱신요망!!')))
                    self.dict_bool['호가잔량필드확인'] = True

                name = self.dict_name[code]
                dt = int(self.str_tday + dt)
                if self.dict_bool['호가잔량필드같음']:
                    data = realdata.split('\t')
                    hoga_tamount = (
                        int(data[61]), int(data[63])
                    )
                    hoga_seprice = (
                        abs(int(data[55])), abs(int(data[49])), abs(int(data[43])), abs(int(data[37])), abs(int(data[31])),
                        abs(int(data[25])), abs(int(data[19])), abs(int(data[13])), abs(int(data[7])), abs(int(data[1]))
                    )
                    hoga_buprice = (
                        abs(int(data[4])), abs(int(data[10])), abs(int(data[16])), abs(int(data[22])), abs(int(data[28])),
                        abs(int(data[34])), abs(int(data[40])), abs(int(data[46])), abs(int(data[52])), abs(int(data[58]))
                    )
                    hoga_samount = (
                        int(data[56]), int(data[50]), int(data[44]), int(data[38]), int(data[32]),
                        int(data[26]), int(data[20]), int(data[14]), int(data[8]), int(data[2])
                    )
                    hoga_bamount = (
                        int(data[5]), int(data[11]), int(data[17]), int(data[23]), int(data[29]),
                        int(data[35]), int(data[41]), int(data[47]), int(data[53]), int(data[59])
                    )
                else:
                    hoga_tamount = (
                        int(self.kw.GetCommRealData(code, 121)),
                        int(self.kw.GetCommRealData(code, 125))
                    )
                    hoga_seprice = (
                        abs(int(self.kw.GetCommRealData(code, 50))),
                        abs(int(self.kw.GetCommRealData(code, 49))),
                        abs(int(self.kw.GetCommRealData(code, 48))),
                        abs(int(self.kw.GetCommRealData(code, 47))),
                        abs(int(self.kw.GetCommRealData(code, 46))),
                        abs(int(self.kw.GetCommRealData(code, 45))),
                        abs(int(self.kw.GetCommRealData(code, 44))),
                        abs(int(self.kw.GetCommRealData(code, 43))),
                        abs(int(self.kw.GetCommRealData(code, 42))),
                        abs(int(self.kw.GetCommRealData(code, 41)))
                    )
                    hoga_buprice = (
                        abs(int(self.kw.GetCommRealData(code, 51))),
                        abs(int(self.kw.GetCommRealData(code, 52))),
                        abs(int(self.kw.GetCommRealData(code, 53))),
                        abs(int(self.kw.GetCommRealData(code, 54))),
                        abs(int(self.kw.GetCommRealData(code, 55))),
                        abs(int(self.kw.GetCommRealData(code, 56))),
                        abs(int(self.kw.GetCommRealData(code, 57))),
                        abs(int(self.kw.GetCommRealData(code, 58))),
                        abs(int(self.kw.GetCommRealData(code, 59))),
                        abs(int(self.kw.GetCommRealData(code, 60)))
                    )
                    hoga_samount = (
                        int(self.kw.GetCommRealData(code, 70)),
                        int(self.kw.GetCommRealData(code, 69)),
                        int(self.kw.GetCommRealData(code, 68)),
                        int(self.kw.GetCommRealData(code, 67)),
                        int(self.kw.GetCommRealData(code, 66)),
                        int(self.kw.GetCommRealData(code, 65)),
                        int(self.kw.GetCommRealData(code, 64)),
                        int(self.kw.GetCommRealData(code, 63)),
                        int(self.kw.GetCommRealData(code, 62)),
                        int(self.kw.GetCommRealData(code, 61))
                    )
                    hoga_bamount = (
                        int(self.kw.GetCommRealData(code, 71)),
                        int(self.kw.GetCommRealData(code, 72)),
                        int(self.kw.GetCommRealData(code, 73)),
                        int(self.kw.GetCommRealData(code, 74)),
                        int(self.kw.GetCommRealData(code, 75)),
                        int(self.kw.GetCommRealData(code, 76)),
                        int(self.kw.GetCommRealData(code, 77)),
                        int(self.kw.GetCommRealData(code, 78)),
                        int(self.kw.GetCommRealData(code, 79)),
                        int(self.kw.GetCommRealData(code, 80))
                    )
            except Exception as e:
                self.kwzservQ.put(('window', (ui_num['S단순텍스트'], f'시스템 명령 오류 알림 - OnReceiveRealData 주식호가잔량 {e}')))
            else:
                self.UpdateHogaData(dt, hoga_tamount, hoga_seprice, hoga_buprice, hoga_samount, hoga_bamount, code, name, start)

    def UpdateTickData(self, code, dt, c, o, h, low, per, dm, v, ch, dmp, jvp, vrp, jsvp, sgta, csp, cbp):
        if self.operation == 1:
            self.operation = 3

        if dt != self.int_jcct and dt > self.int_jcct:
            self.int_jcct = dt

        if code not in self.dict_vipr.keys():
            self.InsertViPrice(code, o)
        elif not self.dict_vipr[code][0] and now() > self.dict_vipr[code][1]:
            self.UpdateViPrice(code, c)

        if code in self.dict_tick.keys():
            prebids, preasks = self.dict_tick[code][13:15]
        else:
            prebids, preasks = 0, 0

        rf = roundfigure_upper5(c, dt)
        bids, asks = 0, 0
        if '+' in v:
            bids = prebids + abs(int(v))
            asks = preasks
        elif '-' in v:
            bids = prebids
            asks = preasks + abs(int(v))

        self.dict_hgbs[code] = (csp, cbp)
        self.dict_tick[code] = [c, o, h, low, per, dm, ch, dmp, jvp, vrp, jsvp, sgta, rf, bids, asks, self.dict_vipr[code][1], self.dict_vipr[code][2], self.dict_vipr[code][-1]]

        if not self.dict_set['주식장초프로세스종료'] and not self.dict_set['장중전략조건검색식사용']:
            dt_ = int(str(dt)[:13])
            if code not in self.dict_arry.keys():
                self.dict_arry[code] = np.array([[dt_, dm]])
            elif dt_ != self.dict_arry[code][-1, 0]:
                self.dict_arry[code] = np.r_[self.dict_arry[code], np.array([[dt_, dm]])]
                if len(self.dict_arry[code]) == self.dict_set['주식순위시간'] * 6:
                    if per >= 0:
                        self.dict_tm5m[code] = dm - self.dict_arry[code][0, 1]
                    elif code in self.dict_tm5m.keys():
                        del self.dict_tm5m[code]
                    self.dict_arry[code] = np.delete(self.dict_arry[code], 0, 0)

    def UpdateHogaData(self, dt, hoga_tamount, hoga_seprice, hoga_buprice, hoga_samount, hoga_bamount, code, name, receivetime):
        sm = 0
        int_logt = int(str(dt)[:12])
        ticksend = False
        if code in self.dict_tick.keys():
            if code in self.dict_hgdt.keys():
                if dt > self.dict_hgdt[code][0] and hoga_bamount[4] != 0:
                    sm = self.dict_tick[code][5] - self.dict_hgdt[code][1]
                    ticksend = True
            else:
                sm = self.dict_tick[code][5]
                ticksend = True

        if ticksend:
            csp, cbp = self.dict_hgbs[code]

            if hoga_seprice[-1] < csp:
                index = 0
                for i, price in enumerate(hoga_seprice[::-1]):
                    if price >= csp:
                        index = i
                        break
                if index <= 5:
                    hoga_seprice = hoga_seprice[5 - index:10 - index]
                    hoga_samount = hoga_samount[5 - index:10 - index]
                else:
                    hoga_seprice = tuple(np.zeros(index - 5)) + hoga_seprice[:10 - index]
                    hoga_samount = tuple(np.zeros(index - 5)) + hoga_samount[:10 - index]
            else:
                hoga_seprice = hoga_seprice[-5:]
                hoga_samount = hoga_samount[-5:]

            if hoga_buprice[0] > cbp:
                index = 0
                for i, price in enumerate(hoga_buprice):
                    if price <= cbp:
                        index = i
                        break
                hoga_buprice = hoga_buprice[index:index + 5]
                hoga_bamount = hoga_bamount[index:index + 5]
                if index > 5:
                    hoga_buprice = hoga_buprice + tuple(np.zeros(index - 5))
                    hoga_bamount = hoga_bamount + tuple(np.zeros(index - 5))
            else:
                hoga_buprice = hoga_buprice[:5]
                hoga_bamount = hoga_bamount[:5]

            c     = self.dict_tick[code][0]
            hlp   = round((c / ((self.dict_tick[code][2] + self.dict_tick[code][3]) / 2) - 1) * 100, 2)
            hgjrt = sum(hoga_samount + hoga_bamount)
            logt  = now() if self.int_logt < int_logt else 0
            gsjm  = 1 if code in self.list_gsjm else 0
            data  = (dt,) + tuple(self.dict_tick[code]) + (sm, hlp) + hoga_tamount + hoga_seprice + hoga_buprice + hoga_samount + hoga_bamount + (hgjrt, gsjm, code, name, logt)

            self.sstgQs[self.dict_sgbn[code]].put(data)
            if code in self.tuple_janng or code in self.tuple_order:
                self.straderQ.put((code, c))

            if self.hoga_code == code:
                if code in self.dict_sghg.keys():
                    shg, hhg = self.dict_sghg[code]
                else:
                    shg, hhg = GetSangHahanga(code in self.tuple_kosd, self.kw.GetMasterLastPrice(code), self.int_hgtime)
                    self.dict_sghg[code] = (shg, hhg)
                c, o, h, low, per, _, ch, _, _, _, _, sgta, _, bids, asks, _, uvi, _ = self.dict_tick[code]
                self.kwzservQ.put(('hoga', (self.dict_name[code], c, per, sgta, self.dict_vipr[code][2], o, h, low)))
                self.kwzservQ.put(('hoga', (-asks, ch)))
                self.kwzservQ.put(('hoga', (bids, ch)))
                self.kwzservQ.put(('hoga', (name,) + hoga_tamount + hoga_seprice[-5:] + hoga_buprice[:5] + hoga_samount[-5:] + hoga_bamount[:5] + (shg, hhg)))

            self.dict_hgdt[code] = [dt, self.dict_tick[code][5]]
            self.dict_tick[code][13:15] = [0, 0]

        if ticksend and self.int_logt < int_logt:
            gap = (now() - receivetime).total_seconds()
            self.kwzservQ.put(('window', (ui_num['S단순텍스트'], f'리시버 연산 시간 알림 - 수신시간과 연산시간의 차이는 [{gap:.6f}]초입니다.')))
            self.int_logt = int_logt

    def InsertViPrice(self, code, o):
        uvi, dvi, hogaunit = GetVIPrice(code in self.tuple_kosd, o, self.int_hgtime)
        self.dict_vipr[code] = [True, timedelta_sec(-3600), uvi, dvi, hogaunit]

    def UpdateViPrice(self, code, key):
        if type(key) == str:
            if code in self.dict_vipr.keys():
                self.dict_vipr[code][:2] = False, timedelta_sec(5)
            else:
                self.dict_vipr[code] = [False, timedelta_sec(5), 0, 0, 0]
            self.kwzservQ.put(('window', (ui_num['S로그텍스트'], f'변동성 완화 장치 발동 - [{code}] {key}')))
        elif type(key) == int:
            uvi, dvi, hogaunit = GetVIPrice(code in self.tuple_kosd, key, self.int_hgtime)
            self.dict_vipr[code] = [True, timedelta_sec(5), uvi, dvi, hogaunit]
