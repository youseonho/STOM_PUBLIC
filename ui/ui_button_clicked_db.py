from PyQt5.QtWidgets import QMessageBox
from utility.setting import ui_num


def dbbutton_clicked_01(ui, windowQ, queryQ, proc_query):
    if not ui.database_control:
        date = ui.db_lineEdittttt_01.text()
        if date == '':
            windowQ.put((ui_num['DB관리'], '일자를 입력하십시오.'))
            return
        if proc_query.is_alive():
            ui.database_control = True
            windowQ.put((ui_num['DB관리'], '주식 일자DB의 지정일자 데이터를 삭제합니다.'))
            queryQ.put(('주식일자DB지정일자삭제', date))


def dbbutton_clicked_02(ui, windowQ, queryQ, proc_query):
    if not ui.database_control:
        time = ui.db_lineEdittttt_02.text()
        if time == '':
            windowQ.put((ui_num['DB관리'], '시간를 입력하십시오.'))
            return
        if proc_query.is_alive():
            ui.database_control = True
            windowQ.put((ui_num['DB관리'], '주식 일자DB의 지정시간이후 데이터를 삭제합니다.'))
            queryQ.put(('주식일자DB지정시간이후삭제', time))


def dbbutton_clicked_03(ui, windowQ, queryQ, proc_query):
    if not ui.database_control:
        time = ui.db_lineEdittttt_03.text()
        if time == '':
            windowQ.put((ui_num['DB관리'], '시간를 입력하십시오.'))
            return
        if proc_query.is_alive():
            ui.database_control = True
            windowQ.put((ui_num['DB관리'], '주식 당일 데이터의 지정시간이후 데이터를 삭제합니다.'))
            queryQ.put(('주식당일데이터지정시간이후삭제', time))


def dbbutton_clicked_04(ui, windowQ, queryQ, proc_query):
    if not ui.database_control:
        date = ui.db_lineEdittttt_04.text()
        if date == '':
            windowQ.put((ui_num['DB관리'], '일자를 입력하십시오.'))
            return
        if proc_query.is_alive():
            ui.database_control = True
            windowQ.put((ui_num['DB관리'], '주식 당일DB의 체결시간을 조정합니다.'))
            queryQ.put(('주식체결시간조정', date))


def dbbutton_clicked_05(ui, windowQ, queryQ, proc_query):
    if not ui.database_control:
        date1 = ui.db_lineEdittttt_05.text()
        date2 = ui.db_lineEdittttt_06.text()
        if '' in (date1, date2):
            windowQ.put((ui_num['DB관리'], '일자를 입력하십시오.'))
            return
        if proc_query.is_alive():
            ui.database_control = True
            windowQ.put((ui_num['DB관리'], '주식 일자DB로 백테DB를 생성합니다.'))
            queryQ.put(('주식백테DB생성', date1, date2))


def dbbutton_clicked_06(ui, windowQ, queryQ, proc_query):
    if not ui.database_control:
        date1 = ui.db_lineEdittttt_07.text()
        date2 = ui.db_lineEdittttt_08.text()
        if '' in (date1, date2):
            windowQ.put((ui_num['DB관리'], '일자를 입력하십시오.'))
            return
        if proc_query.is_alive():
            ui.database_control = True
            windowQ.put((ui_num['DB관리'], '주식 일자DB를 백테DB로 추가합니다.'))
            queryQ.put(('주식백테디비추가1', date1, date2))


def dbbutton_clicked_07(ui, windowQ, queryQ, proc_query):
    if not ui.database_control:
        if proc_query.is_alive():
            ui.database_control = True
            windowQ.put((ui_num['DB관리'], '주식 당일DB를 백테DB로 추가합니다.'))
            queryQ.put(('주식백테디비추가2', ''))


def dbbutton_clicked_08(ui, windowQ, queryQ, proc_query):
    if not ui.database_control:
        if proc_query.is_alive():
            ui.database_control = True
            windowQ.put((ui_num['DB관리'], '주식 당일DB를 일자DB로 분리합니다.'))
            queryQ.put(('주식일자DB분리', ''))


def dbbutton_clicked_09(ui, windowQ, queryQ, proc_query):
    buttonReply = QMessageBox.warning(
        ui.dialog_db, '주식 거래기록 삭제', '체결목록, 잔고목록, 거래목록, 일별목록이 모두 삭제됩니다.\n계속하시겠습니까?\n',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    )
    if buttonReply == QMessageBox.Yes:
        if proc_query.is_alive():
            queryQ.put(('거래디비', 'DELETE FROM s_jangolist'))
            queryQ.put(('거래디비', 'DELETE FROM s_tradelist'))
            queryQ.put(('거래디비', 'DELETE FROM s_chegeollist'))
            queryQ.put(('거래디비', 'DELETE FROM s_totaltradelist'))
            queryQ.put(('거래디비', 'VACUUM'))
            windowQ.put((ui_num['DB관리'], '주식 거래기록 삭제 완료'))


def dbbutton_clicked_10(ui, windowQ, queryQ, proc_query):
    if not ui.database_control:
        date = ui.db_lineEdittttt_09.text()
        if date == '':
            windowQ.put((ui_num['DB관리'], '일자를 입력하십시오.'))
            return
        if proc_query.is_alive():
            ui.database_control = True
            windowQ.put((ui_num['DB관리'], '코인 일자DB의 지정일자 데이터를 삭제합니다.'))
            queryQ.put(('코인일자DB지정일자삭제', date))


