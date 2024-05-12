import random
import sqlite3
import pandas as pd
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QMessageBox, QPushButton
from ui.set_text import famous_saying
from utility.static import strf_time
from utility.setting import DB_TRADELIST, columns_nt, ui_num, columns_nd, DB_SETTING


def opbutton_clicked_01():
    pass


def cpbutton_clicked_01(ui, chartQ):
    backdetail_list = []
    for i, checkbox in enumerate(ui.backcheckbox_list):
        if checkbox.isChecked():
            backdetail_list.append(ui.backdetail_list[i])

    if len(backdetail_list) >= 2:
        chartQ.put(('그래프비교', backdetail_list))
    else:
        QMessageBox.critical(ui.dialog_comp, '오류 알림', '두개 이상의 상세기록을 선택하십시오.\n')


def ttbutton_clicked_01(ui, cmd):
    if '집계' in cmd:
        gubun = 'S' if 'S' in cmd else 'C'
        table = 's_totaltradelist' if 'S' in cmd else 'c_totaltradelist'
        con = sqlite3.connect(DB_TRADELIST)
        df = pd.read_sql(f'SELECT * FROM {table}', con)
        con.close()
        df = df[::-1]
        if len(df) > 0:
            pr = len(df)
            nsp = 100
            for sp in df['수익률'].to_list()[::-1]:
                nsp = nsp + nsp * sp / 100
            nsp = round(nsp - 100, 2)
            nbg, nsg = df['총매수금액'].sum(), df['총매도금액'].sum()
            npg, nmg = df['총수익금액'].sum(), df['총손실금액'].sum()
            nsig = df['수익금합계'].sum()
            df2 = pd.DataFrame(columns=columns_nt)
            df2.loc[0] = pr, nbg, nsg, npg, nmg, nsp, nsig
            ui.update_tablewidget.update_tablewidget((ui_num[f'{gubun}누적합계'], df2))
        else:
            QMessageBox.critical(ui, '오류 알림', '거래목록이 존재하지 않습니다.\n')
            return
        if cmd == f'{gubun}일별집계':
            df.rename(columns={'index': '일자'}, inplace=True)
            ui.update_tablewidget.update_tablewidget((ui_num[f'{gubun}누적상세'], df))
        elif cmd == f'{gubun}월별집계':
            df['연월'] = df['index'].apply(lambda x: str(x)[:6])
            df2 = pd.DataFrame(columns=columns_nd)
            lastmonth = df['연월'][df.index[-1]]
            month = strf_time('%Y%m')
            while int(month) >= int(lastmonth):
                df3 = df[df['연월'] == month]
                if len(df3) > 0:
                    tbg, tsg = df3['총매수금액'].sum(), df3['총매도금액'].sum()
                    sp = round((tsg / tbg - 1) * 100, 2)
                    tpg, tmg = df3['총수익금액'].sum(), df3['총손실금액'].sum()
                    ttsg = df3['수익금합계'].sum()
                    df2.loc[month] = month, tbg, tsg, tpg, tmg, sp, ttsg
                month = str(int(month) - 89) if int(month[4:]) == 1 else str(int(month) - 1)
            ui.update_tablewidget.update_tablewidget((ui_num[f'{gubun}누적상세'], df2))
        elif cmd == f'{gubun}연도별집계':
            df['연도'] = df['index'].apply(lambda x: str(x)[:4])
            df2 = pd.DataFrame(columns=columns_nd)
            lastyear = df['연도'][df.index[-1]]
            year = strf_time('%Y')
            while int(year) >= int(lastyear):
                df3 = df[df['연도'] == year]
                if len(df3) > 0:
                    tbg, tsg = df3['총매수금액'].sum(), df3['총매도금액'].sum()
                    sp = round((tsg / tbg - 1) * 100, 2)
                    tpg, tmg = df3['총수익금액'].sum(), df3['총손실금액'].sum()
                    ttsg = df3['수익금합계'].sum()
                    df2.loc[year] = year, tbg, tsg, tpg, tmg, sp, ttsg
                year = str(int(year) - 1)
            ui.update_tablewidget.update_tablewidget((ui_num[f'{gubun}누적상세'], df2))


def change_back_sdate(ui):
    if ui.sd_scheckBoxxxx_01.isChecked():
        gubun = ui.list_sdateEdittttt.index(ui.dialog_scheduler.focusWidget())
        date = ui.list_sdateEdittttt[gubun].date().toString('yyyyMMdd')
        for i, widget in enumerate(ui.list_sdateEdittttt):
            if i != gubun:
                widget.setDate(QDate.fromString(date, 'yyyyMMdd'))


def change_back_edate(ui):
    if ui.sd_scheckBoxxxx_01.isChecked():
        gubun = ui.list_edateEdittttt.index(ui.dialog_scheduler.focusWidget())
        date = ui.list_edateEdittttt[gubun].date().toString('yyyyMMdd')
        for i, widget in enumerate(ui.list_edateEdittttt):
            if i != gubun:
                widget.setDate(QDate.fromString(date, 'yyyyMMdd'))


