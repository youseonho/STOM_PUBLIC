from PyQt5.QtGui import QFont, QColor
from utility.setting import DICT_SET

qfont12 = QFont()
qfont12.setFamily('나눔고딕')
qfont12.setPixelSize(12)

qfont13 = QFont()
qfont13.setFamily('나눔고딕')
qfont13.setPixelSize(13)

qfont14 = QFont()
qfont14.setFamily('나눔고딕')
qfont14.setPixelSize(14)

# 테마와 상관없이 공통 색깔
color_fg_rt  = QColor(110, 255, 110)
color_cs_hr  = QColor(255, 255, 255)
color_ct_hg  = QColor(255, 255, 0)

color_ma05   = QColor(219, 27, 180)
color_ma10   = QColor(10, 41, 174)
color_ma20   = QColor(239, 174, 0)
color_ma60   = QColor(12, 155, 58)
color_ma120  = QColor(57, 16, 123)
color_ma240  = QColor(80, 80, 85)

color_pluss  = QColor(200, 50, 50)
color_minus  = QColor(50, 50, 200)

style_bc_by  = 'QPushButton{background-color: rgb(150, 100, 100);border-style: solid;border-width: 1px;border-color: rgb(150, 100, 100);} QPushButton:hover{background-color: rgb(170, 120, 120);}'
style_bc_sl  = 'QPushButton{background-color: rgb(100, 100, 150);border-style: solid;border-width: 1px;border-color: rgb(100, 100, 150);} QPushButton:hover{background-color: rgb(120, 120, 170);}'
style_bc_bs  = 'QPushButton{background-color: rgb(80, 130, 80);border-style: solid;border-width: 1px;border-color: rgb(80, 130, 80);} QPushButton:hover{background-color: rgb(100, 150, 100);}'
style_bc_bd  = 'QPushButton{background-color: rgb(30, 80, 30);border-style: solid;border-width: 1px;border-color: rgb(30, 80, 30);} QPushButton:hover{background-color: rgb(50, 100, 50);}'
style_ck_bx  = 'QCheckBox::indicator {width: 15px; height: 15px;}' \
               'QCheckBox::indicator::unchecked {image: url(icon/unchecked.png);}' \
               'QCheckBox::indicator::checked {image: url(icon/checked.png);}'

# 테마 변경시 변경되는 색깔
color_bf_bt = QColor(110, 110, 120)
color_bf_dk = QColor(70, 70, 80)
color_bg_bt = QColor(50, 50, 60)
color_bg_ld = (50, 50, 60, 150)
color_bg_bc = QColor(40, 40, 50)
color_bg_dk = QColor(30, 30, 40)
color_bg_bk = QColor(20, 20, 30)

color_fg_bt = QColor(230, 230, 240)
color_fg_bc = QColor(190, 190, 200)
color_fg_dk = QColor(150, 150, 160)
color_fg_bk = QColor(110, 110, 120)
color_fg_hl = QColor(175, 175, 185)

style_fc_bt = 'QLineEdit{color: rgb(230, 230, 240);}'
style_fc_dk = 'QFrame{color: rgb(150, 150, 160);}'
style_bc_st = 'QPushButton{background-color: rgb(90, 90, 100);border-style: solid;border-width: 1px;border-color: rgb(90, 90, 100);} QPushButton:hover{background-color: rgb(110, 110, 120);}'
style_bc_bt = 'QPushButton{background-color: rgb(70, 70, 80);border-style: solid;border-width: 1px;border-color: rgb(70, 70, 80);} QPushButton:hover{background-color: rgb(90, 90, 100);}'
style_bc_bb = 'QPushButton{background-color: rgb(40, 40, 50);border-style: solid;border-width: 1px;border-color: rgb(40, 40, 50);} QPushButton:hover{background-color: rgb(60, 60, 70);}'
style_bc_dk = 'QPushButton, QTextEdit, QLineEdit, QCheckBox{background-color: rgb(30, 30, 40);border-style: solid;border-width: 1px;border-color: rgb(30, 30, 40);} QPushButton:hover{background-color: rgb(50, 50, 60);}'
style_pgbar = 'QProgressBar{background-color: #20202a;} QProgressBar::chunk {background-color: #5a5a64;}'

