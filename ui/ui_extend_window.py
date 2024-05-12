from PyQt5.QtWidgets import QMessageBox


def extend_window(ui):
    if ui.main_btn not in (2, 3):
        QMessageBox.critical(ui, '오류 알림', '전략탭 확장기능은 전략탭에서만 사용할 수 있습니다.')
        return

    if not ui.extend_window:
        ui.extend_window = True
        ui.setFixedSize(1403, 1368)
        ui.image_label2.setVisible(True)
        ui.progressBarrr.setGeometry(5, 568, 35, 793)
    else:
        ui.extend_window = False
        ui.setFixedSize(1403, 763)
        ui.image_label2.setVisible(False)
        ui.progressBarrr.setGeometry(5, 568, 35, 188)

    if ui.main_btn == 2:
        ui.ss_tab.setGeometry(45, 0, 1353, 1362 if ui.extend_window else 757)
        if ui.ss_pushButtonn_08.isVisible():
            ui.ss_textEditttt_09.setGeometry(7, 10, 1000, 1313 if ui.extend_window else 703)
            ui.ss_progressBar_01.setGeometry(7, 1328 if ui.extend_window else 718, 830, 30)
            ui.ss_pushButtonn_08.setGeometry(842, 1328 if ui.extend_window else 718, 165, 30)
        elif ui.ss_pushButtonn_01.isVisible():
            ui.ss_tableWidget_01.setGeometry(7, 40, 1000, 1318 if ui.extend_window else 713)
            if (ui.extend_window and ui.ss_tableWidget_01.rowCount() < 60) or (
                    not ui.extend_window and ui.ss_tableWidget_01.rowCount() < 32):
                ui.ss_tableWidget_01.setRowCount(60 if ui.extend_window else 32)
        elif ui.svj_pushButton_01.isVisible():
            ui.ss_textEditttt_01.setGeometry(7, 10, 1000, 740 if ui.extend_window else 463)
            ui.ss_textEditttt_02.setGeometry(7, 756 if ui.extend_window else 480, 1000, 602 if ui.extend_window else 272)
            ui.szoo_pushButon_02.setGeometry(952, 761 if ui.extend_window else 483, 50, 20)
        elif ui.svc_pushButton_24.isVisible():
            ui.ss_textEditttt_01.setGeometry(7, 10, 497, 740 if ui.extend_window else 463)
            ui.ss_textEditttt_02.setGeometry(7, 756 if ui.extend_window else 480, 497, 602 if ui.extend_window else 272)
            ui.ss_textEditttt_03.setGeometry(509, 10, 497, 740 if ui.extend_window else 463)
            ui.ss_textEditttt_04.setGeometry(509, 756 if ui.extend_window else 480, 497, 602 if ui.extend_window else 272)
        elif ui.svc_pushButton_21.isVisible():
            ui.ss_textEditttt_05.setGeometry(7, 10, 497, 1347 if ui.extend_window else 740)
            ui.ss_textEditttt_06.setGeometry(509, 10, 497, 1347 if ui.extend_window else 740)
        elif ui.svo_pushButton_05.isVisible():
            ui.ss_textEditttt_07.setGeometry(7, 10, 497, 1347 if ui.extend_window else 740)
            ui.ss_textEditttt_08.setGeometry(509, 10, 497, 1347 if ui.extend_window else 740)
        elif ui.sva_pushButton_01.isVisible():
            ui.ss_textEditttt_03.setGeometry(7, 10, 647, 740 if ui.extend_window else 463)
            ui.ss_textEditttt_04.setGeometry(7, 756 if ui.extend_window else 480, 647, 602 if ui.extend_window else 272)
            ui.ss_textEditttt_06.setGeometry(659, 10, 347, 1347 if ui.extend_window else 740)
            ui.szoo_pushButon_02.setGeometry(599, 761 if ui.extend_window else 483, 50, 20)
        else:
            ui.ss_textEditttt_03.setGeometry(7, 10, 647, 740 if ui.extend_window else 463)
            ui.ss_textEditttt_04.setGeometry(7, 756 if ui.extend_window else 480, 647, 602 if ui.extend_window else 272)
            ui.ss_textEditttt_05.setGeometry(659, 10, 347, 1347 if ui.extend_window else 740)
            ui.szoo_pushButon_02.setGeometry(599, 761 if ui.extend_window else 483, 50, 20)
    else:
        ui.cs_tab.setGeometry(45, 0, 1353, 1362 if ui.extend_window else 757)
        if ui.cs_pushButtonn_08.isVisible():
            ui.cs_textEditttt_09.setGeometry(7, 10, 1000, 1313 if ui.extend_window else 703)
            ui.cs_progressBar_01.setGeometry(7, 1328 if ui.extend_window else 718, 830, 30)
            ui.cs_pushButtonn_08.setGeometry(842, 1328 if ui.extend_window else 718, 165, 30)
        elif ui.cs_pushButtonn_01.isVisible():
            ui.cs_tableWidget_01.setGeometry(7, 40, 1000, 1318 if ui.extend_window else 713)
            if (ui.extend_window and ui.cs_tableWidget_01.rowCount() < 60) or (not ui.extend_window and ui.cs_tableWidget_01.rowCount() < 32):
                ui.cs_tableWidget_01.setRowCount(60 if ui.extend_window else 32)
        elif ui.cvj_pushButton_01.isVisible():
            ui.cs_textEditttt_01.setGeometry(7, 10, 1000, 740 if ui.extend_window else 463)
            ui.cs_textEditttt_02.setGeometry(7, 756 if ui.extend_window else 480, 1000, 602 if ui.extend_window else 272)
            ui.czoo_pushButon_02.setGeometry(952, 761 if ui.extend_window else 483, 50, 20)
        elif ui.cvc_pushButton_24.isVisible():
            ui.cs_textEditttt_01.setGeometry(7, 10, 497, 740 if ui.extend_window else 463)
            ui.cs_textEditttt_02.setGeometry(7, 756 if ui.extend_window else 480, 497, 602 if ui.extend_window else 272)
            ui.cs_textEditttt_03.setGeometry(509, 10, 497, 740 if ui.extend_window else 463)
            ui.cs_textEditttt_04.setGeometry(509, 756 if ui.extend_window else 480, 497, 602 if ui.extend_window else 272)
        elif ui.cvc_pushButton_21.isVisible():
            ui.cs_textEditttt_05.setGeometry(7, 10, 497, 1347 if ui.extend_window else 740)
            ui.cs_textEditttt_06.setGeometry(509, 10, 497, 1347 if ui.extend_window else 740)
        elif ui.cvo_pushButton_05.isVisible():
            ui.cs_textEditttt_07.setGeometry(7, 10, 497, 1347 if ui.extend_window else 740)
            ui.cs_textEditttt_08.setGeometry(509, 10, 497, 1347 if ui.extend_window else 740)
        elif ui.cva_pushButton_01.isVisible():
            ui.cs_textEditttt_03.setGeometry(7, 10, 647, 740 if ui.extend_window else 463)
            ui.cs_textEditttt_04.setGeometry(7, 756 if ui.extend_window else 480, 647, 602 if ui.extend_window else 272)
            ui.cs_textEditttt_06.setGeometry(659, 10, 347, 1347 if ui.extend_window else 740)
            ui.czoo_pushButon_02.setGeometry(599, 761 if ui.extend_window else 483, 50, 20)
        else:
            ui.cs_textEditttt_03.setGeometry(7, 10, 647, 740 if ui.extend_window else 463)
            ui.cs_textEditttt_04.setGeometry(7, 756 if ui.extend_window else 480, 647, 602 if ui.extend_window else 272)
            ui.cs_textEditttt_05.setGeometry(659, 10, 347, 1347 if ui.extend_window else 740)
            ui.czoo_pushButon_02.setGeometry(599, 761 if ui.extend_window else 483, 50, 20)
