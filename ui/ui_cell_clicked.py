import sqlite3
import pandas as pd
from PyQt5.QtCore import QDate, QUrl
from PyQt5.QtWidgets import QMessageBox
from utility.setting import columns_jg, columns_jgf, DB_TRADELIST, ui_num, DB_STRATEGY
from utility.static import strf_time, timedelta_sec, comma2int, comma2float, now


def cell_clicked_01(ui, row, col):
    stock = True
    if ui.focusWidget() in (ui.ctd_tableWidgettt, ui.cgj_tableWidgettt, ui.ccj_tableWidgettt):
        stock = False
    item = ui.focusWidget().item(row, 0)
    if item is None:
        return
    name = item.text()
    linetext = ui.ct_lineEdittttt_03.text()
    tickcount = int(linetext) if linetext != '' else 30
    searchdate = strf_time('%Y%m%d') if stock else strf_time('%Y%m%d', timedelta_sec(-32400))
    code = ui.dict_code[name] if name in ui.dict_code.keys() else name
    ui.ct_lineEdittttt_04.setText(code)
    ui.ct_lineEdittttt_05.setText(name)
    ui.ShowDialog(name, tickcount, searchdate, col)


def cell_clicked_02(ui, row, wdzservQ):
    item = ui.sjg_tableWidgettt.item(row, 0)
    if item is None:
        return
    name = item.text()
    oc = comma2int(ui.sjg_tableWidgettt.item(row, columns_jg.index('보유수량')).text())
    c = comma2int(ui.sjg_tableWidgettt.item(row, columns_jg.index('현재가')).text())
    buttonReply = QMessageBox.question(
        ui, '주식 시장가 매도', f'{name} {oc}주를 시장가매도합니다.\n계속하시겠습니까?\n',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    )
    if buttonReply == QMessageBox.Yes:
        wdzservQ.put(('trader', ('매도', ui.dict_code[name], name, c, oc, now(), True)))


def cell_clicked_03(ui, row, ctraderQ):
    item = ui.cjg_tableWidgettt.item(row, 0)
    if item is None:
        return
    code = item.text()
    columns = columns_jg if 'KRW' in code else columns_jgf
    oc = comma2float(ui.cjg_tableWidgettt.item(row, columns.index('보유수량')).text())
    c = comma2float(ui.cjg_tableWidgettt.item(row, columns.index('현재가')).text())
    buttonReply = QMessageBox.question(
        ui, '코인 시장가 매도', f'{code} {oc}개를 시장가매도합니다.\n계속하시겠습니까?\n',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    )
    if buttonReply == QMessageBox.Yes:
        if ui.CoinTraderProcessAlive():
            if 'KRW' in code:
                ctraderQ.put(('매도', code, c, oc, now(), True))
            else:
                p = ui.cjg_tableWidgettt.item(row, columns_jgf.index('포지션')).text()
                p = 'SELL_LONG' if p == 'LONG' else 'BUY_SHORT'
                ctraderQ.put((p, code, c, oc, now(), True))


def cell_clicked_04(ui, row):
    searchdate = ''
    if ui.focusWidget() == ui.sds_tableWidgettt:
        searchdate = ui.s_calendarWidgett.selectedDate().toString('yyyyMMdd')
    elif ui.focusWidget() == ui.cds_tableWidgettt:
        searchdate = ui.c_calendarWidgett.selectedDate().toString('yyyyMMdd')
    item = ui.focusWidget().item(row, 1)
    if item is None:
        return
    name = item.text()
    linetext = ui.ct_lineEdittttt_03.text()
    tickcount = int(linetext) if linetext != '' else 30
    code = ui.dict_code[name] if name in ui.dict_code.keys() else name
    ui.ct_lineEdittttt_04.setText(code)
    ui.ct_lineEdittttt_05.setText(name)
    ui.ct_dateEdittttt_01.setDate(QDate.fromString(searchdate, 'yyyyMMdd'))
    ui.ShowDialog(name, tickcount, searchdate, 4)


def cell_clicked_05(ui, row):
    gubun = '주식'
    if ui.focusWidget() == ui.cns_tableWidgettt:
        gubun = '코인'
    item = ui.focusWidget().item(row, 0)
    if item is None:
        return
    date = item.text()
    date = date.replace('.', '')
    table_name = 's_tradelist' if gubun == '주식' else 'c_tradelist' if ui.dict_set[
                                                                          '거래소'] == '업비트' else 'c_tradelist_future'

    con = sqlite3.connect(DB_TRADELIST)
    df = pd.read_sql(f"SELECT * FROM {table_name} WHERE 체결시간 LIKE '{date}%'", con)
    con.close()

    if len(date) == 6 and gubun == '코인':
        df['구분용체결시간'] = df['체결시간'].apply(lambda x: x[:6])
        df = df[df['구분용체결시간'] == date]
    elif len(date) == 4 and gubun == '코인':
        df['구분용체결시간'] = df['체결시간'].apply(lambda x: x[:4])
        df = df[df['구분용체결시간'] == date]

    df['index'] = df['index'].apply(lambda x: f'{x[:4]}-{x[4:6]}-{x[6:8]} {x[8:10]}:{x[10:12]}:{x[12:14]}')
    df.set_index('index', inplace=True)
    ui.ShowDialogGraph(df)


