import ctypes
import subprocess
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QCompleter
from multiprocessing import Queue
from matplotlib import font_manager
from matplotlib import pyplot as plt

from ui.set_style import *
from ui.set_icon import SetIcon
from ui.set_table import SetTable
from ui.set_logtap import SetLogTap
from ui.set_cbtap import SetCoinBack
from ui.set_sbtap import SetStockBack
from ui.set_widget import WidgetCreater
from ui.set_setuptap import SetSetupTap
from ui.set_ordertap import SetOrderTap
from ui.set_mainmenu import SetMainMenu
from ui.set_dialog_etc import SetDialogEtc
from ui.set_dialog_back import SetDialogBack
from ui.set_mediaplayer import SetMediaPlayer
from ui.set_dialog_chart import SetDialogChart

from ui.ui_writer import Writer
from ui.ui_zmq import ZmqServ, ZmqRecv
from ui.ui_draw_chart import DrawChart
from ui.ui_draw_treemap import DrawTremap
from ui.ui_extend_window import extend_window
from ui.ui_draw_realchart import DrawRealChart
from ui.ui_update_textedit import UpdateTextedit
from ui.ui_process_starter import process_starter
from ui.ui_draw_jisuchart import DrawRealJisuChart
from ui.ui_update_tablewidget import UpdateTablewidget
from ui.ui_update_progressbar import update_progressbar

from ui.ui_etc import *
from ui.ui_pattern import *
from ui.ui_event_filter import *
from ui.ui_activated_b import *
from ui.ui_activated_c import *
from ui.ui_activated_s import *
from ui.ui_show_dialog import *
from ui.ui_vars_change import *
from ui.ui_cell_clicked import *
from ui.ui_text_changed import *
from ui.ui_process_kill import *
from ui.ui_return_press import *
from ui.ui_activated_etc import *
from ui.ui_process_alive import *
from ui.ui_backtest_engine import *
from ui.ui_key_press_event import *
from ui.ui_checkbox_changed import *
from ui.ui_button_clicked_db import *
from ui.ui_button_clicked_ob import *
from ui.ui_button_clicked_sd import *
from ui.ui_button_clicked_mn import *
from ui.ui_button_clicked_sj import *
from ui.ui_button_clicked_etc import *
from ui.ui_chart_count_change import *
from ui.ui_button_clicked_svc import *
from ui.ui_button_clicked_svj import *
from ui.ui_button_clicked_cvc import *
from ui.ui_button_clicked_cvj import *
from ui.ui_button_clicked_svjs import *
from ui.ui_button_clicked_svjb import *
from ui.ui_button_clicked_cvoa import *
from ui.ui_button_clicked_cvjs import *
from ui.ui_button_clicked_cvjb import *
from ui.ui_button_clicked_svoa import *
from ui.ui_button_clicked_zoom import *
from ui.ui_button_clicked_ss_cs import *
from ui.ui_button_clicked_chart import *

from utility.static import *
from utility.setting import *
from utility.hoga import Hoga
from utility.chart import Chart
from utility.sound import Sound
from utility.query import Query
from utility.chart_items import *
from utility.webcrawling import WebCrawling
from utility.telegram_msg import TelegramMsg


