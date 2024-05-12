from PyQt5.QtWidgets import QMessageBox
from ui.set_style import style_bc_by, style_bc_dk, style_bc_bs, style_bc_bd
from ui.set_text import testtext, rwfttext, gaoptext, vedittxt, optitext, condtext, cedittxt, example_finder, \
    example_finder_future


def cvj_button_clicked_01(ui):
    ui.cs_textEditttt_03.setGeometry(7, 10, 647, 740 if ui.extend_window else 463)
    ui.cs_textEditttt_04.setGeometry(7, 756 if ui.extend_window else 478, 647, 602 if ui.extend_window else 272)
    ui.cs_textEditttt_05.setGeometry(659, 10, 347, 1347 if ui.extend_window else 740)

    ui.cvc_comboBoxxx_02.setGeometry(1012, 115, 165, 30)
    ui.cvc_lineEdittt_02.setGeometry(1182, 115, 165, 30)
    ui.cvc_pushButton_03.setGeometry(1012, 150, 165, 30)
    ui.cvc_pushButton_04.setGeometry(1182, 150, 165, 30)

    ui.czoo_pushButon_01.setGeometry(599, 15, 50, 20)
    ui.czoo_pushButon_02.setGeometry(599, 761 if ui.extend_window else 483, 50, 20)

    ui.czoo_pushButon_01.setText('확대(esc)')
    ui.czoo_pushButon_02.setText('확대(esc)')

    ui.cs_textEditttt_01.setVisible(False)
    ui.cs_textEditttt_02.setVisible(False)
    ui.cs_textEditttt_03.setVisible(True)
    ui.cs_textEditttt_04.setVisible(True)
    ui.cs_textEditttt_05.setVisible(True)
    ui.cs_textEditttt_06.setVisible(False)

    for item in ui.coin_detail_list:
        item.setVisible(False)
    for item in ui.coin_baklog_list:
        item.setVisible(False)
    for item in ui.coin_datedt_list:
        item.setVisible(False)
    for item in ui.coin_backte_list:
        item.setVisible(False)
    for item in ui.coin_opcond_list:
        item.setVisible(False)
    for item in ui.coin_gaopti_list:
        item.setVisible(False)
    for item in ui.coin_rwftvd_list:
        item.setVisible(False)
    for item in ui.coin_esczom_list:
        item.setVisible(True)
    for item in ui.coin_optimz_list:
        item.setVisible(True)
    for item in ui.coin_period_list:
        item.setVisible(True)
    for item in ui.coin_optest_list:
        item.setVisible(True)

    ui.cvc_pushButton_03.setText('최적화 변수범위 로딩(F9)')
    ui.cvc_pushButton_04.setText('최적화 변수범위 저장(F12)')

    ui.image_label1.setVisible(False)
    ui.cvc_labellllll_04.setText(testtext)
    ui.cvc_labellllll_05.setVisible(False)
    ui.cvc_pushButton_21.setVisible(False)
    ui.cvc_pushButton_22.setVisible(False)
    ui.cvc_pushButton_23.setVisible(False)
    ui.cvc_pushButton_24.setVisible(False)
    ui.cvc_pushButton_25.setVisible(False)
    ui.cvc_pushButton_26.setVisible(False)

    ui.cvj_pushButton_09.setFocus()
    cChangeSvjButtonColor(ui)


