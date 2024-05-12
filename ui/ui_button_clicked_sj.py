import os
import random
import shutil
import sqlite3
import pandas as pd
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMessageBox, QLineEdit
from ui.set_logfile import SetLogFile
from ui.set_style import style_bc_bt
from ui.set_text import famous_saying
from utility.setting import DB_SETTING, DB_STRATEGY, DB_PATH
from utility.static import de_text, en_text, qtest_qwait


def sj_button_cicked_01(ui):
    con = sqlite3.connect(DB_SETTING)
    df = pd.read_sql('SELECT * FROM main', con).set_index('index')
    con.close()
    if len(df) > 0:
        ui.sj_main_comBox_01.setCurrentText(df['증권사'][0])
        ui.sj_main_cheBox_01.setChecked(True) if df['주식리시버'][0] else ui.sj_main_cheBox_01.setChecked(False)
        ui.sj_main_cheBox_02.setChecked(True) if df['주식트레이더'][0] else ui.sj_main_cheBox_02.setChecked(False)
        ui.sj_main_cheBox_03.setChecked(True) if df['주식틱데이터저장'][0] else ui.sj_main_cheBox_03.setChecked(False)
        ui.sj_main_comBox_02.setCurrentText(df['거래소'][0])
        ui.sj_main_cheBox_04.setChecked(True) if df['코인리시버'][0] else ui.sj_main_cheBox_04.setChecked(False)
        ui.sj_main_cheBox_05.setChecked(True) if df['코인트레이더'][0] else ui.sj_main_cheBox_05.setChecked(False)
        ui.sj_main_cheBox_06.setChecked(True) if df['코인틱데이터저장'][0] else ui.sj_main_cheBox_06.setChecked(False)
        ui.sj_main_cheBox_07.setChecked(True) if df['장중전략조건검색식사용'][0] else ui.sj_main_cheBox_07.setChecked(False)
        ui.sj_main_cheBox_08.setChecked(True) if not df['장중전략조건검색식사용'][0] else ui.sj_main_cheBox_08.setChecked(
            False)
        ui.sj_main_liEdit_01.setText(str(df['주식순위시간'][0]))
        ui.sj_main_liEdit_02.setText(str(df['주식순위선정'][0]))
        ui.sj_main_liEdit_03.setText(str(df['코인순위시간'][0]))
        ui.sj_main_liEdit_04.setText(str(df['코인순위선정'][0]))
        ui.sj_main_liEdit_05.setText(str(df['리시버실행시간'][0]))
        ui.sj_main_liEdit_06.setText(str(df['트레이더실행시간'][0]))
        ui.sj_main_comBox_03.setCurrentText('격리' if df['바이낸스선물마진타입'][0] == 'ISOLATED' else '교차')
        ui.sj_main_comBox_04.setCurrentText('단방향' if df['바이낸스선물포지션'][0] == 'false' else '양방향')
        ui.sj_main_cheBox_08.setChecked(True) if not df['장중전략조건검색식사용'][0] else ui.sj_main_cheBox_08.setChecked(
            False)
        ui.sj_main_cheBox_09.setChecked(True) if df['버전업'][0] else ui.sj_main_cheBox_09.setChecked(False)
        if df['리시버공유'][0] == 0:
            ui.sj_main_cheBox_10.setChecked(False)
            ui.sj_main_cheBox_11.setChecked(False)
        elif df['리시버공유'][0] == 1:
            ui.sj_main_cheBox_10.setChecked(True)
            ui.sj_main_cheBox_11.setChecked(False)
        elif df['리시버공유'][0] == 2:
            ui.sj_main_cheBox_10.setChecked(False)
            ui.sj_main_cheBox_11.setChecked(True)
    else:
        QMessageBox.critical(ui, '오류 알림', '기본 설정값이\n존재하지 않습니다.\n')


def sj_button_cicked_02(ui):
    con = sqlite3.connect(DB_SETTING)
    df = pd.read_sql('SELECT * FROM sacc', con).set_index('index')
    con.close()
    comob_name = ui.sj_main_comBox_01.currentText()
    if len(df) > 0:
        if comob_name == '키움증권1' and df['아이디1'][0] != '' and df['아이디2'][0] != '':
            ui.sj_sacc_liEdit_01.setText(de_text(ui.dict_set['키'], df['아이디1'][0]))
            ui.sj_sacc_liEdit_02.setText(de_text(ui.dict_set['키'], df['비밀번호1'][0]))
            ui.sj_sacc_liEdit_03.setText(de_text(ui.dict_set['키'], df['인증서비밀번호1'][0]))
            ui.sj_sacc_liEdit_04.setText(de_text(ui.dict_set['키'], df['계좌비밀번호1'][0]))
            ui.sj_sacc_liEdit_05.setText(de_text(ui.dict_set['키'], df['아이디2'][0]))
            ui.sj_sacc_liEdit_06.setText(de_text(ui.dict_set['키'], df['비밀번호2'][0]))
            ui.sj_sacc_liEdit_07.setText(de_text(ui.dict_set['키'], df['인증서비밀번호2'][0]))
            ui.sj_sacc_liEdit_08.setText(de_text(ui.dict_set['키'], df['계좌비밀번호2'][0]))
        elif comob_name == '키움증권2' and df['아이디3'][0] != '' and df['아이디4'][0] != '':
            ui.sj_sacc_liEdit_01.setText(de_text(ui.dict_set['키'], df['아이디3'][0]))
            ui.sj_sacc_liEdit_02.setText(de_text(ui.dict_set['키'], df['비밀번호3'][0]))
            ui.sj_sacc_liEdit_03.setText(de_text(ui.dict_set['키'], df['인증서비밀번호3'][0]))
            ui.sj_sacc_liEdit_04.setText(de_text(ui.dict_set['키'], df['계좌비밀번호3'][0]))
            ui.sj_sacc_liEdit_05.setText(de_text(ui.dict_set['키'], df['아이디4'][0]))
            ui.sj_sacc_liEdit_06.setText(de_text(ui.dict_set['키'], df['비밀번호4'][0]))
            ui.sj_sacc_liEdit_07.setText(de_text(ui.dict_set['키'], df['인증서비밀번호4'][0]))
            ui.sj_sacc_liEdit_08.setText(de_text(ui.dict_set['키'], df['계좌비밀번호4'][0]))
    else:
        QMessageBox.critical(ui, '오류 알림', '주식 계정 설정값이\n존재하지 않습니다.\n')


def sj_button_cicked_03(ui):
    con = sqlite3.connect(DB_SETTING)
    df = pd.read_sql('SELECT * FROM cacc', con).set_index('index')
    con.close()
    combo_name = ui.sj_main_comBox_02.currentText()
    if len(df) > 0:
        if combo_name == '업비트' and df['Access_key1'][0] != '' and df['Secret_key1'][0] != '':
            ui.sj_cacc_liEdit_01.setText(de_text(ui.dict_set['키'], df['Access_key1'][0]))
            ui.sj_cacc_liEdit_02.setText(de_text(ui.dict_set['키'], df['Secret_key1'][0]))
        elif combo_name == '바이낸스선물' and df['Access_key2'][0] != '' and df['Secret_key2'][0] != '':
            ui.sj_cacc_liEdit_01.setText(de_text(ui.dict_set['키'], df['Access_key2'][0]))
            ui.sj_cacc_liEdit_02.setText(de_text(ui.dict_set['키'], df['Secret_key2'][0]))
    else:
        QMessageBox.critical(ui, '오류 알림', '계정 설정값이\n존재하지 않습니다.\n')


def sj_button_cicked_04(ui):
    con = sqlite3.connect(DB_SETTING)
    df = pd.read_sql('SELECT * FROM telegram', con).set_index('index')
    con.close()
    if len(df) > 0 and df['str_bot'][0] != '':
        ui.sj_tele_liEdit_01.setText(de_text(ui.dict_set['키'], df['str_bot'][0]))
        ui.sj_tele_liEdit_02.setText(de_text(ui.dict_set['키'], df['int_id'][0]))
    else:
        QMessageBox.critical(ui, '오류 알림', '텔레그램 봇토큰 및 사용자 아이디\n설정값이 존재하지 않습니다.\n')


def sj_button_cicked_05(ui):
    con = sqlite3.connect(DB_SETTING)
    df = pd.read_sql('SELECT * FROM stock', con).set_index('index')
    con.close()
    con = sqlite3.connect(DB_STRATEGY)
    dfb = pd.read_sql('SELECT * FROM stockbuy', con).set_index('index')
    dfs = pd.read_sql('SELECT * FROM stocksell', con).set_index('index')
    dfob = pd.read_sql('SELECT * FROM stockoptibuy', con).set_index('index')
    dfos = pd.read_sql('SELECT * FROM stockoptisell', con).set_index('index')
    con.close()
    if len(df) > 0:
        ui.sj_stock_ckBox_01.setChecked(True) if df['주식모의투자'][0] else ui.sj_stock_ckBox_01.setChecked(False)
        ui.sj_stock_ckBox_02.setChecked(True) if df['주식알림소리'][0] else ui.sj_stock_ckBox_02.setChecked(False)
        ui.sj_stock_ckBox_03.setChecked(True) if df['주식장초잔고청산'][0] else ui.sj_stock_ckBox_03.setChecked(False)
        ui.sj_stock_ckBox_04.setChecked(True) if df['주식장초프로세스종료'][0] else ui.sj_stock_ckBox_04.setChecked(False)
        ui.sj_stock_ckBox_05.setChecked(True) if df['주식장초컴퓨터종료'][0] else ui.sj_stock_ckBox_05.setChecked(False)
        ui.sj_stock_ckBox_06.setChecked(True) if df['주식장중잔고청산'][0] else ui.sj_stock_ckBox_06.setChecked(False)
        ui.sj_stock_ckBox_07.setChecked(True) if df['주식장중프로세스종료'][0] else ui.sj_stock_ckBox_07.setChecked(False)
        ui.sj_stock_ckBox_08.setChecked(True) if df['주식장중컴퓨터종료'][0] else ui.sj_stock_ckBox_08.setChecked(False)
        ui.sj_stock_ckBox_09.setChecked(True) if df['주식투자금고정'][0] else ui.sj_stock_ckBox_09.setChecked(False)
        ui.sj_stock_ckBox_10.setChecked(True) if df['주식손실중지'][0] else ui.sj_stock_ckBox_10.setChecked(False)
        ui.sj_stock_ckBox_11.setChecked(True) if df['주식수익중지'][0] else ui.sj_stock_ckBox_11.setChecked(False)
        ui.sj_stock_ckBox_12.setChecked(True) if df['주식장초패턴인식'][0] else ui.sj_stock_ckBox_12.setChecked(False)
        ui.sj_stock_ckBox_13.setChecked(True) if df['주식장중패턴인식'][0] else ui.sj_stock_ckBox_13.setChecked(False)
        ui.sj_stock_lEdit_01.setText(str(df['주식장초평균값계산틱수'][0]))
        ui.sj_stock_lEdit_02.setText(str(df['주식장초최대매수종목수'][0]))
        ui.sj_stock_lEdit_03.setText(str(df['주식장초전략종료시간'][0]))
        ui.sj_stock_lEdit_04.setText(str(df['주식장중평균값계산틱수'][0]))
        ui.sj_stock_lEdit_05.setText(str(df['주식장중최대매수종목수'][0]))
        ui.sj_stock_lEdit_06.setText(str(df['주식장중전략종료시간'][0]))
        ui.sj_stock_cbBox_01.clear()
        ui.sj_stock_cbBox_02.clear()
        ui.sj_stock_cbBox_03.clear()
        ui.sj_stock_cbBox_04.clear()
        ui.sj_stock_cbBox_01.addItem('사용안함')
        ui.sj_stock_cbBox_02.addItem('사용안함')
        ui.sj_stock_cbBox_03.addItem('사용안함')
        ui.sj_stock_cbBox_04.addItem('사용안함')
        if len(dfb) > 0:
            stg_list = list(dfb.index)
            stg_list.sort()
            for stg in stg_list:
                ui.sj_stock_cbBox_01.addItem(stg)
                ui.sj_stock_cbBox_03.addItem(stg)
        if len(dfob) > 0:
            stg_list = list(dfob.index)
            stg_list.sort()
            for stg in stg_list:
                ui.sj_stock_cbBox_01.addItem(stg)
                ui.sj_stock_cbBox_03.addItem(stg)
        if df['주식장초매수전략'][0] != '':
            ui.sj_stock_cbBox_01.setCurrentText(df['주식장초매수전략'][0])
        if df['주식장중매수전략'][0] != '':
            ui.sj_stock_cbBox_03.setCurrentText(df['주식장중매수전략'][0])
        if len(dfs) > 0:
            stg_list = list(dfs.index)
            stg_list.sort()
            for stg in stg_list:
                ui.sj_stock_cbBox_02.addItem(stg)
                ui.sj_stock_cbBox_04.addItem(stg)
        if len(dfos) > 0:
            stg_list = list(dfos.index)
            stg_list.sort()
            for stg in stg_list:
                ui.sj_stock_cbBox_02.addItem(stg)
                ui.sj_stock_cbBox_04.addItem(stg)
        if df['주식장초매도전략'][0] != '':
            ui.sj_stock_cbBox_02.setCurrentText(df['주식장초매도전략'][0])
        if df['주식장중매도전략'][0] != '':
            ui.sj_stock_cbBox_04.setCurrentText(df['주식장중매도전략'][0])
        ui.sj_stock_lEdit_07.setText(str(df['주식장초투자금'][0]))
        ui.sj_stock_lEdit_08.setText(str(df['주식장중투자금'][0]))
        ui.sj_stock_lEdit_09.setText(str(df['주식손실중지수익률'][0]))
        ui.sj_stock_lEdit_10.setText(str(df['주식수익중지수익률'][0]))
        if 152000 <= df['주식장중전략종료시간'][0] <= 152759:
            QMessageBox.critical(ui, '오류 알림', '주식 장중전략의 종료시간을\n152000 ~ 152759 구간으로 설정할 수 없습니다.\n')
            return
    else:
        QMessageBox.critical(ui, '오류 알림', '주식 전략 설정값이\n존재하지 않습니다.\n')