class Window(QMainWindow):
    def __init__(self, auto_run_):
        super().__init__()
        self.auto_run = auto_run_
        self.dict_set = DICT_SET
        self.hogaQ    = hogaQ
        self.main_btn = 0
        self.counter  = 0
        self.cpu_per  = 0
        self.int_time = int_hms()
        self.wc       = WidgetCreater(self)

        SetLogFile(self)
        SetIcon(self)
        SetMainMenu(self, self.wc)
        SetTable(self, self.wc)
        SetStockBack(self, self.wc)
        SetCoinBack(self, self.wc)
        SetLogTap(self, self.wc)
        SetSetupTap(self, self.wc)
        SetOrderTap(self, self.wc)
        SetDialogChart(self, self.wc)
        SetDialogEtc(self, self.wc)
        SetDialogBack(self, self.wc)
        SetMediaPlayer(self)

        con1 = sqlite3.connect(DB_SETTING)
        con2 = sqlite3.connect(DB_STOCK_BACK)
        try:
            df = pd.read_sql('SELECT * FROM codename', con1).set_index('index')
        except:
            df = pd.read_sql('SELECT * FROM codename', con2).set_index('index')
        con1.close()
        con2.close()

        self.dict_name = {code: df['종목명'][code] for code in df.index}
        self.dict_code = {name: code for code, name in self.dict_name.items()}

        if len(df) < 10:
            print('setting.db 내에 codename 테이블이 갱신되지 않았습니다.')
            print('주식 수동로그인을 한번 실행하면 codename 테이블이 갱신됩니다.')

        con = sqlite3.connect(DB_COIN_TICK)
        df = pd.read_sql("SELECT name FROM sqlite_master WHERE TYPE = 'table'", con)
        con.close()

        self.ct_lineEdittttt_04.setCompleter(QCompleter(list(self.dict_code.values())))
        self.ct_lineEdittttt_05.setCompleter(QCompleter(list(self.dict_name.values()) + df['name'].to_list()))

        self.back_schedul     = False
        self.showQsize        = False
        self.test_pause       = False
        self.image_search     = False
        self.auto_mode        = False
        self.database_control = False
        self.ssicon_alert     = False
        self.csicon_alert     = False
        self.lgicon_alert     = False
        self.database_chart   = False
        self.daydata_download = False
        self.tickdata_save    = False
        self.backtest_engine  = False
        self.time_sync        = False
        self.extend_window    = False
        self.back_condition   = True

        self.animation        = None
        self.webEngineView    = None
        self.df_test          = None
        self.dict_sgbn        = None
        self.dict_cn          = None
        self.dict_mt          = None

        self.vars             = {}
        self.buy_index        = []
        self.sell_index       = []
        self.back_eprocs      = []
        self.back_eques       = []
        self.back_cprocs      = []
        self.back_cques       = []
        self.avg_list         = []
        self.back_count       = 0
        self.startday         = 0
        self.endday           = 0
        self.starttime        = 0
        self.endtime          = 0
        self.ct_test          = 0
        self.back_scount      = 0

        self.stock_simulator_alive = False
        self.backengin_window_open = False
        self.optuna_window_open    = False

        self.proc_backtester_bb    = None
        self.proc_backtester_bf    = None
        self.proc_backtester_bc    = None
        self.proc_backtester_bp    = None
        self.proc_backtester_o     = None
        self.proc_backtester_ov    = None
        self.proc_backtester_ovc   = None
        self.proc_backtester_ot    = None
        self.proc_backtester_ovt   = None
        self.proc_backtester_ovct  = None
        self.proc_backtester_or    = None
        self.proc_backtester_orv   = None
        self.proc_backtester_orvc  = None
        self.proc_backtester_b     = None
        self.proc_backtester_bv    = None
        self.proc_backtester_bvc   = None
        self.proc_backtester_bt    = None
        self.proc_backtester_bvt   = None
        self.proc_backtester_bvct  = None
        self.proc_backtester_br    = None
        self.proc_backtester_brv   = None
        self.proc_backtester_brvc  = None
        self.proc_backtester_og    = None
        self.proc_backtester_ogv   = None
        self.proc_backtester_ogvc  = None
        self.proc_backtester_oc    = None
        self.proc_backtester_ocv   = None
        self.proc_backtester_ocvc  = None

        self.proc_stomlive         = None
        self.proc_receiver_coin    = None
        self.proc_strategy_coin    = None
        self.proc_trader_coin      = None
        self.proc_coin_kimp        = None
        self.proc_simulator_rv     = None
        self.proc_simulator_td     = None

        self.backdetail_list       = None
        self.backcheckbox_list     = None
        self.order_combo_name_list = []

        self.ctpg_tik_name         = None
        self.ctpg_tik_cline        = None
        self.ctpg_tik_hline        = None
        self.ctpg_tik_xticks       = None
        self.ctpg_tik_arry         = None
        self.ctpg_tik_legend       = {}
        self.ctpg_tik_item         = {}
        self.ctpg_tik_data         = {}
        self.ctpg_tik_factors      = []
        self.ctpg_tik_labels       = []

        self.srqsize = 0
        self.stqsize = 0
        self.ssqsize = 0

        self.df_kp   = None
        self.df_kd   = None
        self.tm_ax1  = None
        self.tm_ax2  = None
        self.df_tm1  = None
        self.df_tm2  = None
        self.tm_cl1  = None
        self.tm_cl2  = None
        self.tm_dt   = False
        self.tm_mc1  = 0
        self.tm_mc2  = 0

        subprocess.Popen('python ./stock/kiwoom_manager.py')

        port_num = get_port_number()
        self.zmqserv = ZmqServ(wdzservQ, port_num)
        self.zmqserv.start()

        self.zmqrecv = ZmqRecv(qlist, port_num + 1)
        self.zmqrecv.start()

        self.qtimer1 = QTimer()
        self.qtimer1.setInterval(1 * 1000)
        # noinspection PyUnresolvedReferences
        self.qtimer1.timeout.connect(self.ProcessStarter)
        self.qtimer1.start()

        self.qtimer2 = QTimer()
        self.qtimer2.setInterval(500)
        # noinspection PyUnresolvedReferences
        self.qtimer2.timeout.connect(self.UpdateProgressBar)
        self.qtimer2.start()

        self.qtimer3 = QTimer()
        self.qtimer3.setInterval(1 * 1000)
        # noinspection PyUnresolvedReferences
        self.qtimer3.timeout.connect(self.UpdateCpuper)
        self.qtimer3.start()

        self.update_textedit    = UpdateTextedit(self, qlist)
        self.update_tablewidget = UpdateTablewidget(self, qlist)
        self.draw_chart         = DrawChart(self)
        self.draw_realchart     = DrawRealChart(self)
        self.draw_realjisuchart = DrawRealJisuChart(self)
        self.draw_treemap       = DrawTremap(self, qlist)

        self.writer = Writer(windowQ)
        # noinspection PyUnresolvedReferences
        self.writer.signal1.connect(self.update_textedit.update_texedit)
        # noinspection PyUnresolvedReferences
        self.writer.signal2.connect(self.update_tablewidget.update_tablewidget)
        # noinspection PyUnresolvedReferences
        self.writer.signal3.connect(self.draw_chart.draw_chart)
        # noinspection PyUnresolvedReferences
        self.writer.signal4.connect(self.draw_realchart.draw_realchart)
        # noinspection PyUnresolvedReferences
        self.writer.signal5.connect(self.draw_realjisuchart.draw_realjisuchart)
        # noinspection PyUnresolvedReferences
        self.writer.signal6.connect(self.draw_treemap.draw_treemap)
        # noinspection PyUnresolvedReferences
        self.writer.signal7.connect(self.ImageUpdate)
        # noinspection PyUnresolvedReferences
        self.writer.signal8.connect(self.UpdateSQsize)
        # noinspection PyUnresolvedReferences
        self.writer.signal9.connect(self.StomliveScreenshot)
        self.writer.start()

        font_name = 'C:/Windows/Fonts/malgun.ttf'
        font_family = font_manager.FontProperties(fname=font_name).get_name()
        plt.rcParams['font.family'] = font_family
        plt.rcParams['axes.unicode_minus'] = False

    # =================================================================================================================
    def ProcessStarter(self):              process_starter(self, qlist)
    def UpdateProgressBar(self):           update_progressbar(self, soundQ, webcQ)
    # =================================================================================================================
    def ImageUpdate(self, data):           update_image(self, data)
    def UpdateSQsize(self, data):          update_sqsize(self, data)
    def UpdateCpuper(self):                update_cpuper(self)
    def UpdateDictSet(self):               update_dictset(self, wdzservQ, creceivQ, ctraderQ, cstgQ, chartQ, proc_chart)
    def ChartClear(self):                  chart_clear(self)
    def ExtendWindow(self):                extend_window(self)
    def CalendarClicked(self, gubun):      calendar_clicked(self, gubun)
    def AutoBackSchedule(self, gubun):     auto_back_schedule(self, gubun, soundQ, teleQ)
    def VideoWidgetClose(self, state):     video_widget_close(self, state)
    def StomliveScreenshot(self, cmd):     stom_live_screenshot(self, cmd, teleQ)
    # =================================================================================================================
    def CheckboxChanged_01(self, state):   checkbox_changed_01(self, state)
    def CheckboxChanged_02(self, state):   checkbox_changed_02(self, state)
    def CheckboxChanged_03(self, state):   checkbox_changed_03(self, state)
    def CheckboxChanged_04(self, state):   checkbox_changed_04(self, state)
    def CheckboxChanged_05(self, state):   checkbox_changed_05(self, state)
    def CheckboxChanged_06(self, state):   checkbox_changed_06(self, state)
    def CheckboxChanged_07(self, state):   checkbox_changed_07(self, state)
    def CheckboxChanged_08(self, state):   checkbox_changed_08(self, state)
    def CheckboxChanged_09(self, state):   checkbox_changed_09(self, state)
    def CheckboxChanged_10(self, state):   checkbox_changed_10(self, state)
    def CheckboxChanged_11(self, state):   checkbox_changed_11(self, state)
    def CheckboxChanged_12(self, state):   checkbox_changed_12(self, state)
    def CheckboxChanged_13(self, state):   checkbox_changed_13(self, state)
    def CheckboxChanged_14(self, state):   checkbox_changed_14(self, state)
    def CheckboxChanged_15(self, state):   checkbox_changed_15(self, state)
    def CheckboxChanged_16(self, state):   checkbox_changed_16(self, state)
    def CheckboxChanged_17(self, state):   checkbox_changed_17(self, state)
    def CheckboxChanged_18(self, state):   checkbox_changed_18(self, state)
    def CheckboxChanged_19(self, state):   checkbox_changed_19(self, state)
    def CheckboxChanged_20(self, state):   checkbox_changed_20(self, state)
    def CheckboxChanged_21(self, state):   checkbox_changed_21(self, state)
    # def CheckboxChanged_22(self, state): checkbox_changed_22(self, state)
    def CheckboxChanged_23(self, state):   checkbox_changed_23(self, state)
    # =================================================================================================================
    def sbCheckboxChanged_01(self, state): sbcheckbox_changed_01(self, state)
    def sbCheckboxChanged_02(self, state): sbcheckbox_changed_02(self, state)
    def ssCheckboxChanged_01(self, state): sscheckbox_changed_01(self, state)
    def ssCheckboxChanged_02(self, state): sscheckbox_changed_02(self, state)
    # =================================================================================================================
    def cbCheckboxChanged_01(self, state): cbcheckbox_changed_01(self, state)
    def cbCheckboxChanged_02(self, state): cbcheckbox_changed_02(self, state)
    def csCheckboxChanged_01(self, state): cscheckbox_changed_01(self, state)
    def csCheckboxChanged_02(self, state): cscheckbox_changed_02(self, state)
    # =================================================================================================================
    @pyqtSlot(int, int)
    def CellClicked_01(self, row, col):    cell_clicked_01(self, row, col)
    @pyqtSlot(int)
    def CellClicked_02(self, row):         cell_clicked_02(self, row, wdzservQ)
    @pyqtSlot(int)
    def CellClicked_03(self, row):         cell_clicked_03(self, row, ctraderQ)
    @pyqtSlot(int)
    def CellClicked_04(self, row):         cell_clicked_04(self, row)
    @pyqtSlot(int)
    def CellClicked_05(self, row):         cell_clicked_05(self, row)
    @pyqtSlot(int)
    def CellClicked_06(self, row):         cell_clicked_06(self, row)
    @pyqtSlot(int)
    def CellClicked_07(self, row):         cell_clicked_07(self, row, chartQ)
    @pyqtSlot(int)
    def CellClicked_08(self, row):         cell_clicked_08(self, row)
    @pyqtSlot(int, int)
    def CellClicked_09(self, row, col):    cell_clicked_09(self, row, col, windowQ)
    @pyqtSlot(int, int)
    def CellClicked_10(self, row, col):    cell_clicked_10(self, row, col)
    def CellClicked_11(self):              cell_clicked_11(self)
    # =================================================================================================================
    def ReturnPress_01(self): return_press_01(self, chartQ)
    def ReturnPress_02(self): return_press_02(self, teleQ)
    # =================================================================================================================
    def TextChanged_01(self): text_changed_01(self)
    def TextChanged_02(self): text_changed_02(self)
    def TextChanged_03(self): text_changed_03(self)
    def TextChanged_04(self): text_changed_04(self)
    def TextChanged_05(self): text_changed_05(self)
    # =================================================================================================================
    def ShowDialogGraph(self, df):                                  show_dialog_graph(self, df)
    def ShowDialog(self, code_or_name, tickcount, searchdate, col): show_dialog(self, code_or_name, tickcount, searchdate, col)
    def ShowDialogWeb(self, show, code):                            show_dialog_web(self, show, code, webcQ)
    def ShowDialogHoga(self, show, coin, code):                     show_dialog_hoga(self, show, coin, code)

    def ShowDialogChart(self, real, coin, code, tickcount=None, searchdate=None, starttime=None, endtime=None, detail=None, buytimes=None):
        show_dialog_chart(self, real, coin, code, proc_chart, cstgQ, wdzservQ, chartQ, tickcount, searchdate, starttime, endtime, detail, buytimes)

    def ShowDialogChart2(self):        show_dialog_chart2(self)
    def ShowQsize(self):               show_qsize(self)
    def ShowDialogFactor(self):        show_dialog_factor(self)
    def ShowDialogTest(self):          show_dialog_test(self)
    def ShowChart(self):               show_chart(self)
    def ShowHoga(self):                show_hoga(self)
    def ShowGiup(self):                show_giup(self)
    def ShowTreemap(self):             show_treemap(self, webcQ)
    def ShowJisu(self):                show_jisu(self)
    def ShowDB(self):                  show_db(self)
    def ShowBackScheduler(self):       show_backscheduler(self)
    def ShowKimp(self):                show_kimp(self, qlist)
    def ShowOrder(self):               show_order(self)
    def ShowVideo(self):               show_video(self)
    def PutHogaCode(self, coin, code): put_hoga_code(self, coin, code, wdzservQ, creceivQ)
    def ChartMoneyTopList(self):       chart_moneytop_list(self)
    # =================================================================================================================
    # =================================================================================================================
    def dbButtonClicked_01(self): dbbutton_clicked_01(self, windowQ, queryQ, proc_query)
    def dbButtonClicked_02(self): dbbutton_clicked_02(self, windowQ, queryQ, proc_query)
    def dbButtonClicked_03(self): dbbutton_clicked_03(self, windowQ, queryQ, proc_query)
    def dbButtonClicked_04(self): dbbutton_clicked_04(self, windowQ, queryQ, proc_query)
    def dbButtonClicked_05(self): dbbutton_clicked_05(self, windowQ, queryQ, proc_query)
    def dbButtonClicked_06(self): dbbutton_clicked_06(self, windowQ, queryQ, proc_query)
    def dbButtonClicked_07(self): dbbutton_clicked_07(self, windowQ, queryQ, proc_query)
    def dbButtonClicked_08(self): dbbutton_clicked_08(self, windowQ, queryQ, proc_query)
    def dbButtonClicked_09(self): dbbutton_clicked_09(self, windowQ, queryQ, proc_query)
    def dbButtonClicked_10(self): dbbutton_clicked_10(self, windowQ, queryQ, proc_query)
    def dbButtonClicked_11(self): dbbutton_clicked_11(self, windowQ, queryQ, proc_query)
    def dbButtonClicked_12(self): dbbutton_clicked_12(self, windowQ, queryQ, proc_query)
    def dbButtonClicked_13(self): dbbutton_clicked_13(self, windowQ, queryQ, proc_query)
    def dbButtonClicked_14(self): dbbutton_clicked_14(self, windowQ, queryQ, proc_query)
    def dbButtonClicked_15(self): dbbutton_clicked_15(self, windowQ, queryQ, proc_query)
    def dbButtonClicked_16(self): dbbutton_clicked_16(self, windowQ, queryQ, proc_query)
    def dbButtonClicked_17(self): dbbutton_clicked_17(self, windowQ, queryQ, proc_query)
    def dbButtonClicked_18(self): dbbutton_clicked_18(self, windowQ, queryQ, proc_query)
    def dbButtonClicked_19(self): dbbutton_clicked_19(self, windowQ, queryQ, proc_query)
    # =================================================================================================================
    def pActivated_01(self):      pactivated_01(self)
    def ptButtonClicked_01(self): ptbutton_clicked_01(self)
    def ptButtonClicked_02(self): ptbutton_clicked_02(self, proc_query, queryQ)
    def ptButtonClicked_03(self): ptbutton_clicked_03(self)
    # =================================================================================================================
    def odButtonClicked_01(self): odbutton_clicked_01(self, ctraderQ, wdzservQ)
    def odButtonClicked_02(self): odbutton_clicked_02(self, ctraderQ, wdzservQ)
    def odButtonClicked_03(self): odbutton_clicked_03(self, ctraderQ)
    def odButtonClicked_04(self): odbutton_clicked_04(self, ctraderQ)
    def odButtonClicked_05(self): odbutton_clicked_05(self, ctraderQ)
    def odButtonClicked_06(self): odbutton_clicked_06(self, ctraderQ)
    def odButtonClicked_07(self): odbutton_clicked_07(self, ctraderQ, wdzservQ)
    def odButtonClicked_08(self): odbutton_clicked_08(self, ctraderQ, wdzservQ)
    # =================================================================================================================
    @staticmethod
    def opButtonClicked_01():          opbutton_clicked_01()
    def cpButtonClicked_01(self):      cpbutton_clicked_01(self, chartQ)
    def ttButtonClicked_01(self, cmd): ttbutton_clicked_01(self, cmd)
    def stButtonClicked_01(self):      stbutton_clicked_01(self)
    def stButtonClicked_02(self):      stbutton_clicked_02(self, proc_query, queryQ)
    def ChangeBacksDate(self):         change_back_sdate(self)
    def ChangeBackeDate(self):         change_back_edate(self)
    # =================================================================================================================
    def beButtonClicked_01(self):      bebutton_clicked_01(self)
    def BacktestEngineKill(self):      backtest_engine_kill(self, windowQ)
    def BackBench(self):               back_bench(self, windowQ, backQ, soundQ, totalQ, liveQ, teleQ)
    def sdButtonClicked_01(self):      sdbutton_clicked_01(self)
    def sdButtonClicked_02(self):      sdbutton_clicked_02(self, windowQ, backQ, soundQ, totalQ, liveQ, teleQ)
    def sdButtonClicked_03(self):      sdbutton_clicked_03(self)
    def sdButtonClicked_04(self):      sdbutton_clicked_04(self)
    def sdButtonClicked_05(self):      sdbutton_clicked_05(self, proc_query, queryQ)
    # =================================================================================================================
    def mnButtonClicked_01(self, index):            mnbutton_c_clicked_01(self, index)
    def mnButtonClicked_02(self):                   mnbutton_c_clicked_02(self)
    def mnButtonClicked_03(self, stocklogin=False): mnbutton_c_clicked_03(self, wdzservQ, soundQ, stocklogin)
    def mnButtonClicked_04(self):                   mnbutton_c_clicked_04(self)
    def mnButtonClicked_05(self):                   mnbutton_c_clicked_05(self, proc_query, queryQ)
    def mnButtonClicked_06(self):                   mnbutton_c_clicked_06(self, proc_query, queryQ)
    # =================================================================================================================
    def ssButtonClicked_01(self): ssbutton_clicked_01(self)
    def ssButtonClicked_02(self): ssbutton_clicked_02(self)
    def ssButtonClicked_03(self): ssbutton_clicked_03(self)
    def ssButtonClicked_04(self): ssbutton_clicked_04(self)
    def ssButtonClicked_05(self): ssbutton_clicked_05(self)
    def ssButtonClicked_06(self): ssbutton_clicked_06(self)
    # =================================================================================================================
    def csButtonClicked_01(self): csbutton_clicked_01(self)
    def csButtonClicked_02(self): csbutton_clicked_02(self)
    def csButtonClicked_03(self): csbutton_clicked_03(self)
    def csButtonClicked_04(self): csbutton_clicked_04(self)
    def csButtonClicked_05(self): csbutton_clicked_05(self)
    def csButtonClicked_06(self): csbutton_clicked_06(self)
    # =================================================================================================================
    def szooButtonClicked_01(self): szoo_button_clicked_01(self)
    def szooButtonClicked_02(self): szoo_button_clicked_02(self)
    def czooButtonClicked_01(self): czoo_button_clicked_01(self)
    def czooButtonClicked_02(self): czoo_button_clicked_02(self)
    # =================================================================================================================
    # =================================================================================================================
    def Activated_01(self):  activated_01(self)
    def Activated_02(self):  activated_02(self)
    def Activated_03(self):  activated_03(self)
    # =================================================================================================================
    def sActivated_01(self): sactivated_01(self)
    def sActivated_02(self): sactivated_02(self)
    def sActivated_03(self): sactivated_03(self)
    def sActivated_04(self): sactivated_04(self)
    def sActivated_05(self): sactivated_05(self)
    def sActivated_06(self): sactivated_06(self)
    def sActivated_07(self): sactivated_07(self)
    def sActivated_08(self): sactivated_08(self)
    def sActivated_09(self): sactivated_09(self)
    def sActivated_10(self): sactivated_10(self)
    # =================================================================================================================
    def cActivated_01(self): cactivated_01(self)
    def cActivated_02(self): cactivated_02(self)
    def cActivated_03(self): cactivated_03(self)
    def cActivated_04(self): cactivated_04(self)
    def cActivated_05(self): cactivated_05(self)
    def cActivated_06(self): cactivated_06(self)
    def cActivated_07(self): cactivated_07(self)
    def cActivated_08(self): cactivated_08(self)
    def cActivated_09(self): cactivated_09(self)
    def cActivated_10(self): cactivated_10(self)
    def cActivated_11(self): cactivated_11(self)
    def cActivated_12(self): cactivated_12(self)
    def cActivated_13(self): cactivated_13(self)
    # =================================================================================================================
    def bActivated_01(self): bactivated_01(self)
    def bActivated_02(self): bactivated_02(self)
    def bActivated_03(self): bactivated_03(self)
    # =================================================================================================================
    def GetFixStrategy(self, strategy, gubun):     return get_fix_strategy(self, strategy, gubun)
    @staticmethod
    def GetOptivarsToGavars(opti_vars_text):       return get_optivars_to_gavars(opti_vars_text)
    @staticmethod
    def GetGavarsToOptivars(ga_vars_text):         return get_gavars_to_optivars(ga_vars_text)
    def GetStgtxtToVarstxt(self, buystg, sellstg): return get_stgtxt_to_varstxt(self, buystg, sellstg)
    @staticmethod
    def GetStgtxtSort(buystg, sellstg):            return get_stgtxt_sort(buystg, sellstg)
    @staticmethod
    def GetStgtxtSort2(optivars, gavars):          return get_stgtxt_sort2(optivars, gavars)
    # =================================================================================================================
    # =================================================================================================================
    def svjbButtonClicked_01(self): svjb_button_clicked_01(self)
    def svjbButtonClicked_02(self): svjb_button_clicked_02(self, proc_query, queryQ)
    def svjbButtonClicked_03(self): svjb_button_clicked_03(self)
    def svjbButtonClicked_04(self): svjb_button_clicked_04(self, wdzservQ)
    def svjbButtonClicked_05(self): svjb_button_clicked_05(self)
    def svjbButtonClicked_06(self): svjb_button_clicked_06(self)
    def svjbButtonClicked_07(self): svjb_button_clicked_07(self)
    def svjbButtonClicked_08(self): svjb_button_clicked_08(self)
    def svjbButtonClicked_09(self): svjb_button_clicked_09(self)
    def svjbButtonClicked_10(self): svjb_button_clicked_10(self)
    def svjbButtonClicked_11(self): svjb_button_clicked_11(self)
    def svjbButtonClicked_12(self): svjb_button_clicked_12(self, wdzservQ)
    # =================================================================================================================
    def svjButtonClicked_01(self): svj_button_clicked_01(self)
    def svjButtonClicked_02(self): svj_button_clicked_02(self)
    def svjButtonClicked_03(self): svj_button_clicked_03(self)
    def svjButtonClicked_04(self): svj_button_clicked_04(self)
    def svjButtonClicked_05(self): svj_button_clicked_05(self)
    def svjButtonClicked_06(self): svj_button_clicked_06(self)
    def svjButtonClicked_07(self): svj_button_clicked_07(self)
    def svjButtonClicked_08(self): svj_button_clicked_08(self)
    def svjButtonClicked_09(self): svj_button_clicked_09(self)
    def svjButtonClicked_10(self): svj_button_clicked_10(self)
    def svjButtonClicked_11(self): svj_button_clicked_11(self, windowQ, backQ, soundQ, totalQ, liveQ, teleQ)
    def svjButtonClicked_12(self): svj_button_clicked_12(self, windowQ, backQ, soundQ, totalQ, liveQ)
    def svjButtonClicked_13(self): svj_button_clicked_13(self)
    def svjButtonClicked_14(self, back_name): svj_button_clicked_14(self, back_name, windowQ, backQ, soundQ, totalQ, liveQ, teleQ)
    def svjButtonClicked_15(self, back_name): svj_button_clicked_15(self, back_name, windowQ, backQ, soundQ, totalQ, liveQ, teleQ)
    def svjButtonClicked_16(self, back_name): svj_button_clicked_16(self, back_name, windowQ, backQ, soundQ, totalQ, liveQ)
    def svjButtonClicked_17(self, back_name): svj_button_clicked_17(self, back_name, windowQ, backQ, soundQ, totalQ, liveQ)
    def svjButtonClicked_18(self): svj_button_clicked_18(self)
    def svjButtonClicked_19(self): svj_button_clicked_19(self)
    def svjButtonClicked_20(self): svj_button_clicked_20(self)
    def svjButtonClicked_21(self): svj_button_clicked_21(self)
    def svjButtonClicked_22(self): svj_button_clicked_22(self)
    def svjButtonClicked_23(self): svj_button_clicked_23(self, windowQ, backQ, totalQ)
    def svjButtonClicked_24(self): svj_button_clicked_24(self, windowQ, backQ, soundQ, totalQ, liveQ, teleQ)
    def svjButtonClicked_25(self): svj_button_clicked_25(self)
    # =================================================================================================================
    def svjsButtonClicked_01(self): svjs_button_clicked_01(self)
    def svjsButtonClicked_02(self): svjs_button_clicked_02(self, proc_query, queryQ)
    def svjsButtonClicked_03(self): svjs_button_clicked_03(self)
    def svjsButtonClicked_04(self): svjs_button_clicked_04(self, wdzservQ)
    def svjsButtonClicked_05(self): svjs_button_clicked_05(self)
    def svjsButtonClicked_06(self): svjs_button_clicked_06(self)
    def svjsButtonClicked_07(self): svjs_button_clicked_07(self)
    def svjsButtonClicked_08(self): svjs_button_clicked_08(self)
    def svjsButtonClicked_09(self): svjs_button_clicked_09(self)
    def svjsButtonClicked_10(self): svjs_button_clicked_10(self)
    def svjsButtonClicked_11(self): svjs_button_clicked_11(self)
    def svjsButtonClicked_12(self): svjs_button_clicked_12(self)
    def svjsButtonClicked_13(self): svjs_button_clicked_13(self)
    def svjsButtonClicked_14(self): svjs_button_clicked_14(self, wdzservQ)
    # =================================================================================================================
    def svcButtonClicked_01(self): svc_button_clicked_01(self)
    def svcButtonClicked_02(self): svc_button_clicked_02(self, proc_query, queryQ)
    def svcButtonClicked_03(self): svc_button_clicked_03(self)
    def svcButtonClicked_04(self): svc_button_clicked_04(self, proc_query, queryQ)
    def svcButtonClicked_05(self): svc_button_clicked_05(self)
    def svcButtonClicked_06(self): svc_button_clicked_06(self, proc_query, queryQ)
    def svcButtonClicked_07(self): svc_button_clicked_07(self)
    def svcButtonClicked_08(self): svc_button_clicked_08(self, proc_query, queryQ)
    def svcButtonClicked_09(self): svc_button_clicked_09(self, proc_query, queryQ)
    def svcButtonClicked_10(self): svc_button_clicked_10(self)
    def svcButtonClicked_11(self): svc_button_clicked_11(self)
    # =================================================================================================================
    def svaButtonClicked_01(self): sva_button_clicked_01(self)
    def svaButtonClicked_02(self): sva_button_clicked_02(self, proc_query, queryQ)
    def svoButtonClicked_01(self): svo_button_clicked_01(self)
    def svoButtonClicked_02(self): svo_button_clicked_02(self, proc_query, queryQ)
    def svoButtonClicked_03(self): svo_button_clicked_03(self)
    def svoButtonClicked_04(self): svo_button_clicked_04(self, proc_query, queryQ)
    def svoButtonClicked_05(self): svo_button_clicked_05(self)
    # =================================================================================================================
    # =================================================================================================================
    def cvjbButtonClicked_01(self): cvjb_button_clicked_01(self)
    def cvjbButtonClicked_02(self): cvjb_button_clicked_02(self, proc_query, queryQ)
    def cvjbButtonClicked_03(self): cvjb_button_clicked_03(self)
    def cvjbButtonClicked_04(self): cvjb_button_clicked_04(self, cstgQ)
    def cvjbButtonClicked_05(self): cvjb_button_clicked_05(self)
    def cvjbButtonClicked_06(self): cvjb_button_clicked_06(self)
    def cvjbButtonClicked_07(self): cvjb_button_clicked_07(self)
    def cvjbButtonClicked_08(self): cvjb_button_clicked_08(self)
    def cvjbButtonClicked_09(self): cvjb_button_clicked_09(self)
    def cvjbButtonClicked_10(self): cvjb_button_clicked_10(self)
    def cvjbButtonClicked_11(self): cvjb_button_clicked_11(self)
    def cvjbButtonClicked_12(self): cvjb_button_clicked_12(self, cstgQ)
    # =================================================================================================================
    def cvjButtonClicked_01(self): cvj_button_clicked_01(self)
    def cvjButtonClicked_02(self): cvj_button_clicked_02(self)
    def cvjButtonClicked_03(self): cvj_button_clicked_03(self)
    def cvjButtonClicked_04(self): cvj_button_clicked_04(self)
    def cvjButtonClicked_05(self): cvj_button_clicked_05(self)
    def cvjButtonClicked_06(self): cvj_button_clicked_06(self)
    def cvjButtonClicked_07(self): cvj_button_clicked_07(self)
    def cvjButtonClicked_08(self): cvj_button_clicked_08(self)
    def cvjButtonClicked_09(self): cvj_button_clicked_09(self)
    def cvjButtonClicked_10(self): cvj_button_clicked_10(self)
    def cvjButtonClicked_11(self): cvj_button_clicked_11(self, windowQ, backQ, soundQ, totalQ, liveQ, teleQ)
    def cvjButtonClicked_12(self): cvj_button_clicked_12(self, windowQ, backQ, soundQ, totalQ, liveQ)
    def cvjButtonClicked_13(self): cvj_button_clicked_13(self)
    def cvjButtonClicked_14(self, back_name): cvj_button_clicked_14(self, back_name, windowQ, backQ, soundQ, totalQ, liveQ, teleQ)
    def cvjButtonClicked_15(self, back_name): cvj_button_clicked_15(self, back_name, windowQ, backQ, soundQ, totalQ, liveQ, teleQ)
    def cvjButtonClicked_16(self, back_name): cvj_button_clicked_16(self, back_name, windowQ, backQ, soundQ, totalQ, liveQ)
    def cvjButtonClicked_17(self, back_name): cvj_button_clicked_17(self, back_name, windowQ, backQ, soundQ, totalQ, liveQ)
    def cvjButtonClicked_18(self): cvj_button_clicked_18(self)
    def cvjButtonClicked_19(self): cvj_button_clicked_19(self)
    def cvjButtonClicked_20(self): cvj_button_clicked_20(self)
    def cvjButtonClicked_21(self): cvj_button_clicked_21(self)
    def cvjButtonClicked_22(self): cvj_button_clicked_22(self)
    def cvjButtonClicked_23(self): cvj_button_clicked_23(self, windowQ, backQ, totalQ)
    def cvjButtonClicked_24(self): cvj_button_clicked_24(self, windowQ, backQ, soundQ, totalQ, liveQ, teleQ)
    def cvjButtonClicked_25(self): cvj_button_clicked_25(self)
    # =================================================================================================================
    def cvjsButtonClicked_01(self): cvjs_button_clicked_01(self)
    def cvjsButtonClicked_02(self): cvjs_button_clicked_02(self, proc_query, queryQ)
    def cvjsButtonClicked_03(self): cvjs_button_clicked_03(self)
    def cvjsButtonClicked_04(self): cvjs_button_clicked_04(self, cstgQ)
    def cvjsButtonClicked_05(self): cvjs_button_clicked_05(self)
    def cvjsButtonClicked_06(self): cvjs_button_clicked_06(self)
    def cvjsButtonClicked_07(self): cvjs_button_clicked_07(self)
    def cvjsButtonClicked_08(self): cvjs_button_clicked_08(self)
    def cvjsButtonClicked_09(self): cvjs_button_clicked_09(self)
    def cvjsButtonClicked_10(self): cvjs_button_clicked_10(self)
    def cvjsButtonClicked_11(self): cvjs_button_clicked_11(self)
    def cvjsButtonClicked_12(self): cvjs_button_clicked_12(self)
    def cvjsButtonClicked_13(self): cvjs_button_clicked_13(self)
    def cvjsButtonClicked_14(self): cvjs_button_clicked_14(self, cstgQ)
    # =================================================================================================================
    def cvcButtonClicked_01(self): cvc_button_clicked_01(self)
    def cvcButtonClicked_02(self): cvc_button_clicked_02(self, proc_query, queryQ)
    def cvcButtonClicked_03(self): cvc_button_clicked_03(self)
    def cvcButtonClicked_04(self): cvc_button_clicked_04(self, proc_query, queryQ)
    def cvcButtonClicked_05(self): cvc_button_clicked_05(self)
    def cvcButtonClicked_06(self): cvc_button_clicked_06(self, proc_query, queryQ)
    def cvcButtonClicked_07(self): cvc_button_clicked_07(self)
    def cvcButtonClicked_08(self): cvc_button_clicked_08(self, proc_query, queryQ)
    def cvcButtonClicked_09(self): cvc_button_clicked_09(self, proc_query, queryQ)
    def cvcButtonClicked_10(self): cvc_button_clicked_10(self)
    def cvcButtonClicked_11(self): cvc_button_clicked_11(self)
    # =================================================================================================================
    def cvaButtonClicked_01(self): cva_button_clicked_01(self)
    def cvaButtonClicked_02(self): cva_button_clicked_02(self, proc_query, queryQ)
    def cvoButtonClicked_01(self): cvo_button_clicked_01(self)
    def cvoButtonClicked_02(self): cvo_button_clicked_02(self, proc_query, queryQ)
    def cvoButtonClicked_03(self): cvo_button_clicked_03(self)
    def cvoButtonClicked_04(self): cvo_button_clicked_04(self, proc_query, queryQ)
    def cvoButtonClicked_06(self): cvo_button_clicked_05(self)
    # =================================================================================================================
    # =================================================================================================================
    def BackTestengineShow(self, gubun):  backtest_engine_show(self, gubun)
    def StartBacktestEngine(self, gubun): start_backtest_engine(self, gubun, windowQ, wdzservQ, backQ, totalQ, webcQ)
    # =================================================================================================================
    @staticmethod
    def BackCodeTest1(stg_code):            return back_code_test1(stg_code, testQ)
    @staticmethod
    def BackCodeTest2(vars_code, ga=False): return back_code_test2(vars_code, testQ, ga)
    @staticmethod
    def BackCodeTest3(gubun, conds_code):   return back_code_test3(gubun, conds_code, testQ)
    @staticmethod
    def ClearBacktestQ():                   clear_backtestQ(backQ, totalQ)
    def BacktestProcessKill(self, gubun):   backtest_process_kill(self, gubun, totalQ)
    # =================================================================================================================
    def lvButtonClicked_01(self):       lvbutton_clicked_01(self)
    def lvButtonClicked_02(self):       lvbutton_clicked_02(self)
    def lvButtonClicked_03(self):       lvbutton_clicked_03(self, proc_query, queryQ)
    def lvCheckChanged_01(self, state): lvcheck_changed_01(self, state)
    # =================================================================================================================
    def ctButtonClicked_01(self):       ct_button_clicked_01(self, wdzservQ, qlist)
    def ctButtonClicked_02(self):       ct_button_clicked_02(self, wdzservQ)
    def ctButtonClicked_03(self):       ct_button_clicked_03(self, windowQ, wdzservQ, cstgQ)
    def ctButtonClicked_04(self):       ct_button_clicked_04(self)
    def ctButtonClicked_05(self):       ct_button_clicked_05(self)
    def ctButtonClicked_06(self):       ct_button_clicked_06(self)
    def ctButtonClicked_07(self):       ct_button_clicked_07(self)
    def ctButtonClicked_08(self):       ct_button_clicked_08(self)
    def ctButtonClicked_09(self):       ct_button_clicked_09(self, proc_query, queryQ)
    def TickInput(self, code, gubun):   tick_put(self, code, gubun, windowQ, wdzservQ, ctraderQ, creceivQ, cstgQ)
    # =================================================================================================================
    def hgButtonClicked_01(self, gubun): hg_button_clicked_01(self, gubun, hogaQ)
    def hgButtonClicked_02(self, gubun): hg_button_clicked_02(self, gubun)
    # =================================================================================================================
    def sjButtonClicked_01(self): sj_button_cicked_01(self)
    def sjButtonClicked_02(self): sj_button_cicked_02(self)
    def sjButtonClicked_03(self): sj_button_cicked_03(self)
    def sjButtonClicked_04(self): sj_button_cicked_04(self)
    def sjButtonClicked_05(self): sj_button_cicked_05(self)
    def sjButtonClicked_06(self): sj_button_cicked_06(self)
    def sjButtonClicked_07(self): sj_button_cicked_07(self)
    def sjButtonClicked_08(self): sj_button_cicked_08(self)
    def sjButtonClicked_09(self): sj_button_cicked_09(self, proc_query, queryQ)
    def sjButtonClicked_10(self): sj_button_cicked_10(self, proc_query, queryQ)
    def sjButtonClicked_11(self): sj_button_cicked_11(self, proc_query, queryQ)
    def sjButtonClicked_12(self): sj_button_cicked_12(self, proc_query, queryQ, teleQ)
    def sjButtonClicked_13(self): sj_button_cicked_13(self, proc_query, queryQ)
    def sjButtonClicked_14(self): sj_button_cicked_14(self, proc_query, queryQ)
    def sjButtonClicked_15(self): sj_button_cicked_15(self, proc_query, queryQ)
    def sjButtonClicked_16(self): sj_button_cicked_16(self, proc_query, queryQ)
    def sjButtonClicked_17(self): sj_button_cicked_17(self)
    def sjButtonClicked_19(self): sj_button_cicked_19(self)
    def sjButtonClicked_20(self): sj_button_cicked_20(self)
    def sjButtonClicked_21(self): sj_button_cicked_21(self)
    def sjButtonClicked_22(self): sj_button_cicked_22(self)
    def sjButtonClicked_23(self): sj_button_cicked_23(self, proc_query, queryQ)
    def sjButtonClicked_24(self): sj_button_cicked_24(self, proc_query, queryQ)
    def sjButtonClicked_25(self): sj_button_cicked_25(self, proc_query, queryQ)
    def sjButtonClicked_26(self): sj_button_cicked_26(self, proc_query, queryQ)
    def sjButtonClicked_27(self): sj_button_cicked_27(self)
    def sjButtonClicked_28(self): sj_button_cicked_28(self, proc_query, queryQ)
    def sjButtonClicked_29(self): sj_button_cicked_29(self)
    def sjButtonClicked_30(self): sj_button_cicked_30(self)
    # =================================================================================================================
    def StomLiveProcessAlive(self):       return stom_live_process_alive(self)
    def SimulatorProcessAlive(self):      return simulator_process_alive(self)
    def CoinReceiverProcessAlive(self):   return coin_receiver_process_alive(self)
    def CoinTraderProcessAlive(self):     return coin_trader_process_alive(self)
    def CoinStrategyProcessAlive(self):   return coin_strategy_process_alive(self)
    def CoinKimpProcessAlive(self):       return coinkimp_process_alive(self)
    def BacktestProcessAlive(self):       return backtest_process_alive(self)
    # =================================================================================================================
    def ChartCountChange(self):           chart_count_change(self)
    def ProcessKill(self):                process_kill(self, wdzservQ, queryQ, kimpQ, creceivQ, ctraderQ)
    def keyPressEvent(self, event):       key_press_event(self, event)
    def eventFilter(self, widget, event): return event_filter(self, widget, event)
    def closeEvent(self, a):              close_event(self, a)
    def GetKlist(self):                   return get_k_list(self)
    # =================================================================================================================


