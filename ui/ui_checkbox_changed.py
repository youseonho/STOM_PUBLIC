import sqlite3
import pandas as pd
from PyQt5.QtCore import Qt
from utility.setting import DB_SETTING
from PyQt5.QtWidgets import QPushButton, QMessageBox


def checkbox_changed_01(ui, state):
    if type(ui.focusWidget()) != QPushButton:
        if state == Qt.Checked:
            con = sqlite3.connect(DB_SETTING)
            df = pd.read_sql('SELECT * FROM sacc', con).set_index('index')
            con.close()
            if len(df) == 0 or df['아이디2'][0] == '':
                ui.sj_main_cheBox_01.nextCheckState()
                QMessageBox.critical(ui, '오류 알림', '두번째 계정이 설정되지 않아\n리시버를 선택할 수 없습니다.\n계정 설정 후 다시 선택하십시오.\n')
            elif not ui.sj_main_cheBox_02.isChecked():
                ui.sj_main_cheBox_02.nextCheckState()
        else:
            if ui.sj_main_cheBox_02.isChecked():
                ui.sj_main_cheBox_02.nextCheckState()


def checkbox_changed_02(ui, state):
    if type(ui.focusWidget()) != QPushButton:
        if state == Qt.Checked:
            con = sqlite3.connect(DB_SETTING)
            df = pd.read_sql('SELECT * FROM sacc', con).set_index('index')
            con.close()
            if len(df) == 0 or df['아이디1'][0] == '':
                ui.sj_main_cheBox_02.nextCheckState()
                QMessageBox.critical(ui, '오류 알림', '첫번째 계정이 설정되지 않아\n트레이더를 선택할 수 없습니다.\n계정 설정 후 다시 선택하십시오.\n')
            elif not ui.sj_main_cheBox_01.isChecked():
                ui.sj_main_cheBox_01.nextCheckState()
        else:
            if ui.sj_main_cheBox_01.isChecked():
                ui.sj_main_cheBox_01.nextCheckState()


def checkbox_changed_03(ui, state):
    if type(ui.focusWidget()) != QPushButton and state == Qt.Checked:
        if ui.sj_main_cheBox_11.isChecked():
            ui.sj_main_cheBox_03.nextCheckState()
            QMessageBox.critical(ui, '오류 알림', '클라이언트용 스톰은\n틱데이터를 저장할 수 없습니다.\n서버용 스톰으로 저장하십시오.\n')
        else:
            if not ui.sj_main_cheBox_01.isChecked():
                ui.sj_main_cheBox_01.nextCheckState()
            if not ui.sj_main_cheBox_02.isChecked():
                ui.sj_main_cheBox_02.nextCheckState()


def checkbox_changed_04(ui, state):
    if type(ui.focusWidget()) != QPushButton:
        if state == Qt.Checked:
            if not ui.sj_main_cheBox_05.isChecked():
                ui.sj_main_cheBox_05.nextCheckState()
        else:
            if ui.sj_main_cheBox_05.isChecked():
                ui.sj_main_cheBox_05.nextCheckState()


def checkbox_changed_05(ui, state):
    if type(ui.focusWidget()) != QPushButton:
        if state == Qt.Checked:
            if not ui.sj_main_cheBox_04.isChecked():
                ui.sj_main_cheBox_04.nextCheckState()
        else:
            if ui.sj_main_cheBox_04.isChecked():
                ui.sj_main_cheBox_04.nextCheckState()


def checkbox_changed_06(ui, state):
    if type(ui.focusWidget()) != QPushButton and state == Qt.Checked:
        if ui.sj_main_cheBox_11.isChecked():
            ui.sj_main_cheBox_03.nextCheckState()
            QMessageBox.critical(ui, '오류 알림', '클라이언트용 스톰은\n틱데이터를 저장할 수 없습니다.\n서버용 스톰으로 저장하십시오.\n')
        else:
            if not ui.sj_main_cheBox_04.isChecked():
                ui.sj_main_cheBox_04.nextCheckState()
            if not ui.sj_main_cheBox_05.isChecked():
                ui.sj_main_cheBox_05.nextCheckState()


