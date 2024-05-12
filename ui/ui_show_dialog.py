import os
import sqlite3
import pandas as pd
from coin.kimp import Kimp
from PyQt5.QtCore import QUrl, Qt
from multiprocessing import Process
from PyQt5.QtWidgets import QVBoxLayout, QTableWidgetItem
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from utility.static import qtest_qwait
from utility.setting import columns_hc, DB_STRATEGY, DB_COIN_BACK, DB_COIN_TICK, DB_STOCK_BACK, DB_STOCK_TICK, DB_PATH
from ui.set_style import style_bc_bt, style_bc_bb


class QuietPage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, p_str, p_int, p_str_1):
        pass


def show_dialog_graph(ui, df):
    if not ui.dialog_graph.isVisible():
        ui.dialog_graph.show()

    df['이익금액'] = df['수익금'].apply(lambda x: x if x >= 0 else 0)
    df['손실금액'] = df['수익금'].apply(lambda x: x if x < 0 else 0)
    df['수익금합계'] = df['수익금'].cumsum()
    df['수익금합계020'] = df['수익금합계'].rolling(window=20).mean().round(2)
    df['수익금합계060'] = df['수익금합계'].rolling(window=60).mean().round(2)
    df['수익금합계120'] = df['수익금합계'].rolling(window=120).mean().round(2)
    df['수익금합계240'] = df['수익금합계'].rolling(window=240).mean().round(2)
    df['수익금합계480'] = df['수익금합계'].rolling(window=480).mean().round(2)

    ui.canvas2.figure.clear()
    ax = ui.canvas2.figure.add_subplot(111)
    ax.bar(df.index, df['이익금액'], label='이익금액', color='r')
    ax.bar(df.index, df['손실금액'], label='손실금액', color='b')
    ax.plot(df.index, df['수익금합계480'], linewidth=0.5, label='수익금합계480', color='k')
    ax.plot(df.index, df['수익금합계240'], linewidth=0.5, label='수익금합계240', color='gray')
    ax.plot(df.index, df['수익금합계120'], linewidth=0.5, label='수익금합계120', color='b')
    ax.plot(df.index, df['수익금합계060'], linewidth=0.5, label='수익금합계60', color='g')
    ax.plot(df.index, df['수익금합계020'], linewidth=0.5, label='수익금합계20', color='r')
    ax.plot(df.index, df['수익금합계'], linewidth=2, label='수익금합계', color='orange')
    count = int(len(df) / 20) if int(len(df) / 20) >= 1 else 1
    ax.set_xticks(list(df.index[::count]))
    ax.tick_params(axis='x', labelrotation=45)
    ax.legend(loc='best')
    ax.grid()
    ui.canvas2.figure.tight_layout()
    ui.canvas2.draw()


def show_dialog(ui, code_or_name, tickcount, searchdate, col):
    coin = False
    if code_or_name in ui.dict_code.keys():
        code = ui.dict_code[code_or_name]
    elif code_or_name in ui.dict_code.values():
        code = code_or_name
    else:
        code = code_or_name
        coin = True

    if col == 0:
        if not coin:
            ui.ShowDialogWeb(True, code)
        else:
            ui.ShowDialogHoga(True, coin, code)
    elif col == 1:
        if not coin:
            ui.ShowDialogWeb(False, code)
        ui.ShowDialogHoga(True, coin, code)
    elif col < 4:
        if not coin:
            ui.ShowDialogWeb(False, code)
        ui.ShowDialogHoga(False, coin, code)
        ui.ShowDialogChart(True, coin, code)
    else:
        if not coin:
            ui.ShowDialogWeb(False, code)
        ui.ShowDialogHoga(False, coin, code)
        ui.ShowDialogChart(False, coin, code, tickcount, searchdate, ui.ct_lineEdittttt_01.text(),
                           ui.ct_lineEdittttt_02.text())


