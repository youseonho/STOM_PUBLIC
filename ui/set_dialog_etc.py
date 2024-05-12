from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QGroupBox, QLabel, QVBoxLayout, QTabWidget, QWidget
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from ui.set_style import style_ck_bx, style_bc_dk, qfont14, style_fc_dk, qfont13
from utility.setting import columns_hj, columns_hc, columns_hg, columns_gc, columns_ns, columns_jm1, columns_jm2, \
    columns_stg1, columns_stg2, DICT_SET, columns_kp, columns_hc2


class SetDialogEtc:
    def __init__(self, ui_class, wc):
        self.ui = ui_class
        self.wc = wc
        self.set()

    def set(self):
        self.ui.dialog_factor = self.wc.setDialog('STOM FACTOR', tab=self.ui.dialog_chart)
        self.ui.dialog_factor.geometry().center()
        self.ui.jp_groupBoxxxxx_01 = QGroupBox(' ', self.ui.dialog_factor)

        checkbox_choice = [int(x) for x in DICT_SET['팩터선택'].split(';')]
        self.ui.ct_checkBoxxxxx_01 = self.wc.setCheckBox('현재가', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[0] else False, changed=self.ui.CheckboxChanged_12, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_02 = self.wc.setCheckBox('체결강도', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[1] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_03 = self.wc.setCheckBox('초당거래대금', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[2] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_04 = self.wc.setCheckBox('초당체결수량', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[3] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_05 = self.wc.setCheckBox('등락율', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[4] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_06 = self.wc.setCheckBox('고저평균등락율', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[5] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_07 = self.wc.setCheckBox('호가총잔량', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[6] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_08 = self.wc.setCheckBox('1호가잔량', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[7] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_09 = self.wc.setCheckBox('5호가잔량합', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[8] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_10 = self.wc.setCheckBox('당일거래대금', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[9] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_11 = self.wc.setCheckBox('누적초당매도수수량', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[10] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_12 = self.wc.setCheckBox('등락율각도', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[11] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_13 = self.wc.setCheckBox('당일거래대금각도', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[12] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_14 = self.wc.setCheckBox('거래대금증감', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[13] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_15 = self.wc.setCheckBox('전일비', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[14] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_16 = self.wc.setCheckBox('회전율', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[15] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_17 = self.wc.setCheckBox('전일동시간비', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[16] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_18 = self.wc.setCheckBox('전일비각도', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[17] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)

        self.ui.ct_checkBoxxxxx_19 = self.wc.setCheckBox('BBAND       tp                     nu                    nd                      ma', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[18] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_20 = self.wc.setCheckBox('MACD        fp                     sp                     sip', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[19] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_21 = self.wc.setCheckBox('APO            fp                     sp                     ma', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[20] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_22 = self.wc.setCheckBox('KAMA        tp', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[21] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_23 = self.wc.setCheckBox('RSI              tp', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[22] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_24 = self.wc.setCheckBox('HT_SINE, HT_LSINE', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[23] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_25 = self.wc.setCheckBox('HT_PHASE, HT_QUDRA', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[24] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_26 = self.wc.setCheckBox('OBV', self.ui.jp_groupBoxxxxx_01, checked=True if checkbox_choice[25] else False, changed=self.ui.CheckboxChanged_23, style=style_ck_bx)

        k = [str(x) for x in self.ui.dict_set['보조지표설정']]
        self.ui.ct_lineEdittttt_21 = self.wc.setLineedit(self.ui.jp_groupBoxxxxx_01, ltext=k[0], style=style_bc_dk)
        self.ui.ct_lineEdittttt_22 = self.wc.setLineedit(self.ui.jp_groupBoxxxxx_01, ltext=k[1], style=style_bc_dk)
        self.ui.ct_lineEdittttt_23 = self.wc.setLineedit(self.ui.jp_groupBoxxxxx_01, ltext=k[2], style=style_bc_dk)
        self.ui.ct_lineEdittttt_24 = self.wc.setLineedit(self.ui.jp_groupBoxxxxx_01, ltext=k[3], style=style_bc_dk)
        self.ui.ct_lineEdittttt_25 = self.wc.setLineedit(self.ui.jp_groupBoxxxxx_01, ltext=k[4], style=style_bc_dk)
        self.ui.ct_lineEdittttt_26 = self.wc.setLineedit(self.ui.jp_groupBoxxxxx_01, ltext=k[5], style=style_bc_dk)
        self.ui.ct_lineEdittttt_27 = self.wc.setLineedit(self.ui.jp_groupBoxxxxx_01, ltext=k[6], style=style_bc_dk)
        self.ui.ct_lineEdittttt_28 = self.wc.setLineedit(self.ui.jp_groupBoxxxxx_01, ltext=k[7], style=style_bc_dk)
        self.ui.ct_lineEdittttt_29 = self.wc.setLineedit(self.ui.jp_groupBoxxxxx_01, ltext=k[8], style=style_bc_dk)
        self.ui.ct_lineEdittttt_30 = self.wc.setLineedit(self.ui.jp_groupBoxxxxx_01, ltext=k[9], style=style_bc_dk)
        self.ui.ct_lineEdittttt_31 = self.wc.setLineedit(self.ui.jp_groupBoxxxxx_01, ltext=k[10], style=style_bc_dk)
        self.ui.ct_lineEdittttt_32 = self.wc.setLineedit(self.ui.jp_groupBoxxxxx_01, ltext=k[11], style=style_bc_dk)

        self.ui.ct_pushButtonnn_07 = self.wc.setPushbutton('보조지표설정 기본값', box=self.ui.jp_groupBoxxxxx_01, click=self.ui.ctButtonClicked_07)
        self.ui.ct_pushButtonnn_08 = self.wc.setPushbutton('보조지표설정 불러오기', box=self.ui.jp_groupBoxxxxx_01, click=self.ui.ctButtonClicked_08)
        self.ui.ct_pushButtonnn_09 = self.wc.setPushbutton('보조지표설정 저장하기', box=self.ui.jp_groupBoxxxxx_01, click=self.ui.ctButtonClicked_09)

        self.ui.factor_checkbox_list = [
            self.ui.ct_checkBoxxxxx_01, self.ui.ct_checkBoxxxxx_02, self.ui.ct_checkBoxxxxx_03, self.ui.ct_checkBoxxxxx_04,
            self.ui.ct_checkBoxxxxx_05, self.ui.ct_checkBoxxxxx_06, self.ui.ct_checkBoxxxxx_07, self.ui.ct_checkBoxxxxx_08,
            self.ui.ct_checkBoxxxxx_09, self.ui.ct_checkBoxxxxx_10, self.ui.ct_checkBoxxxxx_11, self.ui.ct_checkBoxxxxx_12,
            self.ui.ct_checkBoxxxxx_13, self.ui.ct_checkBoxxxxx_14, self.ui.ct_checkBoxxxxx_15, self.ui.ct_checkBoxxxxx_16,
            self.ui.ct_checkBoxxxxx_17, self.ui.ct_checkBoxxxxx_18,  self.ui.ct_checkBoxxxxx_19, self.ui.ct_checkBoxxxxx_20,
            self.ui.ct_checkBoxxxxx_21, self.ui.ct_checkBoxxxxx_22,  self.ui.ct_checkBoxxxxx_23, self.ui.ct_checkBoxxxxx_24,
            self.ui.ct_checkBoxxxxx_25, self.ui.ct_checkBoxxxxx_26
        ]

        self.ui.factor_linedit_list = [
            self.ui.ct_lineEdittttt_21, self.ui.ct_lineEdittttt_22, self.ui.ct_lineEdittttt_23, self.ui.ct_lineEdittttt_24,
            self.ui.ct_lineEdittttt_25, self.ui.ct_lineEdittttt_26, self.ui.ct_lineEdittttt_27, self.ui.ct_lineEdittttt_28,
            self.ui.ct_lineEdittttt_29, self.ui.ct_lineEdittttt_30, self.ui.ct_lineEdittttt_31, self.ui.ct_lineEdittttt_32
        ]

        self.ui.dialog_test = self.wc.setDialog('STOM SIMULATOR', tab=self.ui.dialog_chart)
        self.ui.dialog_test.geometry().center()

        self.ui.tt_groupBoxxxxx_01 = QGroupBox(' ', self.ui.dialog_test)
        text = '시뮬레이터는 시뮬레이터 엔진이 실행중이어하며\n' \
               '차트창 종목명과 좌측 캘린더위젯의 날짜를 기준으로 진행됩니다.\n' \
               '전략은 장중과 똑같이 설정창에서 선택한 전략이 그대로 적용됩니다.\n' \
               '먼저 시뮬레이터 엔진를 구동한 후에 완료 팝업창을 확인하고\n' \
               '시작시간(예:90000)과 종료시간(110000)을 입력 후 시작하십시오.\n' \
               '배속설정은 시뮬레이터가 진행 중이더라도 변경가능하며 즉지 반영됩니다.'
        self.ui.tt_labellllllll_01 = QLabel(text, self.ui.tt_groupBoxxxxx_01)
        self.ui.tt_pushButtonnn_01 = self.wc.setPushbutton('시뮬레이터용 엔진 구동하기', box=self.ui.tt_groupBoxxxxx_01, click=self.ui.ctButtonClicked_01)
        self.ui.tt_pushButtonnn_02 = self.wc.setPushbutton('시뮬레이터용 엔진 종료하기', box=self.ui.tt_groupBoxxxxx_01, click=self.ui.ctButtonClicked_02)
        self.ui.tt_labellllllll_02 = QLabel('시작시간', self.ui.tt_groupBoxxxxx_01)
        self.ui.tt_lineEdittttt_01 = self.wc.setLineedit(self.ui.tt_groupBoxxxxx_01, ltext='90000', style=style_bc_dk)
        self.ui.tt_labellllllll_03 = QLabel('종료시간', self.ui.tt_groupBoxxxxx_01)
        self.ui.tt_lineEdittttt_02 = self.wc.setLineedit(self.ui.tt_groupBoxxxxx_01, ltext='153000', style=style_bc_dk)
        self.ui.tt_labellllllll_04 = QLabel('배속설정', self.ui.tt_groupBoxxxxx_01)
        self.ui.tt_comboBoxxxxx_01 = self.wc.setCombobox(self.ui.tt_groupBoxxxxx_01, items=['1', '2', '4', '8', '16', '32', '64'])
        self.ui.tt_pushButtonnn_03 = self.wc.setPushbutton('시작',    box=self.ui.tt_groupBoxxxxx_01, click=self.ui.ctButtonClicked_03)
        self.ui.tt_pushButtonnn_04 = self.wc.setPushbutton('일시정지', box=self.ui.tt_groupBoxxxxx_01, click=self.ui.ctButtonClicked_04)
        self.ui.tt_pushButtonnn_05 = self.wc.setPushbutton('중지',    box=self.ui.tt_groupBoxxxxx_01, click=self.ui.ctButtonClicked_05)
        self.ui.tt_pushButtonnn_06 = self.wc.setPushbutton('취소',    box=self.ui.tt_groupBoxxxxx_01, click=self.ui.ctButtonClicked_06)

        self.ui.dialog_hoga = self.wc.setDialog('STOM HOGA')
        self.ui.dialog_hoga.geometry().center()

        self.ui.hj_tableWidgett_01 = self.wc.setTablewidget(self.ui.dialog_hoga, columns_hj, 1)
        self.ui.hc_tableWidgett_01 = self.wc.setTablewidget(self.ui.dialog_hoga, columns_hc, 12)
        self.ui.hc_tableWidgett_02 = self.wc.setTablewidget(self.ui.dialog_hoga, columns_hc2, 12, visible=False)
        self.ui.hg_tableWidgett_01 = self.wc.setTablewidget(self.ui.dialog_hoga, columns_hg, 12, clicked=self.ui.CellClicked_10)
        self.ui.hg_lineeeeeeeee_01 = self.wc.setLine(self.ui.dialog_hoga, 1)
        self.ui.hg_labellllllll_01 = QLabel('', self.ui.dialog_hoga)
        self.ui.hg_pushButtonnn_01 = self.wc.setPushbutton('이전(left)',  box=self.ui.dialog_hoga,          click=self.ui.hgButtonClicked_01, cmd='이전', shortcut='left')
        self.ui.hg_pushButtonnn_02 = self.wc.setPushbutton('다음(right)', box=self.ui.dialog_hoga,          click=self.ui.hgButtonClicked_01, cmd='다음', shortcut='right')
        self.ui.hg_pushButtonnn_03 = self.wc.setPushbutton('매수(up)',    box=self.ui.dialog_hoga, color=2, click=self.ui.hgButtonClicked_02, cmd='매수', shortcut='up')
        self.ui.hg_pushButtonnn_04 = self.wc.setPushbutton('매도(down)',  box=self.ui.dialog_hoga, color=3, click=self.ui.hgButtonClicked_02, cmd='매도', shortcut='down')

        self.ui.dialog_info = self.wc.setDialog('STOM INFO')
        self.ui.dialog_info.geometry().center()

        self.ui.gg_textEdittttt_01 = self.wc.setTextEdit(self.ui.dialog_info, font=qfont14)
        self.ui.gs_tableWidgett_01 = self.wc.setTablewidget(self.ui.dialog_info, columns_gc, 20, clicked=self.ui.CellClicked_08)
        self.ui.ns_tableWidgett_01 = self.wc.setTablewidget(self.ui.dialog_info, columns_ns, 10, clicked=self.ui.CellClicked_08)
        self.ui.jm_tableWidgett_01 = self.wc.setTablewidget(self.ui.dialog_info, columns_jm1, 13)
        self.ui.jm_tableWidgett_02 = self.wc.setTablewidget(self.ui.dialog_info, columns_jm2, 13)

        self.ui.dialog_web = self.wc.setDialog('STOM WEB')
        self.ui.dialog_web.geometry().center()

        self.ui.dialog_tree = self.wc.setDialog('STOM TREEMAP')
        self.ui.dialog_tree.geometry().center()
        fig = plt.figure('업종별 테마별 등락율', figsize=(15, 13.3))
        fig.set_facecolor('black')
        self.ui.canvas = FigureCanvas(fig)
        tree_layout = QVBoxLayout(self.ui.dialog_tree)
        tree_layout.setContentsMargins(0, 0, 0, 0)
        tree_layout.addWidget(self.ui.canvas)

        self.ui.dialog_graph = self.wc.setDialog('STOM GRAPH')
        self.ui.dialog_graph.geometry().center()
        fig = plt.figure('누적수익금', figsize=(12, 12))
        self.ui.canvas2 = FigureCanvas(fig)
        tree_layout = QVBoxLayout(self.ui.dialog_graph)
        tree_layout.setContentsMargins(0, 0, 0, 0)
        tree_layout.addWidget(self.ui.canvas2)

        self.ui.dialog_db = self.wc.setDialog('STOM DATABASE')
        self.ui.dialog_db.geometry().center()

        self.ui.sdb_tapWidgettt_01 = QTabWidget(self.ui.dialog_db)
        self.ui.sdb_tab = QWidget()
        self.ui.cdb_tab = QWidget()
        self.ui.sdb_tapWidgettt_01.addTab(self.ui.sdb_tab, '주식DB')
        self.ui.sdb_tapWidgettt_01.addTab(self.ui.cdb_tab, '코인DB')

        self.ui.stg_tapWidgettt_02 = QTabWidget(self.ui.dialog_db)
        self.ui.ssg_tab1 = QWidget()
        self.ui.ssg_tab2 = QWidget()
        self.ui.csg_tab1 = QWidget()
        self.ui.csg_tab2 = QWidget()
        self.ui.bsd_tab0 = QWidget()
        self.ui.stg_tapWidgettt_02.addTab(self.ui.ssg_tab1, '주식전략')
        self.ui.stg_tapWidgettt_02.addTab(self.ui.ssg_tab2, '주식범위')
        self.ui.stg_tapWidgettt_02.addTab(self.ui.csg_tab1, '코인전략')
        self.ui.stg_tapWidgettt_02.addTab(self.ui.csg_tab2, '코인범위')
        self.ui.stg_tapWidgettt_02.addTab(self.ui.bsd_tab0, '백스케쥴')

        self.ui.db_labellllllll_00 = QLabel('셀클릭 시 데이터 삭제', self.ui.dialog_db)

        self.ui.db_groupBoxxxxx_01 = QGroupBox('', self.ui.sdb_tab)
        self.ui.db_groupBoxxxxx_02 = QGroupBox('', self.ui.cdb_tab)

        self.ui.db_labellllllll_18 = QLabel('백테DB의 지정일자 데이터 삭제하기 (일자입력 예: 20220131)', self.ui.db_groupBoxxxxx_01)
        self.ui.db_lineEdittttt_16 = self.wc.setLineedit(self.ui.db_groupBoxxxxx_01, style=style_bc_dk)
        self.ui.db_pushButtonnn_18 = self.wc.setPushbutton('실행', box=self.ui.db_groupBoxxxxx_01, click=self.ui.dbButtonClicked_18)
        self.ui.db_labellllllll_01 = QLabel('일자DB의 지정일자 데이터 삭제하기 (일자입력)', self.ui.db_groupBoxxxxx_01)
        self.ui.db_lineEdittttt_01 = self.wc.setLineedit(self.ui.db_groupBoxxxxx_01, style=style_bc_dk)
        self.ui.db_pushButtonnn_01 = self.wc.setPushbutton('실행', box=self.ui.db_groupBoxxxxx_01, click=self.ui.dbButtonClicked_01)
        self.ui.db_labellllllll_02 = QLabel('일자DB의 지정시간이후 데이터 삭제하기 (시간입력 예: 93000)', self.ui.db_groupBoxxxxx_01)
        self.ui.db_lineEdittttt_02 = self.wc.setLineedit(self.ui.db_groupBoxxxxx_01, style=style_bc_dk)
        self.ui.db_pushButtonnn_02 = self.wc.setPushbutton('실행', box=self.ui.db_groupBoxxxxx_01, click=self.ui.dbButtonClicked_02)
        self.ui.db_labellllllll_03 = QLabel('당일DB의 지정시간이후 데이터 삭제하기 (시간입력)', self.ui.db_groupBoxxxxx_01)
        self.ui.db_lineEdittttt_03 = self.wc.setLineedit(self.ui.db_groupBoxxxxx_01, style=style_bc_dk)
        self.ui.db_pushButtonnn_03 = self.wc.setPushbutton('실행', box=self.ui.db_groupBoxxxxx_01, click=self.ui.dbButtonClicked_03)
        self.ui.db_labellllllll_04 = QLabel('당일DB의 연초개장일 및 수능일 시간 조정 (일자 입력)', self.ui.db_groupBoxxxxx_01)
        self.ui.db_lineEdittttt_04 = self.wc.setLineedit(self.ui.db_groupBoxxxxx_01, style=style_bc_dk)
        self.ui.db_pushButtonnn_04 = self.wc.setPushbutton('실행', box=self.ui.db_groupBoxxxxx_01, click=self.ui.dbButtonClicked_04)
        self.ui.db_labellllllll_05 = QLabel('일자DB로 백테DB 생성하기 (일자 입력)', self.ui.db_groupBoxxxxx_01)
        self.ui.db_lineEdittttt_05 = self.wc.setLineedit(self.ui.db_groupBoxxxxx_01, style=style_bc_dk)
        self.ui.db_lineEdittttt_06 = self.wc.setLineedit(self.ui.db_groupBoxxxxx_01, style=style_bc_dk)
        self.ui.db_pushButtonnn_05 = self.wc.setPushbutton('실행', box=self.ui.db_groupBoxxxxx_01, click=self.ui.dbButtonClicked_05)
        self.ui.db_labellllllll_06 = QLabel('백테DB에 일자DB의 데이터 추가하기', self.ui.db_groupBoxxxxx_01)
        self.ui.db_lineEdittttt_07 = self.wc.setLineedit(self.ui.db_groupBoxxxxx_01, style=style_bc_dk)
        self.ui.db_lineEdittttt_08 = self.wc.setLineedit(self.ui.db_groupBoxxxxx_01, style=style_bc_dk)
        self.ui.db_pushButtonnn_06 = self.wc.setPushbutton('실행', box=self.ui.db_groupBoxxxxx_01, click=self.ui.dbButtonClicked_06)
        self.ui.db_labellllllll_07 = QLabel('백테DB에 당일DB의 데이터 추가하기 (추가 후 콜렉터디비는 삭제됨)', self.ui.db_groupBoxxxxx_01)
        self.ui.db_pushButtonnn_07 = self.wc.setPushbutton('실행', box=self.ui.db_groupBoxxxxx_01, click=self.ui.dbButtonClicked_07)
        self.ui.db_labellllllll_08 = QLabel('당일DB를 일자DB로 분리하기', self.ui.db_groupBoxxxxx_01)
        self.ui.db_pushButtonnn_08 = self.wc.setPushbutton('실행', box=self.ui.db_groupBoxxxxx_01, click=self.ui.dbButtonClicked_08)
        self.ui.db_labellllllll_09 = QLabel('거래기록 테이블 모두 삭제 (체결목록, 잔고목록, 거래목록, 일별실현손익)', self.ui.db_groupBoxxxxx_01)
        self.ui.db_pushButtonnn_09 = self.wc.setPushbutton('실행', box=self.ui.db_groupBoxxxxx_01, click=self.ui.dbButtonClicked_09)

        self.ui.db_labellllllll_19 = QLabel('백테DB의 지정일자 데이터 삭제하기 (일자입력 예: 20220131)', self.ui.db_groupBoxxxxx_02)
        self.ui.db_lineEdittttt_17 = self.wc.setLineedit(self.ui.db_groupBoxxxxx_02, style=style_bc_dk)
        self.ui.db_pushButtonnn_19 = self.wc.setPushbutton('실행', box=self.ui.db_groupBoxxxxx_02, click=self.ui.dbButtonClicked_19)
        self.ui.db_labellllllll_10 = QLabel('일자DB의 지정일자 데이터 삭제하기 (일자입력)', self.ui.db_groupBoxxxxx_02)
        self.ui.db_lineEdittttt_09 = self.wc.setLineedit(self.ui.db_groupBoxxxxx_02, style=style_bc_dk)
        self.ui.db_pushButtonnn_10 = self.wc.setPushbutton('실행', box=self.ui.db_groupBoxxxxx_02, click=self.ui.dbButtonClicked_10)
        self.ui.db_labellllllll_11 = QLabel('일자DB의 지정시간이후 데이터 삭제하기 (시간입력 예: 93000)', self.ui.db_groupBoxxxxx_02)
        self.ui.db_lineEdittttt_10 = self.wc.setLineedit(self.ui.db_groupBoxxxxx_02, style=style_bc_dk)
        self.ui.db_pushButtonnn_11 = self.wc.setPushbutton('실행', box=self.ui.db_groupBoxxxxx_02, click=self.ui.dbButtonClicked_11)
        self.ui.db_labellllllll_12 = QLabel('당일DB의 지정시간이후 데이터 삭제하기 (시간입력)', self.ui.db_groupBoxxxxx_02)
        self.ui.db_lineEdittttt_11 = self.wc.setLineedit(self.ui.db_groupBoxxxxx_02, style=style_bc_dk)
        self.ui.db_pushButtonnn_12 = self.wc.setPushbutton('실행', box=self.ui.db_groupBoxxxxx_02, click=self.ui.dbButtonClicked_12)
        self.ui.db_labellllllll_13 = QLabel('일자DB로 백테DB 생성하기 (일자 입력)', self.ui.db_groupBoxxxxx_02)
        self.ui.db_lineEdittttt_12 = self.wc.setLineedit(self.ui.db_groupBoxxxxx_02, style=style_bc_dk)
        self.ui.db_lineEdittttt_13 = self.wc.setLineedit(self.ui.db_groupBoxxxxx_02, style=style_bc_dk)
        self.ui.db_pushButtonnn_13 = self.wc.setPushbutton('실행', box=self.ui.db_groupBoxxxxx_02, click=self.ui.dbButtonClicked_13)
        self.ui.db_labellllllll_14 = QLabel('백테DB에 일자DB의 데이터 추가하기', self.ui.db_groupBoxxxxx_02)
        self.ui.db_lineEdittttt_14 = self.wc.setLineedit(self.ui.db_groupBoxxxxx_02, style=style_bc_dk)
        self.ui.db_lineEdittttt_15 = self.wc.setLineedit(self.ui.db_groupBoxxxxx_02, style=style_bc_dk)
        self.ui.db_pushButtonnn_14 = self.wc.setPushbutton('실행', box=self.ui.db_groupBoxxxxx_02, click=self.ui.dbButtonClicked_14)
        self.ui.db_labellllllll_15 = QLabel('백테DB에 당일DB의 데이터 추가하기 (추가 후 콜렉터디비는 삭제됨)', self.ui.db_groupBoxxxxx_02)
        self.ui.db_pushButtonnn_15 = self.wc.setPushbutton('실행', box=self.ui.db_groupBoxxxxx_02, click=self.ui.dbButtonClicked_15)
        self.ui.db_labellllllll_16 = QLabel('당일DB를 일자DB로 분리하기', self.ui.db_groupBoxxxxx_02)
        self.ui.db_pushButtonnn_16 = self.wc.setPushbutton('실행', box=self.ui.db_groupBoxxxxx_02, click=self.ui.dbButtonClicked_16)
        self.ui.db_labellllllll_17 = QLabel('거래기록 테이블 모두 삭제 (체결목록, 잔고목록, 거래목록, 일별실현손익)', self.ui.db_groupBoxxxxx_02)
        self.ui.db_pushButtonnn_17 = self.wc.setPushbutton('실행', box=self.ui.db_groupBoxxxxx_02, click=self.ui.dbButtonClicked_17)

        self.ui.db_tableWidgett_01 = self.wc.setTablewidget(self.ui.ssg_tab1, columns_stg1, 8, clicked=self.ui.CellClicked_09)
        self.ui.db_tableWidgett_02 = self.wc.setTablewidget(self.ui.ssg_tab2, columns_stg2, 8, clicked=self.ui.CellClicked_09)
        self.ui.db_tableWidgett_03 = self.wc.setTablewidget(self.ui.csg_tab1, columns_stg1, 8, clicked=self.ui.CellClicked_09)
        self.ui.db_tableWidgett_04 = self.wc.setTablewidget(self.ui.csg_tab2, columns_stg2, 8, clicked=self.ui.CellClicked_09)
        self.ui.db_tableWidgett_05 = self.wc.setTablewidget(self.ui.bsd_tab0, ['백테스트 스케쥴'], 8, clicked=self.ui.CellClicked_09)
        self.ui.db_textEdittttt_01 = self.wc.setTextEdit(self.ui.dialog_db, vscroll=True)

        self.ui.dialog_order = self.wc.setDialog('STOM ORDER')
        self.ui.dialog_order.geometry().center()

        self.ui.od_groupBoxxxxx_01 = QGroupBox('', self.ui.dialog_order)
        self.ui.od_labellllllll_01 = QLabel('주문종목명', self.ui.od_groupBoxxxxx_01)
        self.ui.od_comboBoxxxxx_01 = self.wc.setCombobox(self.ui.od_groupBoxxxxx_01, activated=self.ui.Activated_03)
        self.ui.od_labellllllll_02 = QLabel('주문유형', self.ui.od_groupBoxxxxx_01)
        self.ui.od_comboBoxxxxx_02 = self.wc.setCombobox(self.ui.od_groupBoxxxxx_01, items=['지정가', '시장가', '최유리지정가', '최우선지정가', '지정가IOC', '시장가IOC', '최유리IOC', '지정가FOK', '시장가FOK', '최유리FOK'])
        self.ui.od_labellllllll_03 = QLabel('주문가격', self.ui.od_groupBoxxxxx_01)
        self.ui.od_lineEdittttt_01 = self.wc.setLineedit(self.ui.od_groupBoxxxxx_01, style=style_bc_dk, enter=self.ui.TextChanged_05)
        self.ui.od_labellllllll_04 = QLabel('주문수량', self.ui.od_groupBoxxxxx_01)
        self.ui.od_lineEdittttt_02 = self.wc.setLineedit(self.ui.od_groupBoxxxxx_01, style=style_bc_dk)
        self.ui.od_pushButtonnn_01 = self.wc.setPushbutton('매수', box=self.ui.od_groupBoxxxxx_01, color=2, click=self.ui.odButtonClicked_01)
        self.ui.od_pushButtonnn_02 = self.wc.setPushbutton('매도', box=self.ui.od_groupBoxxxxx_01, color=3, click=self.ui.odButtonClicked_02)
        self.ui.od_pushButtonnn_03 = self.wc.setPushbutton('BUY_LONG', box=self.ui.od_groupBoxxxxx_01, color=2, click=self.ui.odButtonClicked_03)
        self.ui.od_pushButtonnn_04 = self.wc.setPushbutton('SELL_LONG', box=self.ui.od_groupBoxxxxx_01, color=3, click=self.ui.odButtonClicked_04)
        self.ui.od_pushButtonnn_05 = self.wc.setPushbutton('SELL_SHORT', box=self.ui.od_groupBoxxxxx_01, color=2, click=self.ui.odButtonClicked_05)
        self.ui.od_pushButtonnn_06 = self.wc.setPushbutton('BUY_SHORT', box=self.ui.od_groupBoxxxxx_01, color=3, click=self.ui.odButtonClicked_06)
        self.ui.od_pushButtonnn_07 = self.wc.setPushbutton('매수취소', box=self.ui.od_groupBoxxxxx_01, click=self.ui.odButtonClicked_07)
        self.ui.od_pushButtonnn_08 = self.wc.setPushbutton('매도취소', box=self.ui.od_groupBoxxxxx_01, click=self.ui.odButtonClicked_08)

        self.ui.dialog_pattern = self.wc.setDialog('STOM PATTERN')
        self.ui.dialog_pattern.geometry().center()
        self.ui.pt_groupBoxxxxx_01 = QGroupBox('   패턴학습, 패턴테스트, 매매적용 안내', self.ui.dialog_pattern)
        text = '''
        패턴학습은 백테스트에 사용한 전략의 매수, 매도 시점을 기준으로
        조건구간의 틱수 동안, 인식조건을 만족했을 때, 인식구간의 팩터값에
        팩터의 계수를 곱한 다음, 소숫점은 버린 값으로 패턴 학습합니다.
        매수와 매도가 별도의 패턴으로 학습되며 매수, 매도 모두 팩터들을
        중복선택하여 멀티학습시킬 수 있습니다. 인식조건은 현재가대비등락율과
        현재가와 저가 또는 고가의 비교 중, 하나를 선택하여 설정할 수 있습니다.
        패턴학습을 완료하면 학습된 패턴데이터를 파일로 저장하고 백테엔진으로 보냅니다.
        백테엔진으로 전송된 학습데이터는 패턴테스트를 진행할 때 사용됩니다.
        이전 학습데이터를 백테엔진으로 보내려면 학습데이터전송 버튼을 누르십시오. 
        패턴 테스트의 기간은 학습에 사용되지 않은 기간을 선택해야합니다.
        일반 백테스트용 매도수 전략과 학습된 패턴을 사용하여 패턴 테스트가 진행됩니다.
        학습된 패턴데이터 파일은 전략설정에서 패턴인식을 선택하면 매매에 적용됩니다.
        '''
        self.ui.pt_labellllllll_01 = QLabel(text, self.ui.pt_groupBoxxxxx_01)
        self.ui.pt_labellllllll_01.setFont(qfont13)
        self.ui.pt_labellllllll_01.setAlignment(Qt.AlignCenter)
        self.ui.pt_comboBoxxxxx_00 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_01, activated=self.ui.pActivated_01)
        self.ui.pt_pushButtonnn_01 = self.wc.setPushbutton('불러오기', box=self.ui.pt_groupBoxxxxx_01, color=1, click=self.ui.ptButtonClicked_01)
        self.ui.pt_pushButtonnn_02 = self.wc.setPushbutton('저장하기', box=self.ui.pt_groupBoxxxxx_01, color=1, click=self.ui.ptButtonClicked_02)
        self.ui.pt_pushButtonnn_03 = self.wc.setPushbutton('학습데이터전송', box=self.ui.pt_groupBoxxxxx_01, color=1, click=self.ui.ptButtonClicked_03)

        self.ui.pt_groupBoxxxxx_04 = QGroupBox('   패턴 학습 기간, 인식 구간, 조건 구간, 인식 조건 선택', self.ui.dialog_pattern)
        text = ' 패턴 학습 기간 설정 :   시작일자                                               종료일자'
        self.ui.pt_labellllllll_00 = QLabel(text, self.ui.pt_groupBoxxxxx_04)
        if self.ui.dict_set['백테날짜고정']:
            self.ui.pt_dateEdittttt_01 = self.wc.setDateEdit(self.ui.pt_groupBoxxxxx_04, qday=QDate.fromString(self.ui.dict_set['백테날짜'], 'yyyyMMdd'))
        else:
            self.ui.pt_dateEdittttt_01 = self.wc.setDateEdit(self.ui.pt_groupBoxxxxx_04, addday=-int(self.ui.dict_set['백테날짜']))
        self.ui.pt_dateEdittttt_02 = self.wc.setDateEdit(self.ui.pt_groupBoxxxxx_04)
        text = ' 패턴 인식 구간의 틱수                                               패턴 조건 구간의 틱수'
        self.ui.pt_labellllllll_02 = QLabel(text, self.ui.pt_groupBoxxxxx_04)
        item = ['30', '60', '120',  '180', '300', '600']
        self.ui.pt_comboBoxxxxx_14 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_04, items=item)
        item = ['180', '300', '600', '900', '1200', '1800']
        self.ui.pt_comboBoxxxxx_15 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_04, items=item)
        self.ui.pt_checkBoxxxxx_14 = self.wc.setCheckBox('매수 - 현재가 대비 조건구간 고가의 등락율 >= (+)                       %', self.ui.pt_groupBoxxxxx_04, style=style_ck_bx)
        self.ui.pt_lineEdittttt_01 = self.wc.setLineedit(self.ui.pt_groupBoxxxxx_04, ltext='5', style=style_bc_dk)
        self.ui.pt_checkBoxxxxx_15 = self.wc.setCheckBox('매수 - 현재가 <= 조건구간 저가', self.ui.pt_groupBoxxxxx_04, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_34 = self.wc.setCheckBox('매도 - 현재가 대비 조건구간 저가의 등락율 <= (-)                       %', self.ui.pt_groupBoxxxxx_04, style=style_ck_bx)
        self.ui.pt_lineEdittttt_02 = self.wc.setLineedit(self.ui.pt_groupBoxxxxx_04, ltext='5', style=style_bc_dk)
        self.ui.pt_checkBoxxxxx_35 = self.wc.setCheckBox('매도 - 현재가 >= 조건구간 고가', self.ui.pt_groupBoxxxxx_04, style=style_ck_bx)

        self.ui.pt_groupBoxxxxx_02 = QGroupBox('   패턴 인식 매수 팩터 및 계수 선택', self.ui.dialog_pattern)
        self.ui.pt_checkBoxxxxx_01 = self.wc.setCheckBox('등락율', self.ui.pt_groupBoxxxxx_02, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_02 = self.wc.setCheckBox('당일거래대금', self.ui.pt_groupBoxxxxx_02, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_03 = self.wc.setCheckBox('체결강도', self.ui.pt_groupBoxxxxx_02, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_04 = self.wc.setCheckBox('초당매수금액', self.ui.pt_groupBoxxxxx_02, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_05 = self.wc.setCheckBox('초당매도금액', self.ui.pt_groupBoxxxxx_02, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_06 = self.wc.setCheckBox('순매수금액', self.ui.pt_groupBoxxxxx_02, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_07 = self.wc.setCheckBox('초당거래대금', self.ui.pt_groupBoxxxxx_02, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_08 = self.wc.setCheckBox('고저평균대비등락율', self.ui.pt_groupBoxxxxx_02, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_09 = self.wc.setCheckBox('매도1잔량금액', self.ui.pt_groupBoxxxxx_02, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_10 = self.wc.setCheckBox('매수1잔량금액', self.ui.pt_groupBoxxxxx_02, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_11 = self.wc.setCheckBox('매도총잔량금액', self.ui.pt_groupBoxxxxx_02, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_12 = self.wc.setCheckBox('매수총잔량금액', self.ui.pt_groupBoxxxxx_02, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_13 = self.wc.setCheckBox('매도수5호가총금액', self.ui.pt_groupBoxxxxx_02, style=style_ck_bx)
        item = ['1000', '100', '10',  '1', '0.1', '0.01', '0.001', '0.0001', '0.00001', '0.000001', '0.0000001', '0.00000001']
        self.ui.pt_comboBoxxxxx_01 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_02, items=item)
        self.ui.pt_comboBoxxxxx_02 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_02, items=item)
        self.ui.pt_comboBoxxxxx_03 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_02, items=item)
        self.ui.pt_comboBoxxxxx_04 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_02, items=item)
        self.ui.pt_comboBoxxxxx_05 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_02, items=item)
        self.ui.pt_comboBoxxxxx_06 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_02, items=item)
        self.ui.pt_comboBoxxxxx_07 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_02, items=item)
        self.ui.pt_comboBoxxxxx_08 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_02, items=item)
        self.ui.pt_comboBoxxxxx_09 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_02, items=item)
        self.ui.pt_comboBoxxxxx_10 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_02, items=item)
        self.ui.pt_comboBoxxxxx_11 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_02, items=item)
        self.ui.pt_comboBoxxxxx_12 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_02, items=item)
        self.ui.pt_comboBoxxxxx_13 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_02, items=item)

        self.ui.pt_groupBoxxxxx_03 = QGroupBox('   패턴 인식 매도 팩터 및 계수 선택', self.ui.dialog_pattern)
        self.ui.pt_checkBoxxxxx_21 = self.wc.setCheckBox('등락율', self.ui.pt_groupBoxxxxx_03, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_22 = self.wc.setCheckBox('당일거래대금', self.ui.pt_groupBoxxxxx_03, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_23 = self.wc.setCheckBox('체결강도', self.ui.pt_groupBoxxxxx_03, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_24 = self.wc.setCheckBox('초당매수금액', self.ui.pt_groupBoxxxxx_03, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_25 = self.wc.setCheckBox('초당매도금액', self.ui.pt_groupBoxxxxx_03, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_26 = self.wc.setCheckBox('순매수금액', self.ui.pt_groupBoxxxxx_03, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_27 = self.wc.setCheckBox('초당거래대금', self.ui.pt_groupBoxxxxx_03, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_28 = self.wc.setCheckBox('고저평균대비등락율', self.ui.pt_groupBoxxxxx_03, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_29 = self.wc.setCheckBox('매도1잔량금액', self.ui.pt_groupBoxxxxx_03, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_30 = self.wc.setCheckBox('매수1잔량금액', self.ui.pt_groupBoxxxxx_03, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_31 = self.wc.setCheckBox('매도총잔량금액', self.ui.pt_groupBoxxxxx_03, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_32 = self.wc.setCheckBox('매수총잔량금액', self.ui.pt_groupBoxxxxx_03, style=style_ck_bx)
        self.ui.pt_checkBoxxxxx_33 = self.wc.setCheckBox('매도수5호가총금액', self.ui.pt_groupBoxxxxx_03, style=style_ck_bx)
        self.ui.pt_comboBoxxxxx_21 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_03, items=item)
        self.ui.pt_comboBoxxxxx_22 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_03, items=item)
        self.ui.pt_comboBoxxxxx_23 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_03, items=item)
        self.ui.pt_comboBoxxxxx_24 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_03, items=item)
        self.ui.pt_comboBoxxxxx_25 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_03, items=item)
        self.ui.pt_comboBoxxxxx_26 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_03, items=item)
        self.ui.pt_comboBoxxxxx_27 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_03, items=item)
        self.ui.pt_comboBoxxxxx_28 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_03, items=item)
        self.ui.pt_comboBoxxxxx_29 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_03, items=item)
        self.ui.pt_comboBoxxxxx_30 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_03, items=item)
        self.ui.pt_comboBoxxxxx_31 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_03, items=item)
        self.ui.pt_comboBoxxxxx_32 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_03, items=item)
        self.ui.pt_comboBoxxxxx_33 = self.wc.setCombobox(self.ui.pt_groupBoxxxxx_03, items=item)

        self.ui.dialog_optuna = self.wc.setDialog('STOM OPTUNA')
        self.ui.dialog_optuna.geometry().center()
        self.ui.op_groupBoxxxx_01 = QGroupBox(' ', self.ui.dialog_optuna)
        text = '''
        "optuna의 범위설정은 최적화 범위
        설정과 동일합니다. 그대로 사용해도
        되지만, 일부 아는 중요한 값들은
        고정하여 사용하면 초기에 보다
        빠르게 최적값을 탐색할 수 있습니다.
        아래의 빈칸에 콤머로 구분하여
        고정할 변수의 번호를 입력하십시오."
        '''
        self.ui.op_labelllllll_01 = QLabel(text, self.ui.op_groupBoxxxx_01)
        self.ui.op_labelllllll_01.setAlignment(Qt.AlignCenter)
        self.ui.op_lineEditttt_01 = self.wc.setLineedit(self.ui.op_groupBoxxxx_01, style=style_bc_dk)
        text = '''
        "optuna은 기본적으로 범위설정에서
        입력한 간격대로 변수를 탐색합니다.
        하지만 범위설정의 간격을 무시하고
        optuna가 최소, 최대의 범위안에서
        자동으로 탐색하게 할 수 있습니다.
        원하시면 아래의 설정을 사용하십시오."
        '''
        self.ui.op_labelllllll_02 = QLabel(text, self.ui.op_groupBoxxxx_01)
        self.ui.op_labelllllll_02.setAlignment(Qt.AlignCenter)
        self.ui.op_checkBoxxxx_01 = self.wc.setCheckBox('범위간격 자동탐색 사용하기', self.ui.op_groupBoxxxx_01, checked=False, style=style_ck_bx)
        text = '''
        "optuna의 기본 최적화 알고리즘은
        베이지안서치(TPESampler)입니다.
        아래 콤보박스에서 다른 최적화
        알고리즘을 선택할 수 있습니다."
        '''
        self.ui.op_labelllllll_03 = QLabel(text, self.ui.op_groupBoxxxx_01)
        self.ui.op_labelllllll_03.setAlignment(Qt.AlignCenter)
        item_list = ['TPESampler', 'BruteForceSampler', 'CmaEsSampler', 'QMCSampler', 'RandomSampler']
        self.ui.op_comboBoxxxx_01 = self.wc.setCombobox(self.ui.op_groupBoxxxx_01, items=item_list)
        text = '''
        "optuna의 실행 횟수는 변수의
        개수만큼 실행되어도 기준값이
        변경되지 않으면 탐색을 종료하도록
        설정되어 있습니다(0입력시적용).
        설정을 무시하고 기준값 미변경 시
        중단할 횟수를 빈칸에 입력하십시오.
        20회 이하의 횟수로 최적값을 빠르게
        랜덤하게 바꿀 수도 있으며
        200회 이상의 횟수로 고강도 탐색을
        유도할 수도 있습니다."
        '''
        self.ui.op_labelllllll_04 = QLabel(text, self.ui.op_groupBoxxxx_01)
        self.ui.op_labelllllll_04.setAlignment(Qt.AlignCenter)
        self.ui.op_lineEditttt_02 = self.wc.setLineedit(self.ui.op_groupBoxxxx_01, style=style_bc_dk)
        self.ui.op_lineEditttt_02.setText('0')
        text = '''
        "optuna로 실행된 최적화의 정보는
        별도의 데이터베이스에 저장됩니다
        해당 DB의 정보를 열람하려면
        아래 버튼을 클릭하십시오."
        '''
        self.ui.op_labelllllll_05 = QLabel(text, self.ui.op_groupBoxxxx_01)
        self.ui.op_labelllllll_05.setAlignment(Qt.AlignCenter)
        self.ui.op_pushButtonn_01 = self.wc.setPushbutton('OPTUNA DASHBOARD', box=self.ui.op_groupBoxxxx_01, color=3, click=self.ui.opButtonClicked_01)

        self.ui.dialog_pass = self.wc.setDialog('STOM PASSWARD', tab=self.ui)
        self.ui.dialog_pass.geometry().center()
        self.ui.pa_groupBoxxxx_01 = QGroupBox(' ', self.ui.dialog_pass)
        self.ui.pa_labelllllll_01 = QLabel('주식 첫번째 계좌의\n비밀번호을 입력하십시오.\n계정이 없을 경우 입력X\n', self.ui.pa_groupBoxxxx_01)
        self.ui.pa_labelllllll_01.setAlignment(Qt.AlignCenter)
        self.ui.pa_lineEditttt_01 = self.wc.setLineedit(self.ui.pa_groupBoxxxx_01, enter=self.ui.ReturnPress_02, style=style_fc_dk)

        self.ui.dialog_comp = self.wc.setDialog('STOM COMPARISON', tab=self.ui)
        self.ui.dialog_comp.geometry().center()
        self.ui.cp_labelllllll_01 = QLabel('▣ 선택된 두개 이상의 그래프를 비교한다.', self.ui.dialog_comp)
        self.ui.cp_pushButtonn_01 = self.wc.setPushbutton('그래프 비교', box=self.ui.dialog_comp, click=self.ui.cpButtonClicked_01)
        self.ui.cp_tableWidget_01 = self.wc.setTablewidget(self.ui.dialog_comp, ['백테스트 상세기록'], 40, vscroll=True)

        self.ui.dialog_kimp = self.wc.setDialog('STOM KIMP')
        self.ui.dialog_kimp.geometry().center()
        self.ui.kp_tableWidget_01 = self.wc.setTablewidget(self.ui.dialog_kimp, columns_kp, 50, vscroll=True)

        self.ui.dialog_std = self.wc.setDialog('OPTIMIZ STD LIMIT', tab=self.ui)
        self.ui.dialog_std.geometry().center()
        self.ui.st_pushButtonn_01 = self.wc.setPushbutton('불러오기', box=self.ui.dialog_std, click=self.ui.stButtonClicked_01)
        self.ui.st_pushButtonn_02 = self.wc.setPushbutton('저장하기', box=self.ui.dialog_std, click=self.ui.stButtonClicked_02)
        self.ui.st_groupBoxxxx_01 = QGroupBox(' ', self.ui.dialog_std)
        self.ui.st_labelllllll_01 = QLabel('<=    최대낙폭률     <=', self.ui.st_groupBoxxxx_01)
        self.ui.st_labelllllll_02 = QLabel('<=    보유종목수     <=', self.ui.st_groupBoxxxx_01)
        self.ui.st_labelllllll_03 = QLabel('<=          승률          <=', self.ui.st_groupBoxxxx_01)
        self.ui.st_labelllllll_04 = QLabel('<=    평균수익률     <=', self.ui.st_groupBoxxxx_01)
        self.ui.st_labelllllll_05 = QLabel('<= 일평균거래횟수 <=', self.ui.st_groupBoxxxx_01)
        self.ui.st_labelllllll_06 = QLabel('<= 연간예상수익률 <=', self.ui.st_groupBoxxxx_01)
        self.ui.st_labelllllll_07 = QLabel('<=   매매성능지수   <=', self.ui.st_groupBoxxxx_01)
        self.ui.st_lineEditttt_01 = self.wc.setLineedit(self.ui.st_groupBoxxxx_01, style=style_bc_dk)
        self.ui.st_lineEditttt_02 = self.wc.setLineedit(self.ui.st_groupBoxxxx_01, style=style_bc_dk)
        self.ui.st_lineEditttt_03 = self.wc.setLineedit(self.ui.st_groupBoxxxx_01, style=style_bc_dk)
        self.ui.st_lineEditttt_04 = self.wc.setLineedit(self.ui.st_groupBoxxxx_01, style=style_bc_dk)
        self.ui.st_lineEditttt_05 = self.wc.setLineedit(self.ui.st_groupBoxxxx_01, style=style_bc_dk)
        self.ui.st_lineEditttt_06 = self.wc.setLineedit(self.ui.st_groupBoxxxx_01, style=style_bc_dk)
        self.ui.st_lineEditttt_07 = self.wc.setLineedit(self.ui.st_groupBoxxxx_01, style=style_bc_dk)
        self.ui.st_lineEditttt_08 = self.wc.setLineedit(self.ui.st_groupBoxxxx_01, style=style_bc_dk)
        self.ui.st_lineEditttt_09 = self.wc.setLineedit(self.ui.st_groupBoxxxx_01, style=style_bc_dk)
        self.ui.st_lineEditttt_10 = self.wc.setLineedit(self.ui.st_groupBoxxxx_01, style=style_bc_dk)
        self.ui.st_lineEditttt_11 = self.wc.setLineedit(self.ui.st_groupBoxxxx_01, style=style_bc_dk)
        self.ui.st_lineEditttt_12 = self.wc.setLineedit(self.ui.st_groupBoxxxx_01, style=style_bc_dk)
        self.ui.st_lineEditttt_13 = self.wc.setLineedit(self.ui.st_groupBoxxxx_01, style=style_bc_dk)
        self.ui.st_lineEditttt_14 = self.wc.setLineedit(self.ui.st_groupBoxxxx_01, style=style_bc_dk)

        self.ui.dialog_leverage = self.wc.setDialog('BINACE FUTURE LEVERAGE', tab=self.ui)
        self.ui.dialog_leverage.geometry().center()
        self.ui.lv_pushButtonn_01 = self.wc.setPushbutton('불러오기', box=self.ui.dialog_leverage, click=self.ui.lvButtonClicked_02)
        self.ui.lv_pushButtonn_02 = self.wc.setPushbutton('저장하기', box=self.ui.dialog_leverage, click=self.ui.lvButtonClicked_03)
        self.ui.lv_groupBoxxxx_01 = QGroupBox(' ', self.ui.dialog_leverage)
        self.ui.lv_checkBoxxxx_01 = self.wc.setCheckBox('고정 레버리지 (모든 종목의 레버리지 고정)', self.ui.lv_groupBoxxxx_01, style=style_ck_bx, changed=self.ui.lvCheckChanged_01)
        self.ui.lv_lineEditttt_01 = self.wc.setLineedit(self.ui.lv_groupBoxxxx_01, style=style_bc_dk)
        self.ui.lv_groupBoxxxx_02 = QGroupBox(' ', self.ui.dialog_leverage)
        self.ui.lv_checkBoxxxx_02 = self.wc.setCheckBox('변동 레버리지 (변동에 따라 레버리지 변경)        [1~125]', self.ui.lv_groupBoxxxx_02, style=style_ck_bx, changed=self.ui.lvCheckChanged_01)
        self.ui.lv_labelllllll_01 = QLabel('<= 저가대비고가등락율  <', self.ui.lv_groupBoxxxx_02)
        self.ui.lv_labelllllll_02 = QLabel('<= 저가대비고가등락율  <', self.ui.lv_groupBoxxxx_02)
        self.ui.lv_labelllllll_03 = QLabel('<= 저가대비고가등락율  <', self.ui.lv_groupBoxxxx_02)
        self.ui.lv_labelllllll_04 = QLabel('<= 저가대비고가등락율  <', self.ui.lv_groupBoxxxx_02)
        self.ui.lv_labelllllll_05 = QLabel('<= 저가대비고가등락율  <', self.ui.lv_groupBoxxxx_02)
        self.ui.lv_lineEditttt_02 = self.wc.setLineedit(self.ui.lv_groupBoxxxx_02, style=style_bc_dk)
        self.ui.lv_lineEditttt_03 = self.wc.setLineedit(self.ui.lv_groupBoxxxx_02, style=style_bc_dk)
        self.ui.lv_lineEditttt_04 = self.wc.setLineedit(self.ui.lv_groupBoxxxx_02, style=style_bc_dk)
        self.ui.lv_lineEditttt_05 = self.wc.setLineedit(self.ui.lv_groupBoxxxx_02, style=style_bc_dk)
        self.ui.lv_lineEditttt_06 = self.wc.setLineedit(self.ui.lv_groupBoxxxx_02, style=style_bc_dk)
        self.ui.lv_lineEditttt_07 = self.wc.setLineedit(self.ui.lv_groupBoxxxx_02, style=style_bc_dk)
        self.ui.lv_lineEditttt_08 = self.wc.setLineedit(self.ui.lv_groupBoxxxx_02, style=style_bc_dk)
        self.ui.lv_lineEditttt_09 = self.wc.setLineedit(self.ui.lv_groupBoxxxx_02, style=style_bc_dk)
        self.ui.lv_lineEditttt_10 = self.wc.setLineedit(self.ui.lv_groupBoxxxx_02, style=style_bc_dk)
        self.ui.lv_lineEditttt_11 = self.wc.setLineedit(self.ui.lv_groupBoxxxx_02, style=style_bc_dk)
        self.ui.lv_lineEditttt_12 = self.wc.setLineedit(self.ui.lv_groupBoxxxx_02, style=style_bc_dk)
        self.ui.lv_lineEditttt_13 = self.wc.setLineedit(self.ui.lv_groupBoxxxx_02, style=style_bc_dk)
        self.ui.lv_lineEditttt_14 = self.wc.setLineedit(self.ui.lv_groupBoxxxx_02, style=style_bc_dk)
        self.ui.lv_lineEditttt_15 = self.wc.setLineedit(self.ui.lv_groupBoxxxx_02, style=style_bc_dk)
        self.ui.lv_lineEditttt_16 = self.wc.setLineedit(self.ui.lv_groupBoxxxx_02, style=style_bc_dk)

        self.ui.lv_checkbox_listt = [self.ui.lv_checkBoxxxx_01, self.ui.lv_checkBoxxxx_02]

        self.ui.dialog_factor.setFixedSize(395, 370)
        self.ui.jp_groupBoxxxxx_01.setGeometry(5, -10, 385, 373)

        self.ui.ct_checkBoxxxxx_01.setGeometry(10, 25, 120, 20)
        self.ui.ct_checkBoxxxxx_02.setGeometry(140, 25, 120, 20)
        self.ui.ct_checkBoxxxxx_03.setGeometry(275, 25, 120, 20)
        self.ui.ct_checkBoxxxxx_04.setGeometry(10, 50, 120, 20)
        self.ui.ct_checkBoxxxxx_05.setGeometry(140, 50, 120, 20)
        self.ui.ct_checkBoxxxxx_06.setGeometry(275, 50, 120, 20)
        self.ui.ct_checkBoxxxxx_07.setGeometry(10, 75, 120, 20)
        self.ui.ct_checkBoxxxxx_08.setGeometry(140, 75, 120, 20)
        self.ui.ct_checkBoxxxxx_09.setGeometry(275, 75, 120, 20)
        self.ui.ct_checkBoxxxxx_10.setGeometry(10, 100, 120, 20)
        self.ui.ct_checkBoxxxxx_11.setGeometry(140, 100, 120, 20)
        self.ui.ct_checkBoxxxxx_12.setGeometry(275, 100, 120, 20)
        self.ui.ct_checkBoxxxxx_13.setGeometry(10, 125, 120, 20)
        self.ui.ct_checkBoxxxxx_14.setGeometry(140, 125, 120, 20)
        self.ui.ct_checkBoxxxxx_15.setGeometry(275, 125, 120, 20)
        self.ui.ct_checkBoxxxxx_16.setGeometry(10, 150, 120, 20)
        self.ui.ct_checkBoxxxxx_17.setGeometry(140, 150, 120, 20)
        self.ui.ct_checkBoxxxxx_18.setGeometry(275, 150, 120, 20)

        self.ui.ct_checkBoxxxxx_19.setGeometry(10, 175, 380, 20)
        self.ui.ct_checkBoxxxxx_20.setGeometry(10, 200, 380, 20)
        self.ui.ct_checkBoxxxxx_21.setGeometry(10, 225, 380, 20)
        self.ui.ct_checkBoxxxxx_22.setGeometry(10, 250, 380, 20)
        self.ui.ct_checkBoxxxxx_23.setGeometry(10, 275, 380, 20)
        self.ui.ct_checkBoxxxxx_24.setGeometry(10, 300, 380, 20)
        self.ui.ct_checkBoxxxxx_25.setGeometry(10, 325, 380, 20)
        self.ui.ct_checkBoxxxxx_26.setGeometry(10, 350, 380, 20)

        self.ui.ct_lineEdittttt_21.setGeometry(110, 175, 40, 20)
        self.ui.ct_lineEdittttt_22.setGeometry(190, 175, 40, 20)
        self.ui.ct_lineEdittttt_23.setGeometry(270, 175, 40, 20)
        self.ui.ct_lineEdittttt_24.setGeometry(350, 175, 30, 20)
        self.ui.ct_lineEdittttt_25.setGeometry(110, 200, 40, 20)
        self.ui.ct_lineEdittttt_26.setGeometry(190, 200, 40, 20)
        self.ui.ct_lineEdittttt_27.setGeometry(270, 200, 40, 20)
        self.ui.ct_lineEdittttt_28.setGeometry(110, 225, 40, 20)
        self.ui.ct_lineEdittttt_29.setGeometry(190, 225, 40, 20)
        self.ui.ct_lineEdittttt_30.setGeometry(270, 225, 40, 20)
        self.ui.ct_lineEdittttt_31.setGeometry(110, 250, 40, 20)
        self.ui.ct_lineEdittttt_32.setGeometry(110, 275, 40, 20)

        self.ui.ct_pushButtonnn_07.setGeometry(227, 265, 150, 30)
        self.ui.ct_pushButtonnn_08.setGeometry(227, 300, 150, 30)
        self.ui.ct_pushButtonnn_09.setGeometry(227, 335, 150, 30)

        self.ui.dialog_hoga.setFixedSize(572, 355)
        if self.ui.dict_set['창위치기억'] and self.ui.dict_set['창위치'] is not None:
            try:
                self.ui.dialog_hoga.move(self.ui.dict_set['창위치'][16], self.ui.dict_set['창위치'][17])
            except:
                pass
        self.ui.hj_tableWidgett_01.setGeometry(5, 5, 562, 42)
        self.ui.hc_tableWidgett_01.setGeometry(5, 52, 282, 297)
        self.ui.hc_tableWidgett_02.setGeometry(285, 52, 282, 297)
        self.ui.hg_tableWidgett_01.setGeometry(285, 52, 282, 297)
        self.ui.hg_lineeeeeeeee_01.setGeometry(5, 209, 842, 1)
        self.ui.hg_labellllllll_01.setGeometry(10, 354, 130, 30)
        self.ui.hg_pushButtonnn_01.setGeometry(290, 354, 130, 30)
        self.ui.hg_pushButtonnn_02.setGeometry(430, 354, 130, 30)
        self.ui.hg_pushButtonnn_03.setGeometry(570, 354, 130, 30)
        self.ui.hg_pushButtonnn_04.setGeometry(710, 354, 130, 30)

        self.ui.dialog_test.setFixedSize(395, 230)
        self.ui.tt_groupBoxxxxx_01.setGeometry(5, -10, 385, 233)
        self.ui.tt_labellllllll_01.setGeometry(10, 25, 385, 90)
        self.ui.tt_pushButtonnn_01.setGeometry(10, 120, 179, 30)
        self.ui.tt_pushButtonnn_02.setGeometry(199, 120, 179, 30)
        self.ui.tt_labellllllll_02.setGeometry(10, 160, 50, 25)
        self.ui.tt_lineEdittttt_01.setGeometry(65, 160, 60, 25)
        self.ui.tt_labellllllll_03.setGeometry(136, 160, 50, 25)
        self.ui.tt_lineEdittttt_02.setGeometry(191, 160, 60, 25)
        self.ui.tt_labellllllll_04.setGeometry(262, 160, 50, 25)
        self.ui.tt_comboBoxxxxx_01.setGeometry(317, 160, 60, 25)
        self.ui.tt_pushButtonnn_03.setGeometry(10, 195, 84, 30)
        self.ui.tt_pushButtonnn_04.setGeometry(104, 195, 85, 30)
        self.ui.tt_pushButtonnn_05.setGeometry(199, 195, 84, 30)
        self.ui.tt_pushButtonnn_06.setGeometry(293, 195, 85, 30)

        self.ui.dialog_info.setFixedSize(1403, 570)
        if self.ui.dict_set['창위치기억'] and self.ui.dict_set['창위치'] is not None:
            try:
                self.ui.dialog_info.move(self.ui.dict_set['창위치'][8], self.ui.dict_set['창위치'][9])
            except:
                pass
        self.ui.gg_textEdittttt_01.setGeometry(7, 5, 692, 90)
        self.ui.gs_tableWidgett_01.setGeometry(7, 100, 692, 463)
        self.ui.ns_tableWidgett_01.setGeometry(704, 5, 693, 233)
        self.ui.jm_tableWidgett_01.setGeometry(704, 243, 320, 320)
        self.ui.jm_tableWidgett_02.setGeometry(1024, 243, 373, 320)

        self.ui.dialog_web.setFixedSize(1403, 1370 if not DICT_SET['저해상도'] else 1010)
        if self.ui.dict_set['창위치기억'] and self.ui.dict_set['창위치'] is not None:
            try:
                self.ui.dialog_web.move(self.ui.dict_set['창위치'][10], self.ui.dict_set['창위치'][11])
            except:
                pass

        self.ui.dialog_tree.setFixedSize(1403, 1370 if not DICT_SET['저해상도'] else 1010)
        if self.ui.dict_set['창위치기억'] and self.ui.dict_set['창위치'] is not None:
            try:
                self.ui.dialog_tree.move(self.ui.dict_set['창위치'][12], self.ui.dict_set['창위치'][13])
            except:
                pass

        self.ui.dialog_graph.setFixedSize(1403, 1010)

        self.ui.dialog_db.setFixedSize(525, 670)

        self.ui.sdb_tapWidgettt_01.setGeometry(5, 5, 515, 300)
        self.ui.stg_tapWidgettt_02.setGeometry(5, 310, 515, 250)

        self.ui.db_labellllllll_00.setGeometry(355, 312, 300, 20)

        self.ui.db_groupBoxxxxx_01.setGeometry(5, 5, 500, 260)
        self.ui.db_groupBoxxxxx_02.setGeometry(5, 5, 500, 260)

        self.ui.db_labellllllll_18.setGeometry(10, 10, 320, 20)
        self.ui.db_lineEdittttt_16.setGeometry(330, 10, 80, 20)
        self.ui.db_pushButtonnn_18.setGeometry(415, 10, 80, 20)
        self.ui.db_labellllllll_01.setGeometry(10, 35, 320, 20)
        self.ui.db_lineEdittttt_01.setGeometry(330, 35, 80, 20)
        self.ui.db_pushButtonnn_01.setGeometry(415, 35, 80, 20)
        self.ui.db_labellllllll_02.setGeometry(10, 60, 320, 20)
        self.ui.db_lineEdittttt_02.setGeometry(330, 60, 80, 20)
        self.ui.db_pushButtonnn_02.setGeometry(415, 60, 80, 20)
        self.ui.db_labellllllll_03.setGeometry(10, 85, 300, 20)
        self.ui.db_lineEdittttt_03.setGeometry(330, 85, 80, 20)
        self.ui.db_pushButtonnn_03.setGeometry(415, 85, 80, 20)
        self.ui.db_labellllllll_04.setGeometry(10, 110, 300, 20)
        self.ui.db_lineEdittttt_04.setGeometry(330, 110, 80, 20)
        self.ui.db_pushButtonnn_04.setGeometry(415, 110, 80, 20)
        self.ui.db_labellllllll_05.setGeometry(10, 135, 300, 20)
        self.ui.db_lineEdittttt_05.setGeometry(245, 135, 80, 20)
        self.ui.db_lineEdittttt_06.setGeometry(330, 135, 80, 20)
        self.ui.db_pushButtonnn_05.setGeometry(415, 135, 80, 20)
        self.ui.db_labellllllll_06.setGeometry(10, 160, 300, 20)
        self.ui.db_lineEdittttt_07.setGeometry(245, 160, 80, 20)
        self.ui.db_lineEdittttt_08.setGeometry(330, 160, 80, 20)
        self.ui.db_pushButtonnn_06.setGeometry(415, 160, 80, 20)
        self.ui.db_labellllllll_07.setGeometry(10, 185, 400, 20)
        self.ui.db_pushButtonnn_07.setGeometry(415, 185, 80, 20)
        self.ui.db_labellllllll_08.setGeometry(10, 210, 400, 20)
        self.ui.db_pushButtonnn_08.setGeometry(415, 210, 80, 20)
        self.ui.db_labellllllll_09.setGeometry(10, 235, 400, 20)
        self.ui.db_pushButtonnn_09.setGeometry(415, 235, 80, 20)

        self.ui.db_labellllllll_19.setGeometry(10, 10, 320, 20)
        self.ui.db_lineEdittttt_17.setGeometry(330, 10, 80, 20)
        self.ui.db_pushButtonnn_19.setGeometry(415, 10, 80, 20)
        self.ui.db_labellllllll_10.setGeometry(10, 35, 320, 20)
        self.ui.db_lineEdittttt_09.setGeometry(330, 35, 80, 20)
        self.ui.db_pushButtonnn_10.setGeometry(415, 35, 80, 20)
        self.ui.db_labellllllll_11.setGeometry(10, 60, 320, 20)
        self.ui.db_lineEdittttt_10.setGeometry(330, 60, 80, 20)
        self.ui.db_pushButtonnn_11.setGeometry(415, 60, 80, 20)
        self.ui.db_labellllllll_12.setGeometry(10, 85, 300, 20)
        self.ui.db_lineEdittttt_11.setGeometry(330, 85, 80, 20)
        self.ui.db_pushButtonnn_12.setGeometry(415, 85, 80, 20)
        self.ui.db_labellllllll_13.setGeometry(10, 110, 300, 20)
        self.ui.db_lineEdittttt_12.setGeometry(245, 110, 80, 20)
        self.ui.db_lineEdittttt_13.setGeometry(330, 110, 80, 20)
        self.ui.db_pushButtonnn_13.setGeometry(415, 110, 80, 20)
        self.ui.db_labellllllll_14.setGeometry(10, 135, 300, 20)
        self.ui.db_lineEdittttt_14.setGeometry(245, 135, 80, 20)
        self.ui.db_lineEdittttt_15.setGeometry(330, 135, 80, 20)
        self.ui.db_pushButtonnn_14.setGeometry(415, 135, 80, 20)
        self.ui.db_labellllllll_15.setGeometry(10, 160, 400, 20)
        self.ui.db_pushButtonnn_15.setGeometry(415, 160, 80, 20)
        self.ui.db_labellllllll_16.setGeometry(10, 185, 400, 20)
        self.ui.db_pushButtonnn_16.setGeometry(415, 185, 80, 20)
        self.ui.db_labellllllll_17.setGeometry(10, 210, 400, 20)
        self.ui.db_pushButtonnn_17.setGeometry(415, 210, 80, 20)

        self.ui.db_tableWidgett_01.setGeometry(5, 5, 500, 210)
        self.ui.db_tableWidgett_02.setGeometry(5, 5, 500, 210)
        self.ui.db_tableWidgett_03.setGeometry(5, 5, 500, 210)
        self.ui.db_tableWidgett_04.setGeometry(5, 5, 500, 210)
        self.ui.db_tableWidgett_05.setGeometry(5, 5, 500, 210)
        self.ui.db_textEdittttt_01.setGeometry(5, 565, 515, 100)

        self.ui.dialog_order.setFixedSize(232, 303)
        if self.ui.dict_set['창위치기억'] and self.ui.dict_set['창위치'] is not None:
            try:
                self.ui.dialog_order.move(self.ui.dict_set['창위치'][20], self.ui.dict_set['창위치'][21])
            except:
                pass
        self.ui.od_groupBoxxxxx_01.setGeometry(5, 5, 222, 293)
        self.ui.od_labellllllll_01.setGeometry(10, 10, 100, 30)
        self.ui.od_comboBoxxxxx_01.setGeometry(115, 10, 100, 30)
        self.ui.od_labellllllll_02.setGeometry(10, 45, 100, 30)
        self.ui.od_comboBoxxxxx_02.setGeometry(115, 45, 100, 30)
        self.ui.od_labellllllll_03.setGeometry(10, 80, 100, 30)
        self.ui.od_lineEdittttt_01.setGeometry(115, 80, 100, 30)
        self.ui.od_labellllllll_04.setGeometry(10, 115, 100, 30)
        self.ui.od_lineEdittttt_02.setGeometry(115, 115, 100, 30)
        self.ui.od_pushButtonnn_01.setGeometry(10, 150, 100, 30)
        self.ui.od_pushButtonnn_02.setGeometry(115, 150, 100, 30)
        self.ui.od_pushButtonnn_03.setGeometry(10, 185, 100, 30)
        self.ui.od_pushButtonnn_04.setGeometry(115, 185, 100, 30)
        self.ui.od_pushButtonnn_05.setGeometry(10, 220, 100, 30)
        self.ui.od_pushButtonnn_06.setGeometry(115, 220, 100, 30)
        self.ui.od_pushButtonnn_07.setGeometry(10, 255, 100, 30)
        self.ui.od_pushButtonnn_08.setGeometry(115, 255, 100, 30)

        self.ui.dialog_pattern.setFixedSize(495, 765)
        if self.ui.dict_set['창위치기억'] and self.ui.dict_set['창위치'] is not None:
            try:
                self.ui.dialog_pattern.move(self.ui.dict_set['창위치'][22], self.ui.dict_set['창위치'][23])
            except:
                pass
        self.ui.pt_groupBoxxxxx_01.setGeometry(5, 10, 485, 240)
        self.ui.pt_labellllllll_01.setGeometry(-15, 13, 490, 200)
        self.ui.pt_comboBoxxxxx_00.setGeometry(5, 210, 130, 25)
        self.ui.pt_pushButtonnn_01.setGeometry(140, 210, 110, 25)
        self.ui.pt_pushButtonnn_02.setGeometry(255, 210, 110, 25)
        self.ui.pt_pushButtonnn_03.setGeometry(370, 210, 110, 25)

        self.ui.pt_groupBoxxxxx_04.setGeometry(5, 255, 485, 150)
        self.ui.pt_labellllllll_00.setGeometry(5, 25, 475, 20)
        self.ui.pt_dateEdittttt_01.setGeometry(170, 25, 120, 20)
        self.ui.pt_dateEdittttt_02.setGeometry(360, 25, 120, 20)
        self.ui.pt_labellllllll_02.setGeometry(5, 50, 475, 20)
        self.ui.pt_comboBoxxxxx_14.setGeometry(135, 50, 100, 20)
        self.ui.pt_comboBoxxxxx_15.setGeometry(380, 50, 100, 20)
        self.ui.pt_checkBoxxxxx_14.setGeometry(5, 75, 400, 20)
        self.ui.pt_lineEdittttt_01.setGeometry(285, 75, 50, 20)
        self.ui.pt_checkBoxxxxx_34.setGeometry(5, 100, 400, 20)
        self.ui.pt_lineEdittttt_02.setGeometry(285, 100, 50, 20)
        self.ui.pt_checkBoxxxxx_15.setGeometry(5, 125, 235, 20)
        self.ui.pt_checkBoxxxxx_35.setGeometry(245, 125, 235, 20)

        self.ui.pt_groupBoxxxxx_02.setGeometry(5, 410, 240, 350)
        self.ui.pt_checkBoxxxxx_01.setGeometry(5, 25, 120, 20)
        self.ui.pt_checkBoxxxxx_02.setGeometry(5, 50, 120, 20)
        self.ui.pt_checkBoxxxxx_03.setGeometry(5, 75, 120, 20)
        self.ui.pt_checkBoxxxxx_04.setGeometry(5, 100, 120, 20)
        self.ui.pt_checkBoxxxxx_05.setGeometry(5, 125, 120, 20)
        self.ui.pt_checkBoxxxxx_06.setGeometry(5, 150, 120, 20)
        self.ui.pt_checkBoxxxxx_07.setGeometry(5, 175, 120, 20)
        self.ui.pt_checkBoxxxxx_08.setGeometry(5, 200, 120, 20)
        self.ui.pt_checkBoxxxxx_09.setGeometry(5, 225, 120, 20)
        self.ui.pt_checkBoxxxxx_10.setGeometry(5, 250, 120, 20)
        self.ui.pt_checkBoxxxxx_11.setGeometry(5, 275, 120, 20)
        self.ui.pt_checkBoxxxxx_12.setGeometry(5, 300, 120, 20)
        self.ui.pt_checkBoxxxxx_13.setGeometry(5, 325, 120, 20)
        self.ui.pt_comboBoxxxxx_01.setGeometry(135, 25, 100, 20)
        self.ui.pt_comboBoxxxxx_02.setGeometry(135, 50, 100, 20)
        self.ui.pt_comboBoxxxxx_03.setGeometry(135, 75, 100, 20)
        self.ui.pt_comboBoxxxxx_04.setGeometry(135, 100, 100, 20)
        self.ui.pt_comboBoxxxxx_05.setGeometry(135, 125, 100, 20)
        self.ui.pt_comboBoxxxxx_06.setGeometry(135, 150, 100, 20)
        self.ui.pt_comboBoxxxxx_07.setGeometry(135, 175, 100, 20)
        self.ui.pt_comboBoxxxxx_08.setGeometry(135, 200, 100, 20)
        self.ui.pt_comboBoxxxxx_09.setGeometry(135, 225, 100, 20)
        self.ui.pt_comboBoxxxxx_10.setGeometry(135, 250, 100, 20)
        self.ui.pt_comboBoxxxxx_11.setGeometry(135, 275, 100, 20)
        self.ui.pt_comboBoxxxxx_12.setGeometry(135, 300, 100, 20)
        self.ui.pt_comboBoxxxxx_13.setGeometry(135, 325, 100, 20)

        self.ui.pt_groupBoxxxxx_03.setGeometry(250, 410, 240, 350)
        self.ui.pt_checkBoxxxxx_21.setGeometry(5, 25, 120, 20)
        self.ui.pt_checkBoxxxxx_22.setGeometry(5, 50, 120, 20)
        self.ui.pt_checkBoxxxxx_23.setGeometry(5, 75, 120, 20)
        self.ui.pt_checkBoxxxxx_24.setGeometry(5, 100, 120, 20)
        self.ui.pt_checkBoxxxxx_25.setGeometry(5, 125, 120, 20)
        self.ui.pt_checkBoxxxxx_26.setGeometry(5, 150, 120, 20)
        self.ui.pt_checkBoxxxxx_27.setGeometry(5, 175, 120, 20)
        self.ui.pt_checkBoxxxxx_28.setGeometry(5, 200, 120, 20)
        self.ui.pt_checkBoxxxxx_29.setGeometry(5, 225, 120, 20)
        self.ui.pt_checkBoxxxxx_30.setGeometry(5, 250, 120, 20)
        self.ui.pt_checkBoxxxxx_31.setGeometry(5, 275, 120, 20)
        self.ui.pt_checkBoxxxxx_32.setGeometry(5, 300, 120, 20)
        self.ui.pt_checkBoxxxxx_33.setGeometry(5, 325, 120, 20)
        self.ui.pt_comboBoxxxxx_21.setGeometry(135, 25, 100, 20)
        self.ui.pt_comboBoxxxxx_22.setGeometry(135, 50, 100, 20)
        self.ui.pt_comboBoxxxxx_23.setGeometry(135, 75, 100, 20)
        self.ui.pt_comboBoxxxxx_24.setGeometry(135, 100, 100, 20)
        self.ui.pt_comboBoxxxxx_25.setGeometry(135, 125, 100, 20)
        self.ui.pt_comboBoxxxxx_26.setGeometry(135, 150, 100, 20)
        self.ui.pt_comboBoxxxxx_27.setGeometry(135, 175, 100, 20)
        self.ui.pt_comboBoxxxxx_28.setGeometry(135, 200, 100, 20)
        self.ui.pt_comboBoxxxxx_29.setGeometry(135, 225, 100, 20)
        self.ui.pt_comboBoxxxxx_30.setGeometry(135, 250, 100, 20)
        self.ui.pt_comboBoxxxxx_31.setGeometry(135, 275, 100, 20)
        self.ui.pt_comboBoxxxxx_32.setGeometry(135, 300, 100, 20)
        self.ui.pt_comboBoxxxxx_33.setGeometry(135, 325, 100, 20)

        self.ui.dialog_optuna.setFixedSize(220, 670)
        self.ui.op_groupBoxxxx_01.setGeometry(5, -10, 210, 675)
        self.ui.op_labelllllll_01.setGeometry(-10, 10, 210, 130)
        self.ui.op_lineEditttt_01.setGeometry(10, 132, 190, 30)
        self.ui.op_labelllllll_02.setGeometry(-10, 160, 210, 100)
        self.ui.op_checkBoxxxx_01.setGeometry(25, 265, 190, 20)
        self.ui.op_labelllllll_03.setGeometry(-10, 277, 210, 70)
        self.ui.op_comboBoxxxx_01.setGeometry(10, 355, 190, 30)
        self.ui.op_labelllllll_04.setGeometry(-10, 382, 210, 155)
        self.ui.op_lineEditttt_02.setGeometry(10, 537, 190, 30)
        self.ui.op_labelllllll_05.setGeometry(-10, 560, 200, 70)
        self.ui.op_pushButtonn_01.setGeometry(10, 637, 190, 30)

        self.ui.dialog_pass.setFixedSize(200, 100)
        self.ui.pa_groupBoxxxx_01.setGeometry(5, -10, 190, 105)
        self.ui.pa_labelllllll_01.setGeometry(5, 25, 190, 60)
        self.ui.pa_lineEditttt_01.setGeometry(50, 75, 100, 25)

        self.ui.dialog_comp.setFixedSize(350, 763)
        self.ui.cp_labelllllll_01.setGeometry(10, 10, 220, 25)
        self.ui.cp_pushButtonn_01.setGeometry(240, 10, 103, 25)
        self.ui.cp_tableWidget_01.setGeometry(5, 40, 340, 718)

        self.ui.dialog_kimp.setFixedSize(535, 763)
        if self.ui.dict_set['창위치기억'] and self.ui.dict_set['창위치'] is not None:
            try:
                self.ui.dialog_kimp.move(self.ui.dict_set['창위치'][14], self.ui.dict_set['창위치'][15])
            except:
                pass
        self.ui.kp_tableWidget_01.setGeometry(5, 5, 525, 753)

        self.ui.dialog_std.setFixedSize(255, 260)
        self.ui.st_pushButtonn_01.setGeometry(5, 5, 120, 25)
        self.ui.st_pushButtonn_02.setGeometry(130, 5, 120, 25)
        self.ui.st_groupBoxxxx_01.setGeometry(5, 20, 245, 235)
        self.ui.st_labelllllll_01.setGeometry(68, 25, 120, 25)
        self.ui.st_labelllllll_02.setGeometry(68, 55, 120, 25)
        self.ui.st_labelllllll_03.setGeometry(68, 85, 120, 25)
        self.ui.st_labelllllll_04.setGeometry(68, 115, 120, 25)
        self.ui.st_labelllllll_05.setGeometry(68, 145, 120, 25)
        self.ui.st_labelllllll_06.setGeometry(68, 175, 120, 25)
        self.ui.st_labelllllll_07.setGeometry(68, 205, 120, 25)
        self.ui.st_lineEditttt_01.setGeometry(10, 25, 50, 25)
        self.ui.st_lineEditttt_02.setGeometry(187, 25, 50, 25)
        self.ui.st_lineEditttt_03.setGeometry(10, 55, 50, 25)
        self.ui.st_lineEditttt_04.setGeometry(187, 55, 50, 25)
        self.ui.st_lineEditttt_05.setGeometry(10, 85, 50, 25)
        self.ui.st_lineEditttt_06.setGeometry(187, 85, 50, 25)
        self.ui.st_lineEditttt_07.setGeometry(10, 115, 50, 25)
        self.ui.st_lineEditttt_08.setGeometry(187, 115, 50, 25)
        self.ui.st_lineEditttt_09.setGeometry(10, 145, 50, 25)
        self.ui.st_lineEditttt_10.setGeometry(187, 145, 50, 25)
        self.ui.st_lineEditttt_11.setGeometry(10, 175, 50, 25)
        self.ui.st_lineEditttt_12.setGeometry(187, 175, 50, 25)
        self.ui.st_lineEditttt_13.setGeometry(10, 205, 50, 25)
        self.ui.st_lineEditttt_14.setGeometry(187, 205, 50, 25)

        self.ui.dialog_leverage.setFixedSize(330, 280)
        self.ui.lv_pushButtonn_01.setGeometry(5, 5, 157, 30)
        self.ui.lv_pushButtonn_02.setGeometry(167, 5, 157, 30)
        self.ui.lv_groupBoxxxx_01.setGeometry(5, 25, 320, 57)
        self.ui.lv_checkBoxxxx_01.setGeometry(10, 25, 300, 25)
        self.ui.lv_lineEditttt_01.setGeometry(263, 25, 50, 25)
        self.ui.lv_groupBoxxxx_02.setGeometry(5, 70, 320, 205)
        self.ui.lv_checkBoxxxx_02.setGeometry(10, 25, 300, 25)
        self.ui.lv_labelllllll_01.setGeometry(65, 55, 140, 25)
        self.ui.lv_labelllllll_02.setGeometry(65, 85, 140, 25)
        self.ui.lv_labelllllll_03.setGeometry(65, 115, 140, 25)
        self.ui.lv_labelllllll_04.setGeometry(65, 145, 140, 25)
        self.ui.lv_labelllllll_05.setGeometry(65, 175, 140, 25)
        self.ui.lv_lineEditttt_02.setGeometry(10, 55, 50, 25)
        self.ui.lv_lineEditttt_03.setGeometry(205, 55, 50, 25)
        self.ui.lv_lineEditttt_04.setGeometry(263, 55, 50, 25)
        self.ui.lv_lineEditttt_05.setGeometry(10, 85, 50, 25)
        self.ui.lv_lineEditttt_06.setGeometry(205, 85, 50, 25)
        self.ui.lv_lineEditttt_07.setGeometry(263, 85, 50, 25)
        self.ui.lv_lineEditttt_08.setGeometry(10, 115, 50, 25)
        self.ui.lv_lineEditttt_09.setGeometry(205, 115, 50, 25)
        self.ui.lv_lineEditttt_10.setGeometry(263, 115, 50, 25)
        self.ui.lv_lineEditttt_11.setGeometry(10, 145, 50, 25)
        self.ui.lv_lineEditttt_12.setGeometry(205, 145, 50, 25)
        self.ui.lv_lineEditttt_13.setGeometry(263, 145, 50, 25)
        self.ui.lv_lineEditttt_14.setGeometry(10, 175, 50, 25)
        self.ui.lv_lineEditttt_15.setGeometry(205, 175, 50, 25)
        self.ui.lv_lineEditttt_16.setGeometry(263, 175, 50, 25)
