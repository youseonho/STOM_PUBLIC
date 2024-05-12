import pyqtgraph as pg
from PyQt5.QtWidgets import QGroupBox, QLabel, QVBoxLayout
from ui.set_style import style_bc_dk, style_ck_bx, color_bg_bk
from utility.setting import DICT_SET


class SetDialogChart:
    def __init__(self, ui_class, wc):
        self.ui = ui_class
        self.wc = wc
        self.set()

    def set(self):
        self.ui.dialog_chart = self.wc.setDialog('STOM CHART')
        self.ui.dialog_chart.geometry().center()
        self.ui.ct_groupBoxxxxx_01 = QGroupBox(' ', self.ui.dialog_chart)
        self.ui.ct_groupBoxxxxx_02 = QGroupBox(' ', self.ui.dialog_chart)

        self.ui.ct_dateEdittttt_01 = self.wc.setDateEdit(self.ui.ct_groupBoxxxxx_01)
        self.ui.ct_labellllllll_01 = QLabel('시작시간', self.ui.ct_groupBoxxxxx_01)
        self.ui.ct_lineEdittttt_01 = self.wc.setLineedit(self.ui.ct_groupBoxxxxx_01, style=style_bc_dk)
        self.ui.ct_labellllllll_02 = QLabel('종료시간', self.ui.ct_groupBoxxxxx_01)
        self.ui.ct_lineEdittttt_02 = self.wc.setLineedit(self.ui.ct_groupBoxxxxx_01, style=style_bc_dk)
        self.ui.ct_labellllllll_03 = QLabel('평균틱수', self.ui.ct_groupBoxxxxx_01)
        self.ui.ct_lineEdittttt_03 = self.wc.setLineedit(self.ui.ct_groupBoxxxxx_01, ltext='30', style=style_bc_dk)
        self.ui.ct_labellllllll_04 = QLabel('종목코드', self.ui.ct_groupBoxxxxx_01)
        self.ui.ct_lineEdittttt_04 = self.wc.setLineedit(self.ui.ct_groupBoxxxxx_01, enter=self.ui.ReturnPress_01, style=style_bc_dk)
        self.ui.ct_labellllllll_05 = QLabel('종목명', self.ui.ct_groupBoxxxxx_01)
        self.ui.ct_lineEdittttt_05 = self.wc.setLineedit(self.ui.ct_groupBoxxxxx_01, enter=self.ui.ReturnPress_01, style=style_bc_dk)
        self.ui.ct_pushButtonnn_01 = self.wc.setPushbutton('검색하기', box=self.ui.ct_groupBoxxxxx_01, click=self.ui.ReturnPress_01)
        self.ui.ct_checkBoxxxxx_31 = self.wc.setCheckBox('십자선', self.ui.ct_groupBoxxxxx_01, checked=True, style=style_ck_bx)
        self.ui.ct_checkBoxxxxx_32 = self.wc.setCheckBox('정보창', self.ui.ct_groupBoxxxxx_01, checked=True, style=style_ck_bx)
        self.ui.ct_pushButtonnn_02 = self.wc.setPushbutton('펙터설정', box=self.ui.ct_groupBoxxxxx_01, click=self.ui.ShowDialogFactor)
        text = '1. 시작시간과 종료시간을 설정하면 해당시간의 데이터만 표시됩니다.\n' \
               '2. 평균틱수를 설정하면 평균, 최고, 최저값의 기준이 설정한 값으로 변경됩니다.\n' \
               '3. 날짜선택 후 종목코드 및 종목명으로 차트를 검색할 수 있습니다.\n' \
               '4. 팩터설정 버튼 클릭 후 8개의 차트에 표시할 팩터를 선택할 수 있습니다.\n' \
               '5. 시뮬레이터로 장중과 동일하게 차트 및 호가창, 전략을 복기할 수 있습니다.\n' \
               '6. 확장 버튼 클릭 시 설정한 날짜의 거래대금순위 종목의 리스트가 표시됩니다.\n' \
               '7. 확장 버튼은 최초 클릭 시 주식, 다시 클릭 시 코인으로 변경됩니다.\n' \
               '8. 확장 버튼 클릭 후 표시된 테이블에서 종목명 클릭 시 차트가 표시됩니다.\n' \
               '9. 차트에서 마우스 드레그로 영역을 선택하면 줌인됩니다.\n' \
               '10. 줌인된 상태에서 마우스 우클릭시 줌아웃됩니다.\n' \
               '11. 호가창이 열린 상태에서 마우스 좌클릭 시 해당 시간의 호가정보가 표시됩니다.\n' \
               '12. 키움 HTS에 멀티차트와도 연동됩니다. 단, 좌측 일봉, 우측 분봉 상태여야합니다.'
        self.ui.ct_pushButtonnn_03 = self.wc.setPushbutton('도움말', box=self.ui.ct_groupBoxxxxx_01, tip=text)
        self.ui.ct_pushButtonnn_04 = self.wc.setPushbutton('CHART 8', box=self.ui.ct_groupBoxxxxx_01, click=self.ui.ChartCountChange)
        self.ui.ct_pushButtonnn_05 = self.wc.setPushbutton('시뮬레이터', box=self.ui.ct_groupBoxxxxx_01, click=self.ui.ShowDialogTest)
        self.ui.ct_pushButtonnn_06 = self.wc.setPushbutton('확장', box=self.ui.ct_groupBoxxxxx_01, click=self.ui.ShowDialogChart2)

        self.ui.ct_dateEdittttt_02 = self.wc.setDateEdit(self.ui.dialog_chart, changed=self.ui.ChartMoneyTopList)
        self.ui.ct_tableWidgett_01 = self.wc.setTablewidget(self.ui.dialog_chart, ['종목명'], 100, vscroll=True, clicked=self.ui.CellClicked_07)

        self.ui.ctpg = {}
        self.ui.ctpg_cvb = {}
        pg.setConfigOption('background', color_bg_bk)
        self.ui.ctpg_layout = pg.GraphicsLayoutWidget()
        self.ui.ctpg[0], self.ui.ctpg_cvb[0] = self.wc.setaddPlot(self.ui.ctpg_layout, 0, 0)
        self.ui.ctpg[1], self.ui.ctpg_cvb[1] = self.wc.setaddPlot(self.ui.ctpg_layout, 1, 0)
        self.ui.ctpg[2], self.ui.ctpg_cvb[2] = self.wc.setaddPlot(self.ui.ctpg_layout, 2, 0)
        self.ui.ctpg[3], self.ui.ctpg_cvb[3] = self.wc.setaddPlot(self.ui.ctpg_layout, 3, 0)
        self.ui.ctpg[4], self.ui.ctpg_cvb[4] = self.wc.setaddPlot(self.ui.ctpg_layout, 0, 1)
        self.ui.ctpg[5], self.ui.ctpg_cvb[5] = self.wc.setaddPlot(self.ui.ctpg_layout, 1, 1)
        self.ui.ctpg[6], self.ui.ctpg_cvb[6] = self.wc.setaddPlot(self.ui.ctpg_layout, 2, 1)
        self.ui.ctpg[7], self.ui.ctpg_cvb[7] = self.wc.setaddPlot(self.ui.ctpg_layout, 3, 1)

        qGraphicsGridLayout = self.ui.ctpg_layout.ci.layout
        qGraphicsGridLayout.setRowStretchFactor(0, 1)
        qGraphicsGridLayout.setRowStretchFactor(1, 1)
        qGraphicsGridLayout.setRowStretchFactor(2, 1)

        self.ui.ctpg_vboxLayout = QVBoxLayout(self.ui.ct_groupBoxxxxx_02)
        self.ui.ctpg_vboxLayout.setContentsMargins(3, 6, 3, 3)
        self.ui.ctpg_vboxLayout.addWidget(self.ui.ctpg_layout)

        self.ui.dialog_jisu = self.wc.setDialog('STOM JISU')
        self.ui.dialog_jisu.geometry().center()
        self.ui.js_groupBox_01 = QGroupBox(' ', self.ui.dialog_jisu)

        self.ui.jspg = {}
        pg.setConfigOption('background', color_bg_bk)
        jspg = pg.GraphicsLayoutWidget()
        self.ui.jspg[1], _ = self.wc.setaddPlot(jspg, 0, 0, title='<span style="font-size:13px;font-family:나눔고딕;">KOSPI</span>')
        self.ui.jspg[2], _ = self.wc.setaddPlot(jspg, 1, 0, title='<span style="font-size:13px;font-family:나눔고딕;">KOSDAQ</span>')

        jspg_vboxLayout = QVBoxLayout(self.ui.js_groupBox_01)
        jspg_vboxLayout.setContentsMargins(3, 6, 3, 3)
        jspg_vboxLayout.addWidget(jspg)

        self.ui.dialog_chart.setFixedSize(1403, 1370 if not DICT_SET['저해상도'] else 1010)
        if self.ui.dict_set['창위치기억'] and self.ui.dict_set['창위치'] is not None:
            try:
                self.ui.dialog_chart.move(self.ui.dict_set['창위치'][2], self.ui.dict_set['창위치'][3])
            except:
                pass
        self.ui.ct_groupBoxxxxx_01.setGeometry(5, -10, 1393, 62)
        self.ui.ct_groupBoxxxxx_02.setGeometry(5, 40, 1393, 1325 if not DICT_SET['저해상도'] else 965)

        self.ui.ct_dateEdittttt_01.setGeometry(10, 25, 100, 30)
        self.ui.ct_labellllllll_01.setGeometry(120, 25, 50, 30)
        self.ui.ct_lineEdittttt_01.setGeometry(170, 25, 60, 30)
        self.ui.ct_labellllllll_02.setGeometry(240, 25, 50, 30)
        self.ui.ct_lineEdittttt_02.setGeometry(290, 25, 60, 30)
        self.ui.ct_labellllllll_03.setGeometry(360, 25, 50, 30)
        self.ui.ct_lineEdittttt_03.setGeometry(410, 25, 60, 30)
        self.ui.ct_labellllllll_04.setGeometry(480, 25, 50, 30)
        self.ui.ct_lineEdittttt_04.setGeometry(530, 25, 60, 30)
        self.ui.ct_labellllllll_05.setGeometry(605, 25, 50, 30)
        self.ui.ct_lineEdittttt_05.setGeometry(655, 25, 100, 30)
        self.ui.ct_pushButtonnn_01.setGeometry(765, 25, 60, 30)
        self.ui.ct_checkBoxxxxx_31.setGeometry(835, 25, 60, 30)
        self.ui.ct_checkBoxxxxx_32.setGeometry(900, 25, 60, 30)
        self.ui.ct_pushButtonnn_02.setGeometry(965, 25, 80, 30)
        self.ui.ct_pushButtonnn_03.setGeometry(1050, 25, 80, 30)
        self.ui.ct_pushButtonnn_04.setGeometry(1135, 25, 80, 30)
        self.ui.ct_pushButtonnn_05.setGeometry(1220, 25, 80, 30)
        self.ui.ct_pushButtonnn_06.setGeometry(1305, 25, 80, 30)

        self.ui.ct_dateEdittttt_02.setGeometry(1403, 15, 120, 30)
        self.ui.ct_tableWidgett_01.setGeometry(1403, 55, 120, 1310 if not DICT_SET['저해상도'] else 950)

        self.ui.dialog_jisu.setFixedSize(770, 700)
        if self.ui.dict_set['창위치기억'] and self.ui.dict_set['창위치'] is not None:
            try:
                self.ui.dialog_jisu.move(self.ui.dict_set['창위치'][6], self.ui.dict_set['창위치'][7])
            except:
                pass
        self.ui.js_groupBox_01.setGeometry(5, -10, 760, 700)
