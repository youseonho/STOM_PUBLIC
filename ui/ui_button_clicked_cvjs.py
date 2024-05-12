import random
import sqlite3
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QApplication
from utility.setting import DB_STRATEGY
from utility.static import text_not_in_special_characters
from ui.set_style import style_bc_st, style_bc_dk
from ui.set_text import famous_saying, coin_sell_var, coin_future_sell_var, coin_sell1, coin_sell2, coin_sell3, \
    coin_sell4, coin_sell5, coin_sell6, coin_sell7, coin_sell8, coin_sell_signal, coin_future_sell_signal


def cvjs_button_clicked_01(ui):
    if ui.cs_textEditttt_02.isVisible():
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql('SELECT * FROM coinsell', con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.cvjs_comboBoxx_01.clear()
            indexs = list(df.index)
            indexs.sort()
            for i, index in enumerate(indexs):
                ui.cvjs_comboBoxx_01.addItem(index)
                if i == 0:
                    ui.cvjs_lineEditt_01.setText(index)
            ui.cvjs_pushButon_04.setStyleSheet(style_bc_st)


def cvjs_button_clicked_02(ui, proc_query, queryQ):
    strategy_name = ui.cvjs_lineEditt_01.text()
    strategy = ui.cs_textEditttt_02.toPlainText()
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
                queryQ.put(('전략디비', f"DELETE FROM coinsell WHERE `index` = '{strategy_name}'"))
                df = pd.DataFrame({'전략코드': [strategy]}, index=[strategy_name])
                queryQ.put(('전략디비', df, 'coinsell', 'append'))
            ui.cvjs_pushButon_04.setStyleSheet(style_bc_st)
            QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))


def cvjs_button_clicked_03(ui):
    ui.cs_textEditttt_02.clear()
    ui.cs_textEditttt_02.append(coin_sell_var if ui.dict_set['거래소'] == '업비트' else coin_future_sell_var)
    ui.cvjs_pushButon_04.setStyleSheet(style_bc_st)


def cvjs_button_clicked_04(ui, cstgQ):
    strategy = ui.cs_textEditttt_02.toPlainText()
    if strategy == '':
        QMessageBox.critical(ui, '오류 알림', '매도전략의 코드가 공백 상태입니다.\n')
    else:
        buttonReply = QMessageBox.question(
            ui, '전략시작', '매도전략의 연산을 시작합니다. 계속하시겠습니까?\n',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if buttonReply == QMessageBox.Yes:
            if ui.CoinStrategyProcessAlive():
                cstgQ.put(('매도전략', strategy))
            ui.cvjs_pushButon_04.setStyleSheet(style_bc_dk)
            ui.cvjs_pushButon_14.setStyleSheet(style_bc_st)


def cvjs_button_clicked_05(ui):
    ui.cs_textEditttt_02.append(coin_sell1)


def cvjs_button_clicked_06(ui):
    ui.cs_textEditttt_02.append(coin_sell2)


def cvjs_button_clicked_07(ui):
    ui.cs_textEditttt_02.append(coin_sell3)


def cvjs_button_clicked_08(ui):
    ui.cs_textEditttt_02.append(coin_sell4)


def cvjs_button_clicked_09(ui):
    ui.cs_textEditttt_02.append(coin_sell5)


def cvjs_button_clicked_10(ui):
    ui.cs_textEditttt_02.append(coin_sell6)


def cvjs_button_clicked_11(ui):
    ui.cs_textEditttt_02.append(coin_sell7)


def cvjs_button_clicked_12(ui):
    ui.cs_textEditttt_02.append(coin_sell8)


def cvjs_button_clicked_13(ui):
    ui.cs_textEditttt_02.append(coin_sell_signal if ui.dict_set['거래소'] == '업비트' else coin_future_sell_signal)


def cvjs_button_clicked_14(ui, cstgQ):
    if ui.CoinStrategyProcessAlive():
        cstgQ.put('매도전략중지')
    ui.cvjs_pushButon_14.setStyleSheet(style_bc_dk)
    ui.cvjs_pushButon_04.setStyleSheet(style_bc_st)
