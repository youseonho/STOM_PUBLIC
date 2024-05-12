from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QLineEdit
from ui.set_style import style_bc_dk


def return_press_01(ui, chartQ):
    if ui.dialog_chart.focusWidget() in (ui.ct_lineEdittttt_04, ui.ct_lineEdittttt_05, ui.ct_pushButtonnn_01):
        searchdate = ui.ct_dateEdittttt_01.date().toString('yyyyMMdd')
        linetext = ui.ct_lineEdittttt_03.text()
        tickcount = int(linetext) if linetext != '' else 30
        if ui.dialog_chart.focusWidget() == ui.ct_lineEdittttt_04:
            name = ui.ct_lineEdittttt_04.text()
        else:
            name = ui.ct_lineEdittttt_05.text()
        if name in ui.dict_code.keys():
            code = ui.dict_code[name]
        else:
            code = name
            name = ui.dict_name[code] if code in ui.dict_name.keys() else code
        ui.ct_lineEdittttt_04.setText(code)
        ui.ct_lineEdittttt_05.setText(name)
        ui.ShowDialog(name, tickcount, searchdate, 4)
    elif ui.dialog_chart.focusWidget() == ui.ct_tableWidgett_01:
        row = ui.ct_tableWidgett_01.currentIndex().row()
        item = ui.ct_tableWidgett_01.item(row, 0)
        if item is None:
            return
        name = item.text()
        coin = True if 'KRW' in name or 'USDT' in name else False
        code = ui.dict_code[name] if name in ui.dict_code.keys() else name
        searchdate = ui.ct_dateEdittttt_02.date().toString('yyyyMMdd')
        linetext = ui.ct_lineEdittttt_03.text()
        tickcount = int(linetext) if linetext != '' else 30
        ui.ct_lineEdittttt_04.setText(code)
        ui.ct_lineEdittttt_05.setText(name)
        ui.ct_dateEdittttt_01.setDate(QDate.fromString(searchdate, 'yyyyMMdd'))
        chartQ.put((coin, code, tickcount, searchdate, ui.ct_lineEdittttt_01.text(), ui.ct_lineEdittttt_02.text(),
                    ui.GetKlist()))


def return_press_02(ui, teleQ):
    if ui.pa_lineEditttt_01.text() == ui.dict_set['계좌비밀번호1'] or \
            (ui.pa_lineEditttt_01.text() == '' and ui.dict_set['계좌비밀번호1'] is None):
        ui.sj_sacc_liEdit_01.setEchoMode(QLineEdit.Normal)
        ui.sj_sacc_liEdit_02.setEchoMode(QLineEdit.Normal)
        ui.sj_sacc_liEdit_03.setEchoMode(QLineEdit.Normal)
        ui.sj_sacc_liEdit_04.setEchoMode(QLineEdit.Normal)
        ui.sj_sacc_liEdit_05.setEchoMode(QLineEdit.Normal)
        ui.sj_sacc_liEdit_06.setEchoMode(QLineEdit.Normal)
        ui.sj_sacc_liEdit_07.setEchoMode(QLineEdit.Normal)
        ui.sj_sacc_liEdit_08.setEchoMode(QLineEdit.Normal)
        ui.sj_cacc_liEdit_01.setEchoMode(QLineEdit.Normal)
        ui.sj_cacc_liEdit_02.setEchoMode(QLineEdit.Normal)
        ui.sj_tele_liEdit_01.setEchoMode(QLineEdit.Normal)
        ui.sj_tele_liEdit_02.setEchoMode(QLineEdit.Normal)
        ui.sj_etc_pButton_01.setText('계정 텍스트 가리기')
        ui.sj_etc_pButton_01.setStyleSheet(style_bc_dk)
        ui.dialog_pass.close()
    else:
        teleQ.put('경고!! 계정 텍스트 보기 비밀번호 입력 오류가 발생하였습니다.')