def sj_button_cicked_06(ui):
    con = sqlite3.connect(DB_SETTING)
    df = pd.read_sql('SELECT * FROM coin', con).set_index('index')
    con.close()
    con = sqlite3.connect(DB_STRATEGY)
    dfb = pd.read_sql('SELECT * FROM coinbuy', con).set_index('index')
    dfs = pd.read_sql('SELECT * FROM coinsell', con).set_index('index')
    dfob = pd.read_sql('SELECT * FROM coinoptibuy', con).set_index('index')
    dfos = pd.read_sql('SELECT * FROM coinoptisell', con).set_index('index')
    con.close()
    if len(df) > 0:
        ui.sj_coin_cheBox_01.setChecked(True) if df['코인모의투자'][0] else ui.sj_coin_cheBox_01.setChecked(False)
        ui.sj_coin_cheBox_02.setChecked(True) if df['코인알림소리'][0] else ui.sj_coin_cheBox_02.setChecked(False)
        ui.sj_coin_cheBox_03.setChecked(True) if df['코인장초잔고청산'][0] else ui.sj_coin_cheBox_03.setChecked(False)
        ui.sj_coin_cheBox_04.setChecked(True) if df['코인장초프로세스종료'][0] else ui.sj_coin_cheBox_04.setChecked(False)
        ui.sj_coin_cheBox_05.setChecked(True) if df['코인장초컴퓨터종료'][0] else ui.sj_coin_cheBox_05.setChecked(False)
        ui.sj_coin_cheBox_06.setChecked(True) if df['코인장중잔고청산'][0] else ui.sj_coin_cheBox_06.setChecked(False)
        ui.sj_coin_cheBox_07.setChecked(True) if df['코인장중프로세스종료'][0] else ui.sj_coin_cheBox_07.setChecked(False)
        ui.sj_coin_cheBox_08.setChecked(True) if df['코인장중컴퓨터종료'][0] else ui.sj_coin_cheBox_08.setChecked(False)
        ui.sj_coin_cheBox_09.setChecked(True) if df['코인투자금고정'][0] else ui.sj_coin_cheBox_09.setChecked(False)
        ui.sj_coin_cheBox_10.setChecked(True) if df['코인손실중지'][0] else ui.sj_coin_cheBox_10.setChecked(False)
        ui.sj_coin_cheBox_11.setChecked(True) if df['코인수익중지'][0] else ui.sj_coin_cheBox_11.setChecked(False)
        ui.sj_coin_cheBox_12.setChecked(True) if df['코인장초패턴인식'][0] else ui.sj_coin_cheBox_12.setChecked(False)
        ui.sj_coin_cheBox_13.setChecked(True) if df['코인장중패턴인식'][0] else ui.sj_coin_cheBox_13.setChecked(False)
        ui.sj_coin_liEdit_01.setText(str(df['코인장초평균값계산틱수'][0]))
        ui.sj_coin_liEdit_02.setText(str(df['코인장초최대매수종목수'][0]))
        ui.sj_coin_liEdit_03.setText(str(df['코인장초전략종료시간'][0]))
        ui.sj_coin_liEdit_04.setText(str(df['코인장중평균값계산틱수'][0]))
        ui.sj_coin_liEdit_05.setText(str(df['코인장중최대매수종목수'][0]))
        ui.sj_coin_liEdit_06.setText(str(df['코인장중전략종료시간'][0]))
        ui.sj_coin_comBox_01.clear()
        ui.sj_coin_comBox_02.clear()
        ui.sj_coin_comBox_03.clear()
        ui.sj_coin_comBox_04.clear()
        ui.sj_coin_comBox_01.addItem('사용안함')
        ui.sj_coin_comBox_02.addItem('사용안함')
        ui.sj_coin_comBox_03.addItem('사용안함')
        ui.sj_coin_comBox_04.addItem('사용안함')
        if len(dfb) > 0:
            stg_list = list(dfb.index)
            stg_list.sort()
            for stg in stg_list:
                ui.sj_coin_comBox_01.addItem(stg)
                ui.sj_coin_comBox_03.addItem(stg)
        if len(dfob) > 0:
            stg_list = list(dfob.index)
            stg_list.sort()
            for stg in stg_list:
                ui.sj_coin_comBox_01.addItem(stg)
                ui.sj_coin_comBox_03.addItem(stg)
        if df['코인장초매수전략'][0] != '':
            ui.sj_coin_comBox_01.setCurrentText(df['코인장초매수전략'][0])
        if df['코인장중매수전략'][0] != '':
            ui.sj_coin_comBox_03.setCurrentText(df['코인장중매수전략'][0])
        if len(dfs) > 0:
            stg_list = list(dfs.index)
            stg_list.sort()
            for stg in stg_list:
                ui.sj_coin_comBox_02.addItem(stg)
                ui.sj_coin_comBox_04.addItem(stg)
        if len(dfos) > 0:
            stg_list = list(dfos.index)
            stg_list.sort()
            for stg in stg_list:
                ui.sj_coin_comBox_02.addItem(stg)
                ui.sj_coin_comBox_04.addItem(stg)
        if df['코인장초매도전략'][0] != '':
            ui.sj_coin_comBox_02.setCurrentText(df['코인장초매도전략'][0])
        if df['코인장중매도전략'][0] != '':
            ui.sj_coin_comBox_04.setCurrentText(df['코인장중매도전략'][0])
        ui.sj_coin_liEdit_07.setText(str(df['코인장초투자금'][0]))
        ui.sj_coin_liEdit_08.setText(str(df['코인장중투자금'][0]))
        ui.sj_coin_liEdit_09.setText(str(df['코인손실중지수익률'][0]))
        ui.sj_coin_liEdit_10.setText(str(df['코인수익중지수익률'][0]))
        if df['코인장중전략종료시간'][0] > 234500:
            QMessageBox.critical(ui, '오류 알림', '코인 장중전략의 종료시간은\n234500미만으로 설정하십시오.\n')
    else:
        QMessageBox.critical(ui, '오류 알림', '코인 전략 설정값이\n존재하지 않습니다.\n')


def sj_button_cicked_07(ui):
    con = sqlite3.connect(DB_SETTING)
    df = pd.read_sql('SELECT * FROM back', con).set_index('index')
    con.close()
    if len(df) > 0:
        ui.sj_back_cheBox_01.setChecked(True) if df['블랙리스트추가'][0] else ui.sj_back_cheBox_01.setChecked(False)
        ui.sj_back_cheBox_02.setChecked(True) if df['백테주문관리적용'][0] else ui.sj_back_cheBox_02.setChecked(False)
        ui.sj_back_cheBox_03.setChecked(True) if df['백테매수시간기준'][0] else ui.sj_back_cheBox_03.setChecked(False)
        ui.sj_back_cheBox_04.setChecked(True) if df['백테일괄로딩'][0] else ui.sj_back_cheBox_04.setChecked(False)
        ui.sj_back_cheBox_05.setChecked(True) if not df['백테일괄로딩'][0] else ui.sj_back_cheBox_05.setChecked(False)
        ui.sj_back_cheBox_12.setChecked(True) if df['보조지표사용'][0] else ui.sj_back_cheBox_12.setChecked(False)
        ui.sj_back_cheBox_13.setChecked(True) if df['그래프저장하지않기'][0] else ui.sj_back_cheBox_13.setChecked(False)
        ui.sj_back_cheBox_14.setChecked(True) if df['그래프띄우지않기'][0] else ui.sj_back_cheBox_14.setChecked(False)
        ui.sj_back_cheBox_15.setChecked(True) if df['디비자동관리'][0] else ui.sj_back_cheBox_15.setChecked(False)
        ui.sj_back_cheBox_16.setChecked(True) if df['교차검증가중치'][0] else ui.sj_back_cheBox_16.setChecked(False)
        ui.sj_back_comBox_04.clear()
        ui.sj_back_cheBox_19.setChecked(True) if df['백테스케쥴실행'][0] else ui.sj_back_cheBox_19.setChecked(False)
        con = sqlite3.connect(DB_STRATEGY)
        dfs = pd.read_sql('SELECT * FROM schedule', con).set_index('index')
        con.close()
        indexs = list(dfs.index)
        indexs.sort()
        for index in indexs:
            ui.sj_back_comBox_04.addItem(index)
        if df['백테스케쥴요일'][0] == 4:
            ui.sj_back_comBox_05.setCurrentText('금')
        elif df['백테스케쥴요일'][0] == 5:
            ui.sj_back_comBox_05.setCurrentText('토')
        elif df['백테스케쥴요일'][0] == 6:
            ui.sj_back_comBox_05.setCurrentText('일')
        ui.sj_back_liEdit_03.setText(str(df['백테스케쥴시간'][0]))
        ui.sj_back_comBox_03.setCurrentText(df['백테스케쥴구분'][0])
        ui.sj_back_comBox_04.setCurrentText(df['백테스케쥴명'][0])
        ui.sj_back_cheBox_17.setChecked(True) if not df['백테날짜고정'][0] else ui.sj_back_cheBox_17.setChecked(False)
        ui.sj_back_cheBox_18.setChecked(True) if df['백테날짜고정'][0] else ui.sj_back_cheBox_18.setChecked(False)
        if df['백테날짜고정'][0]:
            ui.sj_back_daEdit_01.setDate(QDate.fromString(ui.dict_set['백테날짜'], 'yyyyMMdd'))
        else:
            ui.sj_back_liEdit_02.setText(df['백테날짜'][0])
        ui.sj_back_cheBox_20.setChecked(True) if df['범위자동관리'][0] else ui.sj_back_cheBox_20.setChecked(False)
    else:
        QMessageBox.critical(ui, '오류 알림', '백테 설정값이\n존재하지 않습니다.\n')


def sj_button_cicked_08(ui):
    con = sqlite3.connect(DB_SETTING)
    df = pd.read_sql('SELECT * FROM etc', con).set_index('index')
    con.close()
    if len(df) > 0:
        ui.sj_etc_checBox_01.setChecked(True) if df['인트로숨김'][0] else ui.sj_etc_checBox_01.setChecked(False)
        ui.sj_etc_checBox_02.setChecked(True) if df['저해상도'][0] else ui.sj_etc_checBox_02.setChecked(False)
        ui.sj_etc_checBox_04.setChecked(True) if df['휴무프로세스종료'][0] else ui.sj_etc_checBox_04.setChecked(False)
        ui.sj_etc_checBox_05.setChecked(True) if df['휴무컴퓨터종료'][0] else ui.sj_etc_checBox_05.setChecked(False)
        ui.sj_etc_checBox_03.setChecked(True) if df['창위치기억'][0] else ui.sj_etc_checBox_03.setChecked(False)
        ui.sj_etc_checBox_06.setChecked(True) if df['스톰라이브'][0] else ui.sj_etc_checBox_06.setChecked(False)
        ui.sj_etc_checBox_07.setChecked(True) if df['프로그램종료'][0] else ui.sj_etc_checBox_07.setChecked(False)
        ui.sj_etc_comBoxx_01.setCurrentText(df['테마'][0])
    else:
        QMessageBox.critical(ui, '오류 알림', '기타 설정값이\n존재하지 않습니다.\n')


def sj_button_cicked_09(ui, proc_query, queryQ):
    sg = ui.sj_main_comBox_01.currentText()
    sr = 1 if ui.sj_main_cheBox_01.isChecked() else 0
    st = 1 if ui.sj_main_cheBox_02.isChecked() else 0
    ss = 1 if ui.sj_main_cheBox_03.isChecked() else 0
    cg = ui.sj_main_comBox_02.currentText()
    cr = 1 if ui.sj_main_cheBox_04.isChecked() else 0
    ct = 1 if ui.sj_main_cheBox_05.isChecked() else 0
    cs = 1 if ui.sj_main_cheBox_06.isChecked() else 0
    jj = 1 if ui.sj_main_cheBox_07.isChecked() else 0
    smt = ui.sj_main_liEdit_01.text()
    smd = ui.sj_main_liEdit_02.text()
    cmt = ui.sj_main_liEdit_03.text()
    cmd = ui.sj_main_liEdit_04.text()
    rdt = ui.sj_main_liEdit_05.text()
    tdt = ui.sj_main_liEdit_06.text()
    mt = 'ISOLATED' if ui.sj_main_comBox_03.currentText() == '격리' else 'CROSSED'
    pt = 'false' if ui.sj_main_comBox_04.currentText() == '단방향' else 'true'
    vu = 1 if ui.sj_main_cheBox_09.isChecked() else 0
    if ui.sj_main_cheBox_10.isChecked():
        rg = 1
    elif ui.sj_main_cheBox_11.isChecked():
        rg = 2
    else:
        rg = 0
    if int(cmd) < 10:
        QMessageBox.critical(ui, '오류 알림', '코인순위선정은 10이상의 수만 입력하십시오.\n')
    elif '' in (smt, smd, cmt, cmd, rdt, tdt):
        QMessageBox.critical(ui, '오류 알림', '일부 설정값이 입력되지 않았습니다.\n')
    else:
        smt, smd, cmt, cmd, rdt, tdt = int(smt), int(smd), int(cmt), int(cmd), int(rdt), int(tdt)
        if proc_query.is_alive():
            query = f"UPDATE main SET 증권사 = '{sg}', 주식리시버 = {sr}, 주식트레이더 = {st}, 주식틱데이터저장 = {ss}, " \
                    f"거래소 = '{cg}', 코인리시버 = {cr}, 코인트레이더 = {ct}, 코인틱데이터저장 = {cs}, 장중전략조건검색식사용 = {jj}, " \
                    f"주식순위시간 = {smt}, 주식순위선정 = {smd}, 코인순위시간 = {cmt}, 코인순위선정 = {cmd}, 리시버실행시간 = {rdt}, " \
                    f"트레이더실행시간 = {tdt}, 바이낸스선물마진타입 = '{mt}', 바이낸스선물포지션 = '{pt}', '버전업' = {vu}, '리시버공유' = {rg}"
            queryQ.put(('설정디비', query))
        QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))

        ui.dict_set['증권사'] = sg
        ui.dict_set['주식리시버'] = sr
        ui.dict_set['주식트레이더'] = st
        ui.dict_set['주식틱데이터저장'] = ss
        ui.dict_set['거래소'] = cg
        ui.dict_set['코인리시버'] = cr
        ui.dict_set['코인트레이더'] = ct
        ui.dict_set['코인틱데이터저장'] = cs
        ui.dict_set['장중전략조건검색식사용'] = jj
        ui.dict_set['주식순위시간'] = smt
        ui.dict_set['주식순위선정'] = smd
        ui.dict_set['코인순위시간'] = cmt
        ui.dict_set['코인순위선정'] = cmd
        ui.dict_set['리시버실행시간'] = rdt
        ui.dict_set['트레이더실행시간'] = tdt
        ui.dict_set['바이낸스선물마진타입'] = mt
        ui.dict_set['바이낸스선물포지션'] = pt
        ui.dict_set['버전업'] = vu
        ui.dict_set['리시버공유'] = rg

        if ui.dict_set['거래소'] == '업비트':
            ui.sj_coin_labell_03.setText(
                '장초전략                        백만원,  장중전략                        백만원              전략중지 및 잔고청산  |')
        else:
            ui.sj_coin_labell_03.setText(
                '장초전략                        USDT,   장중전략                        USDT              전략중지 및 잔고청산  |')
        ui.UpdateDictSet()
        SetLogFile(ui)