def show_dialog_web(ui, show, code, webcQ):
    if ui.webEngineView is None:
        ui.webEngineView = QWebEngineView()
        p = QuietPage(ui.webEngineView)
        ui.webEngineView.setPage(p)
        web_layout = QVBoxLayout(ui.dialog_web)
        web_layout.setContentsMargins(0, 0, 0, 0)
        web_layout.addWidget(ui.webEngineView)
    if show and not ui.dialog_web.isVisible():
        ui.dialog_web.show()
    if show and not ui.dialog_info.isVisible():
        ui.dialog_info.show()
    if ui.dialog_web.isVisible() and ui.dialog_info.isVisible():
        ui.webEngineView.load(QUrl(f'https://finance.naver.com/item/main.naver?code={code}'))
        webcQ.put(('기업정보', code))


def show_dialog_hoga(ui, show, coin, code):
    if show and not ui.dialog_hoga.isVisible():
        ui.dialog_hoga.show()
    if ui.dialog_hoga.isVisible():
        ui.PutHogaCode(coin, code)
    if ui.dialog_order.isVisible():
        change = False
        if 'KRW' not in code and 'USDT' not in code:
            name = ui.dict_name[code]
            if name not in ui.order_combo_name_list:
                ui.od_comboBoxxxxx_01.addItem(name)
            ui.od_comboBoxxxxx_01.setCurrentText(name)
            for i in range(100):
                item = ui.sjg_tableWidgettt.item(i, 0)
                if item is not None:
                    if name == item.text():
                        count = ui.sjg_tableWidgettt.item(i, 7).text()
                        ui.od_lineEdittttt_02.setText(count)
                        change = True
                        break
                else:
                    break
        else:
            if code not in ui.order_combo_name_list:
                ui.od_comboBoxxxxx_01.addItem(code)
            ui.od_comboBoxxxxx_01.setCurrentText(code)
            for i in range(100):
                item = ui.cjg_tableWidgettt.item(i, 0)
                if item is not None:
                    if code == item.text():
                        count = ui.cjg_tableWidgettt.item(i, 7 if 'KRW' in code else 8).text()
                        ui.od_lineEdittttt_02.setText(count)
                        change = True
                        break
                else:
                    break
        if not change:
            ui.od_lineEdittttt_01.setText('')
            ui.od_lineEdittttt_02.setText('')


def show_dialog_chart(ui, real, coin, code, proc_chart, cstgQ, wdzservQ, chartQ, tickcount, searchdate, starttime,
                      endtime, detail, buytimes):
    if not ui.dialog_chart.isVisible():
        if ui.main_btn in (1, 3):
            ui.ct_lineEdittttt_01.setText('0')
            ui.ct_lineEdittttt_02.setText('235959')
        else:
            ui.ct_lineEdittttt_01.setText('90000')
            ui.ct_lineEdittttt_02.setText('93000')
        ui.dialog_chart.show()
    if ui.dialog_chart.isVisible() and proc_chart.is_alive():
        if real:
            ui.ChartClear()
            if coin:
                if ui.CoinStrategyProcessAlive(): cstgQ.put(('차트종목코드', code))
            else:
                wdzservQ.put(('strategy', ('차트종목코드', code, ui.dict_sgbn[code])))
        else:
            ui.ChartClear()
            if detail is None:
                chartQ.put((coin, code, tickcount, searchdate, starttime, endtime, ui.GetKlist()))
            else:
                chartQ.put((coin, code, tickcount, searchdate, starttime, endtime, ui.GetKlist(), detail, buytimes))


def show_dialog_chart2(ui):
    if ui.ct_pushButtonnn_06.text() == '확장':
        if ui.ct_pushButtonnn_04.text() == 'CHART 8':
            width = 1528
        elif ui.ct_pushButtonnn_04.text() == 'CHART 12':
            width = 2213
        else:
            width = 2898
        ui.dialog_chart.setFixedSize(width, 1370 if not ui.dict_set['저해상도'] else 1010)
        ui.ct_pushButtonnn_06.setText('주식')
        ui.ct_pushButtonnn_06.setStyleSheet(style_bc_bb)
        ui.ChartMoneyTopList()
    elif ui.ct_pushButtonnn_06.text() == '주식':
        ui.ct_pushButtonnn_06.setText('코인')
        ui.ChartMoneyTopList()
    elif ui.ct_pushButtonnn_06.text() == '코인':
        if ui.ct_pushButtonnn_04.text() == 'CHART 8':
            width = 1403
        elif ui.ct_pushButtonnn_04.text() == 'CHART 12':
            width = 2088
        else:
            width = 2773
        ui.dialog_chart.setFixedSize(width, 1370 if not ui.dict_set['저해상도'] else 1010)
        ui.ct_pushButtonnn_06.setText('확장')
        ui.ct_pushButtonnn_06.setStyleSheet(style_bc_bt)