if DICT_SET['테마'] == '다크브라운':
    color_bf_bt = QColor(120, 110, 110)
    color_bf_dk = QColor(80, 70, 70)
    color_bg_bt = QColor(60, 50, 50)
    color_bg_ld = (60, 50, 50, 150)
    color_bg_bc = QColor(50, 40, 40)
    color_bg_dk = QColor(40, 30, 30)
    color_bg_bk = QColor(30, 20, 20)

    color_fg_bt = QColor(240, 230, 230)
    color_fg_bc = QColor(200, 190, 190)
    color_fg_dk = QColor(160, 150, 150)
    color_fg_bk = QColor(120, 110, 110)
    color_fg_hl = QColor(185, 175, 175)

    style_fc_bt = 'QLineEdit{color: rgb(240, 230, 230);}'
    style_fc_dk = 'QFrame{color: rgb(160, 150, 150);}'
    style_bc_st = 'QPushButton{background-color: rgb(100, 90, 90);border-style: solid;border-width: 1px;border-color: rgb(100, 90, 90);} QPushButton:hover{background-color: rgb(120, 110, 110);}'
    style_bc_bt = 'QPushButton{background-color: rgb(80, 70, 70);border-style: solid;border-width: 1px;border-color: rgb(80, 70, 70);} QPushButton:hover{background-color: rgb(100, 90, 90);}'
    style_bc_bb = 'QPushButton{background-color: rgb(50, 40, 40);border-style: solid;border-width: 1px;border-color: rgb(50, 40, 40);} QPushButton:hover{background-color: rgb(70, 60, 60);}'
    style_bc_dk = 'QPushButton, QTextEdit, QLineEdit, QCheckBox{background-color: rgb(40, 30, 30);border-style: solid;border-width: 1px;border-color: rgb(40, 30, 30);} QPushButton:hover{background-color: rgb(60, 50, 50);}'
    style_pgbar = 'QProgressBar {background-color: #2a2020;} QProgressBar::chunk {background-color: #645a5a;}'

elif DICT_SET['테마'] == '다크그린':
    color_bf_bt = QColor(110, 120, 110)
    color_bf_dk = QColor(70, 80, 70)
    color_bg_bt = QColor(50, 60, 50)
    color_bg_ld = (50, 60, 50, 150)
    color_bg_bc = QColor(40, 50, 40)
    color_bg_dk = QColor(30, 40, 30)
    color_bg_bk = QColor(20, 30, 20)

    color_fg_bt = QColor(230, 240, 230)
    color_fg_bc = QColor(190, 200, 190)
    color_fg_dk = QColor(150, 160, 150)
    color_fg_bk = QColor(110, 120, 110)
    color_fg_hl = QColor(175, 185, 175)

    style_fc_bt = 'QLineEdit{color: rgb(230, 240, 230);}'
    style_fc_dk = 'QFrame{color: rgb(150, 160, 150);}'
    style_bc_st = 'QPushButton{background-color: rgb(90, 100, 90);border-style: solid;border-width: 1px;border-color: rgb(90, 100, 90);} QPushButton:hover{background-color: rgb(110, 120, 110);}'
    style_bc_bt = 'QPushButton{background-color: rgb(70, 80, 70);border-style: solid;border-width: 1px;border-color: rgb(70, 80, 70);} QPushButton:hover{background-color: rgb(90, 100, 90);}'
    style_bc_bb = 'QPushButton{background-color: rgb(50, 40, 50);border-style: solid;border-width: 1px;border-color: rgb(50, 40, 50);} QPushButton:hover{background-color: rgb(70, 60, 70);}'
    style_bc_dk = 'QPushButton, QTextEdit, QLineEdit, QCheckBox{background-color: rgb(30, 40, 30);border-style: solid;border-width: 1px;border-color: rgb(30, 40, 30);} QPushButton:hover{background-color: rgb(50, 60, 50);}'
    style_pgbar = 'QProgressBar {background-color: #202a20;} QProgressBar::chunk {background-color: #5a645a;}'

elif DICT_SET['테마'] == '다크옐로':
    color_bf_bt = QColor(120, 120, 110)
    color_bf_dk = QColor(80, 80, 70)
    color_bg_bt = QColor(60, 60, 50)
    color_bg_ld = (60, 60, 50, 150)
    color_bg_bc = QColor(50, 50, 40)
    color_bg_dk = QColor(40, 40, 30)
    color_bg_bk = QColor(30, 30, 20)

    color_fg_bt = QColor(240, 240, 230)
    color_fg_bc = QColor(200, 200, 190)
    color_fg_dk = QColor(160, 160, 150)
    color_fg_bk = QColor(120, 120, 110)
    color_fg_hl = QColor(185, 185, 175)

    style_fc_bt = 'QLineEdit{color: rgb(240, 240, 230);}'
    style_fc_dk = 'QFrame{color: rgb(160, 160, 150);}'
    style_bc_st = 'QPushButton{background-color: rgb(100, 100, 90);border-style: solid;border-width: 1px;border-color: rgb(100, 100, 90);} QPushButton:hover{background-color: rgb(120, 120, 110);}'
    style_bc_bt = 'QPushButton{background-color: rgb(80, 80, 70);border-style: solid;border-width: 1px;border-color: rgb(80, 80, 70);} QPushButton:hover{background-color: rgb(100, 100, 90);}'
    style_bc_bb = 'QPushButton{background-color: rgb(50, 50, 40);border-style: solid;border-width: 1px;border-color: rgb(50, 50, 40);} QPushButton:hover{background-color: rgb(70, 70, 60);}'
    style_bc_dk = 'QPushButton, QTextEdit, QLineEdit, QCheckBox{background-color: rgb(40, 40, 30);border-style: solid;border-width: 1px;border-color: rgb(40, 40, 30);} QPushButton:hover{background-color: rgb(60, 60, 50);}'
    style_pgbar = 'QProgressBar {background-color: #2a2a20;} QProgressBar::chunk {background-color: #64645a;}'

