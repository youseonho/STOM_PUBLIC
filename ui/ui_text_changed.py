def text_changed_01(ui):
    if ui.dialog_scheduler.focusWidget() not in ui.list_slineEdittttt:
        return
    if ui.sd_scheckBoxxxx_01.isChecked():
        gubun = ui.list_slineEdittttt.index(ui.dialog_scheduler.focusWidget())
        text = ui.list_slineEdittttt[gubun].text()
        for i, widget in enumerate(ui.list_slineEdittttt):
            if i != gubun:
                widget.setText(text)


def text_changed_02(ui):
    if ui.dialog_scheduler.focusWidget() not in ui.list_elineEdittttt:
        return
    if ui.sd_scheckBoxxxx_01.isChecked():
        gubun = ui.list_elineEdittttt.index(ui.dialog_scheduler.focusWidget())
        text = ui.list_elineEdittttt[gubun].text()
        for i, widget in enumerate(ui.list_elineEdittttt):
            if i != gubun:
                widget.setText(text)


def text_changed_03(ui):
    if ui.dialog_scheduler.focusWidget() not in ui.list_blineEdittttt:
        return
    if ui.sd_scheckBoxxxx_01.isChecked():
        gubun = ui.list_blineEdittttt.index(ui.dialog_scheduler.focusWidget())
        text = ui.list_blineEdittttt[gubun].text()
        for i, widget in enumerate(ui.list_blineEdittttt):
            if i != gubun:
                widget.setText(text)


def text_changed_04(ui):
    if ui.dialog_scheduler.focusWidget() not in ui.list_alineEdittttt:
        return
    if ui.sd_scheckBoxxxx_01.isChecked():
        gubun = ui.list_alineEdittttt.index(ui.dialog_scheduler.focusWidget())
        text = ui.list_alineEdittttt[gubun].text()
        for i, widget in enumerate(ui.list_alineEdittttt):
            combo_text = ui.list_gcomboBoxxxxx[i].currentText()
            if i != gubun and '최적화' not in combo_text and '전진분석' not in combo_text:
                widget.setText(text)


def text_changed_05(ui):
    name = ui.od_comboBoxxxxx_01.currentText()
    if name != '':
        if 'KRW' in name:
            order_price = float(ui.od_lineEdittttt_01.text())
            order_count = round(ui.dict_set['코인장초투자금'] * 1_000_000 / order_price, 8)
        elif 'USDT' in name:
            order_price = float(ui.od_lineEdittttt_01.text())
            order_count = round(ui.dict_set['코인장초투자금'] / order_price, 8)
        else:
            order_price = int(ui.od_lineEdittttt_01.text())
            order_count = int(ui.dict_set['주식장초투자금'] * 1_000_000 / order_price)
        ui.od_lineEdittttt_02.setText(str(order_count))
