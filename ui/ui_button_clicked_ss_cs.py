import sqlite3
import pandas as pd
from PIL import Image
from PyQt5.QtWidgets import QMessageBox
from ui.set_style import style_bc_dk
from utility.setting import DB_BACKTEST, ui_num, GRAPH_PATH


def ssbutton_clicked_01(ui):
    con = sqlite3.connect(DB_BACKTEST)
    df = pd.read_sql("SELECT name FROM sqlite_master WHERE TYPE = 'table'", con)
    ui.ss_comboBoxxxx_01.clear()
    for table in df['name'].to_list()[::-1]:
        if 'stock' in table and '_bt_' in table:
            ui.ss_comboBoxxxx_01.addItem(table)
    try:
        df = pd.read_sql(f"SELECT * FROM '{ui.ss_comboBoxxxx_01.currentText()}'", con).set_index('index')
    except:
        pass
    else:
        ui.update_tablewidget.update_tablewidget((ui_num['S상세기록'], df))
    con.close()


def ssbutton_clicked_02(ui):
    con = sqlite3.connect(DB_BACKTEST)
    df = pd.read_sql("SELECT name FROM sqlite_master WHERE TYPE = 'table'", con)
    ui.ss_comboBoxxxx_02.clear()
    for table in df['name'].to_list()[::-1]:
        if 'stock' in table and \
                (
                        'o_' in table or 'ov_' in table or 'ovc_' in table or 'b_' in table or 'bv_' in table or 'bvc_' in table):
            ui.ss_comboBoxxxx_02.addItem(table)
    try:
        df = pd.read_sql(f"SELECT * FROM '{ui.ss_comboBoxxxx_02.currentText()}'", con).set_index('index')
    except:
        pass
    else:
        ui.update_tablewidget.update_tablewidget((ui_num['S상세기록'], df))
    con.close()


def ssbutton_clicked_03(ui):
    con = sqlite3.connect(DB_BACKTEST)
    df = pd.read_sql("SELECT name FROM sqlite_master WHERE TYPE = 'table'", con)
    ui.ss_comboBoxxxx_03.clear()
    for table in df['name'].to_list()[::-1]:
        if 'stock' in table and '_bt_' not in table and (
                't_' in table or 'or_' in table or 'orv_' in table or 'orvc_' in table or 'br_' in table or 'brv_' in table or 'brvc_' in table):
            ui.ss_comboBoxxxx_03.addItem(table)
    try:
        df = pd.read_sql(f"SELECT * FROM '{ui.ss_comboBoxxxx_03.currentText()}'", con).set_index('index')
    except:
        pass
    else:
        ui.update_tablewidget.update_tablewidget((ui_num['S상세기록'], df))
    con.close()


def ssbutton_clicked_04(ui):
    comboBox = None
    if ui.focusWidget() == ui.ss_pushButtonn_02:
        comboBox = ui.ss_comboBoxxxx_01
    elif ui.focusWidget() == ui.ss_pushButtonn_04:
        comboBox = ui.ss_comboBoxxxx_02
    elif ui.focusWidget() == ui.ss_pushButtonn_06:
        comboBox = ui.ss_comboBoxxxx_03

    if comboBox is None:
        return

    file_name = comboBox.currentText()

    try:
        image1 = Image.open(f"{GRAPH_PATH}/{file_name}.png")
        image2 = Image.open(f"{GRAPH_PATH}/{file_name}_.png")
        image1.show()
        image2.show()
    except:
        QMessageBox.critical(ui, '오류 알림', '저장된 그래프 파일이 존재하지 않습니다.\n')


def ssbutton_clicked_05(ui):
    if not ui.dialog_comp.isVisible():
        ui.dialog_comp.show()

        con = sqlite3.connect(DB_BACKTEST)
        df = pd.read_sql("SELECT name FROM sqlite_master WHERE TYPE = 'table'", con)
        con.close()

        if len(df) > 0:
            ui.backdetail_list = [x for x in df['name'].to_list()[::-1] if
                                  'stock' in x and ('t_' in x or 'v_' in x or 'c_' in x or 'vc_' in x)]
            if len(ui.backdetail_list) > 0:
                ui.backcheckbox_list = []
                count = len(ui.backdetail_list)
                ui.cp_tableWidget_01.setRowCount(count)
                for i, backdetailname in enumerate(ui.backdetail_list):
                    checkBox = ui.wc.setCheckBox(backdetailname, ui)
                    ui.backcheckbox_list.append(checkBox)
                    ui.cp_tableWidget_01.setCellWidget(i, 0, checkBox)
                if count < 40:
                    ui.cp_tableWidget_01.setRowCount(40)
    else:
        ui.dialog_comp.close()


def ssbutton_clicked_06(ui):
    buttonReply = QMessageBox.question(
        ui, '백테스트 중지', '백테스트를 중지하면 백테엔진을 재시작해야합니다.\n계속하시겠습니까?\n',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    )
    if buttonReply == QMessageBox.Yes:
        ui.BacktestProcessKill(1)
        ui.ss_progressBar_01.setValue(0)
        ui.ss_progressBar_01.setFormat('%p%')
        ui.back_scount = 0
        ui.back_schedul = False
        ui.ssicon_alert = False
        ui.main_btn_list[2].setIcon(ui.icon_stocks)