def show_qsize(ui):
    if not ui.showQsize:
        ui.qs_pushButton.setStyleSheet(style_bc_bt)
        ui.showQsize = True
    else:
        ui.qs_pushButton.setStyleSheet(style_bc_bb)
        ui.showQsize = False


def show_dialog_factor(ui):
    ui.dialog_factor.show() if not ui.dialog_factor.isVisible() else ui.dialog_factor.close()


def show_dialog_test(ui):
    if not ui.dialog_test.isVisible():
        ui.ct_pushButtonnn_05.setStyleSheet(style_bc_bt)
        ui.dialog_test.show()
    else:
        ui.ct_pushButtonnn_05.setStyleSheet(style_bc_bb)
        ui.dialog_test.close()


def show_chart(ui):
    if not ui.dialog_chart.isVisible():
        if ui.main_btn in (1, 3):
            ui.ct_lineEdittttt_01.setText('0')
            ui.ct_lineEdittttt_02.setText('235959')
        else:
            ui.ct_lineEdittttt_01.setText('90000')
            ui.ct_lineEdittttt_02.setText('93000')
        ui.dialog_chart.show()
    else:
        ui.dialog_chart.close()


def show_hoga(ui):
    if not ui.dialog_hoga.isVisible():
        ui.dialog_hoga.setFixedSize(572, 355)
        ui.hj_tableWidgett_01.setGeometry(5, 5, 562, 42)
        ui.hj_tableWidgett_01.setColumnWidth(0, 140)
        ui.hj_tableWidgett_01.setColumnWidth(1, 140)
        ui.hj_tableWidgett_01.setColumnWidth(2, 140)
        ui.hj_tableWidgett_01.setColumnWidth(3, 140)
        ui.hj_tableWidgett_01.setColumnWidth(4, 140)
        ui.hj_tableWidgett_01.setColumnWidth(5, 140)
        ui.hj_tableWidgett_01.setColumnWidth(6, 140)
        ui.hj_tableWidgett_01.setColumnWidth(7, 140)
        ui.hc_tableWidgett_01.setHorizontalHeaderLabels(columns_hc)
        ui.hc_tableWidgett_02.setVisible(False)
        ui.hg_tableWidgett_01.setGeometry(285, 52, 282, 297)
        ui.dialog_hoga.show()
    else:
        ui.dialog_hoga.close()


def show_giup(ui):
    if ui.webEngineView is None:
        ui.webEngineView = QWebEngineView()
        p = QuietPage(ui.webEngineView)
        ui.webEngineView.setPage(p)
        web_layout = QVBoxLayout(ui.dialog_web)
        web_layout.setContentsMargins(0, 0, 0, 0)
        web_layout.addWidget(ui.webEngineView)
    if not ui.dialog_web.isVisible():
        ui.dialog_web.show()
        ui.webEngineView.load(QUrl('https://markets.hankyung.com/'))
    else:
        ui.dialog_web.close()
    ui.dialog_info.show() if not ui.dialog_info.isVisible() else ui.dialog_info.close()


def show_treemap(ui, webcQ):
    if not ui.dialog_tree.isVisible():
        ui.dialog_tree.show()
        webcQ.put(('트리맵', ''))
    else:
        ui.dialog_tree.close()


def show_jisu(ui):
    ui.dialog_jisu.show() if not ui.dialog_jisu.isVisible() else ui.dialog_jisu.close()