def stbutton_clicked_01(ui):
    con = sqlite3.connect(DB_SETTING)
    df = pd.read_sql('SELECT * FROM back', con).set_index('index')
    con.close()
    std_text = df['최적화기준값제한'][0].split(';')
    ui.st_lineEditttt_01.setText(std_text[0])
    ui.st_lineEditttt_02.setText(std_text[1])
    ui.st_lineEditttt_03.setText(std_text[2])
    ui.st_lineEditttt_04.setText(std_text[3])
    ui.st_lineEditttt_05.setText(std_text[4])
    ui.st_lineEditttt_06.setText(std_text[5])
    ui.st_lineEditttt_07.setText(std_text[6])
    ui.st_lineEditttt_08.setText(std_text[7])
    ui.st_lineEditttt_09.setText(std_text[8])
    ui.st_lineEditttt_10.setText(std_text[9])
    ui.st_lineEditttt_11.setText(std_text[10])
    ui.st_lineEditttt_12.setText(std_text[11])
    ui.st_lineEditttt_13.setText(std_text[12])
    ui.st_lineEditttt_14.setText(std_text[13])


def stbutton_clicked_02(ui, proc_query, queryQ):
    std_text1 = ui.st_lineEditttt_01.text()
    std_text2 = ui.st_lineEditttt_02.text()
    std_text3 = ui.st_lineEditttt_03.text()
    std_text4 = ui.st_lineEditttt_04.text()
    std_text5 = ui.st_lineEditttt_05.text()
    std_text6 = ui.st_lineEditttt_06.text()
    std_text7 = ui.st_lineEditttt_07.text()
    std_text8 = ui.st_lineEditttt_08.text()
    std_text9 = ui.st_lineEditttt_09.text()
    std_text10 = ui.st_lineEditttt_10.text()
    std_text11 = ui.st_lineEditttt_11.text()
    std_text12 = ui.st_lineEditttt_12.text()
    std_text13 = ui.st_lineEditttt_13.text()
    std_text14 = ui.st_lineEditttt_14.text()
    std_list = [std_text1, std_text2, std_text3, std_text4, std_text5, std_text6, std_text7, std_text8, std_text9,
                std_text10, std_text11, std_text12, std_text13, std_text14]
    if '' in std_list:
        QMessageBox.critical(ui.dialog_std, '오류 알림', '일부 제한값이 공백상태입니다.\n')
    else:
        if proc_query.is_alive():
            std_list = ';'.join(std_list)
            query = f"UPDATE back SET 최적화기준값제한 = '{std_list}'"
            queryQ.put(('설정디비', query))
        ui.dict_set['최적화기준값제한'] = std_list
        QMessageBox.information(ui.dialog_std, '저장 완료', random.choice(famous_saying))


def lvbutton_clicked_01(ui):
    ui.dialog_leverage.show() if not ui.dialog_leverage.isVisible() else ui.dialog_leverage.close()


def lvbutton_clicked_02(ui):
    con = sqlite3.connect(DB_SETTING)
    df = pd.read_sql('SELECT * FROM main', con).set_index('index')
    con.close()
    if len(df) > 0:
        ui.lv_checkBoxxxx_01.setChecked(True) if df['바이낸스선물고정레버리지'][0] else ui.lv_checkBoxxxx_01.setChecked(False)
        ui.lv_checkBoxxxx_02.setChecked(True) if not df['바이낸스선물고정레버리지'][0] else ui.lv_checkBoxxxx_02.setChecked(False)
        ui.lv_lineEditttt_01.setText(str(df['바이낸스선물고정레버리지값'][0]))
        binance_lvrg = []
        for text in df['바이낸스선물변동레버리지값'][0].split('^'):
            lvrg_list = text.split(';')
            binance_lvrg.append(lvrg_list)
        ui.lv_lineEditttt_02.setText(binance_lvrg[0][0])
        ui.lv_lineEditttt_03.setText(binance_lvrg[0][1])
        ui.lv_lineEditttt_04.setText(binance_lvrg[0][2])
        ui.lv_lineEditttt_05.setText(binance_lvrg[1][0])
        ui.lv_lineEditttt_06.setText(binance_lvrg[1][1])
        ui.lv_lineEditttt_07.setText(binance_lvrg[1][2])
        ui.lv_lineEditttt_08.setText(binance_lvrg[2][0])
        ui.lv_lineEditttt_09.setText(binance_lvrg[2][1])
        ui.lv_lineEditttt_10.setText(binance_lvrg[2][2])
        ui.lv_lineEditttt_11.setText(binance_lvrg[3][0])
        ui.lv_lineEditttt_12.setText(binance_lvrg[3][1])
        ui.lv_lineEditttt_13.setText(binance_lvrg[3][2])
        ui.lv_lineEditttt_14.setText(binance_lvrg[4][0])
        ui.lv_lineEditttt_15.setText(binance_lvrg[4][1])
        ui.lv_lineEditttt_16.setText(binance_lvrg[4][2])
    else:
        QMessageBox.critical(ui.dialog_leverage, '오류 알림', '기본 설정값이\n존재하지 않습니다.\n')