def sj_button_cicked_10(ui, proc_query, queryQ):
    id1 = ui.sj_sacc_liEdit_01.text()
    ps1 = ui.sj_sacc_liEdit_02.text()
    cp1 = ui.sj_sacc_liEdit_03.text()
    ap1 = ui.sj_sacc_liEdit_04.text()
    id2 = ui.sj_sacc_liEdit_05.text()
    ps2 = ui.sj_sacc_liEdit_06.text()
    cp2 = ui.sj_sacc_liEdit_07.text()
    ap2 = ui.sj_sacc_liEdit_08.text()
    comob_name = ui.sj_main_comBox_01.currentText()
    if '' in (id1, ps1, cp1, ap1, id2, ps2, cp2, ap2):
        QMessageBox.critical(ui, '오류 알림', '일부 설정값이 입력되지 않았습니다.\n')
    else:
        en_id1 = en_text(ui.dict_set['키'], id1)
        en_ps1 = en_text(ui.dict_set['키'], ps1)
        en_cp1 = en_text(ui.dict_set['키'], cp1)
        en_ap1 = en_text(ui.dict_set['키'], ap1)
        en_id2 = en_text(ui.dict_set['키'], id2)
        en_ps2 = en_text(ui.dict_set['키'], ps2)
        en_cp2 = en_text(ui.dict_set['키'], cp2)
        en_ap2 = en_text(ui.dict_set['키'], ap2)
        if comob_name == '키움증권1':
            if proc_query.is_alive():
                query = f"UPDATE sacc SET " \
                        f"아이디1 = '{en_id1}', 비밀번호1 = '{en_ps1}', 인증서비밀번호1 = '{en_cp1}', 계좌비밀번호1 = '{en_ap1}', " \
                        f"아이디2 = '{en_id2}', 비밀번호2 = '{en_ps2}', 인증서비밀번호2 = '{en_cp2}', 계좌비밀번호2 = '{en_ap2}'"
                queryQ.put(('설정디비', query))
            ui.dict_set['아이디1'] = id1
            ui.dict_set['비밀번호1'] = ps1
            ui.dict_set['인증서비밀번호1'] = cp1
            ui.dict_set['계좌비밀번호1'] = ap1
            ui.dict_set['아이디2'] = id2
            ui.dict_set['비밀번호2'] = ps2
            ui.dict_set['인증서비밀번호2'] = cp2
            ui.dict_set['계좌비밀번호2'] = ap2
        else:
            if proc_query.is_alive():
                query = f"UPDATE sacc SET " \
                        f"아이디3 = '{en_id1}', 비밀번호3 = '{en_ps1}', 인증서비밀번호3 = '{en_cp1}', 계좌비밀번호3 = '{en_ap1}', " \
                        f"아이디4 = '{en_id2}', 비밀번호4 = '{en_ps2}', 인증서비밀번호4 = '{en_cp2}', 계좌비밀번호4 = '{en_ap2}'"
                queryQ.put(('설정디비', query))
            ui.dict_set['아이디3'] = id1
            ui.dict_set['비밀번호3'] = ps1
            ui.dict_set['인증서비밀번호3'] = cp1
            ui.dict_set['계좌비밀번호3'] = ap1
            ui.dict_set['아이디4'] = id2
            ui.dict_set['비밀번호4'] = ps2
            ui.dict_set['인증서비밀번호4'] = cp2
            ui.dict_set['계좌비밀번호4'] = ap2
        QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))


def sj_button_cicked_11(ui, proc_query, queryQ):
    access_key = ui.sj_cacc_liEdit_01.text()
    secret_key = ui.sj_cacc_liEdit_02.text()
    if '' in (access_key, secret_key):
        QMessageBox.critical(ui, '오류 알림', '일부 설정값이 입력되지 않았습니다.\n')
    else:
        combo_name = ui.sj_main_comBox_02.currentText()
        if proc_query.is_alive():
            en_access_key = en_text(ui.dict_set['키'], access_key)
            en_secret_key = en_text(ui.dict_set['키'], secret_key)
            if combo_name == '업비트':
                query = f"UPDATE cacc SET Access_key1 = '{en_access_key}', Secret_key1 = '{en_secret_key}'"
            else:
                query = f"UPDATE cacc SET Access_key2 = '{en_access_key}', Secret_key2 = '{en_secret_key}'"
            queryQ.put(('설정디비', query))

        if combo_name == '업비트':
            ui.dict_set['Access_key1'] = access_key
            ui.dict_set['Secret_key1'] = secret_key
        else:
            ui.dict_set['Access_key2'] = access_key
            ui.dict_set['Secret_key2'] = secret_key
        QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))


def sj_button_cicked_12(ui, proc_query, queryQ, teleQ):
    str_bot = ui.sj_tele_liEdit_01.text()
    int_id = ui.sj_tele_liEdit_02.text()
    if '' in (str_bot, int_id):
        QMessageBox.critical(ui, '오류 알림', '일부 설정값이 입력되지 않았습니다.\n')
    else:
        if proc_query.is_alive():
            en_str_bot = en_text(ui.dict_set['키'], str_bot)
            en_int_id = en_text(ui.dict_set['키'], int_id)
            df = pd.DataFrame([[en_str_bot, en_int_id]], columns=['str_bot', 'int_id'], index=[0])
            queryQ.put(('설정디비', df, 'telegram', 'replace'))

        ui.dict_set['텔레그램봇토큰'] = str_bot
        ui.dict_set['텔레그램사용자아이디'] = int(int_id)
        teleQ.put(('설정변경', ui.dict_set))
        QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))


def sj_button_cicked_13(ui, proc_query, queryQ):
    me = 1 if ui.sj_stock_ckBox_01.isChecked() else 0
    sd = 1 if ui.sj_stock_ckBox_02.isChecked() else 0
    cs1 = 1 if ui.sj_stock_ckBox_03.isChecked() else 0
    pc1 = 1 if ui.sj_stock_ckBox_04.isChecked() else 0
    ce1 = 1 if ui.sj_stock_ckBox_05.isChecked() else 0
    cs2 = 1 if ui.sj_stock_ckBox_06.isChecked() else 0
    pc2 = 1 if ui.sj_stock_ckBox_07.isChecked() else 0
    ce2 = 1 if ui.sj_stock_ckBox_08.isChecked() else 0
    ts = 1 if ui.sj_stock_ckBox_09.isChecked() else 0
    cm = 1 if ui.sj_stock_ckBox_10.isChecked() else 0
    cp = 1 if ui.sj_stock_ckBox_11.isChecked() else 0
    p1 = 1 if ui.sj_stock_ckBox_12.isChecked() else 0
    p2 = 1 if ui.sj_stock_ckBox_13.isChecked() else 0
    by1 = ui.sj_stock_cbBox_01.currentText()
    sl1 = ui.sj_stock_cbBox_02.currentText()
    by2 = ui.sj_stock_cbBox_03.currentText()
    sl2 = ui.sj_stock_cbBox_04.currentText()
    at1 = ui.sj_stock_lEdit_01.text()
    bc1 = ui.sj_stock_lEdit_02.text()
    se1 = ui.sj_stock_lEdit_03.text()
    at2 = ui.sj_stock_lEdit_04.text()
    bc2 = ui.sj_stock_lEdit_05.text()
    se2 = ui.sj_stock_lEdit_06.text()
    sc = ui.sj_stock_lEdit_07.text()
    sj = ui.sj_stock_lEdit_08.text()
    cmp = ui.sj_stock_lEdit_09.text()
    cpp = ui.sj_stock_lEdit_10.text()
    if '' in (at1, bc1, se1, at2, bc2, se2, sc, sj, cmp, cpp):
        QMessageBox.critical(ui, '오류 알림', '일부 설정값이 입력되지 않았습니다.\n')
    else:
        at1, bc1, se1, at2, bc2, se2, sc, sj, cmp, cpp = \
            int(at1), int(bc1), int(se1), int(at2), int(bc2), int(se2), float(sc), float(sj), float(cmp), float(cpp)
        if 152000 <= se2 <= 152759 or se2 > 152900:
            QMessageBox.critical(ui, '오류 알림', '주식 장중전략의 종료시간을\n152000~152759, 152901~ 구간으로 설정할 수 없습니다.\n')
            return
        if by1 == '사용안함':
            by1 = ''
        if by2 == '사용안함':
            by2 = ''
        if sl1 == '사용안함':
            sl1 = ''
        if sl2 == '사용안함':
            sl2 = ''

        if proc_query.is_alive():
            query = f"UPDATE stock SET 주식모의투자 = {me}, 주식알림소리 = {sd}, 주식장초매수전략 = '{by1}', 주식장초매도전략 = '{sl1}', " \
                    f"주식장초평균값계산틱수 = {at1}, 주식장초최대매수종목수 = {bc1}, 주식장초전략종료시간 = {se1}, 주식장초잔고청산 = {cs1}, " \
                    f"주식장초프로세스종료 = {pc1}, 주식장초컴퓨터종료 = {ce1}, 주식장중매수전략 = '{by2}', 주식장중매도전략 = '{sl2}', " \
                    f"주식장중평균값계산틱수 = {at2}, 주식장중최대매수종목수 = {bc2}, 주식장중전략종료시간 = {se2}, 주식장중잔고청산 = {cs2}, " \
                    f"주식장중프로세스종료 = {pc2}, 주식장중컴퓨터종료 = {ce2}, 주식투자금고정 = {ts}, 주식장초투자금 = {sc}, " \
                    f"주식장중투자금 = {sj}, 주식손실중지 = {cm}, 주식손실중지수익률 = {cmp}, 주식수익중지 = {cp}, 주식수익중지수익률 = {cpp}, " \
                    f"주식장초패턴인식 = {p1}, 주식장중패턴인식 = {p2}"
            queryQ.put(('설정디비', query))
        QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))

        ui.dict_set['주식모의투자'] = me
        ui.dict_set['주식알림소리'] = sd
        ui.dict_set['주식장초매수전략'] = by1
        ui.dict_set['주식장초매도전략'] = sl1
        ui.dict_set['주식장초평균값계산틱수'] = at1
        ui.dict_set['주식장초최대매수종목수'] = bc1
        ui.dict_set['주식장초전략종료시간'] = se1
        ui.dict_set['주식장초잔고청산'] = cs1
        ui.dict_set['주식장초프로세스종료'] = pc1
        ui.dict_set['주식장초컴퓨터종료'] = ce1
        ui.dict_set['주식장중매수전략'] = by2
        ui.dict_set['주식장중매도전략'] = sl2
        ui.dict_set['주식장중평균값계산틱수'] = at2
        ui.dict_set['주식장중최대매수종목수'] = bc2
        ui.dict_set['주식장중전략종료시간'] = se2
        ui.dict_set['주식장중잔고청산'] = cs2
        ui.dict_set['주식장중프로세스종료'] = pc2
        ui.dict_set['주식장중컴퓨터종료'] = ce2
        ui.dict_set['주식투자금고정'] = ts
        ui.dict_set['주식장초투자금'] = sc
        ui.dict_set['주식장중투자금'] = sj
        ui.dict_set['주식손실중지'] = cm
        ui.dict_set['주식손실중지수익률'] = cmp
        ui.dict_set['주식수익중지'] = cp
        ui.dict_set['주식수익중지수익률'] = cpp
        ui.dict_set['주식장초패턴인식'] = p1
        ui.dict_set['주식장중패턴인식'] = p2
        ui.UpdateDictSet()