def show_db(ui):
    if not ui.dialog_db.isVisible():
        ui.dialog_db.show()

    ui.db_tableWidgett_01.clearContents()
    ui.db_tableWidgett_02.clearContents()
    ui.db_tableWidgett_03.clearContents()
    ui.db_tableWidgett_04.clearContents()
    ui.db_tableWidgett_05.clearContents()

    con = sqlite3.connect(DB_STRATEGY)

    stock_stg_list = ['stockbuy', 'stocksell', 'stockoptibuy', 'stockoptisell']
    maxlow = 0
    for i, stock_stg in enumerate(stock_stg_list):
        df = pd.read_sql(f'SELECT * FROM {stock_stg}', con)
        stg_names = df['index'].to_list()
        stg_names.sort()
        if len(df) > maxlow:
            maxlow = len(df)
            ui.db_tableWidgett_01.setRowCount(maxlow)
        for j, stg_name in enumerate(stg_names):
            item = QTableWidgetItem(stg_name)
            item.setTextAlignment(int(Qt.AlignVCenter | Qt.AlignCenter))
            ui.db_tableWidgett_01.setItem(j, i, item)
    if maxlow < 8:
        ui.db_tableWidgett_01.setRowCount(8)

    stock_stg_list = ['stockoptivars', 'stockvars', 'stockbuyconds', 'stocksellconds']
    maxlow = 0
    for i, stock_stg in enumerate(stock_stg_list):
        df = pd.read_sql(f'SELECT * FROM {stock_stg}', con)
        stg_names = df['index'].to_list()
        stg_names.sort()
        if len(df) > maxlow:
            maxlow = len(df)
            ui.db_tableWidgett_02.setRowCount(maxlow)
        for j, stg_name in enumerate(stg_names):
            item = QTableWidgetItem(stg_name)
            item.setTextAlignment(int(Qt.AlignVCenter | Qt.AlignCenter))
            ui.db_tableWidgett_02.setItem(j, i, item)
    if maxlow < 8:
        ui.db_tableWidgett_02.setRowCount(8)

    maxlow = 0
    coin_stg_list = ['coinbuy', 'coinsell', 'coinoptibuy', 'coinoptisell']
    for i, coin_stg in enumerate(coin_stg_list):
        df = pd.read_sql(f'SELECT * FROM {coin_stg}', con)
        stg_names = df['index'].to_list()
        stg_names.sort()
        if len(df) > maxlow:
            maxlow = len(df)
            ui.db_tableWidgett_03.setRowCount(maxlow)
        for j, stg_name in enumerate(stg_names):
            item = QTableWidgetItem(stg_name)
            item.setTextAlignment(int(Qt.AlignVCenter | Qt.AlignCenter))
            ui.db_tableWidgett_03.setItem(j, i, item)
    if maxlow < 8:
        ui.db_tableWidgett_03.setRowCount(8)

    stock_stg_list = ['coinoptivars', 'coinvars', 'coinbuyconds', 'coinsellconds']
    maxlow = 0
    for i, stock_stg in enumerate(stock_stg_list):
        df = pd.read_sql(f'SELECT * FROM {stock_stg}', con)
        stg_names = df['index'].to_list()
        stg_names.sort()
        if len(df) > maxlow:
            maxlow = len(df)
            ui.db_tableWidgett_04.setRowCount(maxlow)
        for j, stg_name in enumerate(stg_names):
            item = QTableWidgetItem(stg_name)
            item.setTextAlignment(int(Qt.AlignVCenter | Qt.AlignCenter))
            ui.db_tableWidgett_04.setItem(j, i, item)
    if maxlow < 8:
        ui.db_tableWidgett_04.setRowCount(8)

    df = pd.read_sql(f'SELECT * FROM schedule', con)
    stg_names = df['index'].to_list()
    stg_names.sort()
    if len(df) > maxlow:
        maxlow = len(df)
        ui.db_tableWidgett_05.setRowCount(maxlow)
    for j, stg_name in enumerate(stg_names):
        item = QTableWidgetItem(stg_name)
        item.setTextAlignment(int(Qt.AlignVCenter | Qt.AlignCenter))
        ui.db_tableWidgett_05.setItem(j, 0, item)
    if maxlow < 8:
        ui.db_tableWidgett_05.setRowCount(8)

    con.close()


def show_backscheduler(ui):
    ui.dialog_scheduler.show() if not ui.dialog_scheduler.isVisible() else ui.dialog_scheduler.close()