def csbutton_clicked_01(ui):
    con = sqlite3.connect(DB_BACKTEST)
    df = pd.read_sql("SELECT name FROM sqlite_master WHERE TYPE = 'table'", con)
    ui.cs_comboBoxxxx_01.clear()
    for table in df['name'].to_list()[::-1]:
        if 'coin' in table and '_bt_' in table:
            ui.cs_comboBoxxxx_01.addItem(table)
    try:
        df = pd.read_sql(f"SELECT * FROM '{ui.cs_comboBoxxxx_01.currentText()}'", con).set_index('index')
    except:
        pass
    else:
        ui.update_tablewidget.update_tablewidget((ui_num['C상세기록'], df))
    con.close()


def csbutton_clicked_02(ui):
    con = sqlite3.connect(DB_BACKTEST)
    df = pd.read_sql("SELECT name FROM sqlite_master WHERE TYPE = 'table'", con)
    ui.cs_comboBoxxxx_02.clear()
    for table in df['name'].to_list()[::-1]:
        if 'coin' in table and (
                'o_' in table or 'ov_' in table or 'ovc_' in table or 'b_' in table or 'bv_' in table or 'bvc_' in table):
            ui.cs_comboBoxxxx_02.addItem(table)
    try:
        df = pd.read_sql(f"SELECT * FROM '{ui.cs_comboBoxxxx_02.currentText()}'", con).set_index('index')
    except:
        pass
    else:
        ui.update_tablewidget.update_tablewidget((ui_num['C상세기록'], df))
    con.close()


def csbutton_clicked_03(ui):
    con = sqlite3.connect(DB_BACKTEST)
    df = pd.read_sql("SELECT name FROM sqlite_master WHERE TYPE = 'table'", con)
    ui.cs_comboBoxxxx_03.clear()
    for table in df['name'].to_list()[::-1]:
        if 'coin' in table and '_bt_' not in table and (
                't_' in table or 'or_' in table or 'orv_' in table or 'orvc_' in table or 'br_' in table or 'brv_' in table or 'brvc_' in table):
            ui.cs_comboBoxxxx_03.addItem(table)
    try:
        df = pd.read_sql(f"SELECT * FROM '{ui.cs_comboBoxxxx_03.currentText()}'", con).set_index('index')
    except:
        pass
    else:
        ui.update_tablewidget.update_tablewidget((ui_num['C상세기록'], df))
    con.close()


def csbutton_clicked_04(ui):
    comboBox = None
    if ui.focusWidget() == ui.cs_pushButtonn_02:
        comboBox = ui.cs_comboBoxxxx_01
    elif ui.focusWidget() == ui.cs_pushButtonn_04:
        comboBox = ui.cs_comboBoxxxx_02
    elif ui.focusWidget() == ui.cs_pushButtonn_06:
        comboBox = ui.cs_comboBoxxxx_03

    if comboBox is None:
        return

    file_name = comboBox.currentText()

    try:
        image1 = Image.open(f"{GRAPH_PATH}/{file_name}.png")
        image2 = Image.open(f"{GRAPH_PATH}/{file_name}_.png")
        image1.show()
        image2.show()
    except:
        QMessageBox.critical(ui, '오류 알림', '저장된 그래프 파일이 존재하지 않습니다.\n')


def csbutton_clicked_05(ui):
    if not ui.dialog_comp.isVisible():
        ui.dialog_comp.show()

        con = sqlite3.connect(DB_BACKTEST)
        df = pd.read_sql("SELECT name FROM sqlite_master WHERE TYPE = 'table'", con)
        con.close()

        if len(df) > 0:
            ui.backdetail_list = [x for x in df['name'].to_list()[::-1] if
                                  'coin' in x and ('t_' in x or 'v_' in x or 'c_' in x or 'h_' in x)]

        if len(ui.backdetail_list) > 0:
            ui.backcheckbox_list = []
            count = len(ui.backdetail_list)
            ui.cp_tableWidget_01.setRowCount(count)
            for i, backdetailname in enumerate(ui.backdetail_list):
                checkBox = ui.wc.setCheckBox(backdetailname, ui)
                ui.backcheckbox_list.append(checkBox)
                ui.cp_tableWidget_01.setCellWidget(i, 0, checkBox)
            if count < 40:
                ui.cp_tableWidget_01.setRowCount(40)
    else:
        ui.dialog_comp.close()


def csbutton_clicked_06(ui):
    buttonReply = QMessageBox.question(
        ui, '백테스트 중지', '백테스트를 중지하면 백테엔진을 재시작해야합니다.\n계속하시겠습니까?\n',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    )
    if buttonReply == QMessageBox.Yes:
        ui.BacktestProcessKill(1)
        ui.cs_pushButtonn_08.setStyleSheet(style_bc_dk)
        ui.cs_progressBar_01.setValue(0)
        ui.cs_progressBar_01.setFormat('%p%')
        ui.back_scount = 0
        ui.back_schedul = False
        ui.csicon_alert = False
        ui.main_btn_list[3].setIcon(ui.icon_coins)
