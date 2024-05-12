import random
import sqlite3
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QApplication
from ui.set_text import famous_saying
from utility.setting import DB_STRATEGY
from utility.static import text_not_in_special_characters


def cva_button_clicked_01(ui):
    con = sqlite3.connect(DB_STRATEGY)
    df = pd.read_sql('SELECT * FROM coinvars', con).set_index('index')
    con.close()
    if len(df) > 0:
        ui.cva_comboBoxxx_01.clear()
        indexs = list(df.index)
        indexs.sort()
        for i, index in enumerate(indexs):
            ui.cva_comboBoxxx_01.addItem(index)
            if i == 0:
                ui.cva_lineEdittt_01.setText(index)


def cva_button_clicked_02(ui, proc_query, queryQ):
    strategy_name = ui.cva_lineEdittt_01.text()
    strategy = ui.cs_textEditttt_06.toPlainText()
    if strategy_name == '':
        QMessageBox.critical(ui, '오류 알림', 'GA범위의 이름이 공백 상태입니다.\n이름을 입력하십시오.\n')
    elif not text_not_in_special_characters(strategy_name):
        QMessageBox.critical(ui, '오류 알림', 'GA범위의 이름에 특문이 포함되어 있습니다.\n언더바(_)를 제외한 특문을 제거하십시오.\n')
    elif strategy == '':
        QMessageBox.critical(ui, '오류 알림', 'GA범위의 코드가 공백 상태입니다.\n코드를 작성하십시오.\n')
    else:
        if (QApplication.keyboardModifiers() & Qt.ControlModifier) or ui.BackCodeTest2(strategy, ga=True):
            if proc_query.is_alive():
                queryQ.put(('전략디비', f"DELETE FROM coinvars WHERE `index` = '{strategy_name}'"))
                df = pd.DataFrame({'전략코드': [strategy]}, index=[strategy_name])
                queryQ.put(('전략디비', df, 'coinvars', 'append'))
                QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))


def cvo_button_clicked_01(ui):
    con = sqlite3.connect(DB_STRATEGY)
    df = pd.read_sql('SELECT * FROM coinbuyconds', con).set_index('index')
    con.close()
    if len(df) > 0:
        ui.cvo_comboBoxxx_01.clear()
        indexs = list(df.index)
        indexs.sort()
        for i, index in enumerate(indexs):
            ui.cvo_comboBoxxx_01.addItem(index)
            if i == 0:
                ui.cvo_lineEdittt_01.setText(index)


def cvo_button_clicked_02(ui, proc_query, queryQ):
    strategy_name = ui.cvo_lineEdittt_01.text()
    strategy = ui.cs_textEditttt_07.toPlainText()
    if strategy_name == '':
        QMessageBox.critical(ui, '오류 알림', '매수조건의 이름이 공백 상태입니다.\n이름을 입력하십시오.\n')
    elif not text_not_in_special_characters(strategy_name):
        QMessageBox.critical(ui, '오류 알림', '매수조건의 이름에 특문이 포함되어 있습니다.\n언더바(_)를 제외한 특문을 제거하십시오.\n')
    elif strategy == '':
        QMessageBox.critical(ui, '오류 알림', '매수조건의 코드가 공백 상태입니다.\n코드를 작성하십시오.\n')
    else:
        if ui.BackCodeTest3('매수', strategy):
            if proc_query.is_alive():
                queryQ.put(('전략디비', f"DELETE FROM coinbuyconds WHERE `index` = '{strategy_name}'"))
                df = pd.DataFrame({'전략코드': [strategy]}, index=[strategy_name])
                queryQ.put(('전략디비', df, 'coinbuyconds', 'append'))
                QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))


def cvo_button_clicked_03(ui):
    con = sqlite3.connect(DB_STRATEGY)
    df = pd.read_sql('SELECT * FROM coinsellconds', con).set_index('index')
    con.close()
    if len(df) > 0:
        ui.cvo_comboBoxxx_02.clear()
        indexs = list(df.index)
        indexs.sort()
        for i, index in enumerate(indexs):
            ui.cvo_comboBoxxx_02.addItem(index)
            if i == 0:
                ui.cvo_lineEdittt_02.setText(index)


def cvo_button_clicked_04(ui, proc_query, queryQ):
    strategy_name = ui.cvo_lineEdittt_02.text()
    strategy = ui.cs_textEditttt_08.toPlainText()
    if strategy_name == '':
        QMessageBox.critical(ui, '오류 알림', '매도조건의 이름이 공백 상태입니다.\n이름을 입력하십시오.\n')
    elif not text_not_in_special_characters(strategy_name):
        QMessageBox.critical(ui, '오류 알림', '매도조건의 이름에 특문이 포함되어 있습니다.\n언더바(_)를 제외한 특문을 제거하십시오.\n')
    elif strategy == '':
        QMessageBox.critical(ui, '오류 알림', '매도조건의 코드가 공백 상태입니다.\n코드를 작성하십시오.\n')
    else:
        if ui.BackCodeTest3('매도', strategy):
            if proc_query.is_alive():
                queryQ.put(('전략디비', f"DELETE FROM coinsellconds WHERE `index` = '{strategy_name}'"))
                df = pd.DataFrame({'전략코드': [strategy]}, index=[strategy_name])
                queryQ.put(('전략디비', df, 'coinsellconds', 'append'))
                QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))


def cvo_button_clicked_05(ui):
    QMessageBox.critical(ui, '오류 알림', '범위 편집기 상태에서만 작동합니다.\n')
