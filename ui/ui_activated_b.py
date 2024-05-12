import sqlite3
import pandas as pd
from PyQt5.QtWidgets import QMessageBox
from ui.set_text import opti_standard, train_period, valid_period, test_period, optimized_count
from utility.setting import DB_STRATEGY


def bactivated_01(ui):
    try:
        gubun = ui.list_checkBoxxxxxx.index(ui.dialog_scheduler.focusWidget())
    except:
        gubun = ui.list_gcomboBoxxxxx.index(ui.dialog_scheduler.focusWidget())
    gubun2 = 'stock' if ui.sd_pushButtonnn_01.text() == '주식' else 'coin'

    ui.list_bcomboBoxxxxx[gubun].clear()
    ui.list_scomboBoxxxxx[gubun].clear()
    ui.list_vcomboBoxxxxx[gubun].clear()
    ui.list_p1comboBoxxxx[gubun].clear()
    ui.list_p2comboBoxxxx[gubun].clear()
    ui.list_p3comboBoxxxx[gubun].clear()
    ui.list_p4comboBoxxxx[gubun].clear()
    ui.list_tcomboBoxxxxx[gubun].clear()
    back_name = ui.list_gcomboBoxxxxx[gubun].currentText()
    if back_name == '백테스트':
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql(f'SELECT * FROM {gubun2}buy', con).set_index('index')
        if len(df) > 0:
            indexs = list(df.index)
            indexs.sort()
            for i, index in enumerate(indexs):
                ui.list_bcomboBoxxxxx[gubun].addItem(index)

        df = pd.read_sql(f'SELECT * FROM {gubun2}sell', con).set_index('index')
        con.close()
        if len(df) > 0:
            indexs = list(df.index)
            indexs.sort()
            for i, index in enumerate(indexs):
                ui.list_scomboBoxxxxx[gubun].addItem(index)
        ui.list_alineEdittttt[gubun].setText('30')
    else:
        con = sqlite3.connect(DB_STRATEGY)
        if '조건' in back_name:
            df = pd.read_sql(f'SELECT * FROM {gubun2}buyconds', con).set_index('index')
            if len(df) > 0:
                indexs = list(df.index)
                indexs.sort()
                for i, index in enumerate(indexs):
                    ui.list_bcomboBoxxxxx[gubun].addItem(index)

            df = pd.read_sql(f'SELECT * FROM {gubun2}sellconds', con).set_index('index')
            if len(df) > 0:
                indexs = list(df.index)
                indexs.sort()
                for i, index in enumerate(indexs):
                    ui.list_scomboBoxxxxx[gubun].addItem(index)
            ui.list_alineEdittttt[gubun].setText('30')
        else:
            df = pd.read_sql(f'SELECT * FROM {gubun2}optibuy', con).set_index('index')
            if len(df) > 0:
                indexs = list(df.index)
                indexs.sort()
                for i, index in enumerate(indexs):
                    ui.list_bcomboBoxxxxx[gubun].addItem(index)

            df = pd.read_sql(f'SELECT * FROM {gubun2}optisell', con).set_index('index')
            if len(df) > 0:
                indexs = list(df.index)
                indexs.sort()
                for i, index in enumerate(indexs):
                    ui.list_scomboBoxxxxx[gubun].addItem(index)

            if 'GA' in back_name:
                df = pd.read_sql(f'SELECT * FROM {gubun2}vars', con).set_index('index')
            else:
                df = pd.read_sql(f'SELECT * FROM {gubun2}optivars', con).set_index('index')
            if len(df) > 0:
                indexs = list(df.index)
                indexs.sort()
                for i, index in enumerate(indexs):
                    ui.list_vcomboBoxxxxx[gubun].addItem(index)
            ui.list_alineEdittttt[gubun].setText('')
        con.close()

        for item in opti_standard:
            ui.list_tcomboBoxxxxx[gubun].addItem(item)
        for item in train_period:
            ui.list_p1comboBoxxxx[gubun].addItem(item)
        for item in valid_period:
            ui.list_p2comboBoxxxx[gubun].addItem(item)
        for item in test_period:
            ui.list_p3comboBoxxxx[gubun].addItem(item)
        if 'GA' not in back_name and '조건' not in back_name:
            for item in optimized_count:
                ui.list_p4comboBoxxxx[gubun].addItem(item)


