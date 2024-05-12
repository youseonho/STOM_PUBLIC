import psutil
import sqlite3
import pandas as pd
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QApplication
from utility.setting import DB_TRADELIST
from utility.setting import columns_dt, columns_dd, ui_num
from utility.static import thread_decorator, qtest_qwait, strf_time


def update_image(ui, data):
    ui.image_label1.clear()
    qpix = QPixmap()
    qpix.loadFromData(data[1])
    qpix = qpix.scaled(QSize(335, 105), Qt.IgnoreAspectRatio)
    ui.image_label1.setPixmap(qpix)
    ui.image_label2.clear()
    qpix = QPixmap()
    qpix.loadFromData(data[2])
    qpix = qpix.scaled(QSize(335, 602), Qt.IgnoreAspectRatio)
    ui.image_label2.setPixmap(qpix)


def update_sqsize(ui, data):
    ui.srqsize, ui.stqsize, ui.ssqsize = data


@thread_decorator
def update_cpuper(ui):
    ui.cpu_per = int(psutil.cpu_percent(interval=1))


def auto_back_schedule(ui, gubun, soundQ, teleQ):
    if gubun == 1:
        ui.auto_mode = True
        if ui.dict_set['주식알림소리'] or ui.dict_set['코인알림소리']:
            soundQ.put('예약된 백테스트 스케쥴러를 시작합니다.')
        if not ui.dialog_backengine.isVisible():
            ui.BackTestengineShow(ui.dict_set['백테스케쥴구분'])
        qtest_qwait(2)
        ui.BacktestEngineKill()
        qtest_qwait(3)
        ui.StartBacktestEngine(ui.dict_set['백테스케쥴구분'])
    elif gubun == 2:
        if not ui.dialog_scheduler.isVisible():
            ui.dialog_scheduler.show()
        qtest_qwait(2)
        ui.sdButtonClicked_04()
        qtest_qwait(2)
        ui.sd_pushButtonnn_01.setText(ui.dict_set['백테스케쥴구분'])
        ui.sd_dcomboBoxxxx_01.setCurrentText(ui.dict_set['백테스케쥴명'])
        qtest_qwait(2)
        ui.sdButtonClicked_02()
    elif gubun == 3:
        if ui.dialog_scheduler.isVisible():
            ui.dialog_scheduler.close()
        teleQ.put('백테스트 스케쥴러 완료')
        ui.auto_mode = False


def update_dictset(ui, wdzservQ, creceivQ, ctraderQ, cstgQ, chartQ, proc_chart):
    wdzservQ.put(('manager', ('설정변경', ui.dict_set)))
    if ui.CoinReceiverProcessAlive(): creceivQ.put(('설정변경', ui.dict_set))
    if ui.CoinTraderProcessAlive():   ctraderQ.put(('설정변경', ui.dict_set))
    if ui.CoinStrategyProcessAlive(): cstgQ.put(('설정변경', ui.dict_set))
    if proc_chart.is_alive():         chartQ.put(('설정변경', ui.dict_set))
    if ui.backtest_engine:
        for bpq in ui.back_eques:
            bpq.put(('설정변경', ui.dict_set))


def chart_clear(ui):
    ui.ctpg_tik_name = None
    ui.ctpg_tik_cline = None
    ui.ctpg_tik_hline = None
    ui.ctpg_tik_xticks = None
    ui.ctpg_tik_arry = None
    ui.ctpg_tik_legend = {}
    ui.ctpg_tik_item = {}
    ui.ctpg_tik_data = {}
    ui.ctpg_tik_factors = []
    ui.ctpg_tik_labels = []

    ui.ctpg_day_name = None
    ui.ctpg_day_index = None
    ui.ctpg_day_lastmoveavg = None
    ui.ctpg_day_lastcandle = None
    ui.ctpg_day_infiniteline = None
    ui.ctpg_day_lastmoneybar = None
    ui.ctpg_day_legend1 = None
    ui.ctpg_day_legend2 = None
    ui.ctpg_day_ymin = 0
    ui.ctpg_day_ymax = 0

    ui.ctpg_min_name = None
    ui.ctpg_min_index = None
    ui.ctpg_min_lastmoveavg = None
    ui.ctpg_min_lastcandle = None
    ui.ctpg_min_infiniteline = None
    ui.ctpg_min_lastmoneybar = None
    ui.ctpg_min_legend1 = None
    ui.ctpg_min_legend2 = None
    ui.ctpg_min_ymin = 0
    ui.ctpg_min_ymax = 0


def calendar_clicked(ui, gubun):
    if gubun == 'S':
        table = 's_tradelist'
        searchday = ui.s_calendarWidgett.selectedDate().toString('yyyyMMdd')
    else:
        table = 'c_tradelist' if ui.dict_set['거래소'] == '업비트' else 'c_tradelist_future'
        searchday = ui.c_calendarWidgett.selectedDate().toString('yyyyMMdd')
    con = sqlite3.connect(DB_TRADELIST)
    df1 = pd.read_sql(f"SELECT * FROM {table} WHERE 체결시간 LIKE '{searchday}%'", con).set_index('index')
    con.close()
    if len(df1) > 0:
        df1.sort_values(by=['체결시간'], ascending=True, inplace=True)
        if table == 'c_tradelist_future':
            df1 = df1[['체결시간', '종목명', '포지션', '매수금액', '매도금액', '주문수량', '수익률', '수익금']]
        else:
            df1 = df1[['체결시간', '종목명', '매수금액', '매도금액', '주문수량', '수익률', '수익금']]
        nbg, nsg = df1['매수금액'].sum(), df1['매도금액'].sum()
        sp = round((nsg / nbg - 1) * 100, 2)
        npg, nmg, nsig = df1[df1['수익금'] > 0]['수익금'].sum(), df1[df1['수익금'] < 0]['수익금'].sum(), df1['수익금'].sum()
        df2 = pd.DataFrame(columns=columns_dt)
        df2.loc[0] = searchday, nbg, nsg, npg, nmg, sp, nsig
    else:
        df1 = pd.DataFrame(columns=columns_dd)
        df2 = pd.DataFrame(columns=columns_dt)
    ui.update_tablewidget.update_tablewidget((ui_num[f'{gubun}당일합계'], df2))
    ui.update_tablewidget.update_tablewidget((ui_num[f'{gubun}당일상세'], df1))


def video_widget_close(ui, state):
    if state == QMediaPlayer.StoppedState:
        ui.videoWidget.setVisible(False)


def stom_live_screenshot(ui, cmd, teleQ):
    ui.mnButtonClicked_01(4)
    qtest_qwait(1)
    if cmd == 'S스톰라이브':
        mid = 'S'
        ui.slv_tapWidgett_01.setCurrentIndex(ui.slv_index1)
    elif cmd == 'C스톰라이브':
        mid = 'C'
        ui.slv_tapWidgett_01.setCurrentIndex(ui.slv_index2)
    else:
        mid = 'B'
        ui.slv_tapWidgett_01.setCurrentIndex(ui.slv_index3)
    qtest_qwait(1)
    file_name = f'./_log/StomLive_{mid}_{strf_time("%Y%m%d%H%M%S")}.png'
    screen = QApplication.primaryScreen()
    screenshot = screen.grabWindow(ui.winId())
    screenshot.save(file_name, 'png')
    teleQ.put(file_name)
    ui.mnButtonClicked_01(0)