def sj_button_cicked_14(ui, proc_query, queryQ):
    me = 1 if ui.sj_coin_cheBox_01.isChecked() else 0
    sd = 1 if ui.sj_coin_cheBox_02.isChecked() else 0
    cs1 = 1 if ui.sj_coin_cheBox_03.isChecked() else 0
    pc1 = 1 if ui.sj_coin_cheBox_04.isChecked() else 0
    ce1 = 1 if ui.sj_coin_cheBox_05.isChecked() else 0
    cs2 = 1 if ui.sj_coin_cheBox_06.isChecked() else 0
    pc2 = 1 if ui.sj_coin_cheBox_07.isChecked() else 0
    ce2 = 1 if ui.sj_coin_cheBox_08.isChecked() else 0
    tc = 1 if ui.sj_coin_cheBox_09.isChecked() else 0
    cm = 1 if ui.sj_coin_cheBox_10.isChecked() else 0
    cp = 1 if ui.sj_coin_cheBox_11.isChecked() else 0
    p1 = 1 if ui.sj_coin_cheBox_12.isChecked() else 0
    p2 = 1 if ui.sj_coin_cheBox_13.isChecked() else 0
    by1 = ui.sj_coin_comBox_01.currentText()
    sl1 = ui.sj_coin_comBox_02.currentText()
    by2 = ui.sj_coin_comBox_03.currentText()
    sl2 = ui.sj_coin_comBox_04.currentText()
    at1 = ui.sj_coin_liEdit_01.text()
    bc1 = ui.sj_coin_liEdit_02.text()
    se1 = ui.sj_coin_liEdit_03.text()
    at2 = ui.sj_coin_liEdit_04.text()
    bc2 = ui.sj_coin_liEdit_05.text()
    se2 = ui.sj_coin_liEdit_06.text()
    sc = ui.sj_coin_liEdit_07.text()
    sj = ui.sj_coin_liEdit_08.text()
    cmp = ui.sj_coin_liEdit_09.text()
    cpp = ui.sj_coin_liEdit_10.text()
    if '' in (at1, bc1, se1, at2, bc2, se2, sc, sj, cmp, cpp):
        QMessageBox.critical(ui, '오류 알림', '일부 설정값이 입력되지 않았습니다.\n')
    else:
        buttonReply = QMessageBox.question(
            ui, "경고", "코인의 전략 종료시간은 UTC 기준입니다.\n한국시간 -9시간으로 설정하였습니까?\n",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if buttonReply == QMessageBox.Yes:
            at1, bc1, se1, at2, bc2, se2, sc, sj, cmp, cpp = \
                int(at1), int(bc1), int(se1), int(at2), int(bc2), int(se2), float(sc), float(sj), float(cmp), float(cpp)
            if se2 > 234500:
                QMessageBox.critical(ui, '오류 알림', '코인 장중전략의 종료시간은\n234500미만으로 설정하십시오.\n')
                return

            if by1 == '사용안함':
                by1 = ''
            if by2 == '사용안함':
                by2 = ''
            if sl1 == '사용안함':
                sl1 = ''
            if sl2 == '사용안함':
                sl2 = ''

            if proc_query.is_alive():
                query = f"UPDATE coin SET 코인모의투자 = {me}, 코인알림소리 = {sd}, 코인장초매수전략 = '{by1}', 코인장초매도전략 = '{sl1}', " \
                        f"코인장초평균값계산틱수 = {at1}, 코인장초최대매수종목수 = {bc1}, 코인장초전략종료시간 = {se1}, 코인장초잔고청산 = {cs1}, " \
                        f"코인장초프로세스종료 = {pc1}, 코인장초컴퓨터종료 = {ce1}, 코인장중매수전략 = '{by2}', 코인장중매도전략 = '{sl2}', " \
                        f"코인장중평균값계산틱수 = {at2}, 코인장중최대매수종목수 = {bc2}, 코인장중전략종료시간 = {se2}, 코인장중잔고청산 = {cs2}, " \
                        f"코인장중프로세스종료 = {pc2}, 코인장중컴퓨터종료 = {ce2}, 코인투자금고정 = {tc}, 코인장초투자금 = {sc}, " \
                        f"코인장중투자금 = {sj}, 코인손실중지 = {cm}, 코인손실중지수익률 = {cmp}, 코인수익중지 = {cp}, 코인수익중지수익률 = {cpp}, " \
                        f"코인장초패턴인식 = {p1}, 코인장중패턴인식 = {p2}"
                queryQ.put(('설정디비', query))
            QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))

            ui.dict_set['코인모의투자'] = me
            ui.dict_set['코인알림소리'] = sd
            ui.dict_set['코인장초매수전략'] = by1
            ui.dict_set['코인장초매도전략'] = sl1
            ui.dict_set['코인장초평균값계산틱수'] = at1
            ui.dict_set['코인장초최대매수종목수'] = bc1
            ui.dict_set['코인장초전략종료시간'] = se1
            ui.dict_set['코인장초잔고청산'] = cs1
            ui.dict_set['코인장초프로세스종료'] = pc1
            ui.dict_set['코인장초컴퓨터종료'] = ce1
            ui.dict_set['코인장중매수전략'] = by2
            ui.dict_set['코인장중매도전략'] = sl2
            ui.dict_set['코인장중평균값계산틱수'] = at2
            ui.dict_set['코인장중최대매수종목수'] = bc2
            ui.dict_set['코인장중전략종료시간'] = se2
            ui.dict_set['코인장중잔고청산'] = cs2
            ui.dict_set['코인장중프로세스종료'] = pc2
            ui.dict_set['코인장중컴퓨터종료'] = ce2
            ui.dict_set['코인투자금고정'] = tc
            ui.dict_set['코인장초투자금'] = sc
            ui.dict_set['코인장중투자금'] = sj
            ui.dict_set['코인손실중지'] = cm
            ui.dict_set['코인손실중지수익률'] = cmp
            ui.dict_set['코인수익중지'] = cp
            ui.dict_set['코인수익중지수익률'] = cpp
            ui.dict_set['코인장초패턴인식'] = p1
            ui.dict_set['코인장중패턴인식'] = p2
            ui.UpdateDictSet()


def sj_button_cicked_15(ui, proc_query, queryQ):
    bl = 1 if ui.sj_back_cheBox_01.isChecked() else 0
    bbg = 1 if ui.sj_back_cheBox_02.isChecked() else 0
    bsg = 1 if ui.sj_back_cheBox_03.isChecked() else 0
    bld = 1 if ui.sj_back_cheBox_04.isChecked() else 0
    bjj = 1 if ui.sj_back_cheBox_12.isChecked() else 0
    gsv = 1 if ui.sj_back_cheBox_13.isChecked() else 0
    gpl = 1 if ui.sj_back_cheBox_14.isChecked() else 0
    atd = 1 if ui.sj_back_cheBox_15.isChecked() else 0
    ext = 1 if ui.sj_back_cheBox_16.isChecked() else 0
    bdf = 1 if ui.sj_back_cheBox_18.isChecked() else 0
    bwd = 0
    bss = 1 if ui.sj_back_cheBox_19.isChecked() else 0
    if ui.sj_back_comBox_05.currentText() == '금':
        bwd = 4
    elif ui.sj_back_comBox_05.currentText() == '토':
        bwd = 5
    elif ui.sj_back_comBox_05.currentText() == '일':
        bwd = 6
    bst = ui.sj_back_liEdit_03.text()
    abd = ui.sj_back_comBox_03.currentText()
    abn = ui.sj_back_comBox_04.currentText()
    if bdf:
        bd = ui.sj_back_daEdit_01.date().toString('yyyyMMdd')
    else:
        bd = ui.sj_back_liEdit_02.text()
    aa = 1 if ui.sj_back_cheBox_20.isChecked() else 0

    if '' in (bd, bst):
        QMessageBox.critical(ui, '오류 알림', '일부 설정값이 입력되지 않았습니다.\n')
    else:
        bst = int(bst)
        if proc_query.is_alive():
            query = f"UPDATE back SET 블랙리스트추가 = {bl}, 백테주문관리적용 = {bbg}, 백테매수시간기준 = {bsg}, 백테일괄로딩 = {bld}, " \
                    f"그래프저장하지않기 = {gsv}, 그래프띄우지않기 = {gpl}, 디비자동관리 = {atd}, 교차검증가중치 = {ext}, 백테스케쥴실행 = {bss}, " \
                    f"백테스케쥴요일 = {bwd}, 백테스케쥴시간 = {bst}, 백테스케쥴구분 = '{abd}', 백테스케쥴명 = '{abn}', " \
                    f"백테날짜고정 = {bdf}, 백테날짜 = '{bd}', 범위자동관리 = {aa}, 보조지표사용 = {bjj}"
            queryQ.put(('설정디비', query))
        QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))

        pre_bbg = ui.dict_set['백테주문관리적용']
        ui.dict_set['블랙리스트추가'] = bl
        ui.dict_set['백테주문관리적용'] = bbg
        ui.dict_set['백테매수시간기준'] = bsg
        ui.dict_set['백테일괄로딩'] = bld
        ui.dict_set['그래프저장하지않기'] = gsv
        ui.dict_set['그래프띄우지않기'] = gpl
        ui.dict_set['디비자동관리'] = atd
        ui.dict_set['교차검증가중치'] = ext
        ui.dict_set['백테스케쥴실행'] = bss
        ui.dict_set['백테스케쥴요일'] = bwd
        ui.dict_set['백테스케쥴시간'] = bst
        ui.dict_set['백테스케쥴구분'] = abd
        ui.dict_set['백테스케쥴명'] = abn
        ui.dict_set['백테날짜고정'] = bdf
        ui.dict_set['백테날짜'] = bd
        ui.dict_set['범위자동관리'] = aa
        ui.dict_set['보조지표사용'] = bjj
        ui.UpdateDictSet()
        if pre_bbg != bbg:
            ui.BacktestEngineKill()


def sj_button_cicked_16(ui, proc_query, queryQ):
    the = ui.sj_etc_comBoxx_01.currentText()
    inr = 1 if ui.sj_etc_checBox_01.isChecked() else 0
    ldp = 1 if ui.sj_etc_checBox_02.isChecked() else 0
    cgo = 1 if ui.sj_etc_checBox_03.isChecked() else 0
    pe = 1 if ui.sj_etc_checBox_04.isChecked() else 0
    ce = 1 if ui.sj_etc_checBox_05.isChecked() else 0
    slv = 1 if ui.sj_etc_checBox_06.isChecked() else 0
    pex = 1 if ui.sj_etc_checBox_07.isChecked() else 0

    if proc_query.is_alive():
        query = f"UPDATE etc SET 테마 = '{the}', 인트로숨김 = {inr}, 저해상도 = {ldp}, 창위치기억 = {cgo}, " \
                f"휴무프로세스종료 = {pe}, 휴무컴퓨터종료 = {ce}, 스톰라이브 = {slv}, 프로그램종료 = {pex}"
        queryQ.put(('설정디비', query))
    QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))

    ui.dict_set['테마'] = the
    ui.dict_set['저해상도'] = ldp
    ui.dict_set['인트로숨김'] = ldp
    ui.dict_set['창위치기억'] = cgo
    ui.dict_set['휴무프로세스종료'] = pe
    ui.dict_set['휴무컴퓨터종료'] = ce
    ui.dict_set['스톰라이브'] = slv
    ui.dict_set['프로그램종료'] = pex
    ui.UpdateDictSet()


def sj_button_cicked_17(ui):
    if ui.sj_etc_pButton_01.text() == '계정 텍스트 보기':
        ui.pa_lineEditttt_01.clear()
        if not ui.dialog_pass.isVisible():
            ui.dialog_pass.show()
    else:
        ui.sj_sacc_liEdit_01.setEchoMode(QLineEdit.Password)
        ui.sj_sacc_liEdit_02.setEchoMode(QLineEdit.Password)
        ui.sj_sacc_liEdit_03.setEchoMode(QLineEdit.Password)
        ui.sj_sacc_liEdit_04.setEchoMode(QLineEdit.Password)
        ui.sj_sacc_liEdit_05.setEchoMode(QLineEdit.Password)
        ui.sj_sacc_liEdit_06.setEchoMode(QLineEdit.Password)
        ui.sj_sacc_liEdit_07.setEchoMode(QLineEdit.Password)
        ui.sj_sacc_liEdit_08.setEchoMode(QLineEdit.Password)
        ui.sj_cacc_liEdit_01.setEchoMode(QLineEdit.Password)
        ui.sj_cacc_liEdit_02.setEchoMode(QLineEdit.Password)
        ui.sj_tele_liEdit_01.setEchoMode(QLineEdit.Password)
        ui.sj_tele_liEdit_02.setEchoMode(QLineEdit.Password)
        ui.sj_etc_pButton_01.setText('계정 텍스트 보기')
        ui.sj_etc_pButton_01.setStyleSheet(style_bc_bt)


