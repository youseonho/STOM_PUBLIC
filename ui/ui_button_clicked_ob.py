from PyQt5.QtWidgets import QMessageBox
from utility.static import comma2float, comma2int, now


def odbutton_clicked_01(ui, ctraderQ, wdzservQ):
    name = ui.od_comboBoxxxxx_01.currentText()
    ordertype = ui.od_comboBoxxxxx_02.currentText()
    op = ui.od_lineEdittttt_01.text()
    oc = ui.od_lineEdittttt_02.text()
    if '' in (op, oc, name):
        QMessageBox.critical(ui.dialog_order, '오류 알림', '종목명, 주문가격, 주문수량을 올바르게 입력하십시오.\n')
        return
    if 'KRW' in name:
        if ui.CoinTraderProcessAlive():
            ctraderQ.put(('매수', name, comma2float(op), comma2float(oc), now(), False, ordertype))
    elif 'USDT' not in name:
        code = ui.dict_code[name]
        wdzservQ.put(('trader', ('매수', code, name, comma2int(op), comma2int(oc), now(), False, ordertype)))


def odbutton_clicked_02(ui, ctraderQ, wdzservQ):
    name = ui.od_comboBoxxxxx_01.currentText()
    ordertype = ui.od_comboBoxxxxx_02.currentText()
    op = ui.od_lineEdittttt_01.text()
    oc = ui.od_lineEdittttt_02.text()
    if '' in (op, oc, name):
        QMessageBox.critical(ui.dialog_order, '오류 알림', '종목명, 주문가격, 주문수량을 올바르게 입력하십시오.\n')
        return
    if 'KRW' in name:
        if ui.CoinTraderProcessAlive():
            ctraderQ.put(('매도', name, comma2float(op), comma2float(oc), now(), False, ordertype))
    elif 'USDT' not in name:
        code = ui.dict_code[name]
        wdzservQ.put(('trader', ('매도', code, name, comma2int(op), comma2int(oc), now(), False, ordertype)))


def odbutton_clicked_03(ui, ctraderQ):
    name = ui.od_comboBoxxxxx_01.currentText()
    ordertype = ui.od_comboBoxxxxx_02.currentText()
    op = ui.od_lineEdittttt_01.text()
    oc = ui.od_lineEdittttt_02.text()
    if '' in (op, oc, name):
        QMessageBox.critical(ui.dialog_order, '오류 알림', '종목명, 주문가격, 주문수량을 올바르게 입력하십시오.\n')
        return
    if 'USDT' in name and ui.CoinTraderProcessAlive():
        ctraderQ.put(('BUY_LONG', name, comma2float(op), comma2float(oc), now(), False, ordertype))


def odbutton_clicked_04(ui, ctraderQ):
    name = ui.od_comboBoxxxxx_01.currentText()
    ordertype = ui.od_comboBoxxxxx_02.currentText()
    op = ui.od_lineEdittttt_01.text()
    oc = ui.od_lineEdittttt_02.text()
    if '' in (op, oc, name):
        QMessageBox.critical(ui.dialog_order, '오류 알림', '종목명, 주문가격, 주문수량을 올바르게 입력하십시오.\n')
        return
    if 'USDT' in name and ui.CoinTraderProcessAlive():
        ctraderQ.put(('SELL_LONG', name, comma2float(op), comma2float(oc), now(), False, ordertype))


def odbutton_clicked_05(ui, ctraderQ):
    name = ui.od_comboBoxxxxx_01.currentText()
    ordertype = ui.od_comboBoxxxxx_02.currentText()
    op = ui.od_lineEdittttt_01.text()
    oc = ui.od_lineEdittttt_02.text()
    if '' in (op, oc, name):
        QMessageBox.critical(ui.dialog_order, '오류 알림', '종목명, 주문가격, 주문수량을 올바르게 입력하십시오.\n')
        return
    if 'USDT' in name and ui.CoinTraderProcessAlive():
        ctraderQ.put(('SELL_SHORT', name, comma2float(op), comma2float(oc), now(), False, ordertype))


def odbutton_clicked_06(ui, ctraderQ):
    name = ui.od_comboBoxxxxx_01.currentText()
    ordertype = ui.od_comboBoxxxxx_02.currentText()
    op = ui.od_lineEdittttt_01.text()
    oc = ui.od_lineEdittttt_02.text()
    if '' in (op, oc, name):
        QMessageBox.critical(ui.dialog_order, '오류 알림', '종목명, 주문가격, 주문수량을 올바르게 입력하십시오.\n')
        return
    if 'USDT' in name and ui.CoinTraderProcessAlive():
        ctraderQ.put(('BUY_SHORT', name, comma2float(op), comma2float(oc), now(), False, ordertype))


def odbutton_clicked_07(ui, ctraderQ, wdzservQ):
    name = ui.od_comboBoxxxxx_01.currentText()
    if name == '':
        QMessageBox.critical(ui.dialog_order, '오류 알림', '종목명을 선택하십시오.\n종목명은 관심종목 테이블의 리스트입니다.\n')
        return
    if 'KRW' in name:
        if ui.CoinTraderProcessAlive():
            ctraderQ.put(('매수취소', name, 0, 0, now(), False))
    elif 'USDT' in name:
        if ui.CoinTraderProcessAlive():
            ctraderQ.put(('BUY_LONG_CANCEL', name, 0, 0, now(), False))
            ctraderQ.put(('SELL_SHORT_CANCEL', name, 0, 0, now(), False))
    else:
        code = ui.dict_code[name]
        wdzservQ.put(('trader', ('매수취소', code, name, 0, 0, now(), False)))


def odbutton_clicked_08(ui, ctraderQ, wdzservQ):
    name = ui.od_comboBoxxxxx_01.currentText()
    if name == '':
        QMessageBox.critical(ui.dialog_order, '오류 알림', '종목명을 선택하십시오.\n종목명은 관심종목 테이블의 리스트입니다.\n')
        return
    if 'KRW' in name:
        if ui.CoinTraderProcessAlive():
            ctraderQ.put(('매도취소', name, 0, 0, now(), False))
    elif 'USDT' in name:
        if ui.CoinTraderProcessAlive():
            ctraderQ.put(('SELL_LONG_CANCEL', name, 0, 0, now(), False))
            ctraderQ.put(('BUY_SHORT_CANCEL', name, 0, 0, now(), False))
    else:
        code = ui.dict_code[name]
        wdzservQ.put(('trader', ('매도취소', code, name, 0, 0, now(), False)))