def lvbutton_clicked_03(ui, proc_query, queryQ):
    lv0 = 1 if ui.lv_checkBoxxxx_01.isChecked() else 0
    lv1 = ui.lv_lineEditttt_01.text()
    lv2 = ui.lv_lineEditttt_02.text()
    lv3 = ui.lv_lineEditttt_03.text()
    lv4 = ui.lv_lineEditttt_04.text()
    lv5 = ui.lv_lineEditttt_05.text()
    lv6 = ui.lv_lineEditttt_06.text()
    lv7 = ui.lv_lineEditttt_07.text()
    lv8 = ui.lv_lineEditttt_08.text()
    lv9 = ui.lv_lineEditttt_09.text()
    lv10 = ui.lv_lineEditttt_10.text()
    lv11 = ui.lv_lineEditttt_11.text()
    lv12 = ui.lv_lineEditttt_12.text()
    lv13 = ui.lv_lineEditttt_13.text()
    lv14 = ui.lv_lineEditttt_14.text()
    lv15 = ui.lv_lineEditttt_15.text()
    lv16 = ui.lv_lineEditttt_16.text()
    if '' in (lv1, lv2, lv3, lv4, lv5, lv6, lv7, lv8, lv9, lv10, lv11, lv12, lv13, lv14, lv15, lv16):
        QMessageBox.critical(ui.dialog_leverage, '오류 알림', '일부 설정값이 입력되지 않았습니다.\n')
    else:
        lv2, lv3, lv5, lv6, lv8, lv9, lv11, lv12, lv14, lv15 = float(lv2), float(lv3), float(lv5), float(lv6), float(
            lv8), float(lv9), float(lv11), float(lv12), float(lv14), float(lv15)
        lv1, lv4, lv7, lv10, lv13, lv16 = int(lv1), int(lv4), int(lv7), int(lv10), int(lv13), int(lv16)
        if not (
                1 <= lv1 <= 125 and 1 <= lv4 <= 125 and 1 <= lv7 <= 125 and 1 <= lv10 <= 125 and 1 <= lv13 <= 125 and 1 <= lv16 <= 125):
            QMessageBox.critical(ui, '오류 알림', '레버리지 설정을 1부터 125사이로 입력하십시오.\n')
            return
        else:
            if proc_query.is_alive():
                lvrg_text = f'{lv2};{lv3};{lv4}^{lv5};{lv6};{lv7}^{lv8};{lv9};{lv10}^{lv11};{lv12};{lv13}^{lv14};{lv15};{lv16}'
                query = f"UPDATE main SET 바이낸스선물고정레버리지 = {lv0}, 바이낸스선물고정레버리지값 = {lv1}, 바이낸스선물변동레버리지값 = '{lvrg_text}'"
                queryQ.put(('설정디비', query))
            ui.dict_set['바이낸스선물고정레버리지'] = lv0
            ui.dict_set['바이낸스선물고정레버리지값'] = lv1
            ui.dict_set['바이낸스선물변동레버리지값'] = [[lv2, lv3, lv4], [lv5, lv6, lv7], [lv8, lv9, lv10], [lv11, lv12, lv13],
                                            [lv14, lv15, lv16]]
            ui.UpdateDictSet()
            QMessageBox.information(ui.dialog_leverage, '저장 완료', random.choice(famous_saying))


def lvcheck_changed_01(ui, state):
    if type(ui.dialog_leverage.focusWidget()) != QPushButton and state == Qt.Checked:
        for widget in ui.lv_checkbox_listt:
            if widget != ui.dialog_leverage.focusWidget():
                if widget.isChecked():
                    widget.nextCheckState()


def hg_button_clicked_01(ui, gubun, hogaQ):
    if not ui.dialog_hoga.isVisible(): return
    index = ui.hg_labellllllll_01.text()
    if index == '': return
    code = ui.ct_lineEdittttt_04.text()
    name = ui.ct_lineEdittttt_05.text()
    index = index.replace('-', '').replace(' ', '').replace(':', '')
    hogaQ.put(('이전호가정보요청' if gubun == '이전' else '다음호가정보요청', code, name, index))


def hg_button_clicked_02(ui, gubun):
    if not ui.dialog_hoga.isVisible(): return
    cindex = ui.hg_labellllllll_01.text()
    if cindex == '': return
    code = ui.ct_lineEdittttt_04.text()
    name = ui.ct_lineEdittttt_05.text()
    cindex = int(cindex.replace('-', '').replace(' ', '').replace(':', ''))
    index_list = ui.buy_index if gubun == '매수' else ui.sell_index
    if len(index_list) >= 1:
        if cindex < index_list[-1]:
            index_list = [x for x in index_list if cindex < x]
        index = index_list[0]
        if cindex != index:
            ui.hogaQ.put(('매도수호가정보요청', code, name, str(index)))