def dbbutton_clicked_11(ui, windowQ, queryQ, proc_query):
    if not ui.database_control:
        time = ui.db_lineEdittttt_10.text()
        if time == '':
            windowQ.put((ui_num['DB관리'], '시간를 입력하십시오.'))
            return
        if proc_query.is_alive():
            ui.database_control = True
            windowQ.put((ui_num['DB관리'], '코인 일자DB의 지정시간이후 데이터를 삭제합니다.'))
            queryQ.put(('코인일자DB지정시간이후삭제', time))


def dbbutton_clicked_12(ui, windowQ, queryQ, proc_query):
    if not ui.database_control:
        time = ui.db_lineEdittttt_11.text()
        if time == '':
            windowQ.put((ui_num['DB관리'], '시간를 입력하십시오.'))
            return
        if proc_query.is_alive():
            ui.database_control = True
            windowQ.put((ui_num['DB관리'], '코인 당일DB의 지정시간이후 데이터를 삭제합니다.'))
            queryQ.put(('코인당일데이터지정시간이후삭제', time))


def dbbutton_clicked_13(ui, windowQ, queryQ, proc_query):
    if not ui.database_control:
        date1 = ui.db_lineEdittttt_12.text()
        date2 = ui.db_lineEdittttt_13.text()
        if '' in (date1, date2):
            windowQ.put((ui_num['DB관리'], '일자를 입력하십시오.'))
            return
        if proc_query.is_alive():
            ui.database_control = True
            windowQ.put((ui_num['DB관리'], '코인 일자DB로 백테DB를 생성합니다.'))
            queryQ.put(('코인백테DB생성', date1, date2))


def dbbutton_clicked_14(ui, windowQ, queryQ, proc_query):
    if not ui.database_control:
        date1 = ui.db_lineEdittttt_14.text()
        date2 = ui.db_lineEdittttt_15.text()
        if '' in (date1, date2):
            windowQ.put((ui_num['DB관리'], '일자를 입력하십시오.'))
            return
        if proc_query.is_alive():
            ui.database_control = True
            windowQ.put((ui_num['DB관리'], '코인 일자DB를 백테DB로 추가합니다.'))
            queryQ.put(('코인백테디비추가1', date1, date2))


def dbbutton_clicked_15(ui, windowQ, queryQ, proc_query):
    if not ui.database_control:
        if proc_query.is_alive():
            ui.database_control = True
            windowQ.put((ui_num['DB관리'], '코인 당일DB를 백테DB로 추가합니다.'))
            queryQ.put(('코인백테디비추가2', ''))


def dbbutton_clicked_16(ui, windowQ, queryQ, proc_query):
    if not ui.database_control:
        if proc_query.is_alive():
            ui.database_control = True
            windowQ.put((ui_num['DB관리'], '코인 당일DB를 일자DB로 분리합니다.'))
            queryQ.put(('코인일자DB분리', ''))


def dbbutton_clicked_17(ui, windowQ, queryQ, proc_query):
    buttonReply = QMessageBox.warning(
        ui.dialog_db, '코인 거래기록 삭제', '체결목록, 잔고목록, 거래목록, 일별목록이 모두 삭제됩니다.\n계속하시겠습니까?\n',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    )
    if buttonReply == QMessageBox.Yes:
        if proc_query.is_alive():
            queryQ.put(('거래디비', 'DELETE FROM c_jangolist'))
            queryQ.put(('거래디비', 'DELETE FROM c_jangolist_future'))
            queryQ.put(('거래디비', 'DELETE FROM c_tradelist'))
            queryQ.put(('거래디비', 'DELETE FROM c_tradelist_future'))
            queryQ.put(('거래디비', 'DELETE FROM c_chegeollist'))
            queryQ.put(('거래디비', 'DELETE FROM c_totaltradelist'))
            queryQ.put(('거래디비', 'VACUUM'))
            windowQ.put((ui_num['DB관리'], '코인 거래기록 삭제 완료'))


def dbbutton_clicked_18(ui, windowQ, queryQ, proc_query):
    if not ui.database_control:
        date = ui.db_lineEdittttt_16.text()
        if date == '':
            windowQ.put((ui_num['DB관리'], '일자를 입력하십시오.'))
            return
        if proc_query.is_alive():
            ui.database_control = True
            windowQ.put((ui_num['DB관리'], '주식 백테DB의 지정일자 데이터를 삭제합니다.'))
            queryQ.put(('주식백테DB지정일자삭제', date))


def dbbutton_clicked_19(ui, windowQ, queryQ, proc_query):
    if not ui.database_control:
        date = ui.db_lineEdittttt_17.text()
        if date == '':
            windowQ.put((ui_num['DB관리'], '일자를 입력하십시오.'))
            return
        if proc_query.is_alive():
            ui.database_control = True
            windowQ.put((ui_num['DB관리'], '코인 백테DB의 지정일자 데이터를 삭제합니다.'))
            queryQ.put(('코인백테DB지정일자삭제', date))