def cvj_button_clicked_02(ui):
    ui.cs_textEditttt_03.setGeometry(7, 10, 647, 740 if ui.extend_window else 463)
    ui.cs_textEditttt_04.setGeometry(7, 756 if ui.extend_window else 478, 647, 602 if ui.extend_window else 272)
    ui.cs_textEditttt_05.setGeometry(659, 10, 347, 1347 if ui.extend_window else 740)

    ui.cvc_comboBoxxx_02.setGeometry(1012, 115, 165, 30)
    ui.cvc_lineEdittt_02.setGeometry(1182, 115, 165, 30)
    ui.cvc_pushButton_03.setGeometry(1012, 150, 165, 30)
    ui.cvc_pushButton_04.setGeometry(1182, 150, 165, 30)

    ui.czoo_pushButon_01.setGeometry(599, 15, 50, 20)
    ui.czoo_pushButon_02.setGeometry(599, 761 if ui.extend_window else 483, 50, 20)

    ui.czoo_pushButon_01.setText('확대(esc)')
    ui.czoo_pushButon_02.setText('확대(esc)')

    ui.cs_textEditttt_01.setVisible(False)
    ui.cs_textEditttt_02.setVisible(False)
    ui.cs_textEditttt_03.setVisible(True)
    ui.cs_textEditttt_04.setVisible(True)
    ui.cs_textEditttt_05.setVisible(True)
    ui.cs_textEditttt_06.setVisible(False)

    for item in ui.coin_detail_list:
        item.setVisible(False)
    for item in ui.coin_baklog_list:
        item.setVisible(False)
    for item in ui.coin_datedt_list:
        item.setVisible(False)
    for item in ui.coin_backte_list:
        item.setVisible(False)
    for item in ui.coin_opcond_list:
        item.setVisible(False)
    for item in ui.coin_gaopti_list:
        item.setVisible(False)
    for item in ui.coin_optest_list:
        item.setVisible(False)
    for item in ui.coin_esczom_list:
        item.setVisible(True)
    for item in ui.coin_optimz_list:
        item.setVisible(True)
    for item in ui.coin_period_list:
        item.setVisible(True)
    for item in ui.coin_rwftvd_list:
        item.setVisible(True)

    ui.cvc_pushButton_03.setText('최적화 변수범위 로딩(F9)')
    ui.cvc_pushButton_04.setText('최적화 변수범위 저장(F12)')

    ui.image_label1.setVisible(False)
    ui.cvc_labellllll_01.setVisible(False)
    ui.cvc_labellllll_04.setText(rwfttext)
    ui.cvc_labellllll_05.setVisible(False)
    ui.cvc_pushButton_21.setVisible(False)
    ui.cvc_pushButton_22.setVisible(False)
    ui.cvc_pushButton_23.setVisible(False)
    ui.cvc_pushButton_24.setVisible(False)
    ui.cvc_pushButton_25.setVisible(False)
    ui.cvc_pushButton_26.setVisible(False)

    ui.cvj_pushButton_07.setFocus()
    cChangeSvjButtonColor(ui)


def cvj_button_clicked_03(ui):
    ui.cs_textEditttt_03.setGeometry(7, 10, 647, 740 if ui.extend_window else 463)
    ui.cs_textEditttt_04.setGeometry(7, 756 if ui.extend_window else 478, 647, 602 if ui.extend_window else 272)
    ui.cs_textEditttt_06.setGeometry(659, 10, 347, 1347 if ui.extend_window else 740)

    ui.cvc_comboBoxxx_02.setGeometry(1012, 115, 165, 30)
    ui.cvc_lineEdittt_02.setGeometry(1182, 115, 165, 30)
    ui.cvc_pushButton_03.setGeometry(1012, 150, 165, 30)
    ui.cvc_pushButton_04.setGeometry(1182, 150, 165, 30)

    ui.cva_comboBoxxx_01.setGeometry(1012, 115, 165, 30)
    ui.cva_lineEdittt_01.setGeometry(1182, 115, 165, 30)
    ui.cva_pushButton_04.setGeometry(1012, 150, 165, 30)
    ui.cva_pushButton_05.setGeometry(1182, 150, 165, 30)

    ui.czoo_pushButon_01.setGeometry(599, 15, 50, 20)
    ui.czoo_pushButon_02.setGeometry(599, 761 if ui.extend_window else 483, 50, 20)

    ui.czoo_pushButon_01.setText('확대(esc)')
    ui.czoo_pushButon_02.setText('확대(esc)')

    ui.cs_textEditttt_01.setVisible(False)
    ui.cs_textEditttt_02.setVisible(False)
    ui.cs_textEditttt_03.setVisible(True)
    ui.cs_textEditttt_04.setVisible(True)
    ui.cs_textEditttt_05.setVisible(False)
    ui.cs_textEditttt_06.setVisible(True)

    for item in ui.coin_detail_list:
        item.setVisible(False)
    for item in ui.coin_baklog_list:
        item.setVisible(False)
    for item in ui.coin_datedt_list:
        item.setVisible(False)
    for item in ui.coin_backte_list:
        item.setVisible(False)
    for item in ui.coin_opcond_list:
        item.setVisible(False)
    for item in ui.coin_optest_list:
        item.setVisible(False)
    for item in ui.coin_rwftvd_list:
        item.setVisible(False)
    for item in ui.coin_esczom_list:
        item.setVisible(True)
    for item in ui.coin_optimz_list:
        item.setVisible(True)
    for item in ui.coin_period_list:
        item.setVisible(True)
    for item in ui.coin_gaopti_list:
        item.setVisible(True)

    ui.cva_pushButton_04.setText('GA 변수범위 로딩(F9)')
    ui.cva_pushButton_05.setText('GA 변수범위 저장(F12)')

    ui.image_label1.setVisible(False)
    ui.cvc_labellllll_04.setText(gaoptext)
    ui.cvc_labellllll_05.setVisible(False)
    ui.cvc_pushButton_21.setVisible(False)
    ui.cvc_pushButton_22.setVisible(False)
    ui.cvc_pushButton_23.setVisible(False)
    ui.cvc_pushButton_24.setVisible(False)
    ui.cvc_pushButton_25.setVisible(False)
    ui.cvc_pushButton_26.setVisible(False)

    ui.cvj_pushButton_08.setFocus()
    cChangeSvjButtonColor(ui)