if __name__ == '__main__':
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)
    auto_run = 1 if len(sys.argv) > 1 and sys.argv[1] == 'stocklogin' else 0
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--blink-settings=forceDarkModeEnabled=true"
    subprocess.Popen('python64 ./utility/timesync.py')

    windowQ, soundQ, queryQ, teleQ, chartQ, hogaQ, webcQ, backQ, creceivQ, ctraderQ, cstgQ, liveQ, totalQ, testQ, kimpQ, wdzservQ = \
        Queue(), Queue(), Queue(), Queue(), Queue(), Queue(), Queue(), Queue(), Queue(), Queue(), Queue(), Queue(), Queue(), Queue(), Queue(), Queue()
    qlist = [windowQ, soundQ, queryQ, teleQ, chartQ, hogaQ, webcQ, backQ, creceivQ, ctraderQ, cstgQ, liveQ, kimpQ, wdzservQ]

    proc_tele  = Process(target=TelegramMsg, args=(qlist,), daemon=True)
    proc_webc  = Process(target=WebCrawling, args=(qlist,), daemon=True)
    proc_sound = Process(target=Sound, args=(qlist,), daemon=True)
    proc_query = Process(target=Query, args=(qlist,))
    proc_chart = Process(target=Chart, args=(qlist,), daemon=True)
    proc_hoga  = Process(target=Hoga, args=(qlist,), daemon=True)

    proc_tele.start()
    proc_webc.start()
    proc_sound.start()
    proc_query.start()
    proc_chart.start()
    proc_hoga.start()

    app = QApplication(sys.argv)
    app.setStyle('fusion')
    palette = QPalette()
    palette.setColor(QPalette.Window, color_bg_bc)
    palette.setColor(QPalette.Background, color_bg_bc)
    palette.setColor(QPalette.WindowText, color_fg_bc)
    palette.setColor(QPalette.Base, color_bg_bc)
    palette.setColor(QPalette.AlternateBase, color_bg_dk)
    palette.setColor(QPalette.Text, color_fg_bc)
    palette.setColor(QPalette.Button, color_bg_bc)
    palette.setColor(QPalette.ButtonText, color_fg_bc)
    palette.setColor(QPalette.Link, color_fg_bk)
    palette.setColor(QPalette.Highlight, color_fg_hl)
    palette.setColor(QPalette.HighlightedText, color_bg_bk)
    app.setPalette(palette)
    window = Window(auto_run)
    window.show()
    app.exec_()