def bactivated_02(ui):
    if ui.sd_scheckBoxxxx_01.isChecked():
        list_comboBox = None
        if ui.dialog_scheduler.focusWidget() in ui.list_p1comboBoxxxx:
            list_comboBox = ui.list_p1comboBoxxxx
        elif ui.dialog_scheduler.focusWidget() in ui.list_p2comboBoxxxx:
            list_comboBox = ui.list_p2comboBoxxxx
        elif ui.dialog_scheduler.focusWidget() in ui.list_p3comboBoxxxx:
            list_comboBox = ui.list_p3comboBoxxxx
        elif ui.dialog_scheduler.focusWidget() in ui.list_p4comboBoxxxx:
            list_comboBox = ui.list_p4comboBoxxxx
        elif ui.dialog_scheduler.focusWidget() in ui.list_tcomboBoxxxxx:
            list_comboBox = ui.list_tcomboBoxxxxx
        elif ui.dialog_scheduler.focusWidget() in ui.list_bcomboBoxxxxx:
            list_comboBox = ui.list_bcomboBoxxxxx
        elif ui.dialog_scheduler.focusWidget() in ui.list_scomboBoxxxxx:
            list_comboBox = ui.list_scomboBoxxxxx
        elif ui.dialog_scheduler.focusWidget() in ui.list_vcomboBoxxxxx:
            list_comboBox = ui.list_vcomboBoxxxxx

        if list_comboBox is not None:
            index = list_comboBox.index(ui.dialog_scheduler.focusWidget())
            text = list_comboBox[index].currentText()
            back_type = ui.list_gcomboBoxxxxx[index].currentText()
            for i, combobox in enumerate(ui.list_gcomboBoxxxxx):
                if i != index and combobox.currentText() == back_type:
                    list_comboBox[i].setCurrentText(text)

    if ui.dialog_scheduler.focusWidget() in ui.list_p1comboBoxxxx:
        index = ui.list_p1comboBoxxxx.index(ui.dialog_scheduler.focusWidget())
        if '전진분석' in ui.list_gcomboBoxxxxx[index].currentText() and ui.list_p1comboBoxxxx[index].currentText() == 'ALL':
            ui.list_p1comboBoxxxx[index].setCurrentText('3')
            QMessageBox.critical(ui.dialog_scheduler, '오류 알림', '전진분석은 학습기간을 전체로 설정할 수 없습니다.\n')


def bactivated_03(ui):
    try:
        for checkbox in ui.list_checkBoxxxxxx:
            checkbox.setFocus()
            checkbox.setChecked(False)
        if ui.sd_scheckBoxxxx_01.isChecked():
            ui.sd_scheckBoxxxx_01.nextCheckState()
        schedule_name = ui.sd_dcomboBoxxxx_01.currentText()
        ui.sd_dlineEditttt_01.setText(schedule_name)
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql('SELECT * FROM schedule', con).set_index('index')
        con.close()
        schedule = df['스케쥴'][schedule_name]
        schedule = schedule.split('^')
        last = len(schedule) - 1
        for i, values_text in enumerate(schedule):
            if i != last:
                values = values_text.split(';')
                ui.list_checkBoxxxxxx[i].setFocus()
                ui.list_checkBoxxxxxx[i].setChecked(True)
                ui.list_gcomboBoxxxxx[i].setFocus()
                ui.list_gcomboBoxxxxx[i].setCurrentText(values[0])
                ui.list_slineEdittttt[i].setFocus()
                ui.list_slineEdittttt[i].setText(values[1])
                ui.list_elineEdittttt[i].setFocus()
                ui.list_elineEdittttt[i].setText(values[2])
                ui.list_blineEdittttt[i].setFocus()
                ui.list_blineEdittttt[i].setText(values[3])
                ui.list_alineEdittttt[i].setFocus()
                ui.list_alineEdittttt[i].setText(values[4])
                ui.list_p1comboBoxxxx[i].setFocus()
                ui.list_p1comboBoxxxx[i].setCurrentText(values[5])
                ui.list_p2comboBoxxxx[i].setFocus()
                ui.list_p2comboBoxxxx[i].setCurrentText(values[6])
                ui.list_p3comboBoxxxx[i].setFocus()
                ui.list_p3comboBoxxxx[i].setCurrentText(values[7])
                ui.list_p4comboBoxxxx[i].setFocus()
                ui.list_p4comboBoxxxx[i].setCurrentText(values[8])
                ui.list_tcomboBoxxxxx[i].setFocus()
                ui.list_tcomboBoxxxxx[i].setCurrentText(values[9])
                ui.list_bcomboBoxxxxx[i].setFocus()
                ui.list_bcomboBoxxxxx[i].setCurrentText(values[10])
                ui.list_scomboBoxxxxx[i].setFocus()
                ui.list_scomboBoxxxxx[i].setCurrentText(values[11])
                ui.list_vcomboBoxxxxx[i].setFocus()
                ui.list_vcomboBoxxxxx[i].setCurrentText(values[12])
            else:
                values = values_text.split(';')
                ui.sd_scheckBoxxxx_02.setChecked(True) if values[0] == '1' else ui.sd_scheckBoxxxx_02.setChecked(False)
                ui.sd_oclineEdittt_01.setText(values[1])
                ui.sd_oclineEdittt_02.setText(values[2])
                ui.sd_oclineEdittt_03.setText(values[3])
    except:
        pass