def cvj_button_clicked_04(ui):
    ui.cs_textEditttt_05.setGeometry(7, 10, 497, 1347 if ui.extend_window else 740)
    ui.cs_textEditttt_06.setGeometry(509, 10, 497, 1347 if ui.extend_window else 740)

    ui.cvc_comboBoxxx_02.setGeometry(1012, 10, 165, 30)
    ui.cvc_lineEdittt_02.setGeometry(1182, 10, 165, 30)
    ui.cvc_pushButton_03.setGeometry(1012, 45, 165, 30)
    ui.cvc_pushButton_04.setGeometry(1182, 45, 165, 30)

    ui.cva_comboBoxxx_01.setGeometry(1012, 80, 165, 30)
    ui.cva_lineEdittt_01.setGeometry(1182, 80, 165, 30)
    ui.cva_pushButton_04.setGeometry(1012, 115, 165, 30)
    ui.cva_pushButton_05.setGeometry(1182, 115, 165, 30)

    ui.cs_textEditttt_01.setVisible(False)
    ui.cs_textEditttt_02.setVisible(False)
    ui.cs_textEditttt_03.setVisible(False)
    ui.cs_textEditttt_04.setVisible(False)
    ui.cs_textEditttt_05.setVisible(True)
    ui.cs_textEditttt_06.setVisible(True)

    for item in ui.coin_datedt_list:
        item.setVisible(False)
    for item in ui.coin_backte_list:
        item.setVisible(False)
    for item in ui.coin_opcond_list:
        item.setVisible(False)
    for item in ui.coin_detail_list:
        item.setVisible(False)
    for item in ui.coin_baklog_list:
        item.setVisible(False)
    for item in ui.coin_optest_list:
        item.setVisible(False)
    for item in ui.coin_rwftvd_list:
        item.setVisible(False)
    for item in ui.coin_esczom_list:
        item.setVisible(False)
    for item in ui.coin_optimz_list:
        item.setVisible(False)
    for item in ui.coin_period_list:
        item.setVisible(True)
    for item in ui.coin_gaopti_list:
        item.setVisible(True)

    ui.cva_pushButton_04.setText('GA 변수범위 로딩')
    ui.cva_pushButton_05.setText('GA 변수범위 저장')
    ui.cvc_pushButton_03.setText('최적화 변수범위 로딩')
    ui.cvc_pushButton_04.setText('최적화 변수범위 저장')

    ui.cvc_pushButton_06.setVisible(False)
    ui.cvc_pushButton_07.setVisible(False)
    ui.cvc_pushButton_08.setVisible(False)
    ui.cvc_pushButton_27.setVisible(False)
    ui.cvc_pushButton_28.setVisible(False)
    ui.cvc_pushButton_29.setVisible(False)

    ui.cva_pushButton_01.setVisible(False)
    ui.cva_pushButton_02.setVisible(False)
    ui.cva_pushButton_03.setVisible(False)

    ui.cvc_comboBoxxx_02.setVisible(True)
    ui.cvc_lineEdittt_02.setVisible(True)
    ui.cvc_pushButton_03.setVisible(True)
    ui.cvc_pushButton_04.setVisible(True)

    ui.cvc_pushButton_11.setVisible(True)

    ui.image_label1.setVisible(True)
    ui.cvc_labellllll_05.setVisible(True)
    ui.cvc_labellllll_04.setText(gaoptext)
    ui.cvc_labellllll_05.setText(vedittxt)
    ui.cvc_pushButton_21.setVisible(True)
    ui.cvc_pushButton_22.setVisible(True)
    ui.cvc_pushButton_23.setVisible(True)
    ui.cvc_pushButton_24.setVisible(False)
    ui.cvc_pushButton_25.setVisible(False)
    ui.cvc_pushButton_26.setVisible(False)

    ui.cvj_pushButton_12.setFocus()
    cChangeSvjButtonColor(ui)