def sj_button_cicked_19(ui):
    con = sqlite3.connect(DB_SETTING)
    df = pd.read_sql('SELECT * FROM stockbuyorder', con).set_index('index')
    con.close()

    if len(df) > 0:
        ui.sj_sodb_checkBox_01.setChecked(True) if df['주식매수주문구분'][0] == '시장가' else ui.sj_sodb_checkBox_01.setChecked(
            False)
        ui.sj_sodb_checkBox_02.setChecked(True) if df['주식매수주문구분'][0] == '지정가' else ui.sj_sodb_checkBox_02.setChecked(
            False)
        ui.sj_sodb_checkBox_03.setChecked(True) if df['주식매수주문구분'][0] == '최유리지정가' else ui.sj_sodb_checkBox_03.setChecked(
            False)
        ui.sj_sodb_checkBox_04.setChecked(True) if df['주식매수주문구분'][0] == '최우선지정가' else ui.sj_sodb_checkBox_04.setChecked(
            False)
        ui.sj_sodb_checkBox_05.setChecked(True) if df['주식매수주문구분'][0] == '지정가IOC' else ui.sj_sodb_checkBox_05.setChecked(
            False)
        ui.sj_sodb_checkBox_06.setChecked(True) if df['주식매수주문구분'][0] == '시장가IOC' else ui.sj_sodb_checkBox_06.setChecked(
            False)
        ui.sj_sodb_checkBox_07.setChecked(True) if df['주식매수주문구분'][0] == '최유리IOC' else ui.sj_sodb_checkBox_07.setChecked(
            False)
        ui.sj_sodb_checkBox_08.setChecked(True) if df['주식매수주문구분'][0] == '지정가FOK' else ui.sj_sodb_checkBox_08.setChecked(
            False)
        ui.sj_sodb_checkBox_09.setChecked(True) if df['주식매수주문구분'][0] == '시장가FOK' else ui.sj_sodb_checkBox_09.setChecked(
            False)
        ui.sj_sodb_checkBox_10.setChecked(True) if df['주식매수주문구분'][0] == '최유리FOK' else ui.sj_sodb_checkBox_10.setChecked(
            False)
        ui.sj_sodb_lineEdit_01.setText(str(df['주식매수분할횟수'][0]))
        ui.sj_sodb_checkBox_11.setChecked(True) if df['주식매수분할방법'][0] == 1 else ui.sj_sodb_checkBox_11.setChecked(
            False)
        ui.sj_sodb_checkBox_12.setChecked(True) if df['주식매수분할방법'][0] == 2 else ui.sj_sodb_checkBox_12.setChecked(
            False)
        ui.sj_sodb_checkBox_13.setChecked(True) if df['주식매수분할방법'][0] == 3 else ui.sj_sodb_checkBox_13.setChecked(
            False)
        ui.sj_sodb_checkBox_14.setChecked(True) if df['주식매수분할시그널'][0] else ui.sj_sodb_checkBox_14.setChecked(False)
        ui.sj_sodb_checkBox_15.setChecked(True) if df['주식매수분할하방'][0] else ui.sj_sodb_checkBox_15.setChecked(False)
        ui.sj_sodb_checkBox_16.setChecked(True) if df['주식매수분할상방'][0] else ui.sj_sodb_checkBox_16.setChecked(False)
        ui.sj_sodb_lineEdit_02.setText(str(df['주식매수분할하방수익률'][0]))
        ui.sj_sodb_lineEdit_03.setText(str(df['주식매수분할상방수익률'][0]))
        ui.sj_sodb_checkBox_27.setChecked(True) if df['주식매수분할고정수익률'][0] else ui.sj_sodb_checkBox_27.setChecked(
            False)
        ui.sj_sodb_comboBox_01.setCurrentText(str(df['주식매수지정가기준가격'][0]))
        ui.sj_sodb_comboBox_02.setCurrentText(str(df['주식매수지정가호가번호'][0]))
        ui.sj_sodb_comboBox_03.setCurrentText(str(df['주식매수시장가잔량범위'][0]))
        ui.sj_sodb_checkBox_17.setChecked(True) if df['주식매수취소관심이탈'][0] else ui.sj_sodb_checkBox_17.setChecked(False)
        ui.sj_sodb_checkBox_18.setChecked(True) if df['주식매수취소매도시그널'][0] else ui.sj_sodb_checkBox_18.setChecked(
            False)
        ui.sj_sodb_checkBox_19.setChecked(True) if df['주식매수취소시간'][0] else ui.sj_sodb_checkBox_19.setChecked(False)
        ui.sj_sodb_lineEdit_04.setText(str(df['주식매수취소시간초'][0]))
        ui.sj_sodb_checkBox_20.setChecked(True) if df['주식매수금지블랙리스트'][0] else ui.sj_sodb_checkBox_20.setChecked(
            False)
        ui.sj_sodb_checkBox_21.setChecked(True) if df['주식매수금지라운드피겨'][0] else ui.sj_sodb_checkBox_21.setChecked(
            False)
        ui.sj_sodb_lineEdit_05.setText(str(df['주식매수금지라운드호가'][0]))
        ui.sj_sodb_checkBox_22.setChecked(True) if df['주식매수금지손절횟수'][0] else ui.sj_sodb_checkBox_22.setChecked(False)
        ui.sj_sodb_lineEdit_06.setText(str(df['주식매수금지손절횟수값'][0]))
        ui.sj_sodb_checkBox_23.setChecked(True) if df['주식매수금지거래횟수'][0] else ui.sj_sodb_checkBox_23.setChecked(False)
        ui.sj_sodb_lineEdit_07.setText(str(df['주식매수금지거래횟수값'][0]))
        ui.sj_sodb_checkBox_24.setChecked(True) if df['주식매수금지시간'][0] else ui.sj_sodb_checkBox_24.setChecked(False)
        ui.sj_sodb_lineEdit_08.setText(str(df['주식매수금지시작시간'][0]))
        ui.sj_sodb_lineEdit_09.setText(str(df['주식매수금지종료시간'][0]))
        ui.sj_sodb_checkBox_25.setChecked(True) if df['주식매수금지간격'][0] else ui.sj_sodb_checkBox_25.setChecked(False)
        ui.sj_sodb_lineEdit_10.setText(str(df['주식매수금지간격초'][0]))
        ui.sj_sodb_checkBox_26.setChecked(True) if df['주식매수금지손절간격'][0] else ui.sj_sodb_checkBox_26.setChecked(False)
        ui.sj_sodb_lineEdit_11.setText(str(df['주식매수금지손절간격초'][0]))
        ui.sj_sodb_lineEdit_12.setText(str(df['주식매수정정횟수'][0]))
        ui.sj_sodb_comboBox_04.setCurrentText(str(df['주식매수정정호가차이'][0]))
        ui.sj_sodb_comboBox_05.setCurrentText(str(df['주식매수정정호가'][0]))
    else:
        QMessageBox.critical(ui, '오류 알림', '주문관리 주식매수 설정값이\n존재하지 않습니다.\n')


def sj_button_cicked_20(ui):
    con = sqlite3.connect(DB_SETTING)
    df = pd.read_sql('SELECT * FROM stocksellorder', con).set_index('index')
    con.close()

    if len(df) > 0:
        ui.sj_sods_checkBox_01.setChecked(True) if df['주식매도주문구분'][0] == '시장가' else ui.sj_sods_checkBox_01.setChecked(
            False)
        ui.sj_sods_checkBox_02.setChecked(True) if df['주식매도주문구분'][0] == '지정가' else ui.sj_sods_checkBox_02.setChecked(
            False)
        ui.sj_sods_checkBox_03.setChecked(True) if df['주식매도주문구분'][0] == '최유리지정가' else ui.sj_sods_checkBox_03.setChecked(
            False)
        ui.sj_sods_checkBox_04.setChecked(True) if df['주식매도주문구분'][0] == '최우선지정가' else ui.sj_sods_checkBox_04.setChecked(
            False)
        ui.sj_sods_checkBox_05.setChecked(True) if df['주식매도주문구분'][0] == '지정가IOC' else ui.sj_sods_checkBox_05.setChecked(
            False)
        ui.sj_sods_checkBox_06.setChecked(True) if df['주식매도주문구분'][0] == '시장가IOC' else ui.sj_sods_checkBox_06.setChecked(
            False)
        ui.sj_sods_checkBox_07.setChecked(True) if df['주식매도주문구분'][0] == '최유리IOC' else ui.sj_sods_checkBox_07.setChecked(
            False)
        ui.sj_sods_checkBox_08.setChecked(True) if df['주식매도주문구분'][0] == '지정가FOK' else ui.sj_sods_checkBox_08.setChecked(
            False)
        ui.sj_sods_checkBox_09.setChecked(True) if df['주식매도주문구분'][0] == '시장가FOK' else ui.sj_sods_checkBox_09.setChecked(
            False)
        ui.sj_sods_checkBox_10.setChecked(True) if df['주식매도주문구분'][0] == '최유리FOK' else ui.sj_sods_checkBox_10.setChecked(
            False)
        ui.sj_sods_lineEdit_01.setText(str(df['주식매도분할횟수'][0]))
        ui.sj_sods_checkBox_11.setChecked(True) if df['주식매도분할방법'][0] == 1 else ui.sj_sods_checkBox_11.setChecked(
            False)
        ui.sj_sods_checkBox_12.setChecked(True) if df['주식매도분할방법'][0] == 2 else ui.sj_sods_checkBox_12.setChecked(
            False)
        ui.sj_sods_checkBox_13.setChecked(True) if df['주식매도분할방법'][0] == 3 else ui.sj_sods_checkBox_13.setChecked(
            False)
        ui.sj_sods_checkBox_14.setChecked(True) if df['주식매도분할시그널'][0] else ui.sj_sods_checkBox_14.setChecked(False)
        ui.sj_sods_checkBox_15.setChecked(True) if df['주식매도분할하방'][0] else ui.sj_sods_checkBox_15.setChecked(False)
        ui.sj_sods_checkBox_16.setChecked(True) if df['주식매도분할상방'][0] else ui.sj_sods_checkBox_16.setChecked(False)
        ui.sj_sods_lineEdit_02.setText(str(df['주식매도분할하방수익률'][0]))
        ui.sj_sods_lineEdit_03.setText(str(df['주식매도분할상방수익률'][0]))
        ui.sj_sods_comboBox_01.setCurrentText(str(df['주식매도지정가기준가격'][0]))
        ui.sj_sods_comboBox_02.setCurrentText(str(df['주식매도지정가호가번호'][0]))
        ui.sj_sods_comboBox_03.setCurrentText(str(df['주식매도시장가잔량범위'][0]))
        ui.sj_sods_checkBox_17.setChecked(True) if df['주식매도취소관심진입'][0] else ui.sj_sods_checkBox_17.setChecked(False)
        ui.sj_sods_checkBox_18.setChecked(True) if df['주식매도취소매수시그널'][0] else ui.sj_sods_checkBox_18.setChecked(
            False)
        ui.sj_sods_checkBox_19.setChecked(True) if df['주식매도취소시간'][0] else ui.sj_sods_checkBox_19.setChecked(False)
        ui.sj_sods_lineEdit_04.setText(str(df['주식매도취소시간초'][0]))
        ui.sj_sods_checkBox_20.setChecked(True) if df['주식매도손절수익률청산'][0] else ui.sj_sods_checkBox_20.setChecked(
            False)
        ui.sj_sods_lineEdit_05.setText(str(df['주식매도손절수익률'][0]))
        ui.sj_sods_checkBox_21.setChecked(True) if df['주식매도손절수익금청산'][0] else ui.sj_sods_checkBox_21.setChecked(
            False)
        ui.sj_sods_lineEdit_06.setText(str(df['주식매도손절수익금'][0]))
        ui.sj_sods_checkBox_22.setChecked(True) if df['주식매도금지매수횟수'][0] else ui.sj_sods_checkBox_22.setChecked(False)
        ui.sj_sods_lineEdit_07.setText(str(df['주식매도금지매수횟수값'][0]))
        ui.sj_sods_checkBox_23.setChecked(True) if df['주식매도금지라운드피겨'][0] else ui.sj_sods_checkBox_23.setChecked(
            False)
        ui.sj_sods_lineEdit_08.setText(str(df['주식매도금지라운드호가'][0]))
        ui.sj_sods_checkBox_24.setChecked(True) if df['주식매도금지시간'][0] else ui.sj_sods_checkBox_24.setChecked(False)
        ui.sj_sods_lineEdit_09.setText(str(df['주식매도금지시작시간'][0]))
        ui.sj_sods_lineEdit_10.setText(str(df['주식매도금지종료시간'][0]))
        ui.sj_sods_checkBox_25.setChecked(True) if df['주식매도금지간격'][0] else ui.sj_sods_checkBox_25.setChecked(False)
        ui.sj_sods_lineEdit_11.setText(str(df['주식매도금지간격초'][0]))
        ui.sj_sods_lineEdit_12.setText(str(df['주식매도정정횟수'][0]))
        ui.sj_sods_comboBox_04.setCurrentText(str(df['주식매도정정호가차이'][0]))
        ui.sj_sods_comboBox_05.setCurrentText(str(df['주식매도정정호가'][0]))
    else:
        QMessageBox.critical(ui, '오류 알림', '주문관리 주식매도 설정값이\n존재하지 않습니다.\n')


def sj_button_cicked_21(ui):
    con = sqlite3.connect(DB_SETTING)
    df = pd.read_sql('SELECT * FROM coinbuyorder', con).set_index('index')
    con.close()

    if len(df) > 0:
        ui.sj_codb_checkBox_01.setChecked(True) if df['코인매수주문구분'][0] == '시장가' else ui.sj_codb_checkBox_01.setChecked(
            False)
        ui.sj_codb_checkBox_02.setChecked(True) if df['코인매수주문구분'][0] == '지정가' else ui.sj_codb_checkBox_02.setChecked(
            False)
        ui.sj_codb_checkBox_19.setChecked(True) if df['코인매수주문구분'][0] == '지정가IOC' else ui.sj_codb_checkBox_19.setChecked(
            False)
        ui.sj_codb_checkBox_20.setChecked(True) if df['코인매수주문구분'][0] == '지정가FOK' else ui.sj_codb_checkBox_20.setChecked(
            False)
        ui.sj_codb_lineEdit_01.setText(str(df['코인매수분할횟수'][0]))
        ui.sj_codb_checkBox_03.setChecked(True) if df['코인매수분할방법'][0] == 1 else ui.sj_codb_checkBox_03.setChecked(
            False)
        ui.sj_codb_checkBox_04.setChecked(True) if df['코인매수분할방법'][0] == 2 else ui.sj_codb_checkBox_04.setChecked(
            False)
        ui.sj_codb_checkBox_05.setChecked(True) if df['코인매수분할방법'][0] == 3 else ui.sj_codb_checkBox_05.setChecked(
            False)
        ui.sj_codb_checkBox_06.setChecked(True) if df['코인매수분할시그널'][0] else ui.sj_codb_checkBox_06.setChecked(False)
        ui.sj_codb_checkBox_07.setChecked(True) if df['코인매수분할하방'][0] else ui.sj_codb_checkBox_07.setChecked(False)
        ui.sj_codb_checkBox_08.setChecked(True) if df['코인매수분할상방'][0] else ui.sj_codb_checkBox_08.setChecked(False)
        ui.sj_codb_lineEdit_02.setText(str(df['코인매수분할하방수익률'][0]))
        ui.sj_codb_lineEdit_03.setText(str(df['코인매수분할상방수익률'][0]))
        ui.sj_codb_checkBox_27.setChecked(True) if df['코인매수분할고정수익률'][0] else ui.sj_codb_checkBox_27.setChecked(
            False)
        ui.sj_codb_comboBox_01.setCurrentText(str(df['코인매수지정가기준가격'][0]))
        ui.sj_codb_comboBox_02.setCurrentText(str(df['코인매수지정가호가번호'][0]))
        ui.sj_codb_comboBox_03.setCurrentText(str(df['코인매수시장가잔량범위'][0]))
        ui.sj_codb_checkBox_09.setChecked(True) if df['코인매수취소관심이탈'][0] else ui.sj_codb_checkBox_09.setChecked(False)
        ui.sj_codb_checkBox_10.setChecked(True) if df['코인매수취소매도시그널'][0] else ui.sj_codb_checkBox_10.setChecked(
            False)
        ui.sj_codb_checkBox_11.setChecked(True) if df['코인매수취소시간'][0] else ui.sj_codb_checkBox_11.setChecked(False)
        ui.sj_codb_lineEdit_04.setText(str(df['코인매수취소시간초'][0]))
        ui.sj_codb_checkBox_12.setChecked(True) if df['코인매수금지블랙리스트'][0] else ui.sj_codb_checkBox_12.setChecked(
            False)
        ui.sj_codb_checkBox_13.setChecked(True) if df['코인매수금지200원이하'][0] else ui.sj_codb_checkBox_13.setChecked(
            False)
        ui.sj_codb_checkBox_14.setChecked(True) if df['코인매수금지손절횟수'][0] else ui.sj_codb_checkBox_14.setChecked(False)
        ui.sj_codb_lineEdit_05.setText(str(df['코인매수금지손절횟수값'][0]))
        ui.sj_codb_checkBox_15.setChecked(True) if df['코인매수금지거래횟수'][0] else ui.sj_codb_checkBox_15.setChecked(False)
        ui.sj_codb_lineEdit_06.setText(str(df['코인매수금지거래횟수값'][0]))
        ui.sj_codb_checkBox_16.setChecked(True) if df['코인매수금지시간'][0] else ui.sj_codb_checkBox_16.setChecked(False)
        ui.sj_codb_lineEdit_07.setText(str(df['코인매수금지시작시간'][0]))
        ui.sj_codb_lineEdit_08.setText(str(df['코인매수금지종료시간'][0]))
        ui.sj_codb_checkBox_17.setChecked(True) if df['코인매수금지간격'][0] else ui.sj_codb_checkBox_17.setChecked(False)
        ui.sj_codb_lineEdit_09.setText(str(df['코인매수금지간격초'][0]))
        ui.sj_codb_checkBox_18.setChecked(True) if df['코인매수금지손절간격'][0] else ui.sj_codb_checkBox_18.setChecked(False)
        ui.sj_codb_lineEdit_10.setText(str(df['코인매수금지손절간격초'][0]))
        ui.sj_codb_lineEdit_11.setText(str(df['코인매수정정횟수'][0]))
        ui.sj_codb_comboBox_04.setCurrentText(str(df['코인매수정정호가차이'][0]))
        ui.sj_codb_comboBox_05.setCurrentText(str(df['코인매수정정호가'][0]))
    else:
        QMessageBox.critical(ui, '오류 알림', '주문관리 코인매수 설정값이\n존재하지 않습니다.\n')


