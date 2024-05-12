import os
import sqlite3
import pandas as pd
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer, QPropertyAnimation, QSize, QEasingCurve
from ui.set_style import style_bc_bt, style_bc_bb
from utility.setting import GRAPH_PATH, DB_BACKTEST
from utility.static import int_hms, qtest_qwait


def mnbutton_c_clicked_01(ui, index):
    if ui.extend_window:
        QMessageBox.critical(ui, '오류 알림', '전략탭 확장 상태에서는 탭을 변경할 수 없습니다.')
        return
    prev_main_btn = ui.main_btn
    if prev_main_btn == index: return
    ui.image_label1.setVisible(False)
    if index == 3:
        if ui.dict_set['거래소'] == '업비트':
            ui.cvjb_labelllll_03.setText('백테스트 기본설정   배팅(백만)                        평균틱수   ui.vars[0]')
            if ui.cvjb_lineEditt_04.text() == '10000':
                ui.cvjb_lineEditt_04.setText('20')
        else:
            ui.cvjb_labelllll_03.setText('백테스트 기본설정배팅(USDT)                        평균틱수   ui.vars[0]')
            if ui.cvjb_lineEditt_04.text() == '20':
                ui.cvjb_lineEditt_04.setText('10000')
    elif index == 5 and ui.lgicon_alert:
        ui.lgicon_alert = False
        ui.main_btn_list[index].setIcon(ui.icon_log)
    elif index == 6:
        if ui.dict_set['거래소'] == '업비트':
            ui.sj_coin_labell_03.setText(
                '장초전략                        백만원,  장중전략                        백만원              전략중지 및 잔고청산  |')
        else:
            ui.sj_coin_labell_03.setText(
                '장초전략                        USDT,   장중전략                        USDT              전략중지 및 잔고청산  |')

    ui.main_btn = index
    ui.main_btn_list[prev_main_btn].setStyleSheet(style_bc_bb)
    ui.main_btn_list[ui.main_btn].setStyleSheet(style_bc_bt)
    ui.main_box_list[prev_main_btn].setVisible(False)
    ui.main_box_list[ui.main_btn].setVisible(True)
    QTimer.singleShot(400, lambda: ui.image_label1.setVisible(
        True if ui.svc_labellllll_05.isVisible() or ui.cvc_labellllll_05.isVisible() else False))
    ui.animation = QPropertyAnimation(ui.main_box_list[ui.main_btn], b'size')
    ui.animation.setEasingCurve(QEasingCurve.InCirc)
    ui.animation.setDuration(300)
    ui.animation.setStartValue(QSize(0, 757))
    ui.animation.setEndValue(QSize(1353, 757))
    ui.animation.start()


def mnbutton_c_clicked_02(ui):
    if ui.main_btn == 0:
        if not ui.s_calendarWidgett.isVisible():
            boolean1 = False
            boolean2 = True
        else:
            boolean1 = True
            boolean2 = False
        for widget in ui.stock_basic_listt:
            widget.setVisible(boolean1)
        for widget in ui.stock_total_listt:
            widget.setVisible(boolean2)
    elif ui.main_btn == 1:
        if not ui.c_calendarWidgett.isVisible():
            boolean1 = False
            boolean2 = True
        else:
            boolean1 = True
            boolean2 = False
        for widget in ui.coin_basic_listtt:
            widget.setVisible(boolean1)
        for widget in ui.coin_total_listtt:
            widget.setVisible(boolean2)
    else:
        QMessageBox.warning(ui, '오류 알림', '해당 버튼은 트레이더탭에서만 작동합니다.\n')


