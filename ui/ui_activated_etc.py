import sqlite3
import pandas as pd
from PyQt5.QtWidgets import QPushButton
from utility.setting import DB_BACKTEST, ui_num


def activated_01(ui):
    if type(ui.focusWidget()) != QPushButton:
        table_name = ui.focusWidget().currentText()
        if ui.focusWidget() in (ui.ss_comboBoxxxx_01, ui.ss_comboBoxxxx_02, ui.ss_comboBoxxxx_03):
            ui_num_text = 'S상세기록'
        else:
            ui_num_text = 'C상세기록'
        if table_name is None:
            return

        con = sqlite3.connect(DB_BACKTEST)
        df = pd.read_sql(f"SELECT * FROM '{table_name}'", con).set_index('index')
        con.close()
        ui.update_tablewidget.update_tablewidget((ui_num[ui_num_text], df))


def activated_02(ui):
    name = ui.sj_set_comBoxx_01.currentText()
    ui.sj_set_liEditt_01.setText(name)


def activated_03(ui):
    name = ui.od_comboBoxxxxx_01.currentText()
    ui.od_comboBoxxxxx_02.clear()
    if 'KRW' in name:
        items = ['지정가', '시장가']
    elif 'USDT' in name:
        items = ['시장가', '지정가', '지정가IOC', '지정가FOK']
    else:
        items = [
            '지정가', '시장가', '최유리지정가', '최우선지정가', '지정가IOC', '시장가IOC', '최유리IOC', '지정가FOK',
            '시장가FOK', '최유리FOK'
        ]
    for item in items:
        ui.od_comboBoxxxxx_02.addItem(item)