def sj_button_cicked_22(ui):
    con = sqlite3.connect(DB_SETTING)
    df = pd.read_sql('SELECT * FROM coinsellorder', con).set_index('index')
    con.close()

    if len(df) > 0:
        ui.sj_cods_checkBox_01.setChecked(True) if df['코인매도주문구분'][0] == '시장가' else ui.sj_cods_checkBox_01.setChecked(
            False)
        ui.sj_cods_checkBox_02.setChecked(True) if df['코인매도주문구분'][0] == '지정가' else ui.sj_cods_checkBox_02.setChecked(
            False)
        ui.sj_cods_checkBox_19.setChecked(True) if df['코인매도주문구분'][0] == '지정가IOC' else ui.sj_cods_checkBox_19.setChecked(
            False)
        ui.sj_cods_checkBox_20.setChecked(True) if df['코인매도주문구분'][0] == '지정가FOK' else ui.sj_cods_checkBox_20.setChecked(
            False)
        ui.sj_cods_lineEdit_01.setText(str(df['코인매도분할횟수'][0]))
        ui.sj_cods_checkBox_03.setChecked(True) if df['코인매도분할방법'][0] == 1 else ui.sj_cods_checkBox_03.setChecked(
            False)
        ui.sj_cods_checkBox_04.setChecked(True) if df['코인매도분할방법'][0] == 2 else ui.sj_cods_checkBox_04.setChecked(
            False)
        ui.sj_cods_checkBox_05.setChecked(True) if df['코인매도분할방법'][0] == 3 else ui.sj_cods_checkBox_05.setChecked(
            False)
        ui.sj_cods_checkBox_06.setChecked(True) if df['코인매도분할시그널'][0] else ui.sj_cods_checkBox_06.setChecked(False)
        ui.sj_cods_checkBox_07.setChecked(True) if df['코인매도분할하방'][0] else ui.sj_cods_checkBox_07.setChecked(False)
        ui.sj_cods_checkBox_08.setChecked(True) if df['코인매도분할상방'][0] else ui.sj_cods_checkBox_08.setChecked(False)
        ui.sj_cods_lineEdit_02.setText(str(df['코인매도분할하방수익률'][0]))
        ui.sj_cods_lineEdit_03.setText(str(df['코인매도분할상방수익률'][0]))
        ui.sj_cods_comboBox_01.setCurrentText(str(df['코인매도지정가기준가격'][0]))
        ui.sj_cods_comboBox_02.setCurrentText(str(df['코인매도지정가호가번호'][0]))
        ui.sj_cods_comboBox_03.setCurrentText(str(df['코인매도시장가잔량범위'][0]))
        ui.sj_cods_checkBox_09.setChecked(True) if df['코인매도취소관심진입'][0] else ui.sj_cods_checkBox_09.setChecked(False)
        ui.sj_cods_checkBox_10.setChecked(True) if df['코인매도취소매수시그널'][0] else ui.sj_cods_checkBox_10.setChecked(
            False)
        ui.sj_cods_checkBox_11.setChecked(True) if df['코인매도취소시간'][0] else ui.sj_cods_checkBox_11.setChecked(False)
        ui.sj_cods_lineEdit_04.setText(str(df['코인매도취소시간초'][0]))
        ui.sj_cods_checkBox_12.setChecked(True) if df['코인매도손절수익률청산'][0] else ui.sj_cods_checkBox_12.setChecked(
            False)
        ui.sj_cods_lineEdit_05.setText(str(df['코인매도손절수익률'][0]))
        ui.sj_cods_checkBox_13.setChecked(True) if df['코인매도손절수익금청산'][0] else ui.sj_cods_checkBox_13.setChecked(
            False)
        ui.sj_cods_lineEdit_06.setText(str(df['코인매도손절수익금'][0]))
        ui.sj_cods_checkBox_14.setChecked(True) if df['코인매도금지매수횟수'][0] else ui.sj_cods_checkBox_14.setChecked(False)
        ui.sj_cods_lineEdit_07.setText(str(df['코인매도금지매수횟수값'][0]))
        ui.sj_cods_checkBox_15.setChecked(True) if df['코인매도금지시간'][0] else ui.sj_cods_checkBox_15.setChecked(False)
        ui.sj_cods_lineEdit_08.setText(str(df['코인매도금지시작시간'][0]))
        ui.sj_cods_lineEdit_09.setText(str(df['코인매도금지종료시간'][0]))
        ui.sj_cods_checkBox_16.setChecked(True) if df['코인매도금지간격'][0] else ui.sj_cods_checkBox_16.setChecked(False)
        ui.sj_cods_lineEdit_10.setText(str(df['코인매도금지간격초'][0]))
        ui.sj_cods_lineEdit_11.setText(str(df['코인매도정정횟수'][0]))
        ui.sj_cods_comboBox_04.setCurrentText(str(df['코인매도정정호가차이'][0]))
        ui.sj_cods_comboBox_05.setCurrentText(str(df['코인매도정정호가'][0]))
    else:
        QMessageBox.critical(ui, '오류 알림', '주문관리 코인매도 설정값이\n존재하지 않습니다.\n')


def sj_button_cicked_23(ui, proc_query, queryQ):
    od = ''
    if ui.sj_sodb_checkBox_01.isChecked(): od = '시장가'
    if ui.sj_sodb_checkBox_02.isChecked(): od = '지정가'
    if ui.sj_sodb_checkBox_03.isChecked(): od = '최유리지정가'
    if ui.sj_sodb_checkBox_04.isChecked(): od = '최우선지정가'
    if ui.sj_sodb_checkBox_05.isChecked(): od = '지정가IOC'
    if ui.sj_sodb_checkBox_06.isChecked(): od = '시장가IOC'
    if ui.sj_sodb_checkBox_07.isChecked(): od = '최유리IOC'
    if ui.sj_sodb_checkBox_08.isChecked(): od = '지정가FOK'
    if ui.sj_sodb_checkBox_09.isChecked(): od = '시장가FOK'
    if ui.sj_sodb_checkBox_10.isChecked(): od = '최유리FOK'
    dc = ui.sj_sodb_lineEdit_01.text()
    ds = 0
    if ui.sj_sodb_checkBox_11.isChecked(): ds = 1
    if ui.sj_sodb_checkBox_12.isChecked(): ds = 2
    if ui.sj_sodb_checkBox_13.isChecked(): ds = 3
    ds1 = 1 if ui.sj_sodb_checkBox_14.isChecked() else 0
    ds2 = 1 if ui.sj_sodb_checkBox_15.isChecked() else 0
    ds3 = 1 if ui.sj_sodb_checkBox_16.isChecked() else 0
    ds2c = ui.sj_sodb_lineEdit_02.text()
    ds3c = ui.sj_sodb_lineEdit_03.text()
    bp = ui.sj_sodb_comboBox_01.currentText()
    ju = ui.sj_sodb_comboBox_02.currentText()
    su = ui.sj_sodb_comboBox_03.currentText()
    bf = 1 if ui.sj_sodb_checkBox_27.isChecked() else 0
    bc1 = 1 if ui.sj_sodb_checkBox_17.isChecked() else 0
    bc2 = 1 if ui.sj_sodb_checkBox_18.isChecked() else 0
    bc3 = 1 if ui.sj_sodb_checkBox_19.isChecked() else 0
    bc3c = ui.sj_sodb_lineEdit_04.text()
    bb1 = 1 if ui.sj_sodb_checkBox_20.isChecked() else 0
    bb2 = 1 if ui.sj_sodb_checkBox_21.isChecked() else 0
    bb2c = ui.sj_sodb_lineEdit_05.text()
    bb3 = 1 if ui.sj_sodb_checkBox_22.isChecked() else 0
    bb3c = ui.sj_sodb_lineEdit_06.text()
    bb4 = 1 if ui.sj_sodb_checkBox_23.isChecked() else 0
    bb4c = ui.sj_sodb_lineEdit_07.text()
    bb5 = 1 if ui.sj_sodb_checkBox_24.isChecked() else 0
    bb5s = ui.sj_sodb_lineEdit_08.text()
    bb5e = ui.sj_sodb_lineEdit_09.text()
    bb6 = 1 if ui.sj_sodb_checkBox_25.isChecked() else 0
    bb6s = ui.sj_sodb_lineEdit_10.text()
    bb7 = 1 if ui.sj_sodb_checkBox_26.isChecked() else 0
    bb7s = ui.sj_sodb_lineEdit_11.text()
    bb8 = ui.sj_sodb_lineEdit_12.text()
    bb8c = ui.sj_sodb_comboBox_04.currentText()
    bb8h = ui.sj_sodb_comboBox_05.currentText()

    if '' in (od, dc, ds2c, ds3c, ju, su, bc3c, bb2c, bb3c, bb4c, bb5s, bb5e, bb6s, bb8):
        QMessageBox.critical(ui, '오류 알림', '일부 설정값이 입력되지 않았습니다.\n')
    elif ds == 0:
        QMessageBox.critical(ui, '오류 알림', '분할매수방법이 선택되지 않았습니다.\n')
    elif 1 not in (ds1, ds2, ds3):
        QMessageBox.critical(ui, '오류 알림', '추가매수방법이 선택되지 않았습니다.\n')
    else:
        dc, ds2c, ds3c, ju, su, bc3c, bb2c, bb3c, bb4c, bb5s, bb5e, bb6s, bb7s, bb8, bb8c, bb8h = \
            int(dc), float(ds2c), float(ds3c), int(ju), int(su), int(bc3c), int(bb2c), int(bb3c), int(bb4c), \
            int(bb5s), int(bb5e), int(bb6s), int(bb7s), int(bb8), int(bb8c), int(bb8h)
        if dc < 0 or ds2c < 0 or ds3c < 0 or su < 0 or bc3c < 0 or bb2c < 0 or bb3c < 0 or bb4c < 0 or \
                bb5s < 0 or bb5e < 0 or bb6s < 0 or bb7s < 0 or bb8 < 0 or bb8c < 0 or bb8h < 0:
            QMessageBox.critical(ui, '오류 알림', '지정가 호가 외 모든 입력값은 양수여야합니다.\n')
            return
        if dc > 5:
            QMessageBox.critical(ui, '오류 알림', '매수분할횟수는 5을 초과할 수 없습니다.\n')
            return
        if proc_query.is_alive():
            query = f"UPDATE stockbuyorder SET 주식매수주문구분 = '{od}', 주식매수분할횟수 = {dc}, 주식매수분할방법 = {ds}, 주식매수분할시그널 = {ds1}, " \
                    f"주식매수분할하방 = {ds2}, 주식매수분할상방 = {ds3}, 주식매수분할하방수익률 = {ds2c}, 주식매수분할상방수익률 = {ds3c}, " \
                    f"주식매수분할고정수익률 = {bf}, 주식매수지정가기준가격 = '{bp}', 주식매수지정가호가번호 = {ju}, 주식매수시장가잔량범위 = {su}, " \
                    f"주식매수취소관심이탈 = {bc1}, 주식매수취소매도시그널 = {bc2}, 주식매수취소시간 = {bc3}, 주식매수취소시간초 = {bc3c}, " \
                    f"주식매수금지블랙리스트 = {bb1}, 주식매수금지라운드피겨 = {bb2}, 주식매수금지라운드호가 = {bb2c}, 주식매수금지손절횟수 = {bb3}, " \
                    f"주식매수금지손절횟수값 = {bb3c}, 주식매수금지거래횟수 = {bb4}, 주식매수금지거래횟수값 = {bb4c}, 주식매수금지시간 = {bb5}, " \
                    f"주식매수금지시작시간 = {bb5s}, 주식매수금지종료시간 = {bb5e}, 주식매수금지간격 = {bb6}, 주식매수금지간격초 = {bb6s}, " \
                    f"주식매수금지손절간격 = {bb7}, 주식매수금지손절간격초 = {bb7s}, 주식매수정정횟수 = {bb8}, 주식매수정정호가차이 = {bb8c}, " \
                    f"주식매수정정호가 = {bb8h}"
            queryQ.put(('설정디비', query))
        QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))

        ui.dict_set['주식매수주문구분'] = od
        ui.dict_set['주식매수분할횟수'] = dc
        ui.dict_set['주식매수분할방법'] = ds
        ui.dict_set['주식매수분할시그널'] = ds1
        ui.dict_set['주식매수분할하방'] = ds2
        ui.dict_set['주식매수분할상방'] = ds3
        ui.dict_set['주식매수분할하방수익률'] = ds2c
        ui.dict_set['주식매수분할상방수익률'] = ds3c
        ui.dict_set['주식매수분할고정수익률'] = bf
        ui.dict_set['주식매수지정가기준가격'] = bp
        ui.dict_set['주식매수지정가호가번호'] = ju
        ui.dict_set['주식매수시장가잔량범위'] = su
        ui.dict_set['주식매수취소관심이탈'] = bc1
        ui.dict_set['주식매수취소매도시그널'] = bc2
        ui.dict_set['주식매수취소시간'] = bc3
        ui.dict_set['주식매수취소시간초'] = bc3c
        ui.dict_set['주식매수금지블랙리스트'] = bb1
        ui.dict_set['주식매수금지라운드피겨'] = bb2
        ui.dict_set['주식매수금지라운드호가'] = bb2c
        ui.dict_set['주식매수금지손절횟수'] = bb3
        ui.dict_set['주식매수금지손절횟수값'] = bb3c
        ui.dict_set['주식매수금지거래횟수'] = bb4
        ui.dict_set['주식매수금지거래횟수값'] = bb4c
        ui.dict_set['주식매수금지시간'] = bb5
        ui.dict_set['주식매수금지시작시간'] = bb5s
        ui.dict_set['주식매수금지종료시간'] = bb5e
        ui.dict_set['주식매수금지간격'] = bb6
        ui.dict_set['주식매수금지간격초'] = bb6s
        ui.dict_set['주식매수금지손절간격'] = bb7
        ui.dict_set['주식매수금지손절간격초'] = bb7s
        ui.dict_set['주식매수정정횟수'] = bb8
        ui.dict_set['주식매수정정호가차이'] = bb8c
        ui.dict_set['주식매수정정호가'] = bb8h
        ui.UpdateDictSet()