def mnbutton_c_clicked_03(ui, wdzservQ, soundQ, stocklogin=False):
    if stocklogin:
        buttonReply = QMessageBox.Yes
    else:
        if ui.dialog_web.isVisible():
            QMessageBox.critical(ui, '오류 알림', '웹뷰어창이 열린 상태에서는 수동시작할 수 없습니다.\n웹뷰어창을 닫고 재시도하십시오.\n')
            return
        if ui.dict_set['리시버실행시간'] <= int_hms() <= ui.dict_set['트레이더실행시간']:
            QMessageBox.critical(ui, '오류 알림', '리시버 및 트레이더 실행시간 동안은 수동시작할 수 없습니다.\n')
            return
        buttonReply = QMessageBox.question(
            ui, '주식 수동 시작', '주식 리시버 또는 트레이더를 시작합니다.\n이미 실행 중이라면 기존 프로세스는 종료됩니다.\n계속하시겠습니까?\n',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

    if buttonReply == QMessageBox.Yes:
        wdzservQ.put(('manager', '리시버 종료'))
        wdzservQ.put(('manager', '전략연산 종료'))
        wdzservQ.put(('manager', '트레이더 종료'))
        qtest_qwait(3)
        if ui.dict_set['아이디2'] is None:
            QMessageBox.critical(ui, '오류 알림', '두번째 계정이 설정되지 않아\n리시버를 시작할 수 없습니다.\n계정 설정 후 다시 시작하십시오.\n')
        if ui.dict_set['아이디1'] is None:
            QMessageBox.critical(ui, '오류 알림', '첫번째 계정이 설정되지 않아\n트레이더를 시작할 수 없습니다.\n계정 설정 후 다시 시작하십시오.\n')
        if ui.dict_set['주식리시버'] and ui.dict_set['주식트레이더']:
            if ui.dict_set['주식알림소리']:
                soundQ.put('키움증권 OPEN API에 로그인을 시작합니다.')
            wdzservQ.put(('manager', '주식수동시작'))
    ui.ms_pushButton.setStyleSheet(style_bc_bt)


def mnbutton_c_clicked_04(ui):
    if ui.geometry().width() > 1000:
        ui.setFixedSize(722, 383)
        ui.zo_pushButton.setStyleSheet(style_bc_bt)
    else:
        ui.setFixedSize(1403, 763)
        ui.zo_pushButton.setStyleSheet(style_bc_bb)


def mnbutton_c_clicked_05(ui, proc_query, queryQ):
    buttonReply = QMessageBox.warning(
        ui, '백테기록삭제', '백테 그래프 및 기록 DB가 삭제됩니다.\n계속하시겠습니까?\n',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    )
    if buttonReply == QMessageBox.Yes:
        file_list = os.listdir(GRAPH_PATH)
        for file_name in file_list:
            os.remove(f'{GRAPH_PATH}/{file_name}')
        if proc_query.is_alive():
            con = sqlite3.connect(DB_BACKTEST)
            df = pd.read_sql("SELECT name FROM sqlite_master WHERE TYPE = 'table'", con)
            con.close()
            table_list = df['name'].to_list()
            for table_name in table_list:
                queryQ.put(('백테디비', f'DROP TABLE {table_name}'))
            queryQ.put(('백테디비', 'VACUUM'))
        QMessageBox.information(ui, '알림', '백테그래프 및 기록DB가 삭제되었습니다.')


def mnbutton_c_clicked_06(ui, proc_query, queryQ):
    buttonReply = QMessageBox.warning(
        ui, '계정 설정 초기화', '계정 설정 항목이 모두 초기화됩니다.\n계속하시겠습니까?\n',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    )
    if buttonReply == QMessageBox.Yes:
        if proc_query.is_alive():
            queryQ.put(('설정디비', 'DELETE FROM sacc'))
            queryQ.put(('설정디비', 'DELETE FROM cacc'))
            queryQ.put(('설정디비', 'DELETE FROM telegram'))
            columns = [
                "index", "아이디1", "비밀번호1", "인증서비밀번호1", "계좌비밀번호1", "아이디2", "비밀번호2", "인증서비밀번호2", "계좌비밀번호2",
                "아이디3", "비밀번호3", "인증서비밀번호3", "계좌비밀번호3", "아이디4", "비밀번호4", "인증서비밀번호4", "계좌비밀번호4"
            ]
            data = [0, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
            df = pd.DataFrame([data], columns=columns).set_index('index')
            queryQ.put((df, 'sacc', 'append'))
            columns = ["index", "Access_key1", "Secret_key1", "Access_key2", "Secret_key2"]
            data = [0, '', '', '', '']
            df = pd.DataFrame([data], columns=columns).set_index('index')
            queryQ.put((df, 'cacc', 'append'))
            columns = ["index", "str_bot", "int_id"]
            data = [0, '', '']
            df = pd.DataFrame([data], columns=columns).set_index('index')
            queryQ.put((df, 'telegram', 'append'))
            queryQ.put(('설정디비', 'VACUUM'))
        QMessageBox.information(ui, '알림', '계정 설정 항목이 모두 초기화되었습니다.')