def cvj_button_clicked_05(ui):
    ui.cs_textEditttt_03.setGeometry(7, 10, 647, 740 if ui.extend_window else 463)
    ui.cs_textEditttt_04.setGeometry(7, 756 if ui.extend_window else 478, 647, 602 if ui.extend_window else 272)
    ui.cs_textEditttt_05.setGeometry(659, 10, 347, 1347 if ui.extend_window else 740)

    ui.cvc_comboBoxxx_02.setGeometry(1012, 115, 165, 30)
    ui.cvc_lineEdittt_02.setGeometry(1182, 115, 165, 30)
    ui.cvc_pushButton_03.setGeometry(1012, 150, 165, 30)
    ui.cvc_pushButton_04.setGeometry(1182, 150, 165, 30)

    ui.czoo_pushButon_01.setGeometry(599, 15, 50, 20)
    ui.czoo_pushButon_02.setGeometry(599, 761 if ui.extend_window else 483, 50, 20)

    ui.czoo_pushButon_01.setText('확대(esc)')
    ui.czoo_pushButon_02.setText('확대(esc)')

    ui.cs_textEditttt_01.setVisible(False)
    ui.cs_textEditttt_02.setVisible(False)
    ui.cs_textEditttt_03.setVisible(True)
    ui.cs_textEditttt_04.setVisible(True)
    ui.cs_textEditttt_05.setVisible(True)
    ui.cs_textEditttt_06.setVisible(False)

    for item in ui.coin_datedt_list:
        item.setVisible(False)
    for item in ui.coin_backte_list:
        item.setVisible(False)
    for item in ui.coin_opcond_list:
        item.setVisible(False)
    for item in ui.coin_detail_list:
        item.setVisible(False)
    for item in ui.coin_baklog_list:
        item.setVisible(False)
    for item in ui.coin_optest_list:
        item.setVisible(False)
    for item in ui.coin_gaopti_list:
        item.setVisible(False)
    for item in ui.coin_rwftvd_list:
        item.setVisible(False)
    for item in ui.coin_esczom_list:
        item.setVisible(True)
    for item in ui.coin_optimz_list:
        item.setVisible(True)
    for item in ui.coin_period_list:
        item.setVisible(True)

    ui.cvc_pushButton_03.setText('최적화 변수범위 로딩(F9)')
    ui.cvc_pushButton_04.setText('최적화 변수범위 저장(F12)')

    ui.image_label1.setVisible(False)
    ui.cvc_labellllll_04.setText(optitext)
    ui.cvc_labellllll_05.setVisible(False)
    ui.cvc_pushButton_21.setVisible(False)
    ui.cvc_pushButton_22.setVisible(False)
    ui.cvc_pushButton_23.setVisible(False)
    ui.cvc_pushButton_24.setVisible(False)
    ui.cvc_pushButton_25.setVisible(False)
    ui.cvc_pushButton_26.setVisible(False)

    ui.cvj_pushButton_11.setFocus()
    cChangeSvjButtonColor(ui)