def sj_button_cicked_24(ui, proc_query, queryQ):
    od = ''
    if ui.sj_sods_checkBox_01.isChecked(): od = '시장가'
    if ui.sj_sods_checkBox_02.isChecked(): od = '지정가'
    if ui.sj_sods_checkBox_03.isChecked(): od = '최유리지정가'
    if ui.sj_sods_checkBox_04.isChecked(): od = '최우선지정가'
    if ui.sj_sods_checkBox_05.isChecked(): od = '지정가IOC'
    if ui.sj_sods_checkBox_06.isChecked(): od = '시장가IOC'
    if ui.sj_sods_checkBox_07.isChecked(): od = '최유리IOC'
    if ui.sj_sods_checkBox_08.isChecked(): od = '지정가FOK'
    if ui.sj_sods_checkBox_09.isChecked(): od = '시장가FOK'
    if ui.sj_sods_checkBox_10.isChecked(): od = '최유리FOK'
    dc = ui.sj_sods_lineEdit_01.text()
    ds = 0
    if ui.sj_sods_checkBox_11.isChecked(): ds = 1
    if ui.sj_sods_checkBox_12.isChecked(): ds = 2
    if ui.sj_sods_checkBox_13.isChecked(): ds = 3
    ds1 = 1 if ui.sj_sods_checkBox_14.isChecked() else 0
    ds2 = 1 if ui.sj_sods_checkBox_15.isChecked() else 0
    ds3 = 1 if ui.sj_sods_checkBox_16.isChecked() else 0
    ds2c = ui.sj_sods_lineEdit_02.text()
    ds3c = ui.sj_sods_lineEdit_03.text()
    bp = ui.sj_sods_comboBox_01.currentText()
    ju = ui.sj_sods_comboBox_02.currentText()
    su = ui.sj_sods_comboBox_03.currentText()
    bc1 = 1 if ui.sj_sods_checkBox_17.isChecked() else 0
    bc2 = 1 if ui.sj_sods_checkBox_18.isChecked() else 0
    bc3 = 1 if ui.sj_sods_checkBox_19.isChecked() else 0
    bc3c = ui.sj_sods_lineEdit_04.text()
    bb0 = 1 if ui.sj_sods_checkBox_20.isChecked() else 0
    bb0c = ui.sj_sods_lineEdit_05.text()
    bb6 = 1 if ui.sj_sods_checkBox_21.isChecked() else 0
    bb6c = ui.sj_sods_lineEdit_06.text()
    bb1 = 1 if ui.sj_sods_checkBox_22.isChecked() else 0
    bb1c = ui.sj_sods_lineEdit_07.text()
    bb2 = 1 if ui.sj_sods_checkBox_23.isChecked() else 0
    bb2c = ui.sj_sods_lineEdit_08.text()
    bb3 = 1 if ui.sj_sods_checkBox_24.isChecked() else 0
    bb3s = ui.sj_sods_lineEdit_09.text()
    bb3e = ui.sj_sods_lineEdit_10.text()
    bb4 = 1 if ui.sj_sods_checkBox_25.isChecked() else 0
    bb4s = ui.sj_sods_lineEdit_11.text()
    bb5 = ui.sj_sods_lineEdit_12.text()
    bb5c = ui.sj_sods_comboBox_04.currentText()
    bb5h = ui.sj_sods_comboBox_05.currentText()

    if '' in (od, dc, ds2c, ds3c, ju, su, bc3c, bb0c, bb1c, bb2c, bb3s, bb3e, bb4s, bb5, bb6c):
        QMessageBox.critical(ui, '오류 알림', '일부 설정값이 입력되지 않았습니다.\n')
    elif ds == 0:
        QMessageBox.critical(ui, '오류 알림', '분할매도방법이 선택되지 않았습니다.\n')
    elif 1 not in (ds1, ds2, ds3):
        QMessageBox.critical(ui, '오류 알림', '추가매도방법이 선택되지 않았습니다.\n')
    else:
        dc, ds2c, ds3c, ju, su, bc3c, bb0c, bb1c, bb2c, bb3s, bb3e, bb4s, bb5, bb5c, bb5h, bb6c = \
            int(dc), float(ds2c), float(ds3c), int(ju), int(su), int(bc3c), float(bb0c), int(bb1c), int(bb2c), \
            int(bb3s), int(bb3e), int(bb4s), int(bb5), int(bb5c), int(bb5h), int(bb6c)
        if dc < 0 or ds2c < 0 or ds3c < 0 or bc3c < 0 or bb0c < 0 or bb1c < 0 or bb2c < 0 or bb3s < 0 or \
                bb3e < 0 or bb4s < 0 or bb5 < 0 or bb5c < 0 or bb5h < 0 or bb6c < 0:
            QMessageBox.critical(ui, '오류 알림', '모든 값은 양수로 입력하십시오.\n')
            return
        if dc > 5:
            QMessageBox.critical(ui, '오류 알림', '매도분할횟수는 5을 초과할 수 없습니다.\n')
            return
        if bb1c > 4:
            QMessageBox.critical(ui, '오류 알림', '매도금지 매수횟수는 5미만으로 입력하십시오.\n')
            return
        if proc_query.is_alive():
            query = f"UPDATE stocksellorder SET 주식매도주문구분 = '{od}', 주식매도분할횟수 = {dc}, 주식매도분할방법 = {ds}, " \
                    f"주식매도분할시그널 = {ds1}, 주식매도분할하방 = {ds2}, 주식매도분할상방 = {ds3}, 주식매도분할하방수익률 = {ds2c}, " \
                    f"주식매도분할상방수익률 = {ds3c}, 주식매도지정가기준가격 = '{bp}', 주식매도지정가호가번호 = {ju}, 주식매도시장가잔량범위 = {su}, " \
                    f"주식매도취소관심진입 = {bc1}, 주식매도취소매수시그널 = {bc2}, 주식매도취소시간 = {bc3}, 주식매도취소시간초 = {bc3c}, " \
                    f"주식매도손절수익률청산 = {bb0}, 주식매도손절수익률 = {bb0c}, 주식매도손절수익금청산 = {bb6}, 주식매도손절수익금 = {bb6c}, " \
                    f"주식매도금지매수횟수 = {bb1}, 주식매도금지매수횟수값 = {bb1c}, 주식매도금지라운드피겨 = {bb2}, 주식매도금지라운드호가 = {bb2c}, " \
                    f"주식매도금지시간 = {bb3}, 주식매도금지시작시간 = {bb3s}, 주식매도금지종료시간 = {bb3e}, 주식매도금지간격 = {bb4}, " \
                    f"주식매도금지간격초 = {bb4s}, 주식매도정정횟수 = {bb5}, 주식매도정정호가차이 = {bb5c}, 주식매도정정호가 = {bb5h}"
            queryQ.put(('설정디비', query))
        QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))

        ui.dict_set['주식매도주문구분'] = od
        ui.dict_set['주식매도분할횟수'] = dc
        ui.dict_set['주식매도분할방법'] = ds
        ui.dict_set['주식매도분할시그널'] = ds1
        ui.dict_set['주식매도분할하방'] = ds2
        ui.dict_set['주식매도분할상방'] = ds3
        ui.dict_set['주식매도분할하방수익률'] = ds2c
        ui.dict_set['주식매도분할상방수익률'] = ds3c
        ui.dict_set['주식매도지정가기준가격'] = bp
        ui.dict_set['주식매도지정가호가번호'] = ju
        ui.dict_set['주식매도시장가잔량범위'] = su
        ui.dict_set['주식매도취소관심진입'] = bc1
        ui.dict_set['주식매도취소매수시그널'] = bc2
        ui.dict_set['주식매도취소시간'] = bc3
        ui.dict_set['주식매도취소시간초'] = bc3c
        ui.dict_set['주식매도손절수익률청산'] = bb0
        ui.dict_set['주식매도손절수익률'] = bb0c
        ui.dict_set['주식매도손절수익금청산'] = bb6
        ui.dict_set['주식매도손절수익금'] = bb6c
        ui.dict_set['주식매도금지매수횟수'] = bb1
        ui.dict_set['주식매도금지매수횟수값'] = bb1c
        ui.dict_set['주식매도금지라운드피겨'] = bb2
        ui.dict_set['주식매도금지라운드호가'] = bb2c
        ui.dict_set['주식매도금지시간'] = bb3
        ui.dict_set['주식매도금지시작시간'] = bb3s
        ui.dict_set['주식매도금지종료시간'] = bb3e
        ui.dict_set['주식매도금지간격'] = bb4
        ui.dict_set['주식매도금지간격초'] = bb4s
        ui.dict_set['주식매도정정횟수'] = bb5
        ui.dict_set['주식매도정정호가차이'] = bb5c
        ui.dict_set['주식매도정정호가'] = bb5h
        ui.UpdateDictSet()


def sj_button_cicked_25(ui, proc_query, queryQ):
    od = ''
    if ui.sj_codb_checkBox_01.isChecked(): od = '시장가'
    if ui.sj_codb_checkBox_02.isChecked(): od = '지정가'
    if ui.sj_codb_checkBox_19.isChecked(): od = '지정가IOC'
    if ui.sj_codb_checkBox_20.isChecked(): od = '지정가FOK'
    dc = ui.sj_codb_lineEdit_01.text()
    ds = 0
    if ui.sj_codb_checkBox_03.isChecked(): ds = 1
    if ui.sj_codb_checkBox_04.isChecked(): ds = 2
    if ui.sj_codb_checkBox_05.isChecked(): ds = 3
    ds1 = 1 if ui.sj_codb_checkBox_06.isChecked() else 0
    ds2 = 1 if ui.sj_codb_checkBox_07.isChecked() else 0
    ds3 = 1 if ui.sj_codb_checkBox_08.isChecked() else 0
    ds2c = ui.sj_codb_lineEdit_02.text()
    ds3c = ui.sj_codb_lineEdit_03.text()
    bp = ui.sj_codb_comboBox_01.currentText()
    ju = ui.sj_codb_comboBox_02.currentText()
    su = ui.sj_codb_comboBox_03.currentText()
    bf = 1 if ui.sj_codb_checkBox_27.isChecked() else 0
    bc1 = 1 if ui.sj_codb_checkBox_09.isChecked() else 0
    bc2 = 1 if ui.sj_codb_checkBox_10.isChecked() else 0
    bc3 = 1 if ui.sj_codb_checkBox_11.isChecked() else 0
    bc3c = ui.sj_codb_lineEdit_04.text()
    bb1 = 1 if ui.sj_codb_checkBox_12.isChecked() else 0
    bb2 = 1 if ui.sj_codb_checkBox_13.isChecked() else 0
    bb3 = 1 if ui.sj_codb_checkBox_14.isChecked() else 0
    bb3c = ui.sj_codb_lineEdit_05.text()
    bb4 = 1 if ui.sj_codb_checkBox_15.isChecked() else 0
    bb4c = ui.sj_codb_lineEdit_06.text()
    bb5 = 1 if ui.sj_codb_checkBox_16.isChecked() else 0
    bb5s = ui.sj_codb_lineEdit_07.text()
    bb5e = ui.sj_codb_lineEdit_08.text()
    bb6 = 1 if ui.sj_codb_checkBox_17.isChecked() else 0
    bb6s = ui.sj_codb_lineEdit_09.text()
    bb7 = 1 if ui.sj_codb_checkBox_18.isChecked() else 0
    bb7s = ui.sj_codb_lineEdit_10.text()
    bb8 = ui.sj_codb_lineEdit_11.text()
    bb8c = ui.sj_codb_comboBox_04.currentText()
    bb8h = ui.sj_codb_comboBox_05.currentText()

    if '' in (od, dc, ds2c, ds3c, ju, su, bc3c, bb3c, bb4c, bb5s, bb5e, bb6s, bb7s, bb8):
        QMessageBox.critical(ui, '오류 알림', '일부 설정값이 입력되지 않았습니다.\n')
    elif ds == 0:
        QMessageBox.critical(ui, '오류 알림', '분할매수방법이 선택되지 않았습니다.\n')
    elif 1 not in (ds1, ds2, ds3):
        QMessageBox.critical(ui, '오류 알림', '추가매수방법이 선택되지 않았습니다.\n')
    else:
        dc, ds2c, ds3c, ju, su, bc3c, bb3c, bb4c, bb5s, bb5e, bb6s, bb7s, bb8, bb8c, bb8h = \
            int(dc), float(ds2c), float(ds3c), int(ju), int(su), int(bc3c), int(bb3c), int(bb4c), int(bb5s), \
            int(bb5e), int(bb6s), int(bb7s), int(bb8), int(bb8c), int(bb8h)
        if dc < 0 or ds2c < 0 or ds3c < 0 or su < 0 or bc3c < 0 or bb3c < 0 or bb4c < 0 or \
                bb5s < 0 or bb5e < 0 or bb6s < 0 or bb7s < 0:
            QMessageBox.critical(ui, '오류 알림', '지정가 호가 외 모든 입력값은 양수여야합니다.\n')
            return
        if dc > 5:
            QMessageBox.critical(ui, '오류 알림', '매수분할횟수는 5를 초과할 수 없습니다.\n')
            return
        if proc_query.is_alive():
            query = f"UPDATE coinbuyorder SET 코인매수주문구분 = '{od}', 코인매수분할횟수 = {dc}, 코인매수분할방법 = {ds}, 코인매수분할시그널 = {ds1}, " \
                    f"코인매수분할하방 = {ds2}, 코인매수분할상방 = {ds3}, 코인매수분할하방수익률 = {ds2c}, 코인매수분할상방수익률 = {ds3c}, " \
                    f"코인매수분할고정수익률 = {bf}, 코인매수지정가기준가격 = '{bp}', 코인매수지정가호가번호 = {ju}, 코인매수시장가잔량범위 = {su}, " \
                    f"코인매수취소관심이탈 = {bc1}, 코인매수취소매도시그널 = {bc2}, 코인매수취소시간 = {bc3}, 코인매수취소시간초 = {bc3c}, " \
                    f"코인매수금지블랙리스트 = {bb1}, 코인매수금지200원이하 = {bb2}, 코인매수금지손절횟수 = {bb3}, 코인매수금지손절횟수값 = {bb3c}, " \
                    f"코인매수금지거래횟수 = {bb4}, 코인매수금지거래횟수값 = {bb4c}, 코인매수금지시간 = {bb5}, 코인매수금지시작시간 = {bb5s}, " \
                    f"코인매수금지종료시간 = {bb5e}, 코인매수금지간격 = {bb6}, 코인매수금지간격초 = {bb6s}, 코인매수금지손절간격 = {bb7}, " \
                    f"코인매수금지손절간격초 = {bb7s}, 코인매수정정횟수 = {bb8}, 코인매수정정호가차이 = {bb8c}, 코인매수정정호가 = {bb8h}"
            queryQ.put(('설정디비', query))
        QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))

        ui.dict_set['코인매수주문구분'] = od
        ui.dict_set['코인매수분할횟수'] = dc
        ui.dict_set['코인매수분할방법'] = ds
        ui.dict_set['코인매수분할시그널'] = ds1
        ui.dict_set['코인매수분할하방'] = ds2
        ui.dict_set['코인매수분할상방'] = ds3
        ui.dict_set['코인매수분할하방수익률'] = ds2c
        ui.dict_set['코인매수분할상방수익률'] = ds3c
        ui.dict_set['코인매수분할고정수익률'] = bf
        ui.dict_set['코인매수지정가기준가격'] = bp
        ui.dict_set['코인매수지정가호가번호'] = ju
        ui.dict_set['코인매수시장가잔량범위'] = su
        ui.dict_set['코인매수취소관심이탈'] = bc1
        ui.dict_set['코인매수취소매도시그널'] = bc2
        ui.dict_set['코인매수취소시간'] = bc3
        ui.dict_set['코인매수취소시간초'] = bc3c
        ui.dict_set['코인매수금지블랙리스트'] = bb1
        ui.dict_set['코인매수금지200원이하'] = bb2
        ui.dict_set['코인매수금지손절횟수'] = bb3
        ui.dict_set['코인매수금지손절횟수값'] = bb3c
        ui.dict_set['코인매수금지거래횟수'] = bb4
        ui.dict_set['코인매수금지거래횟수값'] = bb4c
        ui.dict_set['코인매수금지시간'] = bb5
        ui.dict_set['코인매수금지시작시간'] = bb5s
        ui.dict_set['코인매수금지종료시간'] = bb5e
        ui.dict_set['코인매수금지간격'] = bb6
        ui.dict_set['코인매수금지간격초'] = bb6s
        ui.dict_set['코인매수금지손절간격'] = bb7
        ui.dict_set['코인매수금지손절간격초'] = bb7s
        ui.dict_set['코인매수정정횟수'] = bb8
        ui.dict_set['코인매수정정호가차이'] = bb8c
        ui.dict_set['코인매수정정호가'] = bb8h
        ui.UpdateDictSet()


