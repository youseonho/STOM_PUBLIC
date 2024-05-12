import sqlite3
import pandas as pd
from PyQt5.QtWidgets import QMessageBox
from utility.setting import DB_STRATEGY


def cactivated_01(ui):
    strategy_name = ui.cvjb_comboBoxx_01.currentText()
    if strategy_name != '':
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql(f"SELECT * FROM coinbuy WHERE `index` = '{strategy_name}'", con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.cs_textEditttt_01.clear()
            ui.cs_textEditttt_01.append(df['전략코드'][strategy_name])
            ui.cvjb_lineEditt_01.setText(strategy_name)
        else:
            QMessageBox.critical(ui, '오류 알림', '전략이 DB에 존재하지 않습니다.\n전략을 다시 로딩하십시오.\n')


def cactivated_02(ui):
    strategy_name = ui.cvjs_comboBoxx_01.currentText()
    if strategy_name != '':
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql(f"SELECT * FROM coinsell WHERE `index` = '{strategy_name}'", con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.cs_textEditttt_02.clear()
            ui.cs_textEditttt_02.append(df['전략코드'][strategy_name])
            ui.cvjs_lineEditt_01.setText(strategy_name)
        else:
            QMessageBox.critical(ui, '오류 알림', '전략이 DB에 존재하지 않습니다.\n전략을 다시 로딩하십시오.\n')


def cactivated_03(ui):
    strategy_name = ui.cvc_comboBoxxx_01.currentText()
    if strategy_name != '':
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql(f"SELECT * FROM coinoptibuy WHERE `index` = '{strategy_name}'", con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.cs_textEditttt_03.clear()
            ui.cs_textEditttt_03.append(df['전략코드'][strategy_name])
            ui.cvc_lineEdittt_01.setText(strategy_name)
        else:
            QMessageBox.critical(ui, '오류 알림', '전략이 DB에 존재하지 않습니다.\n전략을 다시 로딩하십시오.\n')


def cactivated_04(ui):
    strategy_name = ui.cvc_comboBoxxx_02.currentText()
    if strategy_name != '':
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql(f"SELECT * FROM coinoptivars WHERE `index` = '{strategy_name}'", con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.cs_textEditttt_05.clear()
            ui.cs_textEditttt_05.append(df['전략코드'][strategy_name])
            ui.cvc_lineEdittt_02.setText(strategy_name)
        else:
            QMessageBox.critical(ui, '오류 알림', '범위가 DB에 존재하지 않습니다.\n범위을 다시 로딩하십시오.\n')


def cactivated_05(ui):
    strategy_name = ui.cvc_comboBoxxx_08.currentText()
    if strategy_name != '':
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql(f"SELECT * FROM coinoptisell WHERE `index` = '{strategy_name}'", con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.cs_textEditttt_04.clear()
            ui.cs_textEditttt_04.append(df['전략코드'][strategy_name])
            ui.cvc_lineEdittt_03.setText(strategy_name)
        else:
            QMessageBox.critical(ui, '오류 알림', '전략이 DB에 존재하지 않습니다.\n전략을 다시 로딩하십시오.\n')


def cactivated_06(ui):
    strategy_name = ui.cva_comboBoxxx_01.currentText()
    if strategy_name != '':
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql(f"SELECT * FROM coinvars WHERE `index` = '{strategy_name}'", con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.cs_textEditttt_06.clear()
            ui.cs_textEditttt_06.append(df['전략코드'][strategy_name])
            ui.cva_lineEdittt_01.setText(strategy_name)
        else:
            QMessageBox.critical(ui, '오류 알림', '범위가 DB에 존재하지 않습니다.\n범위을 다시 로딩하십시오.\n')


def cactivated_07(ui):
    strategy_name = ui.cvo_comboBoxxx_01.currentText()
    if strategy_name != '':
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql(f"SELECT * FROM coinbuyconds WHERE `index` = '{strategy_name}'", con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.cs_textEditttt_07.clear()
            ui.cs_textEditttt_07.append(df['전략코드'][strategy_name])
            ui.cvo_lineEdittt_01.setText(strategy_name)
        else:
            QMessageBox.critical(ui, '오류 알림', '조건이 DB에 존재하지 않습니다.\n조건을 다시 로딩하십시오.\n')


def cactivated_08(ui):
    strategy_name = ui.cvo_comboBoxxx_02.currentText()
    if strategy_name != '':
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql(f"SELECT * FROM coinsellconds WHERE `index` = '{strategy_name}'", con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.cs_textEditttt_08.clear()
            ui.cs_textEditttt_08.append(df['전략코드'][strategy_name])
            ui.cvo_lineEdittt_02.setText(strategy_name)
        else:
            QMessageBox.critical(ui, '오류 알림', '조건이 DB에 존재하지 않습니다.\n조건을 다시 로딩하십시오.\n')


def cactivated_09(ui):
    strategy_name = ui.sj_coin_comBox_01.currentText()
    if strategy_name != '':
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql(f"SELECT * FROM coinoptibuy WHERE `index` = '{strategy_name}'", con).set_index('index')
        con.close()
        if len(df) > 0:
            optivars = [var for var in list(df.loc[strategy_name])[1:] if var != 9999. and var is not None]
            QMessageBox.warning(
                ui, '경고',
                '최적화용 전략 선택시 최적값으로 전략이 실행됩니다.\n'
                '다음 변수값을 확인하십시오\n'
                f'{optivars}\n'
                f'매도전략 또한 반드시 최적화용 전략으로 변경하십시오.\n'
                f'최적화 백테스트를 실행할 경우 자동으로 변경됩니다.\n'
            )


def cactivated_10(ui):
    strategy_name = ui.sj_coin_comBox_03.currentText()
    if strategy_name != '':
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql(f"SELECT * FROM coinoptibuy WHERE `index` = '{strategy_name}'", con).set_index('index')
        con.close()
        if len(df) > 0:
            optivars = [var for var in list(df.loc[strategy_name])[1:] if var != 9999. and var is not None]
            QMessageBox.warning(
                ui, '경고',
                '최적화용 전략 선택시 최적값으로 전략이 실행됩니다.\n'
                '다음 변수값을 확인하십시오\n'
                f'{optivars}\n'
                f'매도전략 또한 반드시 최적화용 전략으로 변경하십시오.\n'
                f'최적화 백테스트를 실행할 경우 자동으로 변경됩니다.\n'
            )


def cactivated_11(ui):
    coin_trade_name = ui.sj_main_comBox_02.currentText()
    if coin_trade_name != '업비트':
        ui.sj_main_liEdit_03.setText('5')
        ui.sj_main_liEdit_04.setText('10')


def cactivated_12(ui):
    if ui.dict_set['거래소'] == '바이낸스선물' and ui.sj_main_comBox_03.currentText() == '교차':
        ui.sj_main_comBox_03.setCurrentText('격리')
        QMessageBox.warning(ui, '경고', '현재 바이낸스 선물 마진타입은 격리타입만 지원합니다.\n')


def cactivated_13(ui):
    if ui.dict_set['거래소'] == '바이낸스선물' and ui.sj_main_comBox_04.currentText() == '양방향':
        ui.sj_main_comBox_04.setCurrentText('단방향')
        QMessageBox.warning(ui, '경고', '현재 바이낸스 선물 포지션모드는 단방향만 지원합니다.\n')
