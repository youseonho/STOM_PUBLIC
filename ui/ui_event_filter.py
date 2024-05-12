from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox


def event_filter(ui, widget, event):
    if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
        if widget == ui.ss_textEditttt_01:
            ui.ss_textEditttt_01.insertPlainText('    ')
        elif widget == ui.ss_textEditttt_02:
            ui.ss_textEditttt_02.insertPlainText('    ')
        elif widget == ui.ss_textEditttt_03:
            ui.ss_textEditttt_03.insertPlainText('    ')
        elif widget == ui.ss_textEditttt_04:
            ui.ss_textEditttt_04.insertPlainText('    ')
        elif widget == ui.cs_textEditttt_01:
            ui.cs_textEditttt_01.insertPlainText('    ')
        elif widget == ui.cs_textEditttt_02:
            ui.cs_textEditttt_02.insertPlainText('    ')
        elif widget == ui.cs_textEditttt_03:
            ui.cs_textEditttt_03.insertPlainText('    ')
        elif widget == ui.cs_textEditttt_04:
            ui.cs_textEditttt_04.insertPlainText('    ')
        return True
    elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Escape:
        if not ui.svc_pushButton_24.isVisible():
            if widget in (ui.ss_textEditttt_01, ui.ss_textEditttt_03):
                ui.szooButtonClicked_01()
            elif widget in (ui.ss_textEditttt_02, ui.ss_textEditttt_04):
                ui.szooButtonClicked_02()
        if not ui.cvc_pushButton_24.isVisible():
            if widget in (ui.cs_textEditttt_01, ui.cs_textEditttt_03):
                ui.czooButtonClicked_01()
            elif widget in (ui.cs_textEditttt_02, ui.cs_textEditttt_04):
                ui.czooButtonClicked_02()
        return True
    elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_F1:
        if ui.main_btn == 2:
            if ui.svj_pushButton_01.isVisible():
                ui.ss_textEditttt_01.setFocus()
                ui.svjbButtonClicked_01()
            elif ui.svc_pushButton_06.isVisible() or ui.sva_pushButton_03.isVisible():
                ui.ss_textEditttt_03.setFocus()
                ui.svcButtonClicked_01()
            elif ui.svo_pushButton_05.isVisible():
                ui.ss_textEditttt_07.setFocus()
                ui.svoButtonClicked_01()
        elif ui.main_btn == 3:
            if ui.cvj_pushButton_01.isVisible():
                ui.cs_textEditttt_01.setFocus()
                ui.cvjbButtonClicked_01()
            elif ui.cvc_pushButton_06.isVisible() or ui.cva_pushButton_01.isVisible():
                ui.cs_textEditttt_04.setFocus()
                ui.cvcButtonClicked_01()
            elif ui.cvo_pushButton_05.isVisible():
                ui.cs_textEditttt_08.setFocus()
                ui.cvoButtonClicked_01()
        return True
    elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_F2:
        if ui.main_btn == 2:
            if ui.svj_pushButton_01.isVisible():
                ui.ss_textEditttt_01.setFocus()
                ui.svjb_comboBoxx_01.showPopup()
            elif ui.svc_pushButton_06.isVisible() or ui.sva_pushButton_03.isVisible():
                ui.ss_textEditttt_03.setFocus()
                ui.svc_comboBoxxx_01.showPopup()
            elif ui.svo_pushButton_05.isVisible():
                ui.ss_textEditttt_07.setFocus()
                ui.svo_comboBoxxx_01.showPopup()
        elif ui.main_btn == 3:
            if ui.cvj_pushButton_01.isVisible():
                ui.cs_textEditttt_01.setFocus()
                ui.cvjb_comboBoxx_01.showPopup()
            elif ui.cvc_pushButton_06.isVisible() or ui.cva_pushButton_01.isVisible():
                ui.cs_textEditttt_04.setFocus()
                ui.cvc_comboBoxxx_01.showPopup()
            elif ui.cvo_pushButton_05.isVisible():
                ui.cs_textEditttt_08.setFocus()
                ui.cvo_comboBoxxx_01.showPopup()
        return True
    elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_F3:
        if ui.main_btn == 2:
            if ui.svj_pushButton_01.isVisible():
                ui.svjb_lineEditt_01.setFocus()
            elif ui.svc_pushButton_06.isVisible() or ui.sva_pushButton_03.isVisible():
                ui.svc_lineEdittt_01.setFocus()
            elif ui.svo_pushButton_05.isVisible():
                ui.svo_lineEdittt_01.setFocus()
        elif ui.main_btn == 3:
            if ui.cvj_pushButton_01.isVisible():
                ui.cvjb_lineEditt_01.setFocus()
            elif ui.cvc_pushButton_06.isVisible() or ui.cva_pushButton_01.isVisible():
                ui.cvc_lineEdittt_01.setFocus()
            elif ui.cvo_pushButton_05.isVisible():
                ui.cvo_lineEdittt_01.setFocus()
        return True
    elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_F5:
        if ui.main_btn == 2:
            if ui.svj_pushButton_01.isVisible():
                ui.ss_textEditttt_02.setFocus()
                ui.svjsButtonClicked_01()
            elif ui.svc_pushButton_06.isVisible() or ui.sva_pushButton_03.isVisible():
                ui.ss_textEditttt_04.setFocus()
                ui.svcButtonClicked_05()
            elif ui.svo_pushButton_05.isVisible():
                ui.ss_textEditttt_05.setFocus()
                ui.svoButtonClicked_03()
        elif ui.main_btn == 3:
            if ui.cvj_pushButton_01.isVisible():
                ui.cs_textEditttt_02.setFocus()
                ui.cvjsButtonClicked_01()
            elif ui.cvc_pushButton_06.isVisible() or ui.cva_pushButton_01.isVisible():
                ui.cs_textEditttt_05.setFocus()
                ui.cvcButtonClicked_07()
            elif ui.cvo_pushButton_05.isVisible():
                ui.cs_textEditttt_06.setFocus()
                ui.cvoButtonClicked_03()
        return True
    elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_F6:
        if ui.main_btn == 2:
            if ui.svj_pushButton_01.isVisible():
                ui.ss_textEditttt_02.setFocus()
                ui.svjs_comboBoxx_01.showPopup()
            elif ui.svc_pushButton_06.isVisible() or ui.sva_pushButton_03.isVisible():
                ui.ss_textEditttt_03.setFocus()
                ui.svc_comboBoxxx_08.showPopup()
            elif ui.svo_pushButton_05.isVisible():
                ui.ss_textEditttt_04.setFocus()
                ui.svo_comboBoxxx_02.showPopup()
        elif ui.main_btn == 3:
            if ui.cvj_pushButton_01.isVisible():
                ui.cs_textEditttt_02.setFocus()
                ui.cvjs_comboBoxx_01.showPopup()
            elif ui.cvc_pushButton_06.isVisible() or ui.cva_pushButton_01.isVisible():
                ui.cs_textEditttt_04.setFocus()
                ui.cvc_comboBoxxx_08.showPopup()
            elif ui.cvo_pushButton_05.isVisible():
                ui.cs_textEditttt_05.setFocus()
                ui.cvo_comboBoxxx_02.showPopup()
        return True
    elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_F7:
        if ui.main_btn == 2:
            if ui.svj_pushButton_01.isVisible():
                ui.svjs_lineEditt_01.setFocus()
            elif ui.svc_pushButton_06.isVisible() or ui.sva_pushButton_03.isVisible():
                ui.svc_lineEdittt_03.setFocus()
            elif ui.svo_pushButton_05.isVisible():
                ui.svo_lineEdittt_02.setFocus()
        elif ui.main_btn == 3:
            if ui.cvj_pushButton_01.isVisible():
                ui.cvjs_lineEditt_01.setFocus()
            elif ui.cvc_pushButton_06.isVisible() or ui.cva_pushButton_01.isVisible():
                ui.cvc_lineEdittt_03.setFocus()
            elif ui.cvo_pushButton_05.isVisible():
                ui.cvo_lineEdittt_02.setFocus()
        return True
    elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_F9:
        if ui.main_btn == 2:
            if ui.svc_pushButton_06.isVisible():
                ui.ss_textEditttt_05.setFocus()
                ui.svcButtonClicked_03()
            elif ui.sva_pushButton_03.isVisible():
                ui.ss_textEditttt_06.setFocus()
                ui.svaButtonClicked_01()
        elif ui.main_btn == 3:
            if ui.cvc_pushButton_06.isVisible():
                ui.cs_textEditttt_06.setFocus()
                ui.cvcButtonClicked_03()
            elif ui.cva_pushButton_01.isVisible():
                ui.cs_textEditttt_07.setFocus()
                ui.cvaButtonClicked_02()
        return True
    elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_F10:
        if ui.main_btn == 2:
            if ui.svc_pushButton_06.isVisible():
                ui.ss_textEditttt_05.setFocus()
                ui.svc_comboBoxxx_02.showPopup()
            elif ui.sva_pushButton_03.isVisible():
                ui.ss_textEditttt_06.setFocus()
                ui.sva_comboBoxxx_01.showPopup()
        elif ui.main_btn == 3:
            if ui.cvc_pushButton_06.isVisible():
                ui.cs_textEditttt_06.setFocus()
                ui.cvc_comboBoxxx_02.showPopup()
            elif ui.cva_pushButton_01.isVisible():
                ui.cs_textEditttt_07.setFocus()
                ui.cva_comboBoxxx_01.showPopup()
        return True
    elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_F11:
        if ui.main_btn == 2:
            if ui.svc_pushButton_06.isVisible():
                ui.svc_lineEdittt_02.setFocus()
            elif ui.sva_pushButton_03.isVisible():
                ui.sva_lineEdittt_01.setFocus()
        elif ui.main_btn == 3:
            if ui.cvc_pushButton_06.isVisible():
                ui.cvc_lineEdittt_02.setFocus()
            elif ui.cva_pushButton_01.isVisible():
                ui.cva_lineEdittt_01.setFocus()
        return True
    else:
        return QMainWindow.eventFilter(ui, widget, event)


def close_event(ui, a):
    buttonReply = QMessageBox.question(
        ui, "프로그램 종료", "프로그램을 종료합니다.",
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    )
    if buttonReply == QMessageBox.Yes:
        ui.ProcessKill()
        a.accept()
    else:
        a.ignore()