def checkbox_changed_07(ui, state):
    if type(ui.focusWidget()) != QPushButton and state != Qt.Checked:
        buttonReply = QMessageBox.question(
            ui, '경고', '트레이더 실행 중에 모의모드를 해제하면\n바로 실매매로 전환됩니다. 해제하시겠습니까?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if buttonReply != QMessageBox.Yes:
            ui.sj_stock_ckBox_01.nextCheckState()


def checkbox_changed_08(ui, state):
    if type(ui.focusWidget()) != QPushButton and state != Qt.Checked and ui.CoinTraderProcessAlive():
        ui.sj_coin_cheBox_01.nextCheckState()
        QMessageBox.critical(ui, '오류 알림', '트레이더 실행 중에는 모의모드를 해제할 수 없습니다.\n')


def checkbox_changed_09(ui, state):
    if type(ui.focusWidget()) != QPushButton and state == Qt.Checked:
        for widget in ui.sproc_exit_listtt:
            if widget != ui.focusWidget():
                if widget.isChecked():
                    widget.nextCheckState()


def checkbox_changed_10(ui, state):
    if type(ui.focusWidget()) != QPushButton and state == Qt.Checked:
        for widget in ui.cproc_exit_listtt:
            if widget != ui.focusWidget():
                if widget.isChecked():
                    widget.nextCheckState()


def checkbox_changed_11(ui, state):
    if type(ui.focusWidget()) != QPushButton and state == Qt.Checked:
        for widget in ui.com_exit_list:
            if widget != ui.focusWidget():
                if widget.isChecked():
                    widget.nextCheckState()


def checkbox_changed_12(ui, state):
    if type(ui.focusWidget()) != QPushButton and state != Qt.Checked:
        if ui.dialog_factor.focusWidget() == ui.ct_checkBoxxxxx_01:
            ui.ct_checkBoxxxxx_01.nextCheckState()
            QMessageBox.critical(ui.dialog_factor, '오류 알림', '현재가는 해제할 수 없습니다.\n')


def checkbox_changed_13(ui, state):
    if type(ui.focusWidget()) != QPushButton and state == Qt.Checked:
        for widget in ui.sj_ilbunback_listtt:
            if widget != ui.focusWidget() and widget.isChecked():
                widget.nextCheckState()


def checkbox_changed_14(ui, state):
    if type(ui.focusWidget()) != QPushButton and state == Qt.Checked:
        if not ui.sj_back_cheBox_14.isChecked():
            ui.sj_back_cheBox_14.nextCheckState()


def checkbox_changed_15(ui, state):
    if type(ui.focusWidget()) != QPushButton and state != Qt.Checked:
        if ui.sj_back_cheBox_13.isChecked():
            ui.sj_back_cheBox_13.nextCheckState()


def checkbox_changed_16(ui, state):
    if type(ui.focusWidget()) != QPushButton and state != Qt.Checked:
        if ui.sj_back_cheBox_06.isChecked():
            ui.sj_back_cheBox_06.nextCheckState()


def checkbox_changed_17(ui, state):
    gubun = ui.list_checkBoxxxxxx.index(ui.dialog_scheduler.focusWidget())
    if state == Qt.Checked:
        for item in ('백테스트',
                     '그리드 최적화', '그리드 검증 최적화', '그리드 교차검증 최적화',
                     '그리드 최적화 테스트', '그리드 검증 최적화 테스트', '그리드 교차검증 최적화 테스트',
                     '그리드 최적화 전진분석', '그리드 검증 최적화 전진분석', '그리드 교차검증 최적화 전진분석',
                     '베이지안 최적화', '베이지안 검증 최적화', '베이지안 교차검증 최적화',
                     '베이지안 최적화 테스트', '베이지안 검증 최적화 테스트', '베이지안 교차검증 최적화 테스트',
                     '베이지안 최적화 전진분석', '베이지안 검증 최적화 전진분석', '베이지안 교차검증 최적화 전진분석',
                     'GA 최적화', '검증 GA 최적화', '교차검증 GA 최적화',
                     '조건 최적화', '검증 조건 최적화', '교차검증 조건 최적화'):
            ui.list_gcomboBoxxxxx[gubun].addItem(item)
    else:
        ui.list_gcomboBoxxxxx[gubun].clear()
        ui.list_bcomboBoxxxxx[gubun].clear()
        ui.list_scomboBoxxxxx[gubun].clear()
        ui.list_vcomboBoxxxxx[gubun].clear()
        ui.list_p1comboBoxxxx[gubun].clear()
        ui.list_p2comboBoxxxx[gubun].clear()
        ui.list_p3comboBoxxxx[gubun].clear()
        ui.list_p4comboBoxxxx[gubun].clear()
        ui.list_tcomboBoxxxxx[gubun].clear()


def checkbox_changed_18(ui, state):
    if type(ui.focusWidget()) != QPushButton:
        if state == Qt.Checked:
            if ui.sj_back_cheBox_18.isChecked():
                ui.sj_back_cheBox_18.nextCheckState()
        else:
            if not ui.sj_back_cheBox_18.isChecked():
                ui.sj_back_cheBox_18.nextCheckState()


def checkbox_changed_19(ui, state):
    if type(ui.focusWidget()) != QPushButton:
        if state == Qt.Checked:
            if ui.sj_back_cheBox_17.isChecked():
                ui.sj_back_cheBox_17.nextCheckState()
        else:
            if not ui.sj_back_cheBox_17.isChecked():
                ui.sj_back_cheBox_17.nextCheckState()


def checkbox_changed_20(ui, state):
    if type(ui.focusWidget()) != QPushButton and state == Qt.Checked:
        for widget in ui.sj_checkbox_list:
            if widget != ui.focusWidget():
                if widget.isChecked():
                    widget.nextCheckState()


def checkbox_changed_21(ui, state):
    if type(ui.focusWidget()) != QPushButton:
        if state == Qt.Checked:
            if ui.focusWidget() == ui.sj_main_cheBox_10:
                if ui.sj_main_cheBox_11.isChecked():
                    ui.sj_main_cheBox_11.nextCheckState()
            else:
                if ui.sj_main_cheBox_10.isChecked():
                    ui.sj_main_cheBox_10.nextCheckState()
        elif not ui.sj_main_cheBox_11.isChecked() and not ui.sj_main_cheBox_10.isChecked() and not ui.sj_main_cheBox_09.isChecked():
            ui.sj_main_cheBox_09.nextCheckState()


# def checkbox_changed_22(ui, state):
#     if type(ui.focusWidget()) != QPushButton and state != Qt.Checked:
#         if ui.focusWidget() == ui.sj_main_cheBox_09:
#             if not ui.sj_main_cheBox_11.isChecked() and not ui.sj_main_cheBox_10.isChecked():
#                 ui.sj_main_cheBox_09.nextCheckState()

# noinspection PyUnusedLocal
def checkbox_changed_23(ui, state):
    ui.ctpg_tik_name = None


def sbcheckbox_changed_01(ui, state):
    if type(ui.focusWidget()) != QPushButton and state == Qt.Checked:
        for widget in ui.sodb_checkbox_list1:
            if widget != ui.focusWidget():
                if widget.isChecked():
                    widget.nextCheckState()


def sbcheckbox_changed_02(ui, state):
    if type(ui.focusWidget()) != QPushButton and state == Qt.Checked:
        for widget in ui.sodb_checkbox_list2:
            if widget != ui.focusWidget():
                if widget.isChecked():
                    widget.nextCheckState()


def sscheckbox_changed_01(ui, state):
    if type(ui.focusWidget()) != QPushButton and state == Qt.Checked:
        for widget in ui.sods_checkbox_list1:
            if widget != ui.focusWidget():
                if widget.isChecked():
                    widget.nextCheckState()


def sscheckbox_changed_02(ui, state):
    if type(ui.focusWidget()) != QPushButton and state == Qt.Checked:
        for widget in ui.sods_checkbox_list2:
            if widget != ui.focusWidget():
                if widget.isChecked():
                    widget.nextCheckState()


def cbcheckbox_changed_01(ui, state):
    if type(ui.focusWidget()) != QPushButton and state == Qt.Checked:
        for widget in ui.codb_checkbox_list1:
            if widget != ui.focusWidget():
                if widget.isChecked():
                    widget.nextCheckState()
    if ui.dict_set['거래소'] == '업비트':
        if ui.sj_codb_checkBox_19.isChecked() or ui.sj_codb_checkBox_20.isChecked():
            if ui.sj_codb_checkBox_19.isChecked():
                ui.sj_codb_checkBox_19.nextCheckState()
            else:
                ui.sj_codb_checkBox_20.nextCheckState()
            QMessageBox.critical(ui, '오류 알림', '업비트는 해당주문유형을 사용할 수 없습니다.\n')
            ui.sj_codb_checkBox_01.setFocus()
            ui.sj_codb_checkBox_01.setChecked(True)


def cbcheckbox_changed_02(ui, state):
    if type(ui.focusWidget()) != QPushButton and state == Qt.Checked:
        for widget in ui.codb_checkbox_list2:
            if widget != ui.focusWidget():
                if widget.isChecked():
                    widget.nextCheckState()


def cscheckbox_changed_01(ui, state):
    if type(ui.focusWidget()) != QPushButton and state == Qt.Checked:
        for widget in ui.cods_checkbox_list1:
            if widget != ui.focusWidget():
                if widget.isChecked():
                    widget.nextCheckState()
    if ui.dict_set['거래소'] == '업비트':
        if ui.sj_cods_checkBox_19.isChecked() or ui.sj_cods_checkBox_20.isChecked():
            if ui.sj_cods_checkBox_19.isChecked():
                ui.sj_codb_checkBox_19.nextCheckState()
            else:
                ui.sj_cods_checkBox_20.nextCheckState()
            QMessageBox.critical(ui, '오류 알림', '업비트는 해당주문유형을 사용할 수 없습니다.\n')
            ui.sj_cods_checkBox_01.setFocus()
            ui.sj_cods_checkBox_01.setChecked(True)


def cscheckbox_changed_02(ui, state):
    if type(ui.focusWidget()) != QPushButton and state == Qt.Checked:
        for widget in ui.cods_checkbox_list2:
            if widget != ui.focusWidget():
                if widget.isChecked():
                    widget.nextCheckState()
