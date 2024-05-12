import sqlite3
import pandas as pd
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QApplication
from utility.setting import DB_TRADELIST
from utility.static import strf_time, timedelta_sec, comma2int, comma2float


def key_press_event(ui, event):
    if event.key() in (Qt.Key_Return, Qt.Key_Enter):
        if ui.dialog_scheduler.focusWidget() == ui.sd_dpushButtonn_01:
            return
        elif QApplication.keyboardModifiers() & Qt.AltModifier:
            if ui.BacktestProcessAlive():
                if ui.main_btn == 2:
                    ui.ssButtonClicked_06()
                elif ui.main_btn == 3:
                    ui.csButtonClicked_06()
            else:
                if ui.main_btn == 2:
                    if ui.svj_pushButton_01.isVisible():
                        ui.svjButtonClicked_11()
                elif ui.main_btn == 3:
                    if ui.cvj_pushButton_01.isVisible():
                        ui.cvjButtonClicked_11()
        elif ui.focusWidget() in (ui.std_tableWidgettt, ui.sgj_tableWidgettt, ui.scj_tableWidgettt, ui.ctd_tableWidgettt, ui.cgj_tableWidgettt, ui.ccj_tableWidgettt):
            stock = True
            if ui.focusWidget() in (ui.ctd_tableWidgettt, ui.cgj_tableWidgettt, ui.ccj_tableWidgettt):
                stock = False
            row  = ui.focusWidget().currentIndex().row()
            col  = ui.focusWidget().currentIndex().column()
            item = ui.focusWidget().item(row, 0)
            if item is not None:
                name       = item.text()
                linetext   = ui.ct_lineEdittttt_03.text()
                tickcount  = int(linetext) if linetext != '' else 30
                searchdate = strf_time('%Y%m%d') if stock else strf_time('%Y%m%d', timedelta_sec(-32400))
                code       = ui.dict_code[name] if name in ui.dict_code.keys() else name
                ui.ct_lineEdittttt_04.setText(code)
                ui.ct_lineEdittttt_05.setText(name)
                ui.ShowDialog(name, tickcount, searchdate, col)
        elif ui.focusWidget() in (ui.sds_tableWidgettt, ui.cds_tableWidgettt):
            if ui.focusWidget() == ui.sds_tableWidgettt:
                searchdate  = ui.s_calendarWidgett.selectedDate().toString('yyyyMMdd')
            else:
                searchdate  = ui.c_calendarWidgett.selectedDate().toString('yyyyMMdd')
            row  = ui.focusWidget().currentIndex().row()
            item = ui.focusWidget().item(row, 1)
            if item is not None:
                name      = item.text()
                linetext  = ui.ct_lineEdittttt_03.text()
                tickcount = int(linetext) if linetext != '' else 30
                code      = ui.dict_code[name] if name in ui.dict_code.keys() else name
                ui.ct_lineEdittttt_04.setText(code)
                ui.ct_lineEdittttt_05.setText(name)
                ui.ct_dateEdittttt_01.setDate(QDate.fromString(searchdate, 'yyyyMMdd'))
                ui.ShowDialog(name, tickcount, searchdate, 4)
        elif ui.focusWidget() in (ui.sns_tableWidgettt, ui.cns_tableWidgettt):
            if ui.focusWidget() == ui.sns_tableWidgettt:
                gubun = '주식'
            else:
                gubun = '코인'
            row  = ui.focusWidget().currentIndex().row()
            item = ui.focusWidget().item(row, 0)
            if item is not None:
                date = item.text()
                date = date.replace('.', '')
                if gubun == '주식':
                    table_name = 's_tradelist'
                elif ui.dict_set['거래소'] == '업비트':
                    table_name = 'c_tradelist'
                else:
                    table_name = 'c_tradelist_future'
                con = sqlite3.connect(DB_TRADELIST)
                df  = pd.read_sql(f"SELECT * FROM {table_name} WHERE 체결시간 LIKE '{date}%'", con)
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
        elif ui.focusWidget() in (ui.ss_tableWidget_01, ui.cs_tableWidget_01):
            tableWidget  = ui.ss_tableWidget_01 if ui.focusWidget() == ui.ss_tableWidget_01 else ui.cs_tableWidget_01
            row  = tableWidget.currentIndex().row()
            item = tableWidget.item(row, 0)
            if item is not None:
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
                ui.ShowDialogChart(False, coin, code, 30, searchdate, ui.ct_lineEdittttt_01.text(), ui.ct_lineEdittttt_02.text(), detail, buytimes)
    elif event.key() in (Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_5, Qt.Key_6, Qt.Key_7, Qt.Key_8, Qt.Key_9, Qt.Key_0):
        if QApplication.keyboardModifiers() & Qt.ControlModifier:
            if ui.main_btn == 2:
                if event.key() == Qt.Key_1:
                    ui.svjButtonClicked_09()
                elif event.key() == Qt.Key_2:
                    ui.svjButtonClicked_05()
                elif event.key() == Qt.Key_3:
                    ui.svjButtonClicked_01()
                elif event.key() == Qt.Key_4:
                    ui.svjButtonClicked_02()
                elif event.key() == Qt.Key_5:
                    ui.svjButtonClicked_03()
                elif event.key() == Qt.Key_6:
                    ui.svjButtonClicked_10()
                elif event.key() == Qt.Key_7:
                    ui.svjButtonClicked_04()
                elif event.key() == Qt.Key_8:
                    ui.svjButtonClicked_06()
                elif event.key() == Qt.Key_9:
                    ui.svjButtonClicked_07()
                elif event.key() == Qt.Key_0:
                    ui.svjButtonClicked_08()
            elif ui.main_btn == 3:
                if event.key() == Qt.Key_1:
                    ui.cvjButtonClicked_09()
                elif event.key() == Qt.Key_2:
                    ui.cvjButtonClicked_05()
                elif event.key() == Qt.Key_3:
                    ui.cvjButtonClicked_01()
                elif event.key() == Qt.Key_4:
                    ui.cvjButtonClicked_02()
                elif event.key() == Qt.Key_5:
                    ui.cvjButtonClicked_03()
                elif event.key() == Qt.Key_6:
                    ui.cvjButtonClicked_10()
                elif event.key() == Qt.Key_7:
                    ui.cvjButtonClicked_04()
                elif event.key() == Qt.Key_8:
                    ui.cvjButtonClicked_06()
                elif event.key() == Qt.Key_9:
                    ui.cvjButtonClicked_07()
                elif event.key() == Qt.Key_0:
                    ui.cvjButtonClicked_08()
    elif event.key() == Qt.Key_F4:
        if ui.main_btn == 2:
            if ui.svj_pushButton_01.isVisible():
                ui.ss_textEditttt_01.setFocus()
                ui.svjbButtonClicked_02()
            elif ui.svc_pushButton_06.isVisible() or ui.svc_pushButton_15.isVisible() or ui.svc_pushButton_18.isVisible() or ui.sva_pushButton_01.isVisible():
                ui.ss_textEditttt_03.setFocus()
                ui.svcButtonClicked_02()
            elif ui.svo_pushButton_05.isVisible():
                ui.ss_textEditttt_07.setFocus()
                ui.svoButtonClicked_02()
        elif ui.main_btn == 3:
            if ui.cvj_pushButton_01.isVisible():
                ui.cs_textEditttt_01.setFocus()
                ui.cvjbButtonClicked_02()
            elif ui.cvc_pushButton_06.isVisible() or ui.cvc_pushButton_15.isVisible() or ui.cvc_pushButton_18.isVisible() or ui.cva_pushButton_01.isVisible():
                ui.cs_textEditttt_03.setFocus()
                ui.cvcButtonClicked_02()
            elif ui.cvo_pushButton_05.isVisible():
                ui.cs_textEditttt_07.setFocus()
                ui.cvoButtonClicked_02()
    elif event.key() == Qt.Key_F8:
        if ui.main_btn == 2:
            if ui.svj_pushButton_01.isVisible():
                ui.ss_textEditttt_02.setFocus()
                ui.svjsButtonClicked_02()
            elif ui.svc_pushButton_06.isVisible() or ui.svc_pushButton_15.isVisible() or ui.svc_pushButton_18.isVisible() or ui.sva_pushButton_01.isVisible():
                ui.ss_textEditttt_04.setFocus()
                ui.svcButtonClicked_06()
            elif ui.svo_pushButton_05.isVisible():
                ui.ss_textEditttt_08.setFocus()
                ui.svoButtonClicked_04()
        elif ui.main_btn == 3:
            if ui.cvj_pushButton_01.isVisible():
                ui.cs_textEditttt_02.setFocus()
                ui.cvjsButtonClicked_02()
            elif ui.cvc_pushButton_06.isVisible() or ui.cvc_pushButton_15.isVisible() or ui.cvc_pushButton_18.isVisible() or ui.cva_pushButton_01.isVisible():
                ui.cs_textEditttt_04.setFocus()
                ui.cvcButtonClicked_06()
            elif ui.cvo_pushButton_05.isVisible():
                ui.cs_textEditttt_08.setFocus()
                ui.cvoButtonClicked_04()
    elif event.key() == Qt.Key_F12:
        if ui.main_btn == 2:
            if ui.svc_pushButton_06.isVisible():
                ui.ss_textEditttt_05.setFocus()
                ui.svcButtonClicked_04()
            elif ui.sva_pushButton_03.isVisible():
                ui.ss_textEditttt_06.setFocus()
                ui.svaButtonClicked_02()
        elif ui.main_btn == 3:
            if ui.cvc_pushButton_06.isVisible():
                ui.cs_textEditttt_05.setFocus()
                ui.cvcButtonClicked_04()
            elif ui.cva_pushButton_03.isVisible():
                ui.cs_textEditttt_06.setFocus()
                ui.cvaButtonClicked_02()
