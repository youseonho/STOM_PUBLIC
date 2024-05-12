def szoo_button_clicked_01(ui):
    if ui.svj_pushButton_01.isVisible():
        if ui.szoo_pushButon_01.text() == '확대(esc)':
            ui.szoo_pushButon_01.setText('축소(esc)')
            ui.szoo_pushButon_01.setGeometry(952, 15, 50, 20)
            ui.ss_textEditttt_01.setGeometry(7, 10, 1000, 1347 if ui.extend_window else 740)
            ui.ss_textEditttt_02.setVisible(False)
            ui.szoo_pushButon_02.setVisible(False)
        else:
            ui.szoo_pushButon_01.setText('확대(esc)')
            ui.szoo_pushButon_01.setGeometry(952, 15, 50, 20)
            ui.ss_textEditttt_01.setGeometry(7, 10, 1000, 740 if ui.extend_window else 463)
            ui.ss_textEditttt_02.setVisible(True)
            ui.szoo_pushButon_02.setVisible(True)
    else:
        if ui.szoo_pushButon_01.text() == '확대(esc)':
            ui.szoo_pushButon_01.setText('축소(esc)')
            ui.szoo_pushButon_01.setGeometry(952, 15, 50, 20)
            ui.ss_textEditttt_03.setGeometry(7, 10, 1000, 1347 if ui.extend_window else 740)
            ui.ss_textEditttt_04.setVisible(False)
            if ui.sva_pushButton_01.isVisible():
                ui.ss_textEditttt_06.setVisible(False)
            else:
                ui.ss_textEditttt_05.setVisible(False)
            ui.szoo_pushButon_02.setVisible(False)
        else:
            ui.szoo_pushButon_01.setText('확대(esc)')
            ui.szoo_pushButon_01.setGeometry(599, 15, 50, 20)
            ui.ss_textEditttt_03.setGeometry(7, 10, 647, 740 if ui.extend_window else 463)
            ui.ss_textEditttt_04.setVisible(True)
            if ui.sva_pushButton_01.isVisible():
                ui.ss_textEditttt_06.setVisible(True)
            else:
                ui.ss_textEditttt_05.setVisible(True)
            ui.szoo_pushButon_02.setVisible(True)


def szoo_button_clicked_02(ui):
    if ui.svj_pushButton_01.isVisible():
        if ui.szoo_pushButon_02.text() == '확대(esc)':
            ui.szoo_pushButon_02.setText('축소(esc)')
            ui.szoo_pushButon_02.setGeometry(952, 15, 50, 20)
            ui.ss_textEditttt_02.setGeometry(7, 10, 1000, 1347 if ui.extend_window else 740)
            ui.ss_textEditttt_01.setVisible(False)
            ui.szoo_pushButon_01.setVisible(False)
        else:
            ui.szoo_pushButon_02.setText('확대(esc)')
            ui.szoo_pushButon_02.setGeometry(952, 761 if ui.extend_window else 483, 50, 20)
            ui.ss_textEditttt_02.setGeometry(7, 756 if ui.extend_window else 480, 1000,
                                             602 if ui.extend_window else 272)
            ui.ss_textEditttt_01.setVisible(True)
            ui.szoo_pushButon_01.setVisible(True)
    else:
        if ui.szoo_pushButon_02.text() == '확대(esc)':
            ui.szoo_pushButon_02.setText('축소(esc)')
            ui.szoo_pushButon_02.setGeometry(952, 15, 50, 20)
            ui.ss_textEditttt_04.setGeometry(7, 10, 1000, 1347 if ui.extend_window else 740)
            ui.ss_textEditttt_03.setVisible(False)
            if ui.sva_pushButton_01.isVisible():
                ui.ss_textEditttt_06.setVisible(False)
            else:
                ui.ss_textEditttt_05.setVisible(False)
            ui.szoo_pushButon_01.setVisible(False)
        else:
            ui.szoo_pushButon_02.setText('확대(esc)')
            ui.szoo_pushButon_02.setGeometry(599, 761 if ui.extend_window else 483, 50, 20)
            ui.ss_textEditttt_04.setGeometry(7, 756 if ui.extend_window else 480, 647, 602 if ui.extend_window else 272)
            ui.ss_textEditttt_03.setVisible(True)
            if ui.sva_pushButton_01.isVisible():
                ui.ss_textEditttt_06.setVisible(True)
            else:
                ui.ss_textEditttt_05.setVisible(True)
            ui.szoo_pushButon_01.setVisible(True)


