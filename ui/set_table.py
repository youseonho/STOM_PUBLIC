from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QCalendarWidget, QTabWidget
from utility.setting import columns_tt, columns_td, columns_tj, columns_jg, columns_gj, columns_cj, columns_dt, \
    columns_dd, columns_nt, columns_nd, columns_sb, columns_sd


class SetTable:
    def __init__(self, ui_class, wc):
        self.ui = ui_class
        self.wc = wc
        self.set()

    def set(self):
        self.ui.stt_tableWidgettt = self.wc.setTablewidget(self.ui.st_tab, columns_tt, 1)
        self.ui.std_tableWidgettt = self.wc.setTablewidget(self.ui.st_tab, columns_td, 13, clicked=self.ui.CellClicked_01)
        self.ui.stj_tableWidgettt = self.wc.setTablewidget(self.ui.st_tab, columns_tj, 1)
        self.ui.sjg_tableWidgettt = self.wc.setTablewidget(self.ui.st_tab, columns_jg, 13, clicked=self.ui.CellClicked_02)
        self.ui.sgj_tableWidgettt = self.wc.setTablewidget(self.ui.st_tab, columns_gj, 15, clicked=self.ui.CellClicked_01)
        self.ui.scj_tableWidgettt = self.wc.setTablewidget(self.ui.st_tab, columns_cj, 15, clicked=self.ui.CellClicked_01)

        self.ui.stock_basic_listt = [
            self.ui.stt_tableWidgettt, self.ui.std_tableWidgettt, self.ui.stj_tableWidgettt,
            self.ui.sjg_tableWidgettt, self.ui.sgj_tableWidgettt, self.ui.scj_tableWidgettt,
        ]

        self.ui.s_calendarWidgett = QCalendarWidget(self.ui.st_tab)
        todayDate = QDate.currentDate()
        self.ui.s_calendarWidgett.setCurrentPage(todayDate.year(), todayDate.month())
        # noinspection PyUnresolvedReferences
        self.ui.s_calendarWidgett.clicked.connect(lambda: self.ui.CalendarClicked('S'))
        self.ui.sdt_tableWidgettt = self.wc.setTablewidget(self.ui.st_tab, columns_dt, 1)
        self.ui.sds_tableWidgettt = self.wc.setTablewidget(self.ui.st_tab, columns_dd, 19, clicked=self.ui.CellClicked_04)

        self.ui.snt_pushButton_01 = self.wc.setPushbutton('일별집계', box=self.ui.st_tab, click=self.ui.ttButtonClicked_01, cmd='S일별집계')
        self.ui.snt_pushButton_02 = self.wc.setPushbutton('월별집계', box=self.ui.st_tab, click=self.ui.ttButtonClicked_01, cmd='S월별집계')
        self.ui.snt_pushButton_03 = self.wc.setPushbutton('연도별집계', box=self.ui.st_tab, click=self.ui.ttButtonClicked_01, cmd='S연도별집계')
        self.ui.snt_tableWidgettt = self.wc.setTablewidget(self.ui.st_tab, columns_nt, 1, clicked=self.ui.CellClicked_11)
        self.ui.sns_tableWidgettt = self.wc.setTablewidget(self.ui.st_tab, columns_nd, 28, clicked=self.ui.CellClicked_05)

        self.ui.stock_total_listt = [
            self.ui.s_calendarWidgett, self.ui.sdt_tableWidgettt, self.ui.sds_tableWidgettt, self.ui.snt_pushButton_01,
            self.ui.snt_pushButton_02, self.ui.snt_pushButton_03, self.ui.snt_tableWidgettt, self.ui.sns_tableWidgettt
        ]

        for widget in self.ui.stock_total_listt:
            widget.setVisible(False)

        self.ui.slv_tapWidgett_01 = QTabWidget(self.ui.lv_tab)
        self.ui.slv_index1 = self.ui.slv_tapWidgett_01.addTab(self.ui.slv_tab, '주식 라이브')
        self.ui.slv_index2 = self.ui.slv_tapWidgett_01.addTab(self.ui.clv_tab, '코인 라이브')
        self.ui.slv_index3 = self.ui.slv_tapWidgett_01.addTab(self.ui.blv_tab, '백테 라이브')

        self.ui.slsd_tableWidgett = self.wc.setTablewidget(self.ui.slv_tab, columns_tt, 30)
        self.ui.slsn_tableWidgett = self.wc.setTablewidget(self.ui.slv_tab, columns_nt, 1)
        self.ui.slst_tableWidgett = self.wc.setTablewidget(self.ui.slv_tab, columns_nd, 28)

        self.ui.slcd_tableWidgett = self.wc.setTablewidget(self.ui.clv_tab, columns_tt, 30)
        self.ui.slcn_tableWidgett = self.wc.setTablewidget(self.ui.clv_tab, columns_nt, 1)
        self.ui.slct_tableWidgett = self.wc.setTablewidget(self.ui.clv_tab, columns_nd, 28)

        self.ui.slbd_tableWidgett = self.wc.setTablewidget(self.ui.blv_tab, columns_sb, 3)
        self.ui.slbt_tableWidgett = self.wc.setTablewidget(self.ui.blv_tab, columns_sd, 26, vscroll=True)

        # =============================================================================================================

        self.ui.ctt_tableWidgettt = self.wc.setTablewidget(self.ui.ct_tab, columns_tt, 1)
        self.ui.ctd_tableWidgettt = self.wc.setTablewidget(self.ui.ct_tab, columns_td, 13, clicked=self.ui.CellClicked_01)
        self.ui.ctj_tableWidgettt = self.wc.setTablewidget(self.ui.ct_tab, columns_tj, 1)
        self.ui.cjg_tableWidgettt = self.wc.setTablewidget(self.ui.ct_tab, columns_jg, 13, clicked=self.ui.CellClicked_03)
        self.ui.cgj_tableWidgettt = self.wc.setTablewidget(self.ui.ct_tab, columns_gj, 15, clicked=self.ui.CellClicked_01)
        self.ui.ccj_tableWidgettt = self.wc.setTablewidget(self.ui.ct_tab, columns_cj, 15, clicked=self.ui.CellClicked_01)

        self.ui.coin_basic_listtt = [
            self.ui.ctt_tableWidgettt, self.ui.ctd_tableWidgettt, self.ui.ctj_tableWidgettt,
            self.ui.cjg_tableWidgettt, self.ui.cgj_tableWidgettt, self.ui.ccj_tableWidgettt,
        ]

        self.ui.c_calendarWidgett = QCalendarWidget(self.ui.ct_tab)
        self.ui.c_calendarWidgett.setCurrentPage(todayDate.year(), todayDate.month())
        # noinspection PyUnresolvedReferences
        self.ui.c_calendarWidgett.clicked.connect(lambda: self.ui.CalendarClicked('C'))
        self.ui.cdt_tableWidgettt = self.wc.setTablewidget(self.ui.ct_tab, columns_dt, 1)
        self.ui.cds_tableWidgettt = self.wc.setTablewidget(self.ui.ct_tab, columns_dd, 19, clicked=self.ui.CellClicked_04)

        self.ui.cnt_pushButton_01 = self.wc.setPushbutton('일별집계', box=self.ui.ct_tab, click=self.ui.ttButtonClicked_01, cmd='C일별집계')
        self.ui.cnt_pushButton_02 = self.wc.setPushbutton('월별집계', box=self.ui.ct_tab, click=self.ui.ttButtonClicked_01, cmd='C월별집계')
        self.ui.cnt_pushButton_03 = self.wc.setPushbutton('연도별집계', box=self.ui.ct_tab, click=self.ui.ttButtonClicked_01, cmd='C연도별집계')
        self.ui.cnt_tableWidgettt = self.wc.setTablewidget(self.ui.ct_tab, columns_nt, 1, clicked=self.ui.CellClicked_11)
        self.ui.cns_tableWidgettt = self.wc.setTablewidget(self.ui.ct_tab, columns_nd, 28, clicked=self.ui.CellClicked_05)

        self.ui.coin_total_listtt = [
            self.ui.c_calendarWidgett, self.ui.cdt_tableWidgettt, self.ui.cds_tableWidgettt, self.ui.cnt_pushButton_01,
            self.ui.cnt_pushButton_02, self.ui.cnt_pushButton_03, self.ui.cnt_tableWidgettt, self.ui.cns_tableWidgettt
        ]

        for widget in self.ui.coin_total_listtt:
            widget.setVisible(False)

        self.ui.stt_tableWidgettt.setGeometry(7, 10, 668, 42)
        self.ui.std_tableWidgettt.setGeometry(7, 57, 668, 320)
        self.ui.stj_tableWidgettt.setGeometry(7, 382, 668, 42)
        self.ui.sjg_tableWidgettt.setGeometry(7, 429, 668, 320)
        self.ui.sgj_tableWidgettt.setGeometry(680, 10, 668, 367)
        self.ui.scj_tableWidgettt.setGeometry(680, 382, 668, 367)

        self.ui.s_calendarWidgett.setGeometry(7, 10, 668, 245)
        self.ui.sdt_tableWidgettt.setGeometry(7, 260, 668, 42)
        self.ui.sds_tableWidgettt.setGeometry(7, 307, 668, 442)

        self.ui.snt_pushButton_01.setGeometry(680, 10, 219, 30)
        self.ui.snt_pushButton_02.setGeometry(904, 10, 219, 30)
        self.ui.snt_pushButton_03.setGeometry(1128, 10, 220, 30)
        self.ui.snt_tableWidgettt.setGeometry(680, 45, 668, 42)
        self.ui.sns_tableWidgettt.setGeometry(680, 92, 668, 657)

        self.ui.slv_tapWidgett_01.setGeometry(7, 10, 1341, 740)

        self.ui.slsd_tableWidgett.setGeometry(5, 5, 663, 702)
        self.ui.slsn_tableWidgett.setGeometry(672, 5, 662, 42)
        self.ui.slst_tableWidgett.setGeometry(672, 52, 662, 655)

        self.ui.slcd_tableWidgett.setGeometry(5, 5, 663, 702)
        self.ui.slcn_tableWidgett.setGeometry(672, 5, 662, 42)
        self.ui.slct_tableWidgett.setGeometry(672, 52, 662, 655)

        self.ui.slbd_tableWidgett.setGeometry(5, 5, 1328, 89)
        self.ui.slbt_tableWidgett.setGeometry(5, 100, 1328, 607)

        self.ui.ctt_tableWidgettt.setGeometry(7, 10, 668, 42)
        self.ui.ctd_tableWidgettt.setGeometry(7, 57, 668, 320)
        self.ui.ctj_tableWidgettt.setGeometry(7, 382, 668, 42)
        self.ui.cjg_tableWidgettt.setGeometry(7, 429, 668, 320)
        self.ui.cgj_tableWidgettt.setGeometry(680, 10, 668, 367)
        self.ui.ccj_tableWidgettt.setGeometry(680, 382, 668, 367)

        self.ui.c_calendarWidgett.setGeometry(7, 10, 668, 245)
        self.ui.cdt_tableWidgettt.setGeometry(7, 230, 668, 42)
        self.ui.cds_tableWidgettt.setGeometry(7, 307, 668, 442)

        self.ui.cnt_pushButton_01.setGeometry(680, 10, 219, 30)
        self.ui.cnt_pushButton_02.setGeometry(904, 10, 219, 30)
        self.ui.cnt_pushButton_03.setGeometry(1128, 10, 220, 30)
        self.ui.cnt_tableWidgettt.setGeometry(680, 45, 668, 42)
        self.ui.cns_tableWidgettt.setGeometry(680, 92, 668, 657)
