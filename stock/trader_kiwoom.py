import sqlite3
from kiwoom import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QThread, QTimer
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utility.setting import ui_num, columns_cj, columns_tj, columns_jg, columns_td, columns_tt, DB_TRADELIST, DICT_SET, dict_order
from utility.static import now, strf_time, strp_time, timedelta_sec, int_hms, qtest_qwait, GetKiwoomPgSgSp, GetHogaunit


class Updater(QThread):
    signal1 = pyqtSignal(tuple)
    signal2 = pyqtSignal(str)

    def __init__(self, straderQ):
        super().__init__()
        self.straderQ = straderQ

    def run(self):
        while True:
            data = self.straderQ.get()
            if type(data) == tuple:
                # noinspection PyUnresolvedReferences
                self.signal1.emit(data)
            elif type(data) == str:
                # noinspection PyUnresolvedReferences
                self.signal2.emit(data)


class TraderKiwoom:
    def __init__(self, qlist):
        app = QApplication(sys.argv)
        self.kwzservQ  = qlist[0]
        self.sreceivQ  = qlist[1]
        self.straderQ  = qlist[2]
        self.sstgQs    = qlist[3]
        self.dict_set  = DICT_SET

        if self.dict_set['트레이더프로파일링']:
            import cProfile
            self.pr = cProfile.Profile()
            self.pr.enable()

        self.df_cj = pd.DataFrame(columns=columns_cj)
        self.df_jg = pd.DataFrame(columns=columns_jg)
        self.df_tj = pd.DataFrame(columns=columns_tj)
        self.df_td = pd.DataFrame(columns=columns_td)
        self.df_tt = pd.DataFrame(columns=columns_tt)

        self.dict_buy  = {}
        self.dict_sell = {}
        self.dict_name = {}
        self.dict_curc = {}
        self.dict_sgbn = {}
        self.dict_intg = {
            '장운영상태': 1,
            '예수금': 0,
            '추정예수금': 0,
            '추정예탁자산': 0,
            '종목당투자금': 0
        }
        self.dict_strg = {
            '당일날짜': strf_time('%Y%m%d'),
            '계좌번호': ''
        }
        self.dict_bool = {
            '계좌조회': False,
            '트레이더시작': False,
            '장초전략잔고청산': False,
            '장중전략잔고청산': False,
            '프로세스종료': False
        }
        curr_time      = now()
        remaintime     = (strp_time('%Y%m%d%H%M%S', self.dict_strg['당일날짜'] + '090100') - curr_time).total_seconds()
        self.dict_time = {
            '휴무종료': timedelta_sec(remaintime) if remaintime > 0 else None,
            '주문시간': curr_time
        }
        self.int_hgtime = int(strf_time('%Y%m%d%H%M%S'))
        self.tuple_kosd  = None

        self.intg_odsn = 3000                                   # 주문용 화면번호
        self.dict_snst = {x: True for x in range(3000, 3150)}   # 화면번호 사용중 여부 기록용 키:화면번호, 벨류:사용가능유무
        self.dict_sncd = {}                                     # 사용한 화면번호의 종목코드 키:화면번호, 벨류:종목코드

        self.LoadDatabase()
        self.kw = Kiwoom(self, 'Trader')
        self.KiwoomLogin()

        self.updater = Updater(self.straderQ)
        # noinspection PyUnresolvedReferences
        self.updater.signal1.connect(self.UpdateTuple)
        # noinspection PyUnresolvedReferences
        self.updater.signal2.connect(self.UpdateString)
        self.updater.start()

        self.qtimer1 = QTimer()
        self.qtimer1.setInterval(1 * 1000)
        # noinspection PyUnresolvedReferences
        self.qtimer1.timeout.connect(self.Scheduler)
        self.qtimer1.start()

        self.qtimer2 = QTimer()
        self.qtimer2.setInterval(500)
        # noinspection PyUnresolvedReferences
        self.qtimer2.timeout.connect(self.PutJangoDF)
        self.qtimer2.start()

        app.exec_()

    def LoadDatabase(self):
        con = sqlite3.connect(DB_TRADELIST)
        self.df_cj = pd.read_sql(f"SELECT * FROM s_chegeollist WHERE 체결시간 LIKE '{self.dict_strg['당일날짜']}%'", con).set_index('index')
        self.df_td = pd.read_sql(f"SELECT * FROM s_tradelist WHERE 체결시간 LIKE '{self.dict_strg['당일날짜']}%'", con).set_index('index')

        if len(self.df_cj) > 0: self.kwzservQ.put(('window', (ui_num['S체결목록'], self.df_cj[::-1])))
        if len(self.df_td) > 0: self.kwzservQ.put(('window', (ui_num['S거래목록'], self.df_td[::-1])))
        if self.dict_set['주식모의투자']:
            self.df_jg = pd.read_sql('SELECT * FROM s_jangolist', con).set_index('index')
            if len(self.df_jg) > 0: self.sreceivQ.put(('잔고목록', tuple(self.df_jg.index)))
        con.close()

        self.kwzservQ.put(('window', (ui_num['S로그텍스트'], '시스템 명령 실행 알림 - 데이터베이스 정보 불러오기 완료')))

    def KiwoomLogin(self):
        self.kw.CommConnect()
        self.dict_strg['계좌번호'] = self.kw.GetAccountNumber()
        self.tuple_kosd = self.kw.GetCodeListByMarket('10')
        list_code = self.kw.GetCodeListByMarket('0') + self.tuple_kosd
        dummy_time = timedelta_sec(-3600)
        self.dict_name = {code: [self.kw.GetMasterCodeName(code), dummy_time, dummy_time, dummy_time] for code in list_code}

        if int_hms() > 90000:
            self.dict_intg['장운영상태'] = 3

        self.kwzservQ.put(('window', (ui_num['S로그텍스트'], '시스템 명령 실행 알림 - OpenAPI 로그인 완료')))
        text = '주식 전략연산 및 트레이더를 시작하였습니다.'
        if self.dict_set['주식알림소리']: self.kwzservQ.put(('sound', text))
        self.kwzservQ.put(('tele', text))

    def UpdateTuple(self, data):
        if len(data) in (7, 8):
            self.CheckOrder(data)
        elif len(data) == 2:
            if type(data[1]) == int:
                code, c = data
                self.dict_curc[code] = c
                try:
                    if c != self.df_jg['현재가'][code]:
                        jg = self.df_jg['매입금액'][code]
                        jc = int(self.df_jg['보유수량'][code])
                        pg, sg, sp = GetKiwoomPgSgSp(jg, jc * c)
                        columns = ['현재가', '수익률', '평가손익', '평가금액']
                        self.df_jg.loc[code, columns] = c, sp, sg, pg
                except:
                    pass
            elif data[0] == '관심진입':
                if data[1] in self.dict_sell.keys():
                    self.CancelOrder(data[1], '매도')
            elif data[0] == '관심이탈':
                if data[1] in self.dict_buy.keys():
                    self.CancelOrder(data[1], '매수')
            elif data[0] == '설정변경':
                self.dict_set = data[1]
            elif data[0] == '종목구분번호':
                self.dict_sgbn = data[1]

    def UpdateString(self, data):
        if data == 'S체결목록':
            self.kwzservQ.put(('tele', self.df_cj)) if len(self.df_cj) > 0 else self.kwzservQ.put(('tele', '현재는 주식체결목록이 없습니다.'))
        elif data == 'S거래목록':
            self.kwzservQ.put(('tele', self.df_td)) if len(self.df_td) > 0 else self.kwzservQ.put(('tele', '현재는 주식거래목록이 없습니다.'))
        elif data == 'S잔고평가':
            self.kwzservQ.put(('tele', self.df_jg)) if len(self.df_jg) > 0 else self.kwzservQ.put(('tele', '현재는 주식잔고목록이 없습니다.'))
        elif data == 'S잔고청산':
            self.JangoCheongsan('수동')
        elif data == '프로파일링결과':
            self.pr.print_stats(sort='cumulative')
        elif data == '프로세스종료':
            if not self.dict_bool['프로세스종료']:
                self.dict_bool['프로세스종료'] = True
                QTimer.singleShot(180 * 1000, self.SysExit)

    def CheckOrder(self, data):
        if len(data) == 7:
            gubun, code, name, op, oc, signal_time, manual = data
            ordertype = None
        else:
            gubun, code, name, op, oc, signal_time, manual, ordertype = data

        NIJ = code not in self.df_jg.index
        INB = code in self.dict_buy.keys()
        INS = code in self.dict_sell.keys()

        on = ''
        cancel = False
        curr_time = now()
        if manual:
            if NIJ:
                cancel = True
            elif INS:
                cancel = True
        elif gubun == '매수':
            if self.dict_intg['추정예수금'] < oc * op:
                if code not in self.dict_name.keys() or curr_time > self.dict_name[code][1]:
                    self.CreateOrder('시드부족', code, name, op, oc, '', signal_time, manual, None)
                    self.dict_name[code][1] = timedelta_sec(180)
                cancel = True
            elif INB:
                cancel = True
        elif gubun == '매도':
            if NIJ or INS:
                cancel = True
        elif '취소' in gubun:
            df = self.GetMichegeolDF(name, gubun.replace('취소', ''))
            if len(df) > 0:
                mc = df['미체결수량'].iloc[-1]
                if mc > 0:
                    oc = mc
                    on = df['주문번호'].iloc[-1]
                else:
                    cancel = True
            else:
                cancel = True

            if gubun == '매수취소' and not INB:   cancel = True
            elif gubun == '매도취소' and not INS: cancel = True

        if cancel:
            if '취소' not in gubun:
                self.PutOrderComplete(f'{gubun}취소', code)
        else:
            if manual and gubun in ('매수', '매도'):
                self.PutOrderComplete(f'{gubun}주문', code)

            if oc > 0:
                self.CreateOrder(gubun, code, name, op, oc, on, signal_time, manual, ordertype)
            else:
                self.PutOrderComplete(f'{gubun}취소', code)

    def CreateOrder(self, gubun, code, name, op, oc, on, signal_time, manual, ordertype):
        og = 0
        if gubun == '매수':      og = 1
        elif gubun == '매도':    og = 2
        elif gubun == '매수취소': og = 3
        elif gubun == '매도취소': og = 4
        elif gubun == '매수정정': og = 5
        elif gubun == '매도정정': og = 6

        if manual:
            ogn = '03'
        elif '매수' in gubun:
            ogn = dict_order[self.dict_set['주식매수주문구분']] if ordertype is None else dict_order[ordertype]
        else:
            ogn = dict_order[self.dict_set['주식매도주문구분']] if ordertype is None else dict_order[ordertype]

        if manual:
            if not (self.dict_set['주식모의투자'] or gubun == '시드부족'):
                op = 0
        elif gubun == '매수':
            if self.dict_set['주식매수주문구분'] not in ('지정가', '지정가IOC', '지정가FOK'):
                if not (self.dict_set['주식모의투자'] or gubun == '시드부족'):
                    op = 0
        elif gubun == '매도':
            if self.dict_set['주식매도주문구분'] not in ('지정가', '지정가IOC', '지정가FOK'):
                if not (self.dict_set['주식모의투자'] or gubun == '시드부족'):
                    op = 0

        if oc > 0:
            if self.dict_set['주식모의투자'] or gubun == '시드부족':
                self.OrderTimeLog(signal_time)
                ct = strf_time('%Y%m%d%H%M%S')
                if gubun == '시드부족':
                    self.UpdateChejanData(code, name, op, '체결', gubun, oc, 0, oc, op, 0, ct, on, '', '')
                else:
                    self.UpdateChejanData(code, name, op, '체결', gubun, oc, oc, 0, op, op, ct, on, '', '')
            else:
                self.SendOrder([gubun, 0, self.dict_strg['계좌번호'], og, code, int(oc), int(op), ogn, on], name, signal_time)

    def SendOrder(self, order, name, signal_time):
        curr_time = now()
        if curr_time < self.dict_time['주문시간']:
            next_time = (self.dict_time['주문시간'] - curr_time).total_seconds()
            QTimer.singleShot(int(next_time * 1000), lambda: self.SendOrder(order, name, signal_time))
            return

        while not self.dict_snst[self.intg_odsn]:
            self.intg_odsn = self.intg_odsn + 1 if self.intg_odsn + 1 < 3150 else 3000
        order[1] = self.intg_odsn

        self.OrderTimeLog(signal_time)
        ret = self.kw.SendOrder(order)
        if ret == 0:
            self.kwzservQ.put(('window', (ui_num['S로그텍스트'], f'주문 관리 시스템 알림 - [전송] {name} | {order[6]} | {order[5]} | {order[0]}')))
            self.dict_time['주문시간'] = timedelta_sec(0.2)
            self.dict_snst[self.intg_odsn] = False
            self.dict_sncd[self.intg_odsn] = order[4]
        else:
            self.PutOrderComplete(f'{order[0]}취소', order[4])
            self.kwzservQ.put(('window', (ui_num['S로그텍스트'], f'시스템 명령 오류 알림 - [주문 실패] {name} | {order[6]} | {order[5]} | {order[0]}')))

    def Scheduler(self):
        if not self.dict_bool['계좌조회']:
            self.GetAccountjanGo()

        if not self.dict_bool['트레이더시작']:
            self.OperationRealreg()

        inthms = int_hms()
        if self.dict_intg['장운영상태'] in (2, 3):
            if self.dict_set['주식장초전략종료시간'] <= inthms < self.dict_set['주식장초전략종료시간'] + 10:
                if not self.dict_bool['장초전략잔고청산']:
                    self.JangoCheongsan('장초')

            if self.dict_set['주식장중전략종료시간'] <= inthms < self.dict_set['주식장중전략종료시간'] + 10:
                if not self.dict_bool['장중전략잔고청산']:
                    self.JangoCheongsan('장중')

        self.UpdateTotaljango(inthms)

    def GetAccountjanGo(self):
        self.dict_bool['계좌조회'] = True

        if not self.dict_set['주식모의투자']:
            df = self.kw.Block_Request('opw00018', 계좌번호=self.dict_strg['계좌번호'], 비밀번호='', 비밀번호입력매체구분='00', 조회구분=2, output='계좌평가잔고개별합산', next=0)
            if df['종목명'][0] != '':
                df.rename(columns={'종목번호': 'index', '수익률(%)': '수익률'}, inplace=True)
                df['index'] = df['index'].apply(lambda x: x.strip()[1:])
                df['수익률'] = df['수익률'].apply(lambda x: round(float(x) / 100, 2))
                columns = ['매입가', '현재가', '평가손익', '매입금액', '평가금액', '보유수량']
                df[columns] = df[columns].astype(int)
                df['평가손익'] = df['평가금액'] - df['매입금액']
                df['분할매수횟수'] = 5
                df['분할매도횟수'] = 0
                df['매수시간'] = self.dict_strg['당일날짜'] + '080000'
                columns = ['index', '종목명', '매입가', '현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량', '분할매수횟수', '분할매도횟수', '매수시간']
                df = df[columns]
                self.df_jg = df.set_index('index')

                if len(self.df_jg) > 0:
                    self.sreceivQ.put(('잔고목록', tuple(self.df_jg.index)))

        while True:
            df = self.kw.Block_Request('opw00004', 계좌번호=self.dict_strg['계좌번호'], 비밀번호='', 상장폐지조회구분=0, 비밀번호입력매체구분='00', output='계좌평가현황', next=0)
            if df['D+2추정예수금'][0] != '':
                if self.dict_set['주식모의투자']:
                    con = sqlite3.connect(DB_TRADELIST)
                    df = pd.read_sql('SELECT * FROM s_tradelist', con)
                    con.close()
                    self.dict_intg['예수금'] = 100_000_000 - self.df_jg['매입금액'].sum() + df['수익금'].sum()
                    if self.dict_intg['예수금'] < 100_000_000: self.dict_intg['예수금'] = 100_000_000
                else:
                    self.dict_intg['예수금'] = int(df['D+2추정예수금'][0])

                self.dict_intg['추정예수금'] = self.dict_intg['예수금'] * 2
                break
            else:
                self.kwzservQ.put(('window', (ui_num['S로그텍스트'], '시스템 명령 오류 알림 - 오류가 발생하여 계좌평가현황을 재조회합니다.')))
                qtest_qwait(3.35)

        while True:
            df = self.kw.Block_Request('opw00018', 계좌번호=self.dict_strg['계좌번호'], 비밀번호='', 비밀번호입력매체구분='00', 조회구분=2, output='계좌평가결과', next=0)
            if df['추정예탁자산'][0] != '':
                if self.dict_set['주식모의투자']:
                    self.dict_intg['추정예탁자산'] = self.dict_intg['예수금'] + self.df_jg['평가금액'].sum()
                    self.df_tj.loc[self.dict_strg['당일날짜']] = self.dict_intg['추정예탁자산'], self.dict_intg['예수금'], 0, 0, 0, 0, 0
                else:
                    self.dict_intg['추정예탁자산'] = int(df['추정예탁자산'][0])
                    tsp = float(int(df['총수익률(%)'][0]) / 100)
                    tsg = int(df['총평가손익금액'][0])
                    tbg = int(df['총매입금액'][0])
                    tpg = int(df['총평가금액'][0])
                    self.df_tj.loc[self.dict_strg['당일날짜']] = self.dict_intg['추정예탁자산'], self.dict_intg['예수금'], 0, tsp, tsg, tbg, tpg

                self.kwzservQ.put(('window', (ui_num['S잔고평가'], self.df_tj)))
                break
            else:
                self.kwzservQ.put(('window', (ui_num['S로그텍스트'], '시스템 명령 오류 알림 - 오류가 발생하여 계좌평가결과를 재조회합니다.')))
                qtest_qwait(3.35)

        if len(self.df_td) > 0:
            self.UpdateTotaltradelist(first=True)
        self.kwzservQ.put(('window', (ui_num['S로그텍스트'], '시스템 명령 실행 알림 - 계좌 조회 완료')))

    def OperationRealreg(self):
        self.dict_bool['트레이더시작'] = True
        self.kw.SetRealReg([sn_oper, ' ', '215;20;214', 0])
        self.kwzservQ.put(('window', (ui_num['S로그텍스트'], '시스템 명령 실행 알림 - 장운영시간 등록 완료')))
        self.kwzservQ.put(('window', (ui_num['S로그텍스트'], '시스템 명령 실행 알림 - 트레이더 시작')))

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

        if (gubun == '수동' or self.dict_set[f'주식{gubun}잔고청산']) and len(self.df_jg) > 0:
            for code in self.df_jg.index:
                c, oc = self.df_jg['현재가'][code], self.df_jg['보유수량'][code]
                name = self.dict_name[code][0]
                if self.dict_set['주식모의투자']:
                    self.UpdateChejanData(code, name, c, '체결', '매도', oc, oc, 0, c, c, strf_time('%Y%m%d%H%M%S'), '', '', '')
                else:
                    self.CheckOrder(('매도', code, name, c, oc, now(), True))

            if self.dict_set['주식알림소리']:
                self.kwzservQ.put(('sound', f'주식 {gubun}전략 잔고청산 주문을 전송하였습니다.'))
            self.kwzservQ.put(('window', (ui_num['S로그텍스트'], f'시스템 명령 실행 알림 - {gubun}전략 잔고청산 주문 완료')))

    def CancelOrder(self, code, gubun):
        name = self.dict_name[code][0]
        df = self.GetMichegeolDF(name, gubun)
        if len(df) > 0:
            mc = df['미체결수량'].iloc[-1]
            if mc > 0:
                self.CreateOrder(f'{gubun}취소', code, name, 0, mc, df['주문번호'].iloc[-1], now(), False, None)

    def SysExit(self):
        self.dict_bool['프로세스종료'] = True
        if self.qtimer1.isActive():  self.qtimer1.stop()
        if self.updater.isRunning(): self.updater.quit()
        self.RemoveAllRealreg()
        self.SaveDayData()
        self.kwzservQ.put(('tele', '주식 트레이더 종료'))
        qtest_qwait(10)
        self.kwzservQ.put(('window', (ui_num['S로그텍스트'], '시스템 명령 실행 알림 - 트레이더 종료')))

    def RemoveAllRealreg(self):
        self.kw.SetRealRemove(['ALL', 'ALL'])
        if self.dict_set['주식알림소리']:
            self.kwzservQ.put(('sound', '실시간 주문체결 데이터의 수신을 중단하였습니다.'))
        self.kwzservQ.put(('window', (ui_num['S로그텍스트'], '시스템 명령 실행 알림 - 실시간 데이터 중단 완료')))

    def SaveDayData(self):
        if self.dict_intg['장운영상태'] != 1 and len(self.df_td) > 0:
            con = sqlite3.connect(DB_TRADELIST)
            df = pd.read_sql(f"SELECT * FROM s_totaltradelist WHERE `index` = '{self.dict_strg['당일날짜']}'", con)
            con.close()
            if len(df) == 0:
                df = self.df_tt[['총매수금액', '총매도금액', '총수익금액', '총손실금액', '수익률', '수익금합계']]
                self.kwzservQ.put(('query', ('거래디비', df, 's_totaltradelist', 'append')))
                if self.dict_set['주식알림소리']:
                    self.kwzservQ.put(('sound', '일별실현손익를 저장하였습니다.'))
                self.kwzservQ.put(('window', (ui_num['S로그텍스트'], '시스템 명령 실행 알림 - 일별실현손익 저장 완료')))

    def PutJangoDF(self):
        if not self.dict_bool['프로세스종료']:
            data = ('잔고목록', self.df_jg)
            for q in self.sstgQs:
                q.put(data)

    # noinspection PyUnusedLocal
    def OnReceiveMsg(self, sScrNo, sRQName, sTrCode, sMsg):
        print(f'[{now()}]{sMsg}')
        self.kwzservQ.put(('window', (ui_num['S오더텍스트'], f'{sMsg}')))
        if '매수증거금' in sMsg:
            sn = int(sScrNo)
            code = self.dict_sncd[sn] if sn in self.dict_sncd.keys() else ''
            self.PutOrderComplete('매수취소', code)

    # noinspection PyUnusedLocal
    def OnReceiveRealData(self, code, realtype, realdata):
        if realtype == '장시작시간':
            try:
                self.dict_intg['장운영상태'] = int(self.kw.GetCommRealData(code, 215))
                current = self.kw.GetCommRealData(code, 20)
            except:
                pass
            else:
                self.OperationAlert(current)

    def OperationAlert(self, current):
        if self.dict_set['주식알림소리']:
            if current == '084000':
                self.kwzservQ.put(('sound', '장시작 20분 전입니다.'))
            elif current == '085000':
                self.kwzservQ.put(('sound', '장시작 10분 전입니다.'))
            elif current == '085500':
                self.kwzservQ.put(('sound', '장시작 5분 전입니다.'))
            elif current == '085900':
                self.kwzservQ.put(('sound', '장시작 1분 전입니다.'))
            elif current == '085930':
                self.kwzservQ.put(('sound', '장시작 30초 전입니다.'))
            elif current == '085940':
                self.kwzservQ.put(('sound', '장시작 20초 전입니다.'))
            elif current == '085950':
                self.kwzservQ.put(('sound', '장시작 10초 전입니다.'))
            elif current == '090000':
                self.kwzservQ.put(('sound', f"{self.dict_strg['당일날짜'][:4]}년 {self.dict_strg['당일날짜'][4:6]}월 "
                                            f"{self.dict_strg['당일날짜'][6:]}일 장이 시작되었습니다."))
            elif current == '152000':
                self.kwzservQ.put(('sound', '장마감 10분 전입니다.'))
            elif current == '152500':
                self.kwzservQ.put(('sound', '장마감 5분 전입니다.'))
            elif current == '152900':
                self.kwzservQ.put(('sound', '장마감 1분 전입니다.'))
            elif current == '152930':
                self.kwzservQ.put(('sound', '장마감 30초 전입니다.'))
            elif current == '152940':
                self.kwzservQ.put(('sound', '장마감 20초 전입니다.'))
            elif current == '152950':
                self.kwzservQ.put(('sound', '장마감 10초 전입니다.'))
            elif current == '153000':
                self.kwzservQ.put(('sound', f"{self.dict_strg['당일날짜'][:4]}년 {self.dict_strg['당일날짜'][4:6]}월 "
                                            f"{self.dict_strg['당일날짜'][6:]}일 장이 종료되었습니다."))

    # noinspection PyUnusedLocal
    def OnReceiveChejanData(self, gubun, itemcnt, fidlist):
        if self.dict_set['주식모의투자']:
            return

        if gubun == '0':
            try:
                code       = self.kw.GetChejanData(9001).strip('A')
                name       = self.dict_name[code][0]
                sc = abs(int(self.kw.GetChejanData(27)))
                ot         = self.kw.GetChejanData(913)
                og         = self.kw.GetChejanData(905)[1:]
                op     = int(self.kw.GetChejanData(901))
                oc     = int(self.kw.GetChejanData(900))
                mc     = int(self.kw.GetChejanData(902))
                ct     = self.dict_strg['당일날짜'] + self.kw.GetChejanData(908)
                on         = self.kw.GetChejanData(9203)
                sn     = int(self.kw.GetChejanData(920))
            except Exception as e:
                self.kwzservQ.put(('window', (ui_num['S로그텍스트'], f'시스템 명령 오류 알림 - OnReceiveChejanData 0 {e}')))
            else:
                try:
                    cp = int(self.kw.GetChejanData(914))
                    cc = int(self.kw.GetChejanData(915))
                    oon    = self.kw.GetChejanData(904)
                except:
                    cp  = 0
                    cc  = 0
                    oon = 0
                self.UpdateChejanData(code, name, sc, ot, og, oc, cc, mc, op, cp, ct, on, oon, sn)

    def UpdateChejanData(self, code, name, sc, ot, og, oc, cc, mc, op, cp, ct, on, oon, sn):
        index = strf_time('%Y%m%d%H%M%S%f')
        if index in self.df_cj.index:
            while index in self.df_cj.index:
                index = str(int(index) + 1)

        if ot == '접수' and mc > 0:
            if og == '매수':
                self.dict_buy[code] = [timedelta_sec(self.dict_set['주식매수취소시간초']), 0, op, GetHogaunit(code in self.tuple_kosd, op, self.int_hgtime)]
                if '지정가' in self.dict_set['주식매수주문구분']:
                    self.dict_intg['추정예수금'] -= oc * op
                else:
                    self.dict_intg['추정예수금'] -= oc * sc
            elif og == '매도':
                self.dict_sell[code] = [timedelta_sec(self.dict_set['주식매도취소시간초']), 0, op, GetHogaunit(code in self.tuple_kosd, op, self.int_hgtime)]
            elif og == '매수정정':
                fix_count = self.dict_buy[code][1] + 1
                self.dict_buy[code] = [timedelta_sec(self.dict_set['주식매수취소시간초']), fix_count, op, GetHogaunit(code in self.tuple_kosd, op, self.int_hgtime)]
                df = self.df_cj[self.df_cj['주문번호'] == oon]
                if len(df) > 0:
                    oop = df['주문가격'].iloc[-1]
                    self.dict_intg['추정예수금'] += oc * oop
                    self.dict_intg['추정예수금'] -= oc * op
                    self.dict_snst[sn] = True
            elif og == '매도정정':
                fix_count = self.dict_sell[code][1] + 1
                self.dict_sell[code] = [timedelta_sec(self.dict_set['주식매도취소시간초']), fix_count, op, GetHogaunit(code in self.tuple_kosd, op, self.int_hgtime)]
                df = self.df_cj[self.df_cj['주문번호'] == oon]
                if len(df) > 0:
                    if df['미체결수량'].iloc[-1] > 0:
                        self.dict_snst[sn] = True

            self.UpdateChegeollist(index, code, name, og if '정정' in og else og + ot, oc, cc, mc, cp, ct, op, on)
            self.kwzservQ.put(('window', (ui_num['S로그텍스트'], f'주문 관리 시스템 알림 - [{ot}] {name} | {op} | {oc} | {og}')))

        elif ot == '체결' and og in ('매수', '매도'):
            if og == '매수':
                if code in self.df_jg.index:
                    jc = self.df_jg['보유수량'][code] + cc
                    jg = self.df_jg['매입금액'][code] + cc * cp
                    jp = int(round(jg / jc))
                    pg, sg, sp = GetKiwoomPgSgSp(jg, jc * cp)
                    columns = ['매입가', '현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량', '매수시간']
                    self.df_jg.loc[code, columns] = jp, cp, sp, sg, jg, pg, jc, ct
                else:
                    jc = cc
                    jg = cc * cp
                    jp = cp
                    pg, sg, sp = GetKiwoomPgSgSp(jg, jc * cp)
                    self.df_jg.loc[code] = name, jp, cp, sp, sg, jg, pg, jc, 0, 0, ct

                if mc == 0:
                    self.df_jg.loc[code, '분할매수횟수'] = self.df_jg['분할매수횟수'][code] + 1
                    if code in self.dict_buy.keys():
                        del self.dict_buy[code]

            else:
                if code not in self.df_jg.index:
                    return

                jc = self.df_jg['보유수량'][code] - cc
                jp = self.df_jg['매입가'][code]
                if jc != 0:
                    jg = jp * jc
                    pg, sg, sp = GetKiwoomPgSgSp(jg, jc * cp)
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
                pg, sg, sp = GetKiwoomPgSgSp(jg, cc * cp)
                self.UpdateTradelist(index, name, jg, pg, cc, sp, sg, ct)

                if sp < 0:
                    self.dict_name[code][3] = timedelta_sec(self.dict_set['주식매수금지손절간격초'])

            columns = ['매입가', '현재가', '평가손익', '매입금액', '평가금액', '보유수량', '분할매수횟수', '분할매도횟수']
            self.df_jg[columns] = self.df_jg[columns].astype(int)
            self.df_jg.sort_values(by=['매입금액'], ascending=False, inplace=True)

            self.PutJangoDF()
            if mc == 0:
                if not self.dict_set['주식모의투자']: self.dict_snst[sn] = True
                self.PutOrderComplete(og + '완료', code)

            self.UpdateChegeollist(index, code, name, og, oc, cc, mc, cp, ct, op, on)

            if og == '매수':
                self.dict_intg['예수금'] -= cc * cp
            else:
                self.dict_intg['예수금'] += jg + sg
                self.dict_intg['추정예수금'] += jg + sg

            self.kwzservQ.put(('query', ('거래디비', self.df_jg, 's_jangolist', 'replace')))
            if self.dict_set['주식알림소리']:
                self.kwzservQ.put(('sound', f'{name} {cc}주를 {og}하였습니다'))
            self.kwzservQ.put(('window', (ui_num['S로그텍스트'], f'주문 관리 시스템 알림 - [{ot}] {name} | {cp} | {cc} | {og}')))

        elif ot == '체결' and og == '시드부족':
            self.UpdateChegeollist(index, code, name, og, oc, cc, mc, cp, ct, op, on)

        elif ot == '확인' and og in ('매수취소', '매도취소'):
            df = self.GetMichegeolDF(name, og.replace('취소', ''))
            if len(df) > 0 and df['미체결수량'].iloc[-1] > 0:
                if df['체결수량'].iloc[-1] > 0 and code in self.df_jg.index:
                    if og == '매수취소':
                        self.df_jg.loc[code, '분할매수횟수'] = self.df_jg['분할매수횟수'][code] + 1
                    elif og == '매도취소':
                        self.df_jg.loc[code, '분할매도횟수'] = self.df_jg['분할매도횟수'][code] + 1
                    self.PutJangoDF()

                if og == '매수취소':
                    self.dict_intg['추정예수금'] += df['미체결수량'].iloc[-1] * df['주문가격'].iloc[-1]

                if og == '매수취소' and code in self.dict_buy.keys():
                    del self.dict_buy[code]
                elif og == '매도취소' and code in self.dict_sell.keys():
                    del self.dict_sell[code]

            if not self.dict_set['주식모의투자']: self.dict_snst[sn] = True
            self.PutOrderComplete(og, code)
            self.UpdateChegeollist(index, code, name, og, oc, cc, mc, cp, ct, op, on)

            if self.dict_set['주식알림소리']:
                self.kwzservQ.put(('sound', f'{name} {oc}주를 {og}하였습니다'))
            self.kwzservQ.put(('window', (ui_num['S로그텍스트'], f'주문 관리 시스템 알림 - [{ot}] {name} | {op} | {oc} | {og}')))

        self.sreceivQ.put(('잔고목록', tuple(self.df_jg.index)))
        self.sreceivQ.put(('주문목록', self.GetOrderCodeList()))

    def UpdateTradelist(self, index, name, jg, pg, cc, sp, sg, ct):
        self.df_td.loc[index] = name, jg, pg, cc, sp, sg, ct
        self.kwzservQ.put(('window', (ui_num['S거래목록'], self.df_td[::-1])))

        df = pd.DataFrame([[name, jg, pg, cc, sp, sg, ct]], columns=columns_td, index=[index])
        self.kwzservQ.put(('query', ('거래디비', df, 's_tradelist', 'append')))

        self.UpdateTotaltradelist()

    def UpdateTotaltradelist(self, first=False):
        tdt = len(self.df_td.drop_duplicates(['종목명', '체결시간']))
        tbg = self.df_td['매수금액'].sum()
        tsg = self.df_td['매도금액'].sum()
        sig = self.df_td[self.df_td['수익금'] > 0]['수익금'].sum()
        ssg = self.df_td[self.df_td['수익금'] < 0]['수익금'].sum()
        sg  = self.df_td['수익금'].sum()
        sp  = round(sg / self.dict_intg['추정예탁자산'] * 100, 2)

        self.df_tt = pd.DataFrame([[tdt, tbg, tsg, sig, ssg, sp, sg]], columns=columns_tt, index=[self.dict_strg['당일날짜']])
        self.kwzservQ.put(('window', (ui_num['S실현손익'], self.df_tt)))

        if not first:
            self.kwzservQ.put(('tele', f'거래횟수 {tdt}회 / 총매수금액 {int(tbg):,}원 / 총매도금액 {int(tsg):,}원 / 총수익금액 {int(sig):,}원 / '
                                       f'총손실금액 {int(ssg):,}원 / 수익률 {sp:.2f}% / 수익금합계 {int(sg):,}원'))

        if self.dict_set['스톰라이브']:
            sp = round(sg / tbg * 100, 2)
            df = pd.DataFrame([[tdt, tbg, tsg, sig, ssg, sp, sg]], columns=columns_tt, index=[self.dict_strg['당일날짜']])
            self.kwzservQ.put(('live', ('주식', df)))

    def UpdateChegeollist(self, index, code, name, og, oc, cc, mc, cp, ct, op, on):
        self.dict_name[code][2] = timedelta_sec(self.dict_set['주식매수금지간격초'])
        self.df_cj.loc[index] = name, og, oc, cc, mc, cp, ct, op, on
        self.kwzservQ.put(('window', (ui_num['S체결목록'], self.df_cj[::-1])))

        df = pd.DataFrame([[name, og, oc, cc, mc, cp, ct, op, on]], columns=columns_cj, index=[index])
        self.kwzservQ.put(('query', ('거래디비', df, 's_chegeollist', 'append')))

    def UpdateTotaljango(self, inthms):
        if len(self.df_jg) > 0:
            tsg = self.df_jg['평가손익'].sum()
            tbg = self.df_jg['매입금액'].sum()
            tpg = self.df_jg['평가금액'].sum()
            bct = len(self.df_jg)
            tsp = round(tsg / tbg * 100, 2)
            ttg = self.dict_intg['예수금'] + tpg
            self.df_tj.loc[self.dict_strg['당일날짜']] = ttg, self.dict_intg['예수금'], bct, tsp, tsg, tbg, tpg
        else:
            self.df_tj.loc[self.dict_strg['당일날짜']] = self.dict_intg['예수금'], self.dict_intg['예수금'], 0, 0.0, 0, 0, 0

        tsg = self.df_jg['평가손익'].sum() + self.df_td['수익금'].sum()
        if self.dict_set['주식손실중지']:
            std = self.dict_intg['추정예탁자산'] * self.dict_set['주식손실중지수익률'] / 100
            if std < -tsg: self.StrategyStop()
        if self.dict_set['주식수익중지']:
            std = self.dict_intg['추정예탁자산'] * self.dict_set['주식수익중지수익률'] / 100
            if std < tsg: self.StrategyStop()

        if self.dict_set['주식투자금고정']:
            if inthms < self.dict_set['주식장초전략종료시간']:
                tujagm = int(self.dict_set['주식장초투자금'] * 1_000_000)
            else:
                tujagm = int(self.dict_set['주식장중투자금'] * 1_000_000)
        else:
            if inthms < self.dict_set['주식장초전략종료시간']:
                if '시장가' in self.dict_set['주식매수주문구분']:
                    tujagm = int((self.dict_intg['추정예탁자산'] - self.dict_intg['추정예탁자산'] / self.dict_set['주식장초최대매수종목수'] * 0.3) / self.dict_set['주식장초최대매수종목수'])
                else:
                    tujagm = int(self.dict_intg['추정예탁자산'] * 0.98 / self.dict_set['주식장초최대매수종목수'])
            else:
                if '시장가' in self.dict_set['주식매수주문구분']:
                    tujagm = int((self.dict_intg['추정예탁자산'] - self.dict_intg['추정예탁자산'] / self.dict_set['주식장중최대매수종목수'] * 0.3) / self.dict_set['주식장중최대매수종목수'])
                else:
                    tujagm = int(self.dict_intg['추정예탁자산'] * 0.98 / self.dict_set['주식장중최대매수종목수'])

        if self.dict_intg['종목당투자금'] != tujagm:
            self.dict_intg['종목당투자금'] = tujagm
            for q in self.sstgQs:
                q.put(('종목당투자금', self.dict_intg['종목당투자금']))

        self.kwzservQ.put(('window', (ui_num['S잔고목록'], self.df_jg)))
        self.kwzservQ.put(('window', (ui_num['S잔고평가'], self.df_tj)))

    def StrategyStop(self):
        for q in self.sstgQs:
            q.put('매수전략중지')
            # q.put('매도전략중지')
        self.JangoCheongsan('수동')

    def PutOrderComplete(self, cmsg, code):
        self.sstgQs[self.dict_sgbn[code]].put((cmsg, code))

    def OrderTimeLog(self, signal_time):
        gap = (now() - signal_time).total_seconds()
        self.kwzservQ.put(('window', (ui_num['S단순텍스트'], f'시그널 주문 시간 알림 - 발생시간과 주문시간의 차이는 [{gap:.6f}]초입니다.')))

    def GetOrderCodeList(self):
        return tuple(self.dict_buy.keys()) + tuple(self.dict_sell.keys())

    def GetMichegeolDF(self, name, gubun):
        return self.df_cj[(self.df_cj['종목명'] == name) & ((self.df_cj['주문구분'] == gubun) | (self.df_cj['주문구분'] == f'{gubun}접수') | (self.df_cj['주문구분'] == f'{gubun}정정'))]