def czoo_button_clicked_01(ui):
    if ui.cvj_pushButton_01.isVisible():
        if ui.czoo_pushButon_01.text() == '확대(esc)':
            ui.czoo_pushButon_01.setText('축소(esc)')
            ui.czoo_pushButon_01.setGeometry(952, 15, 50, 20)
            ui.cs_textEditttt_01.setGeometry(7, 10, 1000, 1347 if ui.extend_window else 740)
            ui.cs_textEditttt_02.setVisible(False)
            ui.czoo_pushButon_02.setVisible(False)
        else:
            ui.czoo_pushButon_01.setText('확대(esc)')
            ui.czoo_pushButon_01.setGeometry(952, 15, 50, 20)
            ui.cs_textEditttt_01.setGeometry(7, 10, 1000, 740 if ui.extend_window else 463)
            ui.cs_textEditttt_02.setVisible(True)
            ui.czoo_pushButon_02.setVisible(True)
    else:
        if ui.czoo_pushButon_01.text() == '확대(esc)':
            ui.czoo_pushButon_01.setText('축소(esc)')
            ui.czoo_pushButon_01.setGeometry(952, 15, 50, 20)
            ui.cs_textEditttt_03.setGeometry(7, 10, 1000, 1347 if ui.extend_window else 740)
            ui.cs_textEditttt_04.setVisible(False)
            if ui.cva_pushButton_01.isVisible():
                ui.cs_textEditttt_06.setVisible(False)
            else:
                ui.cs_textEditttt_05.setVisible(False)
            ui.czoo_pushButon_02.setVisible(False)
        else:
            ui.czoo_pushButon_01.setText('확대(esc)')
            ui.czoo_pushButon_01.setGeometry(599, 15, 50, 20)
            ui.cs_textEditttt_03.setGeometry(7, 10, 647, 740 if ui.extend_window else 463)
            ui.cs_textEditttt_04.setVisible(True)
            if ui.cva_pushButton_01.isVisible():
                ui.cs_textEditttt_06.setVisible(True)
            else:
                ui.cs_textEditttt_05.setVisible(True)
            ui.czoo_pushButon_02.setVisible(True)


def czoo_button_clicked_02(ui):
    if ui.cvj_pushButton_01.isVisible():
        if ui.czoo_pushButon_02.text() == '확대(esc)':
            ui.czoo_pushButon_02.setText('축소(esc)')
            ui.czoo_pushButon_02.setGeometry(952, 15, 50, 20)
            ui.cs_textEditttt_02.setGeometry(7, 10, 1000, 1347 if ui.extend_window else 740)
            ui.cs_textEditttt_01.setVisible(False)
            ui.czoo_pushButon_01.setVisible(False)
        else:
            ui.czoo_pushButon_02.setText('확대(esc)')
            ui.czoo_pushButon_02.setGeometry(952, 761 if ui.extend_window else 483, 50, 20)
            ui.cs_textEditttt_02.setGeometry(7, 756 if ui.extend_window else 480, 1000,
                                             602 if ui.extend_window else 272)
            ui.cs_textEditttt_01.setVisible(True)
            ui.czoo_pushButon_01.setVisible(True)
    else:
        if ui.czoo_pushButon_02.text() == '확대(esc)':
            ui.czoo_pushButon_02.setText('축소(esc)')
            ui.czoo_pushButon_02.setGeometry(952, 15, 50, 20)
            ui.cs_textEditttt_04.setGeometry(7, 10, 1000, 1347 if ui.extend_window else 740)
            ui.cs_textEditttt_03.setVisible(False)
            if ui.cva_pushButton_01.isVisible():
                ui.cs_textEditttt_06.setVisible(False)
            else:
                ui.cs_textEditttt_05.setVisible(False)
            ui.czoo_pushButon_01.setVisible(False)
        else:
            ui.czoo_pushButon_02.setText('확대(esc)')
            ui.czoo_pushButon_02.setGeometry(599, 761 if ui.extend_window else 483, 50, 20)
            ui.cs_textEditttt_04.setGeometry(7, 756 if ui.extend_window else 478, 647, 602 if ui.extend_window else 272)
            ui.cs_textEditttt_03.setVisible(True)
            if ui.cva_pushButton_01.isVisible():
                ui.cs_textEditttt_06.setVisible(True)
            else:
                ui.cs_textEditttt_05.setVisible(True)
            ui.czoo_pushButon_01.setVisible(True)