def cvj_button_clicked_06(ui):
    ui.cs_textEditttt_01.setGeometry(7, 10, 497, 740 if ui.extend_window else 463)
    ui.cs_textEditttt_02.setGeometry(7, 756 if ui.extend_window else 478, 497, 602 if ui.extend_window else 272)
    ui.cs_textEditttt_03.setGeometry(509, 10, 497, 740 if ui.extend_window else 463)
    ui.cs_textEditttt_04.setGeometry(509, 756 if ui.extend_window else 478, 497, 602 if ui.extend_window else 272)

    ui.cvjb_comboBoxx_01.setGeometry(1012, 10, 165, 30)
    ui.cvjb_pushButon_01.setGeometry(1182, 10, 165, 30)
    ui.cvjs_comboBoxx_01.setGeometry(1012, 478, 165, 30)
    ui.cvjs_pushButon_01.setGeometry(1182, 478, 165, 30)

    ui.cvc_comboBoxxx_02.setGeometry(1012, 115, 165, 30)
    ui.cvc_lineEdittt_02.setGeometry(1182, 115, 165, 30)
    ui.cvc_pushButton_03.setGeometry(1012, 150, 165, 30)
    ui.cvc_pushButton_04.setGeometry(1182, 150, 165, 30)

    ui.cs_textEditttt_01.setVisible(True)
    ui.cs_textEditttt_02.setVisible(True)
    ui.cs_textEditttt_03.setVisible(True)
    ui.cs_textEditttt_04.setVisible(True)
    ui.cs_textEditttt_05.setVisible(False)
    ui.cs_textEditttt_06.setVisible(False)

    for item in ui.coin_datedt_list:
        item.setVisible(False)
    for item in ui.coin_backte_list:
        item.setVisible(False)
    for item in ui.coin_opcond_list:
        item.setVisible(False)
    for item in ui.coin_detail_list:
        item.setVisible(False)
    for item in ui.coin_baklog_list:
        item.setVisible(False)
    for item in ui.coin_gaopti_list:
        item.setVisible(False)
    for item in ui.coin_optest_list:
        item.setVisible(False)
    for item in ui.coin_rwftvd_list:
        item.setVisible(False)
    for item in ui.coin_esczom_list:
        item.setVisible(False)
    for item in ui.coin_optimz_list:
        item.setVisible(True)
    for item in ui.coin_period_list:
        item.setVisible(True)

    ui.cvjb_pushButon_01.setText('매수전략 로딩')
    ui.cvjs_pushButon_01.setText('매도전략 로딩')

    ui.cvjb_comboBoxx_01.setVisible(True)
    ui.cvjb_pushButon_01.setVisible(True)
    ui.cvjs_comboBoxx_01.setVisible(True)
    ui.cvjs_pushButon_01.setVisible(True)

    ui.cvc_lineEdittt_04.setVisible(False)
    ui.cvc_pushButton_13.setVisible(False)
    ui.cvc_lineEdittt_05.setVisible(False)
    ui.cvc_pushButton_14.setVisible(False)

    ui.image_label1.setVisible(False)
    ui.cvc_labellllll_04.setText(optitext)
    ui.cvc_labellllll_05.setVisible(False)
    ui.cvc_pushButton_21.setVisible(False)
    ui.cvc_pushButton_22.setVisible(False)
    ui.cvc_pushButton_23.setVisible(False)
    ui.cvc_pushButton_24.setVisible(True)
    ui.cvc_pushButton_25.setVisible(True)
    ui.cvc_pushButton_26.setVisible(True)

    ui.cvj_pushButton_16.setFocus()
    cChangeSvjButtonColor(ui)


def change_pre_button_edit(ui):
    if ui.cvj_pushButton_01.isVisible():
        ui.cvj_pushButton_15.setStyleSheet(style_bc_bd)
    elif ui.cvc_pushButton_32.isVisible():
        ui.cvj_pushButton_09.setStyleSheet(style_bc_bd)
    elif ui.cvc_pushButton_35.isVisible():
        ui.cvj_pushButton_07.setStyleSheet(style_bc_bd)
    elif ui.cva_pushButton_03.isVisible():
        ui.cvj_pushButton_08.setStyleSheet(style_bc_bd)
    elif ui.cvo_pushButton_08.isVisible():
        ui.cvj_pushButton_10.setStyleSheet(style_bc_bd)
    elif ui.cvc_pushButton_23.isVisible():
        ui.cvj_pushButton_12.setStyleSheet(style_bc_bd)
    elif ui.cvc_pushButton_26.isVisible():
        ui.cvj_pushButton_16.setStyleSheet(style_bc_bd)
    elif ui.cvc_pushButton_29.isVisible():
        ui.cvj_pushButton_11.setStyleSheet(style_bc_bd)