def sj_button_cicked_26(ui, proc_query, queryQ):
    od = ''
    if ui.sj_cods_checkBox_01.isChecked(): od = '시장가'
    if ui.sj_cods_checkBox_02.isChecked(): od = '지정가'
    if ui.sj_cods_checkBox_19.isChecked(): od = '시장가IOC'
    if ui.sj_cods_checkBox_20.isChecked(): od = '지정가FOK'
    dc = ui.sj_cods_lineEdit_01.text()
    ds = 0
    if ui.sj_cods_checkBox_03.isChecked(): ds = 1
    if ui.sj_cods_checkBox_04.isChecked(): ds = 2
    if ui.sj_cods_checkBox_05.isChecked(): ds = 3
    ds1 = 1 if ui.sj_cods_checkBox_06.isChecked() else 0
    ds2 = 1 if ui.sj_cods_checkBox_07.isChecked() else 0
    ds3 = 1 if ui.sj_cods_checkBox_08.isChecked() else 0
    ds2c = ui.sj_cods_lineEdit_02.text()
    ds3c = ui.sj_cods_lineEdit_03.text()
    bp = ui.sj_cods_comboBox_01.currentText()
    ju = ui.sj_cods_comboBox_02.currentText()
    su = ui.sj_cods_comboBox_03.currentText()
    bc1 = 1 if ui.sj_cods_checkBox_09.isChecked() else 0
    bc2 = 1 if ui.sj_cods_checkBox_10.isChecked() else 0
    bc3 = 1 if ui.sj_cods_checkBox_11.isChecked() else 0
    bc3c = ui.sj_cods_lineEdit_04.text()
    bb0 = 1 if ui.sj_cods_checkBox_12.isChecked() else 0
    bb0c = ui.sj_cods_lineEdit_05.text()
    bb6 = 1 if ui.sj_cods_checkBox_13.isChecked() else 0
    bb6c = ui.sj_cods_lineEdit_06.text()
    bb1 = 1 if ui.sj_cods_checkBox_14.isChecked() else 0
    bb1c = ui.sj_cods_lineEdit_07.text()
    bb3 = 1 if ui.sj_cods_checkBox_15.isChecked() else 0
    bb3s = ui.sj_cods_lineEdit_08.text()
    bb3e = ui.sj_cods_lineEdit_09.text()
    bb4 = 1 if ui.sj_cods_checkBox_16.isChecked() else 0
    bb4s = ui.sj_cods_lineEdit_10.text()
    bb5 = ui.sj_cods_lineEdit_11.text()
    bb5c = ui.sj_cods_comboBox_04.currentText()
    bb5h = ui.sj_cods_comboBox_05.currentText()

    if '' in (od, dc, ds2c, ds3c, ju, su, bc3c, bb3s, bb3e, bb4s, bb5):
        QMessageBox.critical(ui, '오류 알림', '일부 설정값이 입력되지 않았습니다.\n')
    elif ds == 0:
        QMessageBox.critical(ui, '오류 알림', '분할매도방법이 선택되지 않았습니다.\n')
    elif 1 not in (ds1, ds2, ds3):
        QMessageBox.critical(ui, '오류 알림', '추가매도방법이 선택되지 않았습니다.\n')
    else:
        dc, ds2c, ds3c, ju, su, bc3c, bb0c, bb1c, bb3s, bb3e, bb4s, bb5, bb5c, bb5h, bb6c = \
            int(dc), float(ds2c), float(ds3c), int(ju), int(su), int(bc3c), float(bb0c), int(bb1c), int(bb3s), \
            int(bb3e), int(bb4s), int(bb5), float(bb5c), int(bb5h), int(bb6c)
        if dc < 0 or ds2c < 0 or ds3c < 0 or bc3c < 0 or bb0c < 0 or bb1c < 0 or bb3s < 0 or bb3e < 0 or \
                bb4s < 0 or bb5 < 0 or bb5c < 0 or bb5h < 0 or bb6c < 0:
            QMessageBox.critical(ui, '오류 알림', '모든 값은 양수로 입력하십시오.\n')
            return
        if dc > 5:
            QMessageBox.critical(ui, '오류 알림', '매도분할횟수는 5을 초과할 수 없습니다.\n')
            return
        if bb1c > 4:
            QMessageBox.critical(ui, '오류 알림', '매도금지 매수횟수는 5미만으로 입력하십시오.\n')
            return
        if proc_query.is_alive():
            query = f"UPDATE coinsellorder SET 코인매도주문구분 = '{od}', 코인매도분할횟수 = {dc}, 코인매도분할방법 = {ds}, " \
                    f"코인매도분할시그널 = {ds1}, 코인매도분할하방 = {ds2}, 코인매도분할상방 = {ds3}, 코인매도분할하방수익률 = {ds2c}, " \
                    f"코인매도분할상방수익률 = {ds3c}, 코인매도지정가기준가격 = '{bp}', 코인매도지정가호가번호 = {ju}, 코인매도시장가잔량범위 = {su}, " \
                    f"코인매도취소관심진입 = {bc1}, 코인매도취소매수시그널 = {bc2}, 코인매도취소시간 = {bc3}, 코인매도취소시간초 = {bc3c}, " \
                    f"코인매도손절수익률청산 = {bb0}, 코인매도손절수익률 = {bb0c}, 코인매도손절수익금청산 = {bb6}, 코인매도손절수익금 = {bb6c}, " \
                    f"코인매도금지매수횟수 = {bb1}, 코인매도금지매수횟수값 = {bb1c}, 코인매도금지시간 = {bb3}, 코인매도금지시작시간 = {bb3s}, " \
                    f"코인매도금지종료시간 = {bb3e}, 코인매도금지간격 = {bb4}, 코인매도금지간격초 = {bb4s}, 코인매도정정횟수 = {bb5}, " \
                    f"코인매도정정호가차이 = {bb5c}, 코인매도정정호가 = {bb5h}"
            queryQ.put(('설정디비', query))
        QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))

        ui.dict_set['코인매도주문구분'] = od
        ui.dict_set['코인매도분할횟수'] = dc
        ui.dict_set['코인매도분할방법'] = ds
        ui.dict_set['코인매도분할시그널'] = ds1
        ui.dict_set['코인매도분할하방'] = ds2
        ui.dict_set['코인매도분할상방'] = ds3
        ui.dict_set['코인매도분할하방수익률'] = ds2c
        ui.dict_set['코인매도분할상방수익률'] = ds3c
        ui.dict_set['코인매도지정가기준가격'] = bp
        ui.dict_set['코인매도지정가호가번호'] = ju
        ui.dict_set['코인매도시장가잔량범위'] = su
        ui.dict_set['코인매도취소관심진입'] = bc1
        ui.dict_set['코인매도취소매수시그널'] = bc2
        ui.dict_set['코인매도취소시간'] = bc3
        ui.dict_set['코인매도취소시간초'] = bc3c
        ui.dict_set['코인매도손절수익률청산'] = bb0
        ui.dict_set['코인매도손절수익률'] = bb0c
        ui.dict_set['코인매도손절수익금청산'] = bb6
        ui.dict_set['코인매도손절수익금'] = bb6c
        ui.dict_set['코인매도금지매수횟수'] = bb1
        ui.dict_set['코인매도금지매수횟수값'] = bb1c
        ui.dict_set['코인매도금지시간'] = bb3
        ui.dict_set['코인매도금지시작시간'] = bb3s
        ui.dict_set['코인매도금지종료시간'] = bb3e
        ui.dict_set['코인매도금지간격'] = bb4
        ui.dict_set['코인매도금지간격초'] = bb4s
        ui.dict_set['코인매도정정횟수'] = bb5
        ui.dict_set['코인매도정정호가차이'] = bb5c
        ui.dict_set['코인매도정정호가'] = bb5h


def sj_button_cicked_27(ui):
    LoadSettings(ui)


def sj_button_cicked_28(ui, proc_query, queryQ):
    name = ui.sj_set_comBoxx_01.currentText()
    if name == '':
        QMessageBox.critical(ui, '오류 알림', '설정이름이 선택되지 않았습니다.\n')
        return
    origin_file = f'{DB_PATH}/setting_{name}.db'
    copy_file = f'{DB_PATH}/setting.db'
    file_list = os.listdir(DB_PATH)
    if f'setting_{name}.db' not in file_list:
        QMessageBox.critical(ui, '오류 알림', '설정파일이 존재하지 않았습니다.\n')
        return
    if proc_query.is_alive():
        queryQ.put(('설정변경', origin_file, copy_file))
        qtest_qwait(2)
        ui.sjButtonClicked_01()
        ui.sjButtonClicked_02()
        ui.sjButtonClicked_03()
        ui.sjButtonClicked_04()
        ui.sjButtonClicked_05()
        ui.sjButtonClicked_06()
        ui.sjButtonClicked_07()
        ui.sjButtonClicked_08()
        ui.sjButtonClicked_19()
        ui.sjButtonClicked_20()
        ui.sjButtonClicked_21()
        ui.sjButtonClicked_22()
        ui.sjButtonClicked_09()
        ui.sjButtonClicked_10()
        ui.sjButtonClicked_11()
        ui.sjButtonClicked_12()
        ui.sjButtonClicked_13()
        ui.sjButtonClicked_14()
        ui.sjButtonClicked_15()
        ui.sjButtonClicked_16()
        ui.sjButtonClicked_23()
        ui.sjButtonClicked_24()
        ui.sjButtonClicked_25()
        ui.sjButtonClicked_26()
        QMessageBox.information(ui, '모든 설정 적용 완료', random.choice(famous_saying))


def sj_button_cicked_29(ui):
    name = ui.sj_set_comBoxx_01.currentText()
    if name == '':
        QMessageBox.critical(ui, '오류 알림', '설정이름이 선택되지 않았습니다.\n')
        return
    remove_file = f'{DB_PATH}/setting_{name}.db'
    os.remove(remove_file)
    LoadSettings(ui)
    QMessageBox.information(ui, '삭제 완료', random.choice(famous_saying))


def sj_button_cicked_30(ui):
    name = ui.sj_set_liEditt_01.text()
    if name == '':
        QMessageBox.critical(ui, '오류 알림', '설정이름이 입력되지 않았습니다.\n')
        return
    origin_file = f'{DB_PATH}/setting.db'
    copy_file = f'{DB_PATH}/setting_{name}.db'
    shutil.copy(origin_file, copy_file)
    LoadSettings(ui)
    QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))


def LoadSettings(ui):
    ui.sj_set_comBoxx_01.clear()
    file_list = os.listdir(DB_PATH)
    file_list = [x for x in file_list if 'setting_' in x]
    for file_name in file_list:
        name = file_name.replace('setting_', '').replace('.db', '')
        ui.sj_set_comBoxx_01.addItem(name)
