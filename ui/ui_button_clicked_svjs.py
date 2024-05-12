import random
import sqlite3
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QApplication
from utility.setting import DB_STRATEGY
from utility.static import text_not_in_special_characters
from ui.set_style import style_bc_st, style_bc_dk
from ui.set_text import famous_saying, stock_sell_var, stock_sell1, stock_sell2, stock_sell3, stock_sell4, stock_sell5, \
    stock_sell6, stock_sell7, stock_sell8, stock_sell_signal


def svjs_button_clicked_01(ui):
    if ui.ss_textEditttt_02.isVisible():
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql('SELECT * FROM stocksell', con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.svjs_comboBoxx_01.clear()
            indexs = list(df.index)
            indexs.sort()
            for i, index in enumerate(indexs):
                ui.svjs_comboBoxx_01.addItem(index)
                if i == 0:
                    ui.svjs_lineEditt_01.setText(index)
            ui.svjs_pushButon_04.setStyleSheet(style_bc_st)


def svjs_button_clicked_02(ui, proc_query, queryQ):
    strategy_name = ui.svjs_lineEditt_01.text()
    strategy = ui.ss_textEditttt_02.toPlainText()
    strategy = ui.GetFixStrategy(strategy, '매도')

    if strategy_name == '':
        QMessageBox.critical(ui, '오류 알림', '매도전략의 이름이 공백 상태입니다.\n이름을 입력하십시오.\n')
    elif not text_not_in_special_characters(strategy_name):
        QMessageBox.critical(ui, '오류 알림', '매도전략의 이름에 특문이 포함되어 있습니다.\n언더바(_)를 제외한 특문을 제거하십시오.\n')
    elif strategy == '':
        QMessageBox.critical(ui, '오류 알림', '매도전략의 코드가 공백 상태입니다.\n코드를 작성하십시오.\n')
    else:
        if 'self.tickcols' in strategy or (QApplication.keyboardModifiers() & Qt.ControlModifier) or ui.BackCodeTest1(
                strategy):
            if proc_query.is_alive():
                queryQ.put(('전략디비', f"DELETE FROM stocksell WHERE `index` = '{strategy_name}'"))
                df = pd.DataFrame({'전략코드': [strategy]}, index=[strategy_name])
                queryQ.put(('전략디비', df, 'stocksell', 'append'))
            ui.svjs_pushButon_04.setStyleSheet(style_bc_st)
            QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))


def svjs_button_clicked_03(ui):
    ui.ss_textEditttt_02.clear()
    ui.ss_textEditttt_02.append(stock_sell_var)
    ui.svjs_pushButon_04.setStyleSheet(style_bc_st)


def svjs_button_clicked_04(ui, wdzservQ):
    strategy = ui.ss_textEditttt_02.toPlainText()
    if strategy == '':
        QMessageBox.critical(ui, '오류 알림', '매도전략의 코드가 공백 상태입니다.\n')
    else:
        buttonReply = QMessageBox.question(
            ui, '전략시작', '매도전략의 연산을 시작합니다. 계속하시겠습니까?\n',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if buttonReply == QMessageBox.Yes:
            wdzservQ.put(('strategy', ('매도전략', strategy)))
            ui.svjs_pushButon_04.setStyleSheet(style_bc_dk)
            ui.svjs_pushButon_14.setStyleSheet(style_bc_st)


def svjs_button_clicked_05(ui):
    ui.ss_textEditttt_02.append(stock_sell1)


def svjs_button_clicked_06(ui):
    ui.ss_textEditttt_02.append(stock_sell2)


def svjs_button_clicked_07(ui):
    ui.ss_textEditttt_02.append(stock_sell3)


def svjs_button_clicked_08(ui):
    ui.ss_textEditttt_02.append(stock_sell4)


def svjs_button_clicked_09(ui):
    ui.ss_textEditttt_02.append(stock_sell5)


def svjs_button_clicked_10(ui):
    ui.ss_textEditttt_02.append(stock_sell6)


def svjs_button_clicked_11(ui):
    ui.ss_textEditttt_02.append(stock_sell7)


def svjs_button_clicked_12(ui):
    ui.ss_textEditttt_02.append(stock_sell8)


def svjs_button_clicked_13(ui):
    ui.ss_textEditttt_02.append(stock_sell_signal)


def svjs_button_clicked_14(ui, wdzservQ):
    wdzservQ.put(('strategy', '매도전략중지'))
    ui.svjs_pushButon_14.setStyleSheet(style_bc_dk)
    ui.svjs_pushButon_04.setStyleSheet(style_bc_st)