def cvj_button_clicked_07(ui):
    change_pre_button_edit(ui)
    ui.cs_textEditttt_01.setVisible(False)
    ui.cs_textEditttt_02.setVisible(False)
    ui.cs_textEditttt_03.setVisible(False)
    ui.cs_textEditttt_04.setVisible(False)
    ui.cs_textEditttt_05.setVisible(False)
    ui.cs_textEditttt_06.setVisible(False)
    ui.cs_textEditttt_07.setVisible(False)
    ui.cs_textEditttt_08.setVisible(False)

    ui.cs_textEditttt_09.setGeometry(7, 10, 1000, 1313 if ui.extend_window else 703)
    ui.cs_progressBar_01.setGeometry(7, 1328 if ui.extend_window else 718, 830, 30)
    ui.cs_pushButtonn_08.setGeometry(842, 1328 if ui.extend_window else 718, 165, 30)

    for item in ui.coin_esczom_list:
        item.setVisible(False)
    for item in ui.coin_detail_list:
        item.setVisible(False)
    for item in ui.coin_baklog_list:
        item.setVisible(True)

    ui.cs_pushButtonn_08.setStyleSheet(style_bc_by)
    ui.cvj_pushButton_13.setFocus()
    ui.cvj_pushButton_13.setStyleSheet(style_bc_dk)
    ui.cvj_pushButton_14.setStyleSheet(style_bc_bs)


def cvj_button_clicked_08(ui):
    change_pre_button_edit(ui)
    ui.cs_textEditttt_01.setVisible(False)
    ui.cs_textEditttt_02.setVisible(False)
    ui.cs_textEditttt_03.setVisible(False)
    ui.cs_textEditttt_04.setVisible(False)
    ui.cs_textEditttt_05.setVisible(False)
    ui.cs_textEditttt_06.setVisible(False)
    ui.cs_textEditttt_07.setVisible(False)
    ui.cs_textEditttt_08.setVisible(False)

    ui.cs_tableWidget_01.setGeometry(7, 40, 1000, 1318 if ui.extend_window else 713)
    if (ui.extend_window and ui.cs_tableWidget_01.rowCount() < 60) or \
            (not ui.extend_window and ui.cs_tableWidget_01.rowCount() < 32):
        ui.cs_tableWidget_01.setRowCount(60 if ui.extend_window else 32)

    for item in ui.coin_esczom_list:
        item.setVisible(False)
    for item in ui.coin_baklog_list:
        item.setVisible(False)
    for item in ui.coin_detail_list:
        item.setVisible(True)

    ui.cvj_pushButton_14.setFocus()
    ui.cvj_pushButton_14.setStyleSheet(style_bc_dk)
    ui.cvj_pushButton_13.setStyleSheet(style_bc_bs)


def cvj_button_clicked_09(ui):
    ui.cs_textEditttt_01.setGeometry(7, 10, 1000, 740 if ui.extend_window else 463)
    ui.cs_textEditttt_02.setGeometry(7, 756 if ui.extend_window else 478, 1000, 602 if ui.extend_window else 272)

    ui.cvjb_comboBoxx_01.setGeometry(1012, 10, 165, 25)
    ui.cvjb_pushButon_01.setGeometry(1012, 40, 165, 30)
    ui.cvjs_comboBoxx_01.setGeometry(1012, 478, 165, 25)
    ui.cvjs_pushButon_01.setGeometry(1012, 508, 165, 30)

    ui.czoo_pushButon_01.setGeometry(952, 15, 50, 20)
    ui.czoo_pushButon_02.setGeometry(952, 761 if ui.extend_window else 483, 50, 20)

    ui.czoo_pushButon_01.setText('확대(esc)')
    ui.czoo_pushButon_02.setText('확대(esc)')

    ui.cs_textEditttt_01.setVisible(True)
    ui.cs_textEditttt_02.setVisible(True)
    ui.cs_textEditttt_03.setVisible(False)
    ui.cs_textEditttt_04.setVisible(False)
    ui.cs_textEditttt_05.setVisible(False)
    ui.cs_textEditttt_06.setVisible(False)

    for item in ui.coin_optimz_list:
        item.setVisible(False)
    for item in ui.coin_period_list:
        item.setVisible(False)
    for item in ui.coin_opcond_list:
        item.setVisible(False)
    for item in ui.coin_detail_list:
        item.setVisible(False)
    for item in ui.coin_baklog_list:
        item.setVisible(False)
    for item in ui.coin_gaopti_list:
        item.setVisible(False)
    for item in ui.coin_optest_list:
        item.setVisible(False)
    for item in ui.coin_rwftvd_list:
        item.setVisible(False)
    for item in ui.coin_datedt_list:
        item.setVisible(True)
    for item in ui.coin_esczom_list:
        item.setVisible(True)
    for item in ui.coin_backte_list:
        item.setVisible(True)

    ui.cvjb_pushButon_01.setText('매수전략 로딩(F1)')
    ui.cvjs_pushButon_01.setText('매도전략 로딩(F5)')

    ui.image_label1.setVisible(False)
    ui.cvc_labellllll_05.setVisible(False)
    ui.cvc_pushButton_21.setVisible(False)
    ui.cvc_pushButton_22.setVisible(False)
    ui.cvc_pushButton_23.setVisible(False)
    ui.cvc_pushButton_24.setVisible(False)
    ui.cvc_pushButton_25.setVisible(False)
    ui.cvc_pushButton_26.setVisible(False)

    ui.cvj_pushButton_15.setFocus()
    cChangeSvjButtonColor(ui)


