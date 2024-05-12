import random
import sqlite3
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QApplication
from utility.setting import DB_STRATEGY
from utility.static import text_not_in_special_characters
from ui.set_style import style_bc_st, style_bc_dk
from ui.set_text import famous_saying, stock_buy_var, stock_buy1, stock_buy2, stock_buy3, stock_buy4, stock_buy5, \
    stock_buy6, stock_buy_signal


def svjb_button_clicked_01(ui):
    if ui.ss_textEditttt_01.isVisible():
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql('SELECT * FROM stockbuy', con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.svjb_comboBoxx_01.clear()
            indexs = list(df.index)
            indexs.sort()
            for i, index in enumerate(indexs):
                ui.svjb_comboBoxx_01.addItem(index)
                if i == 0:
                    ui.svjb_lineEditt_01.setText(index)
            ui.svjb_pushButon_04.setStyleSheet(style_bc_st)


def svjb_button_clicked_02(ui, proc_query, queryQ):
    strategy_name = ui.svjb_lineEditt_01.text()
    strategy = ui.ss_textEditttt_01.toPlainText()
    if 'self.tickcols' not in strategy:
        strategy = ui.GetFixStrategy(strategy, '매수')

    if strategy_name == '':
        QMessageBox.critical(ui, '오류 알림', '매수전략의 이름이 공백 상태입니다.\n이름을 입력하십시오.\n')
    elif not text_not_in_special_characters(strategy_name):
        QMessageBox.critical(ui, '오류 알림', '매수전략의 이름에 특문이 포함되어 있습니다.\n언더바(_)를 제외한 특문을 제거하십시오.\n')
    elif strategy == '':
        QMessageBox.critical(ui, '오류 알림', '매수전략의 코드가 공백 상태입니다.\n코드를 작성하십시오.\n')
    else:
        if 'self.tickcols' in strategy or (QApplication.keyboardModifiers() & Qt.ControlModifier) or ui.BackCodeTest1(
                strategy):
            if proc_query.is_alive():
                queryQ.put(('전략디비', f"DELETE FROM stockbuy WHERE `index` = '{strategy_name}'"))
                df = pd.DataFrame({'전략코드': [strategy]}, index=[strategy_name])
                queryQ.put(('전략디비', df, 'stockbuy', 'append'))
            ui.svjb_pushButon_04.setStyleSheet(style_bc_st)
            QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))


def svjb_button_clicked_03(ui):
    ui.ss_textEditttt_01.clear()
    ui.ss_textEditttt_01.append(stock_buy_var)
    ui.svjb_pushButon_04.setStyleSheet(style_bc_st)


def svjb_button_clicked_04(ui, wdzservQ):
    strategy = ui.ss_textEditttt_01.toPlainText()
    if strategy == '':
        QMessageBox.critical(ui, '오류 알림', '매수전략의 코드가 공백 상태입니다.\n')
    else:
        buttonReply = QMessageBox.question(
            ui, '전략시작', '매수전략의 연산을 시작합니다. 계속하시겠습니까?\n',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if buttonReply == QMessageBox.Yes:
            wdzservQ.put(('strategy', ('매수전략', strategy)))
            ui.svjb_pushButon_04.setStyleSheet(style_bc_dk)
            ui.svjb_pushButon_12.setStyleSheet(style_bc_st)


def svjb_button_clicked_05(ui):
    ui.ss_textEditttt_01.append(stock_buy1)


def svjb_button_clicked_06(ui):
    ui.ss_textEditttt_01.append(stock_buy2)


def svjb_button_clicked_07(ui):
    ui.ss_textEditttt_01.append(stock_buy3)


def svjb_button_clicked_08(ui):
    ui.ss_textEditttt_01.append(stock_buy4)


def svjb_button_clicked_09(ui):
    ui.ss_textEditttt_01.append(stock_buy5)


def svjb_button_clicked_10(ui):
    ui.ss_textEditttt_01.append(stock_buy6)


def svjb_button_clicked_11(ui):
    ui.ss_textEditttt_01.append(stock_buy_signal)


def svjb_button_clicked_12(ui, wdzservQ):
    wdzservQ.put(('strategy', '매수전략중지'))
    ui.svjb_pushButon_12.setStyleSheet(style_bc_dk)
    ui.svjb_pushButon_04.setStyleSheet(style_bc_st)