def cell_clicked_06(ui, row):
    tableWidget = None
    if ui.focusWidget() == ui.ss_tableWidget_01:
        tableWidget = ui.ss_tableWidget_01
    elif ui.focusWidget() == ui.cs_tableWidget_01:
        tableWidget = ui.cs_tableWidget_01
    if tableWidget is None:
        return
    item = tableWidget.item(row, 0)
    if item is None:
        return

    name = item.text()
    searchdate = tableWidget.item(row, 2).text()[:8]
    buytime = comma2int(tableWidget.item(row, 2).text())
    selltime = comma2int(tableWidget.item(row, 3).text())
    buyprice = comma2float(tableWidget.item(row, 5).text())
    sellprice = comma2float(tableWidget.item(row, 6).text())
    detail = [buytime, buyprice, selltime, sellprice]
    buytimes = tableWidget.item(row, 13).text()

    coin = True if 'KRW' in name or 'USDT' in name else False
    code = ui.dict_code[name] if name in ui.dict_code.keys() else name
    ui.ct_lineEdittttt_04.setText(code)
    ui.ct_lineEdittttt_05.setText(name)
    ui.ct_dateEdittttt_01.setDate(QDate.fromString(searchdate, 'yyyyMMdd'))
    tickcount = int(ui.cvjb_lineEditt_05.text()) if coin else int(ui.svjb_lineEditt_05.text())
    ui.ShowDialogChart(False, coin, code, tickcount, searchdate, ui.ct_lineEdittttt_01.text(),
                       ui.ct_lineEdittttt_02.text(), detail, buytimes)


def cell_clicked_07(ui, row, chartQ):
    item = ui.ct_tableWidgett_01.item(row, 0)
    if item is None:
        return
    name = item.text()
    coin = True if 'KRW' in name or 'USDT' in name else False
    code = ui.dict_code[name] if name in ui.dict_code.keys() else name
    searchdate = ui.ct_dateEdittttt_02.date().toString('yyyyMMdd')
    linetext = ui.ct_lineEdittttt_03.text()
    tickcount = int(linetext) if linetext != '' else 30
    ui.ct_lineEdittttt_04.setText(code)
    ui.ct_lineEdittttt_05.setText(name)
    ui.ct_dateEdittttt_01.setDate(QDate.fromString(searchdate, 'yyyyMMdd'))
    chartQ.put(
        (coin, code, tickcount, searchdate, ui.ct_lineEdittttt_01.text(), ui.ct_lineEdittttt_02.text(), ui.GetKlist()))


def cell_clicked_08(ui, row):
    item = ui.dialog_info.focusWidget().item(row, 3)
    if item is None:
        return
    if ui.dialog_web.isVisible():
        ui.webEngineView.load(QUrl(item.text()))