def cvj_button_clicked_10(ui):
    ui.cs_textEditttt_07.setGeometry(7, 10, 497, 1347 if ui.extend_window else 740)
    ui.cs_textEditttt_08.setGeometry(509, 10, 497, 1347 if ui.extend_window else 740)

    ui.cs_textEditttt_01.setVisible(False)
    ui.cs_textEditttt_02.setVisible(False)
    ui.cs_textEditttt_03.setVisible(False)
    ui.cs_textEditttt_04.setVisible(False)
    ui.cs_textEditttt_05.setVisible(False)
    ui.cs_textEditttt_06.setVisible(False)

    for item in ui.coin_esczom_list:
        item.setVisible(False)
    for item in ui.coin_backte_list:
        item.setVisible(False)
    for item in ui.coin_detail_list:
        item.setVisible(False)
    for item in ui.coin_baklog_list:
        item.setVisible(False)
    for item in ui.coin_gaopti_list:
        item.setVisible(False)
    for item in ui.coin_optest_list:
        item.setVisible(False)
    for item in ui.coin_rwftvd_list:
        item.setVisible(False)
    for item in ui.coin_datedt_list:
        item.setVisible(False)
    for item in ui.coin_optimz_list:
        item.setVisible(True)
    for item in ui.coin_period_list:
        item.setVisible(True)
    for item in ui.coin_opcond_list:
        item.setVisible(True)

    ui.cvc_lineEdittt_04.setVisible(False)
    ui.cvc_lineEdittt_05.setVisible(False)
    ui.cvc_pushButton_13.setVisible(False)
    ui.cvc_pushButton_14.setVisible(False)

    ui.cvc_comboBoxxx_08.setVisible(False)
    ui.cvc_lineEdittt_03.setVisible(False)
    ui.cvc_pushButton_09.setVisible(False)
    ui.cvc_pushButton_10.setVisible(False)

    ui.cvc_comboBoxxx_02.setVisible(False)
    ui.cvc_lineEdittt_02.setVisible(False)
    ui.cvc_pushButton_03.setVisible(False)
    ui.cvc_pushButton_04.setVisible(False)

    ui.image_label1.setVisible(True)
    ui.cvc_labellllll_01.setVisible(False)
    ui.cvc_labellllll_04.setVisible(True)
    ui.cvc_labellllll_05.setVisible(True)
    ui.cvc_labellllll_04.setText(condtext)
    ui.cvc_labellllll_05.setText(cedittxt)
    ui.cvc_pushButton_21.setVisible(False)
    ui.cvc_pushButton_22.setVisible(False)
    ui.cvc_pushButton_23.setVisible(False)
    ui.cvc_pushButton_24.setVisible(False)
    ui.cvc_pushButton_25.setVisible(False)
    ui.cvc_pushButton_26.setVisible(False)

    ui.cvj_pushButton_10.setFocus()
    cChangeSvjButtonColor(ui)


# noinspection PyUnusedLocal
def cvj_button_clicked_11(ui, windowQ, backQ, soundQ, totalQ, liveQ, teleQ):
    pass


