from PyQt5.QtWidgets import QWidget, QLabel, QGroupBox
from ui.set_style import qfont12, style_pgbar


class SetMainMenu:
    def __init__(self, ui_class, wc):
        self.ui = ui_class
        self.wc = wc
        self.set()

    def set(self):
        self.ui.setFont(qfont12)
        self.ui.setWindowTitle('STOM')
        self.ui.setWindowIcon(self.ui.icon_main)
        self.ui.geometry().center()

        self.ui.pushButton_01 = self.wc.setPushbutton('', icon=self.ui.icon_stock,  color=0, click=self.ui.mnButtonClicked_01, cmd=0, shortcut='Alt+1', tip='주식 트레이더(Alt+1)')
        self.ui.pushButton_02 = self.wc.setPushbutton('', icon=self.ui.icon_coin,   color=6, click=self.ui.mnButtonClicked_01, cmd=1, shortcut='Alt+2', tip='코인 트레이더(Alt+2)')
        self.ui.pushButton_03 = self.wc.setPushbutton('', icon=self.ui.icon_stocks, color=6, click=self.ui.mnButtonClicked_01, cmd=2, shortcut='Alt+3', tip='주식 전략(Alt+3)')
        self.ui.pushButton_04 = self.wc.setPushbutton('', icon=self.ui.icon_coins,  color=6, click=self.ui.mnButtonClicked_01, cmd=3, shortcut='Alt+4', tip='코인 전략(Alt+4)')
        self.ui.pushButton_05 = self.wc.setPushbutton('', icon=self.ui.icon_live,   color=6, click=self.ui.mnButtonClicked_01, cmd=4, shortcut='Alt+5', tip='스톰 라이브(Alt+5)')
        self.ui.pushButton_06 = self.wc.setPushbutton('', icon=self.ui.icon_log,    color=6, click=self.ui.mnButtonClicked_01, cmd=5, shortcut='Alt+6', tip='로그(Alt+6)')
        self.ui.pushButton_07 = self.wc.setPushbutton('', icon=self.ui.icon_set,    color=6, click=self.ui.mnButtonClicked_01, cmd=6, shortcut='Alt+7', tip='설정(Alt+7)')

        self.ui.main_btn_list = [
            self.ui.pushButton_01, self.ui.pushButton_02, self.ui.pushButton_03, self.ui.pushButton_04,
            self.ui.pushButton_05, self.ui.pushButton_06, self.ui.pushButton_07
        ]

        self.ui.st_tab = QGroupBox('', self.ui)
        self.ui.ct_tab = QGroupBox('', self.ui)
        self.ui.ss_tab = QGroupBox('', self.ui)
        self.ui.cs_tab = QGroupBox('', self.ui)
        self.ui.lv_tab = QGroupBox('', self.ui)
        self.ui.lg_tab = QGroupBox('', self.ui)
        self.ui.sj_tab = QGroupBox('', self.ui)

        self.ui.st_tab.setVisible(True)
        self.ui.ct_tab.setVisible(False)
        self.ui.ss_tab.setVisible(False)
        self.ui.cs_tab.setVisible(False)
        self.ui.lv_tab.setVisible(False)
        self.ui.lg_tab.setVisible(False)
        self.ui.sj_tab.setVisible(False)

        self.ui.main_box_list = [
            self.ui.st_tab, self.ui.ct_tab, self.ui.ss_tab, self.ui.cs_tab, self.ui.lv_tab, self.ui.lg_tab, self.ui.sj_tab
        ]

        self.ui.slv_tab = QWidget()
        self.ui.clv_tab = QWidget()
        self.ui.blv_tab = QWidget()

        self.ui.ssd_tab = QWidget()
        self.ui.sod_tab = QWidget()

        self.ui.progressBarrr = self.wc.setProgressBar(self.ui, vertical=True, style=style_pgbar)
        self.ui.at_pushButton = self.wc.setPushbutton('Alt')
        self.ui.tt_pushButton = self.wc.setPushbutton('T', color=6, click=self.ui.mnButtonClicked_02, shortcut='Alt+T', tip='수익집계')
        self.ui.ms_pushButton = self.wc.setPushbutton('S', color=6, click=self.ui.mnButtonClicked_03, shortcut='Alt+S', tip='주식수동시작')
        self.ui.dd_pushButton = self.wc.setPushbutton('D', color=6, click=self.ui.ShowDB,             shortcut='Alt+D', tip='DB관리')
        self.ui.kp_pushButton = self.wc.setPushbutton('P', color=6, click=self.ui.ShowKimp,           shortcut='Alt+P', tip='김프')
        self.ui.zo_pushButton = self.wc.setPushbutton('Z', color=6, click=self.ui.mnButtonClicked_04, shortcut='Alt+Z', tip='축소확대')
        self.ui.ct_pushButton = self.wc.setPushbutton('C', color=6, click=self.ui.ShowChart,          shortcut='Alt+C', tip='차트창')
        self.ui.hg_pushButton = self.wc.setPushbutton('H', color=6, click=self.ui.ShowHoga,           shortcut='Alt+H', tip='호가창')
        self.ui.gu_pushButton = self.wc.setPushbutton('G', color=6, click=self.ui.ShowGiup,           shortcut='Alt+G', tip='기업정보')
        self.ui.uj_pushButton = self.wc.setPushbutton('U', color=6, click=self.ui.ShowTreemap,        shortcut='Alt+U', tip='트리맵')
        self.ui.js_pushButton = self.wc.setPushbutton('K', color=6, click=self.ui.ShowJisu,           shortcut='Alt+K', tip='지수차트')
        self.ui.qs_pushButton = self.wc.setPushbutton('Q', color=6, click=self.ui.ShowQsize,          shortcut='Alt+Q', tip='큐사이즈')
        self.ui.bs_pushButton = self.wc.setPushbutton('B', color=6, click=self.ui.ShowBackScheduler,  shortcut='Alt+B', tip='백테스케쥴러')
        self.ui.cl_pushButton = self.wc.setPushbutton('Ctrl')
        self.ui.bd_pushButton = self.wc.setPushbutton('B', color=6, click=self.ui.mnButtonClicked_05, shortcut='Ctrl+B', tip='백테기록삭제')
        self.ui.ad_pushButton = self.wc.setPushbutton('A', color=6, click=self.ui.mnButtonClicked_06, shortcut='Ctrl+A', tip='계정삭제')
        self.ui.c2_pushButton = self.wc.setPushbutton('Ctrl')
        self.ui.sf_pushButton = self.wc.setPushbutton('Shift')
        self.ui.bb_pushButton = self.wc.setPushbutton('B', color=6, click=self.ui.BackBench, shortcut='Ctrl+Shift+B', tip='백테엔진 밴치테스트')
        self.ui.od_pushButton = self.wc.setPushbutton('O', color=6, click=self.ui.ShowOrder, shortcut='Ctrl+Shift+O', tip='수동주문창')
        self.ui.vv_pushButton = self.wc.setPushbutton('V', color=6, click=self.ui.ShowVideo, shortcut='Ctrl+Shift+V', tip='인트로영상재생')
        self.ui.zz_pushButton = self.wc.setPushbutton('E', color=6, click=self.ui.ExtendWindow, shortcut='Ctrl+Shift+E', tip='전략탭확장')

        self.ui.image_label1 = QLabel(self.ui)
        self.ui.image_label2 = QLabel(self.ui)
        self.ui.image_label1.setVisible(False)
        self.ui.image_label2.setVisible(False)

        self.ui.setFixedSize(1403, 763)
        if self.ui.dict_set['창위치기억'] and self.ui.dict_set['창위치'] is not None:
            try:
                self.ui.move(self.ui.dict_set['창위치'][0], self.ui.dict_set['창위치'][1])
            except:
                pass
        self.ui.pushButton_01.setGeometry(5, 5, 35, 40)
        self.ui.pushButton_02.setGeometry(5, 45, 35, 40)
        self.ui.pushButton_03.setGeometry(5, 85, 35, 40)
        self.ui.pushButton_04.setGeometry(5, 125, 35, 40)
        self.ui.pushButton_05.setGeometry(5, 165, 35, 40)
        self.ui.pushButton_06.setGeometry(5, 205, 35, 40)
        self.ui.pushButton_07.setGeometry(5, 245, 35, 40)
        self.ui.st_tab.setGeometry(45, 0, 1353, 757)
        self.ui.ct_tab.setGeometry(45, 0, 1353, 757)
        self.ui.ss_tab.setGeometry(45, 0, 1353, 757)
        self.ui.cs_tab.setGeometry(45, 0, 1353, 757)
        self.ui.lg_tab.setGeometry(45, 0, 1353, 757)
        self.ui.sj_tab.setGeometry(45, 0, 1353, 757)
        self.ui.lv_tab.setGeometry(45, 0, 1353, 757)
        self.ui.at_pushButton.setGeometry(5, 290, 35, 15)
        self.ui.tt_pushButton.setGeometry(8, 310, 16, 15)
        self.ui.ms_pushButton.setGeometry(23, 310, 16, 15)
        self.ui.dd_pushButton.setGeometry(8, 330, 16, 15)
        self.ui.kp_pushButton.setGeometry(23, 330, 16, 15)
        self.ui.zo_pushButton.setGeometry(8, 350, 16, 15)
        self.ui.ct_pushButton.setGeometry(23, 350, 16, 15)
        self.ui.hg_pushButton.setGeometry(8, 370, 16, 15)
        self.ui.gu_pushButton.setGeometry(23, 370, 16, 15)
        self.ui.uj_pushButton.setGeometry(8, 390, 16, 15)
        self.ui.js_pushButton.setGeometry(23, 390, 16, 15)
        self.ui.qs_pushButton.setGeometry(8, 410, 16, 15)
        self.ui.bs_pushButton.setGeometry(23, 410, 16, 15)
        self.ui.cl_pushButton.setGeometry(5, 430, 35, 15)
        self.ui.bd_pushButton.setGeometry(8, 450, 16, 15)
        self.ui.ad_pushButton.setGeometry(23, 450, 16, 15)
        self.ui.c2_pushButton.setGeometry(5, 470, 35, 15)
        self.ui.sf_pushButton.setGeometry(5, 485, 35, 15)
        self.ui.bb_pushButton.setGeometry(8, 505, 16, 15)
        self.ui.od_pushButton.setGeometry(23, 505, 16, 15)
        self.ui.vv_pushButton.setGeometry(8, 525, 16, 15)
        self.ui.zz_pushButton.setGeometry(23, 525, 16, 15)
        self.ui.progressBarrr.setGeometry(5, 548, 35, 208)
        self.ui.image_label1.setGeometry(1057, 478, 335, 105)
        self.ui.image_label2.setGeometry(1057, 756, 335, 602)