def cell_clicked_09(ui, row, col, windowQ):
    if ui.dialog_db.focusWidget() == ui.db_tableWidgett_01:
        item = ui.db_tableWidgett_01.item(row, col)
        if item is None:
            return
        stg_name = item.text()
        buttonReply = QMessageBox.question(
            ui.dialog_db, '전략 삭제', f'주식전략 "{stg_name}"을(를) 삭제합니다.\n계속하시겠습니까?\n',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if buttonReply == QMessageBox.Yes:
            con = sqlite3.connect(DB_STRATEGY)
            cur = con.cursor()
            if col == 0:
                query = f'DELETE FROM stockbuy WHERE "index" = "{stg_name}"'
            elif col == 1:
                query = f'DELETE FROM stocksell WHERE "index" = "{stg_name}"'
            elif col == 2:
                query = f'DELETE FROM stockoptibuy WHERE "index" = "{stg_name}"'
            else:
                query = f'DELETE FROM stockoptisell WHERE "index" = "{stg_name}"'
            cur.execute(query)
            con.commit()
            con.close()
            windowQ.put((ui_num['DB관리'], f'DB 명령 실행 알림 - 주식전략 "{stg_name}" 삭제 완료'))
    elif ui.dialog_db.focusWidget() == ui.db_tableWidgett_02:
        item = ui.db_tableWidgett_02.item(row, col)
        if item is None:
            return
        stg_name = item.text()
        buttonReply = QMessageBox.question(
            ui.dialog_db, '범위 또는 조건 삭제', f'주식 범위 또는 조건 "{stg_name}"을(를) 삭제합니다.\n계속하시겠습니까?\n',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if buttonReply == QMessageBox.Yes:
            con = sqlite3.connect(DB_STRATEGY)
            cur = con.cursor()
            if col == 0:
                query = f'DELETE FROM stockoptivars WHERE "index" = "{stg_name}"'
            elif col == 1:
                query = f'DELETE FROM stockvars WHERE "index" = "{stg_name}"'
            elif col == 2:
                query = f'DELETE FROM stockbuyconds WHERE "index" = "{stg_name}"'
            else:
                query = f'DELETE FROM stocksellconds WHERE "index" = "{stg_name}"'
            cur.execute(query)
            con.commit()
            con.close()
            windowQ.put((ui_num['DB관리'], f'DB 명령 실행 알림 - 주식 범위 또는 조건 "{stg_name}" 삭제 완료'))
    elif ui.dialog_db.focusWidget() == ui.db_tableWidgett_03:
        item = ui.db_tableWidgett_03.item(row, col)
        if item is None:
            return
        stg_name = item.text()
        buttonReply = QMessageBox.question(
            ui.dialog_db, '전략 삭제', f'코인전략 "{stg_name}"을(를) 삭제합니다.\n계속하시겠습니까?\n',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if buttonReply == QMessageBox.Yes:
            con = sqlite3.connect(DB_STRATEGY)
            cur = con.cursor()
            if col == 0:
                query = f'DELETE FROM coinbuy WHERE "index" = "{stg_name}"'
            elif col == 1:
                query = f'DELETE FROM coinsell WHERE "index" = "{stg_name}"'
            elif col == 2:
                query = f'DELETE FROM coinoptibuy WHERE "index" = "{stg_name}"'
            else:
                query = f'DELETE FROM coinoptisell WHERE "index" = "{stg_name}"'
            cur.execute(query)
            con.commit()
            con.close()
            windowQ.put((ui_num['DB관리'], f'DB 명령 실행 알림 - 코인전략 "{stg_name}" 삭제 완료'))
    elif ui.dialog_db.focusWidget() == ui.db_tableWidgett_04:
        item = ui.db_tableWidgett_04.item(row, col)
        if item is None:
            return
        stg_name = item.text()
        buttonReply = QMessageBox.question(
            ui.dialog_db, '범위 또는 조건 삭제', f'코인 범위 또는 조건 "{stg_name}"을(를) 삭제합니다.\n계속하시겠습니까?\n',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if buttonReply == QMessageBox.Yes:
            con = sqlite3.connect(DB_STRATEGY)
            cur = con.cursor()
            if col == 0:
                query = f'DELETE FROM coinoptivars WHERE "index" = "{stg_name}"'
            elif col == 1:
                query = f'DELETE FROM coinvars WHERE "index" = "{stg_name}"'
            elif col == 2:
                query = f'DELETE FROM coinbuyconds WHERE "index" = "{stg_name}"'
            else:
                query = f'DELETE FROM coinsellconds WHERE "index" = "{stg_name}"'
            cur.execute(query)
            con.commit()
            con.close()
            windowQ.put((ui_num['DB관리'], f'DB 명령 실행 알림 - 코인 범위 또는 조건 "{stg_name}" 삭제 완료'))
    elif ui.dialog_db.focusWidget() == ui.db_tableWidgett_05:
        item = ui.db_tableWidgett_05.item(row, col)
        if item is None:
            return
        stg_name = item.text()
        buttonReply = QMessageBox.question(
            ui.dialog_db, '스케쥴 삭제', f'스케쥴 "{stg_name}"을(를) 삭제합니다.\n계속하시겠습니까?\n',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if buttonReply == QMessageBox.Yes:
            con = sqlite3.connect(DB_STRATEGY)
            cur = con.cursor()
            query = f'DELETE FROM schedule WHERE "index" = "{stg_name}"'
            cur.execute(query)
            con.commit()
            con.close()
            windowQ.put((ui_num['DB관리'], f'DB 명령 실행 알림 - 스케쥴 "{stg_name}" 삭제 완료'))

    ui.ShowDB()


def cell_clicked_10(ui, row, col):
    item = ui.hg_tableWidgett_01.item(row, col)
    if item is not None:
        text = item.text()
        if '.' in text:
            order_price = comma2float(text)
        else:
            order_price = comma2int(text)
        ui.od_lineEdittttt_01.setText(str(order_price))
        ui.TextChanged_05()


def cell_clicked_11(ui):
    table_name = 's_tradelist' if ui.focusWidget() == ui.snt_tableWidgettt else 'c_tradelist' if ui.dict_set[
                                                                                                     '거래소'] == '업비트' else 'c_tradelist_future'
    con = sqlite3.connect(DB_TRADELIST)
    df = pd.read_sql(f"SELECT * FROM {table_name}", con)
    con.close()
    df['index'] = df['index'].apply(lambda x: f'{x[:4]}-{x[4:6]}-{x[6:8]} {x[8:10]}:{x[10:12]}:{x[12:14]}')
    df.set_index('index', inplace=True)
    ui.ShowDialogGraph(df)