def show_kimp(ui, qlist):
    if not ui.dialog_kimp.isVisible():
        ui.dialog_kimp.show()
        if not ui.CoinKimpProcessAlive():
            ui.proc_coin_kimp = Process(target=Kimp, args=(qlist,))
            ui.proc_coin_kimp.start()
    else:
        ui.dialog_kimp.close()
        if ui.CoinKimpProcessAlive():
            ui.proc_coin_kimp.kill()
            qtest_qwait(3)


def show_order(ui):
    if not ui.dialog_order.isVisible():
        ui.dialog_order.show()

        tableWidget = None
        if ui.main_btn == 0:
            tableWidget = ui.sgj_tableWidgettt
        elif ui.main_btn == 1:
            tableWidget = ui.cgj_tableWidgettt

        if tableWidget is not None:
            ui.od_comboBoxxxxx_01.clear()
            for row in range(100):
                item = tableWidget.item(row, 0)
                if item is not None:
                    name = item.text()
                    ui.order_combo_name_list.append(name)
                    ui.od_comboBoxxxxx_01.addItem(name)
                else:
                    break
    else:
        ui.dialog_order.close()


def show_video(ui):
    ui.videoWidget.setVisible(True)
    ui.mediaPlayer.play()


def put_hoga_code(ui, coin, code, wdzservQ, creceivQ):
    if coin:
        wdzservQ.put(('receiver', ('호가종목코드', '000000')))
        if ui.CoinReceiverProcessAlive():  creceivQ.put(('호가종목코드', code))
    else:
        if ui.CoinReceiverProcessAlive():  creceivQ.put(('호가종목코드', '000000'))
        wdzservQ.put(('receiver', ('호가종목코드', code)))


def chart_moneytop_list(ui):
    searchdate = ui.ct_dateEdittttt_02.date().toString('yyyyMMdd')
    starttime = ui.ct_lineEdittttt_01.text()
    endtime = ui.ct_lineEdittttt_02.text()
    coin = True if ui.ct_pushButtonnn_06.text() == '코인' else False

    if coin:
        db_name1 = f'{DB_PATH}/coin_tick_{searchdate}.db'
        db_name2 = DB_COIN_BACK
        db_name3 = DB_COIN_TICK
    else:
        db_name1 = f'{DB_PATH}/stock_tick_{searchdate}.db'
        db_name2 = DB_STOCK_BACK
        db_name3 = DB_STOCK_TICK

    df = None
    try:
        if os.path.isfile(db_name1):
            con = sqlite3.connect(db_name1)
            df = pd.read_sql(
                f"SELECT * FROM moneytop WHERE `index` LIKE '{searchdate}%' and `index` % 1000000 >= {starttime} and `index` % 1000000 <= {endtime}",
                con)
            con.close()
        elif os.path.isfile(db_name2):
            con = sqlite3.connect(db_name2)
            df = pd.read_sql(
                f"SELECT * FROM moneytop WHERE `index` LIKE '{searchdate}%' and `index` % 1000000 >= {starttime} and `index` % 1000000 <= {endtime}",
                con)
            con.close()
        elif os.path.isfile(db_name3):
            con = sqlite3.connect(db_name3)
            df = pd.read_sql(
                f"SELECT * FROM moneytop WHERE `index` LIKE '{searchdate}%' and `index` % 1000000 >= {starttime} and `index` % 1000000 <= {endtime}",
                con)
            con.close()
    except:
        pass

    if df is None or len(df) == 0:
        ui.ct_tableWidgett_01.clearContents()
        return

    table_list = list(set(';'.join(df['거래대금순위'].to_list()[30:]).split(';')))
    name_list = [ui.dict_name[code] if code in ui.dict_name.keys() else code for code in
                 table_list] if not coin else table_list
    name_list.sort()

    ui.ct_tableWidgett_01.setRowCount(len(name_list))
    for i, name in enumerate(name_list):
        item = QTableWidgetItem(name)
        item.setTextAlignment(int(Qt.AlignVCenter | Qt.AlignLeft))
        ui.ct_tableWidgett_01.setItem(i, 0, item)
    if len(name_list) < 100:
        ui.ct_tableWidgett_01.setRowCount(100)