# noinspection PyUnusedLocal
def cvj_button_clicked_12(ui, windowQ, backQ, soundQ, totalQ, liveQ):
    pass


def cvj_button_clicked_13(ui):
    if ui.cs_textEditttt_01.isVisible():
        ui.cs_textEditttt_01.clear()
        ui.cs_textEditttt_02.clear()
        ui.cs_textEditttt_01.append(example_finder if ui.dict_set['거래소'] == '업비트' else example_finder_future)


# noinspection PyUnusedLocal
def cvj_button_clicked_14(ui, back_name, windowQ, backQ, soundQ, totalQ, liveQ, teleQ):
    pass


# noinspection PyUnusedLocal
def cvj_button_clicked_15(ui, back_name, windowQ, backQ, soundQ, totalQ, liveQ, teleQ):
    pass


# noinspection PyUnusedLocal
def cvj_button_clicked_16(ui, back_name, windowQ, backQ, soundQ, totalQ, liveQ):
    pass


# noinspection PyUnusedLocal
def cvj_button_clicked_17(ui, back_name, windowQ, backQ, soundQ, totalQ, liveQ):
    pass


def cvj_button_clicked_18(ui):
    opti_vars_text = ui.cs_textEditttt_05.toPlainText()
    if opti_vars_text != '':
        ga_vars_text = ui.GetOptivarsToGavars(opti_vars_text)
        ui.cs_textEditttt_06.clear()
        ui.cs_textEditttt_06.append(ga_vars_text)
    else:
        QMessageBox.critical(ui, '오류 알림', '현재 최적화 범위 코드가 공백 상태입니다.\n최적화 범위 코드를 작성하거나 로딩하십시오.\n')


def cvj_button_clicked_19(ui):
    ga_vars_text = ui.cs_textEditttt_06.toPlainText()
    if ga_vars_text != '':
        opti_vars_text = ui.GetGavarsToOptivars(ga_vars_text)
        ui.cs_textEditttt_05.clear()
        ui.cs_textEditttt_05.append(opti_vars_text)
    else:
        QMessageBox.critical(ui, '오류 알림', '현재 GA 범위 코드가 공백 상태입니다.\nGA 범위 코드를 작성하거나 로딩하십시오.\n')


def cvj_button_clicked_20(ui):
    buystg = ui.cs_textEditttt_01.toPlainText()
    sellstg = ui.cs_textEditttt_02.toPlainText()
    buystg_str, sellstg_str = ui.GetStgtxtToVarstxt(buystg, sellstg)
    ui.cs_textEditttt_03.clear()
    ui.cs_textEditttt_04.clear()
    ui.cs_textEditttt_03.append(buystg_str)
    ui.cs_textEditttt_04.append(sellstg_str)


def cvj_button_clicked_21(ui):
    optivars = ui.cs_textEditttt_05.toPlainText()
    gavars = ui.cs_textEditttt_06.toPlainText()
    optivars_str, gavars_str = ui.GetStgtxtSort2(optivars, gavars)
    ui.cs_textEditttt_05.clear()
    ui.cs_textEditttt_06.clear()
    ui.cs_textEditttt_05.append(optivars_str)
    ui.cs_textEditttt_06.append(gavars_str)


def cvj_button_clicked_22(ui):
    buystg = ui.cs_textEditttt_03.toPlainText()
    sellstg = ui.cs_textEditttt_04.toPlainText()
    buystg_str, sellstg_str = ui.GetStgtxtSort(buystg, sellstg)
    ui.cs_textEditttt_03.clear()
    ui.cs_textEditttt_04.clear()
    ui.cs_textEditttt_03.append(buystg_str)
    ui.cs_textEditttt_04.append(sellstg_str)


# noinspection PyUnusedLocal
def cvj_button_clicked_23(ui, windowQ, backQ, totalQ):
    pass


# noinspection PyUnusedLocal
def cvj_button_clicked_24(ui, windowQ, backQ, soundQ, totalQ, liveQ, teleQ):
    pass


def cvj_button_clicked_25(ui):
    if not ui.dialog_pattern.isVisible():
        ui.dialog_pattern.show()
    else:
        ui.dialog_pattern.close()


def cChangeSvjButtonColor(ui):
    for button in ui.coin_editer_list:
        button.setStyleSheet(style_bc_dk if ui.focusWidget() == button else style_bc_bs)
