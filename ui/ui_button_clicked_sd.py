import os
import random
import sqlite3
import pandas as pd
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLineEdit, QMessageBox
from ui.set_text import famous_saying
from utility.setting import DB_STRATEGY, ui_num
from utility.static import qtest_qwait


def bebutton_clicked_01(ui):
    if ui.main_btn == 2 or (ui.dialog_scheduler.isVisible() and ui.sd_pushButtonnn_01.text() == '주식'):
        if not ui.backtest_engine:
            ui.StartBacktestEngine('주식')
        else:
            buttonReply = QMessageBox.question(
                ui.dialog_backengine, '백테엔진', '이미 백테스트 엔진이 구동중입니다.\n엔진을 재시작하시겠습니까?\n',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if buttonReply == QMessageBox.Yes:
                ui.BacktestEngineKill()
                qtest_qwait(3)
                ui.StartBacktestEngine('주식')
    elif ui.main_btn == 3 or (ui.dialog_scheduler.isVisible() and ui.sd_pushButtonnn_01.text() == '코인'):
        if not ui.backtest_engine:
            ui.StartBacktestEngine('코인')
        else:
            buttonReply = QMessageBox.question(
                ui.dialog_backengine, '백테엔진', '이미 백테스트 엔진이 구동중입니다.\n엔진을 재시작하시겠습니까?\n',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if buttonReply == QMessageBox.Yes:
                ui.BacktestEngineKill()
                qtest_qwait(3)
                ui.StartBacktestEngine('코인')


def backtest_engine_kill(ui, windowQ):
    ui.ClearBacktestQ()
    for p in ui.back_cprocs:
        p.kill()
    for p in ui.back_eprocs:
        p.kill()
    for q in ui.back_eques:
        q.close()
    ui.back_eprocs = []
    ui.back_cprocs = []
    ui.back_eques = []
    ui.back_cques = []
    ui.dict_cn = None
    ui.dict_mt = None
    ui.back_count = 0
    ui.startday = 0
    ui.endday = 0
    ui.starttime = 0
    ui.endtime = 0
    ui.backtest_engine = False
    windowQ.put((ui_num['백테엔진'], '<font color=#45cdf7>모든 백테엔진 프로세스가 종료되었습니다.</font>'))


# noinspection PyUnusedLocal
def back_bench(ui, windowQ, backQ, soundQ, totalQ, liveQ, teleQ):
    pass


def sdbutton_clicked_01(ui):
    if type(ui.dialog_scheduler.focusWidget()) != QLineEdit:
        if ui.sd_pushButtonnn_01.text() == '주식':
            ui.sd_pushButtonnn_01.setText('코인')
        else:
            ui.sd_pushButtonnn_01.setText('주식')


# noinspection PyUnusedLocal
def sdbutton_clicked_02(ui, windowQ, backQ, soundQ, totalQ, liveQ, teleQ):
    pass


def StopScheduler(ui, gubun=False):
    ui.back_scount = 0
    ui.back_schedul = False
    if ui.auto_mode:
        ui.AutoBackSchedule(3)
    if gubun and ui.sd_scheckBoxxxx_02.isChecked():
        QTimer.singleShot(180 * 1000, ui.ProcessKill)
        os.system('shutdown /s /t 300')


def sdbutton_clicked_03(ui):
    if ui.sd_pushButtonnn_01.text() == '주식':
        ui.ssButtonClicked_06()
    else:
        ui.csButtonClicked_06()
    for progressBar in ui.list_progressBarrr:
        progressBar.setValue(0)


def sdbutton_clicked_04(ui):
    con = sqlite3.connect(DB_STRATEGY)
    df = pd.read_sql('SELECT * FROM schedule', con).set_index('index')
    con.close()
    if len(df) > 0:
        if ui.sd_scheckBoxxxx_01.isChecked():
            ui.sd_scheckBoxxxx_01.nextCheckState()
        ui.sd_dcomboBoxxxx_01.clear()
        indexs = list(df.index)
        indexs.sort()
        for i, index in enumerate(indexs):
            ui.sd_dcomboBoxxxx_01.addItem(index)
            if i == 0:
                ui.sd_dlineEditttt_01.setText(index)


def sdbutton_clicked_05(ui, proc_query, queryQ):
    schedule_name = ui.sd_dlineEditttt_01.text()
    if schedule_name == '':
        QMessageBox.critical(ui.dialog_scheduler, '오류 알림', '스케쥴 이름이 공백 상태입니다.\n')
    else:
        schedule = ''
        for i in range(16):
            if ui.list_checkBoxxxxxx[i].isChecked():
                schedule += ui.list_gcomboBoxxxxx[i].currentText() + ';'
                schedule += ui.list_slineEdittttt[i].text() + ';'
                schedule += ui.list_elineEdittttt[i].text() + ';'
                schedule += ui.list_blineEdittttt[i].text() + ';'
                schedule += ui.list_alineEdittttt[i].text() + ';'
                schedule += ui.list_p1comboBoxxxx[i].currentText() + ';'
                schedule += ui.list_p2comboBoxxxx[i].currentText() + ';'
                schedule += ui.list_p3comboBoxxxx[i].currentText() + ';'
                schedule += ui.list_p4comboBoxxxx[i].currentText() + ';'
                schedule += ui.list_tcomboBoxxxxx[i].currentText() + ';'
                schedule += ui.list_bcomboBoxxxxx[i].currentText() + ';'
                schedule += ui.list_scomboBoxxxxx[i].currentText() + ';'
                schedule += ui.list_vcomboBoxxxxx[i].currentText() + '^'
        schedule += '1;' if ui.sd_scheckBoxxxx_02.isChecked() else '0;'
        schedule += ui.sd_oclineEdittt_01.text() + ';'
        schedule += ui.sd_oclineEdittt_02.text() + ';'
        schedule += ui.sd_oclineEdittt_03.text()
        if proc_query.is_alive():
            queryQ.put(('전략디비', f"DELETE FROM schedule WHERE `index` = '{schedule_name}'"))
            df = pd.DataFrame({'스케쥴': [schedule]}, index=[schedule_name])
            queryQ.put(('전략디비', df, 'schedule', 'append'))
        QMessageBox.information(ui.dialog_scheduler, '저장 완료', random.choice(famous_saying))
