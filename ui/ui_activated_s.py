import sqlite3
import pandas as pd
from PyQt5.QtWidgets import QMessageBox
from utility.setting import DB_STRATEGY


def sactivated_01(ui):
    strategy_name = ui.svjb_comboBoxx_01.currentText()
    if strategy_name != '':
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql(f"SELECT * FROM stockbuy WHERE `index` = '{strategy_name}'", con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.ss_textEditttt_01.clear()
            ui.ss_textEditttt_01.append(df['전략코드'][strategy_name])
            ui.svjb_lineEditt_01.setText(strategy_name)
        else:
            QMessageBox.critical(ui, '오류 알림', '전략이 DB에 존재하지 않습니다.\n전략을 다시 로딩하십시오.\n')


def sactivated_02(ui):
    strategy_name = ui.svjs_comboBoxx_01.currentText()
    if strategy_name != '':
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql(f"SELECT * FROM stocksell WHERE `index` = '{strategy_name}'", con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.ss_textEditttt_02.clear()
            ui.ss_textEditttt_02.append(df['전략코드'][strategy_name])
            ui.svjs_lineEditt_01.setText(strategy_name)
        else:
            QMessageBox.critical(ui, '오류 알림', '전략이 DB에 존재하지 않습니다.\n전략을 다시 로딩하십시오.\n')


def sactivated_03(ui):
    strategy_name = ui.svc_comboBoxxx_01.currentText()
    if strategy_name != '':
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql(f"SELECT * FROM stockoptibuy WHERE `index` = '{strategy_name}'", con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.ss_textEditttt_03.clear()
            ui.ss_textEditttt_03.append(df['전략코드'][strategy_name])
            ui.svc_lineEdittt_01.setText(strategy_name)
        else:
            QMessageBox.critical(ui, '오류 알림', '전략이 DB에 존재하지 않습니다.\n전략을 다시 로딩하십시오.\n')


def sactivated_04(ui):
    strategy_name = ui.svc_comboBoxxx_02.currentText()
    if strategy_name != '':
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql(f"SELECT * FROM stockoptivars WHERE `index` = '{strategy_name}'", con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.ss_textEditttt_05.clear()
            ui.ss_textEditttt_05.append(df['전략코드'][strategy_name])
            ui.svc_lineEdittt_02.setText(strategy_name)
        else:
            QMessageBox.critical(ui, '오류 알림', '범위가 DB에 존재하지 않습니다.\n범위을 다시 로딩하십시오.\n')


def sactivated_05(ui):
    strategy_name = ui.svc_comboBoxxx_08.currentText()
    if strategy_name != '':
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql(f"SELECT * FROM stockoptisell WHERE `index` = '{strategy_name}'", con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.ss_textEditttt_04.clear()
            ui.ss_textEditttt_04.append(df['전략코드'][strategy_name])
            ui.svc_lineEdittt_03.setText(strategy_name)
        else:
            QMessageBox.critical(ui, '오류 알림', '전략이 DB에 존재하지 않습니다.\n전략을 다시 로딩하십시오.\n')


def sactivated_06(ui):
    strategy_name = ui.sva_comboBoxxx_01.currentText()
    if strategy_name != '':
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql(f"SELECT * FROM stockvars WHERE `index` = '{strategy_name}'", con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.ss_textEditttt_06.clear()
            ui.ss_textEditttt_06.append(df['전략코드'][strategy_name])
            ui.sva_lineEdittt_01.setText(strategy_name)
        else:
            QMessageBox.critical(ui, '오류 알림', '범위가 DB에 존재하지 않습니다.\n범위을 다시 로딩하십시오.\n')


def sactivated_07(ui):
    strategy_name = ui.svo_comboBoxxx_01.currentText()
    if strategy_name != '':
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql(f"SELECT * FROM stockbuyconds WHERE `index` = '{strategy_name}'", con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.ss_textEditttt_07.clear()
            ui.ss_textEditttt_07.append(df['전략코드'][strategy_name])
            ui.svo_lineEdittt_01.setText(strategy_name)
        else:
            QMessageBox.critical(ui, '오류 알림', '조건이 DB에 존재하지 않습니다.\n조건을 다시 로딩하십시오.\n')


def sactivated_08(ui):
    strategy_name = ui.svo_comboBoxxx_02.currentText()
    if strategy_name != '':
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql(f"SELECT * FROM stocksellconds WHERE `index` = '{strategy_name}'", con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.ss_textEditttt_08.clear()
            ui.ss_textEditttt_08.append(df['전략코드'][strategy_name])
            ui.svo_lineEdittt_02.setText(strategy_name)
        else:
            QMessageBox.critical(ui, '오류 알림', '조건이 DB에 존재하지 않습니다.\n조건을 다시 로딩하십시오.\n')


def sactivated_09(ui):
    strategy_name = ui.sj_stock_cbBox_01.currentText()
    if strategy_name != '':
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql(f"SELECT * FROM stockoptibuy WHERE `index` = '{strategy_name}'", con).set_index('index')
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


def sactivated_10(ui):
    strategy_name = ui.sj_stock_cbBox_03.currentText()
    if strategy_name != '':
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql(f"SELECT * FROM stockoptibuy WHERE `index` = '{strategy_name}'", con).set_index('index')
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
