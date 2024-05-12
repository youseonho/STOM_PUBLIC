import random
import sqlite3
import pandas as pd
from PyQt5.QtWidgets import QMessageBox
from ui.set_text import famous_saying
from utility.setting import DB_SETTING


# noinspection PyUnusedLocal
def ct_button_clicked_01(ui, wdzservQ, qlist):
    pass


# noinspection PyUnusedLocal
def ct_button_clicked_02(ui, wdzservQ):
    pass


# noinspection PyUnusedLocal
def ct_button_clicked_03(ui, windowQ, wdzservQ, cstgQ):
    pass


# noinspection PyUnusedLocal
def ct_button_clicked_04(ui):
    pass


def ct_button_clicked_05(ui):
    ui.df_test = None


def ct_button_clicked_06(ui):
    ui.dialog_test.close()


def ct_button_clicked_07(ui):
    k = ['5', '2', '2', '0', '12', '26', '9', '12', '26', '0', '12', '26', '0', '5', '0.7', '0.5', '0.05', '30', '14',
         '10', '10']
    for i, linedit in enumerate(ui.factor_linedit_list):
        linedit.setText(k[i])


def ct_button_clicked_08(ui):
    con = sqlite3.connect(DB_SETTING)
    df = pd.read_sql('SELECT * FROM back', con)
    k_list = df['보조지표설정'][0]
    k_list = k_list.split(';')
    con.close()
    for i, linedit in enumerate(ui.factor_linedit_list):
        linedit.setText(k_list[i])


def ct_button_clicked_09(ui, proc_query, queryQ):
    k_list = []
    for linedit in ui.factor_linedit_list:
        k_list.append(linedit.text())
    k_list = ';'.join(k_list)
    if proc_query.is_alive():
        query = f"UPDATE back SET 보조지표설정 = '{k_list}'"
        queryQ.put(('설정디비', query))
    QMessageBox.information(ui.dialog_factor, '저장 완료', random.choice(famous_saying))


def get_k_list(ui):
    k_list = []
    for linedit in ui.factor_linedit_list:
        k_list.append(linedit.text())
    k_list = [int(x) if '.' not in x else float(x) for x in k_list]
    return k_list


# noinspection PyUnusedLocal
def tick_put(ui, code, gubun, windowQ, wdzservQ, ctraderQ, creceivQ, cstgQ):
    pass