elif DICT_SET['테마'] == '다크라임':
    color_bf_bt = QColor(110, 120, 120)
    color_bf_dk = QColor(70, 80, 80)
    color_bg_bt = QColor(50, 60, 60)
    color_bg_ld = (50, 60, 60, 150)
    color_bg_bc = QColor(40, 50, 50)
    color_bg_dk = QColor(30, 40, 40)
    color_bg_bk = QColor(20, 30, 30)

    color_fg_bt = QColor(230, 240, 240)
    color_fg_bc = QColor(190, 200, 200)
    color_fg_dk = QColor(150, 160, 160)
    color_fg_bk = QColor(110, 120, 120)
    color_fg_hl = QColor(175, 185, 185)

    style_fc_bt = 'QLineEdit{color: rgb(230, 240, 240);}'
    style_fc_dk = 'QFrame{color: rgb(150, 160, 160);}'
    style_bc_st = 'QPushButton{background-color: rgb(90, 100, 100);border-style: solid;border-width: 1px;border-color: rgb(90, 100, 100);} QPushButton:hover{background-color: rgb(110, 120, 120);}'
    style_bc_bt = 'QPushButton{background-color: rgb(70, 80, 80);border-style: solid;border-width: 1px;border-color: rgb(70, 80, 80);} QPushButton:hover{background-color: rgb(90, 100, 100);}'
    style_bc_bb = 'QPushButton{background-color: rgb(40, 50, 50);border-style: solid;border-width: 1px;border-color: rgb(40, 50, 50);} QPushButton:hover{background-color: rgb(60, 70, 70);}'
    style_bc_dk = 'QPushButton, QTextEdit, QLineEdit, QCheckBox{background-color: rgb(30, 40, 40);border-style: solid;border-width: 1px;border-color: rgb(30, 40, 40);} QPushButton:hover{background-color: rgb(50, 60, 60);}'
    style_pgbar = 'QProgressBar {background-color: #202a2a;} QProgressBar::chunk {background-color: #5a6464;}'

elif DICT_SET['테마'] == '다크퍼플':
    color_bf_bt = QColor(120, 110, 120)
    color_bf_dk = QColor(80, 70, 80)
    color_bg_bt = QColor(60, 50, 60)
    color_bg_ld = (60, 50, 60, 150)
    color_bg_bc = QColor(50, 40, 50)
    color_bg_dk = QColor(40, 30, 40)
    color_bg_bk = QColor(30, 20, 30)

    color_fg_bt = QColor(240, 230, 240)
    color_fg_bc = QColor(200, 190, 200)
    color_fg_dk = QColor(160, 150, 160)
    color_fg_bk = QColor(120, 110, 120)
    color_fg_hl = QColor(185, 175, 185)

    style_fc_bt = 'QLineEdit{color: rgb(240, 230, 240);}'
    style_fc_dk = 'QFrame{color: rgb(160, 150, 160);}'
    style_bc_st = 'QPushButton{background-color: rgb(100, 90, 100);border-style: solid;border-width: 1px;border-color: rgb(100, 90, 100);} QPushButton:hover{background-color: rgb(120, 110, 120);}'
    style_bc_bt = 'QPushButton{background-color: rgb(80, 70, 80);border-style: solid;border-width: 1px;border-color: rgb(80, 70, 80);} QPushButton:hover{background-color: rgb(100, 90, 100);}'
    style_bc_bb = 'QPushButton{background-color: rgb(50, 40, 50);border-style: solid;border-width: 1px;border-color: rgb(50, 40, 50);} QPushButton:hover{background-color: rgb(70, 60, 70);}'
    style_bc_dk = 'QPushButton, QTextEdit, QLineEdit, QCheckBox{background-color: rgb(40, 30, 40);border-style: solid;border-width: 1px;border-color: rgb(40, 30, 40);} QPushButton:hover{background-color: rgb(60, 50, 60);}'
    style_pgbar = 'QProgressBar {background-color: #2a202a;} QProgressBar::chunk {background-color: #645a64;}'
