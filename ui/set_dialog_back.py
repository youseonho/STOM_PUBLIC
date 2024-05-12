import psutil
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QGroupBox, QLabel
from ui.set_style import style_ck_bx, style_pgbar, style_bc_dk


class SetDialogBack:
    def __init__(self, ui_class, wc):
        self.ui = ui_class
        self.wc = wc
        self.set()

    def set(self):
        self.ui.dialog_backengine = self.wc.setDialog('STOM BACKTEST ENGINE')
        self.ui.dialog_backengine.geometry().center()

        self.ui.be_groupBoxxxxx_01 = QGroupBox('', self.ui.dialog_backengine)
        self.ui.be_labellllllll_04 = QLabel('▣ 백테엔진의 데이터 로딩 시 분류 방법을 선택하십시오. 한종목 백테 시 우측 콤보박스 선택', self.ui.be_groupBoxxxxx_01)
        self.ui.be_comboBoxxxxx_01 = self.wc.setCombobox(self.ui.be_groupBoxxxxx_01, items=['종목코드별 분류', '일자별 분류', '한종목 로딩'])
        self.ui.be_comboBoxxxxx_02 = self.wc.setCombobox(self.ui.be_groupBoxxxxx_01, items=['데이터없음'])
        self.ui.be_labellllllll_01 = QLabel('▣ 백테엔진에 로딩할 데이터의 시작 및 종료 날짜와 시간를 입력하십시오.', self.ui.be_groupBoxxxxx_01)
        if self.ui.dict_set['백테날짜고정']:
            self.ui.be_dateEdittttt_01 = self.wc.setDateEdit(self.ui.be_groupBoxxxxx_01, qday=QDate.fromString(self.ui.dict_set['백테날짜'], 'yyyyMMdd'))
        else:
            self.ui.be_dateEdittttt_01 = self.wc.setDateEdit(self.ui.be_groupBoxxxxx_01, addday=-int(self.ui.dict_set['백테날짜']))
        self.ui.be_dateEdittttt_02 = self.wc.setDateEdit(self.ui.be_groupBoxxxxx_01)
        self.ui.be_lineEdittttt_01 = self.wc.setLineedit(self.ui.be_groupBoxxxxx_01, style=style_bc_dk)
        self.ui.be_lineEdittttt_02 = self.wc.setLineedit(self.ui.be_groupBoxxxxx_01, style=style_bc_dk)
        self.ui.be_labellllllll_02 = QLabel('▣ 사용할 평균값틱수를 콤머로 구분입력하고 백테엔진의 멀티수를 입력하십시오.', self.ui.be_groupBoxxxxx_01)
        self.ui.be_lineEdittttt_03 = self.wc.setLineedit(self.ui.be_groupBoxxxxx_01, ltext='30', style=style_bc_dk)
        self.ui.be_lineEdittttt_04 = self.wc.setLineedit(self.ui.be_groupBoxxxxx_01, ltext=f'{int(psutil.cpu_count() * 1.5)}', style=style_bc_dk)
        text = '▣ 백테엔진을 시작하면 멀티수 만큼 프로세스가 생성되고 지정한 날짜의 데이터를 분할해서\n\n' \
               '   로딩합니다. 데이터를 일정하게 분할하여 백테속도를 향상시키기 위해 다소 시간이\n\n' \
               '   소요될 수 있습니다. 백테엔진은 프로그램을 종료하기 전까지 종료되지 않습니다.'
        self.ui.be_labellllllll_03 = QLabel(text, self.ui.be_groupBoxxxxx_01)
        self.ui.be_pushButtonnn_01 = self.wc.setPushbutton('백테스트 엔진 시작', box=self.ui.be_groupBoxxxxx_01, click=self.ui.beButtonClicked_01)
        self.ui.be_textEditxxxx_01 = self.wc.setTextEdit(self.ui.be_groupBoxxxxx_01, vscroll=True)

        self.ui.dialog_scheduler = self.wc.setDialog('STOM BACKTEST SCHEDULER')
        self.ui.dialog_scheduler.geometry().center()
        self.ui.sd_groupBoxxxxx_01 = QGroupBox('', self.ui.dialog_scheduler)
        self.ui.sd_groupBoxxxxx_02 = QGroupBox('', self.ui.dialog_scheduler)

        self.ui.sd_labellllllll_00 = QLabel('▣ 매수조건수                     매도조건수                    최적화횟수', self.ui.sd_groupBoxxxxx_01)
        self.ui.sd_oclineEdittt_01 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_01, ltext='10', style=style_bc_dk)
        self.ui.sd_oclineEdittt_02 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_01, ltext='5', style=style_bc_dk)
        self.ui.sd_oclineEdittt_03 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_01, ltext='1000', style=style_bc_dk)
        self.ui.sd_scheckBoxxxx_01 = self.wc.setCheckBox('일괄변경', self.ui.sd_groupBoxxxxx_01, checked=True, style=style_ck_bx)
        self.ui.sd_scheckBoxxxx_02 = self.wc.setCheckBox('완료 후 컴퓨터 종료', self.ui.sd_groupBoxxxxx_01, style=style_ck_bx)

        self.ui.sd_dcomboBoxxxx_01 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_01, activated=self.ui.bActivated_03)
        self.ui.sd_dpushButtonn_01 = self.wc.setPushbutton('스케쥴 로딩', box=self.ui.sd_groupBoxxxxx_01, click=self.ui.sdButtonClicked_04)
        self.ui.sd_dlineEditttt_01 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_01, style=style_bc_dk)
        self.ui.sd_dpushButtonn_02 = self.wc.setPushbutton('스케쥴 저장', box=self.ui.sd_groupBoxxxxx_01, click=self.ui.sdButtonClicked_05)

        self.ui.sd_pushButtonnn_01 = self.wc.setPushbutton('주식', box=self.ui.sd_groupBoxxxxx_01, click=self.ui.sdButtonClicked_01)
        self.ui.sd_pushButtonnn_02 = self.wc.setPushbutton('시작', box=self.ui.sd_groupBoxxxxx_01, color=2, click=self.ui.sdButtonClicked_02)
        self.ui.sd_pushButtonnn_03 = self.wc.setPushbutton('중지', box=self.ui.sd_groupBoxxxxx_01, color=2, click=self.ui.sdButtonClicked_03)

        text = '                           백테유형                           시작일자                   ' \
               '종료일자               시작시간      종료시간     배팅    틱수      ' \
               '학습         검증         확인          횟수      최적화기준                  매수                                 ' \
               '매도                                   범위                                         상태'
        self.ui.sd_labellllllll_01 = QLabel(text, self.ui.sd_groupBoxxxxx_02)
        self.ui.sd_checkBoxxxxx_01 = self.wc.setCheckBox('    ', self.ui.sd_groupBoxxxxx_02, changed=self.ui.CheckboxChanged_17, style=style_ck_bx)
        self.ui.sd_checkBoxxxxx_02 = self.wc.setCheckBox('    ', self.ui.sd_groupBoxxxxx_02, changed=self.ui.CheckboxChanged_17, style=style_ck_bx)
        self.ui.sd_checkBoxxxxx_03 = self.wc.setCheckBox('    ', self.ui.sd_groupBoxxxxx_02, changed=self.ui.CheckboxChanged_17, style=style_ck_bx)
        self.ui.sd_checkBoxxxxx_04 = self.wc.setCheckBox('    ', self.ui.sd_groupBoxxxxx_02, changed=self.ui.CheckboxChanged_17, style=style_ck_bx)
        self.ui.sd_checkBoxxxxx_05 = self.wc.setCheckBox('    ', self.ui.sd_groupBoxxxxx_02, changed=self.ui.CheckboxChanged_17, style=style_ck_bx)
        self.ui.sd_checkBoxxxxx_06 = self.wc.setCheckBox('    ', self.ui.sd_groupBoxxxxx_02, changed=self.ui.CheckboxChanged_17, style=style_ck_bx)
        self.ui.sd_checkBoxxxxx_07 = self.wc.setCheckBox('    ', self.ui.sd_groupBoxxxxx_02, changed=self.ui.CheckboxChanged_17, style=style_ck_bx)
        self.ui.sd_checkBoxxxxx_08 = self.wc.setCheckBox('    ', self.ui.sd_groupBoxxxxx_02, changed=self.ui.CheckboxChanged_17, style=style_ck_bx)
        self.ui.sd_checkBoxxxxx_09 = self.wc.setCheckBox('    ', self.ui.sd_groupBoxxxxx_02, changed=self.ui.CheckboxChanged_17, style=style_ck_bx)
        self.ui.sd_checkBoxxxxx_10 = self.wc.setCheckBox('    ', self.ui.sd_groupBoxxxxx_02, changed=self.ui.CheckboxChanged_17, style=style_ck_bx)
        self.ui.sd_checkBoxxxxx_11 = self.wc.setCheckBox('    ', self.ui.sd_groupBoxxxxx_02, changed=self.ui.CheckboxChanged_17, style=style_ck_bx)
        self.ui.sd_checkBoxxxxx_12 = self.wc.setCheckBox('    ', self.ui.sd_groupBoxxxxx_02, changed=self.ui.CheckboxChanged_17, style=style_ck_bx)
        self.ui.sd_checkBoxxxxx_13 = self.wc.setCheckBox('    ', self.ui.sd_groupBoxxxxx_02, changed=self.ui.CheckboxChanged_17, style=style_ck_bx)
        self.ui.sd_checkBoxxxxx_14 = self.wc.setCheckBox('    ', self.ui.sd_groupBoxxxxx_02, changed=self.ui.CheckboxChanged_17, style=style_ck_bx)
        self.ui.sd_checkBoxxxxx_15 = self.wc.setCheckBox('    ', self.ui.sd_groupBoxxxxx_02, changed=self.ui.CheckboxChanged_17, style=style_ck_bx)
        self.ui.sd_checkBoxxxxx_16 = self.wc.setCheckBox('    ', self.ui.sd_groupBoxxxxx_02, changed=self.ui.CheckboxChanged_17, style=style_ck_bx)

        self.ui.list_checkBoxxxxxx = [
            self.ui.sd_checkBoxxxxx_01, self.ui.sd_checkBoxxxxx_02, self.ui.sd_checkBoxxxxx_03, self.ui.sd_checkBoxxxxx_04,
            self.ui.sd_checkBoxxxxx_05, self.ui.sd_checkBoxxxxx_06, self.ui.sd_checkBoxxxxx_07, self.ui.sd_checkBoxxxxx_08,
            self.ui.sd_checkBoxxxxx_09, self.ui.sd_checkBoxxxxx_10, self.ui.sd_checkBoxxxxx_11, self.ui.sd_checkBoxxxxx_12,
            self.ui.sd_checkBoxxxxx_13, self.ui.sd_checkBoxxxxx_14, self.ui.sd_checkBoxxxxx_15, self.ui.sd_checkBoxxxxx_16
        ]

        self.ui.sd_gcomboBoxxxx_01 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_01)
        self.ui.sd_gcomboBoxxxx_02 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_01)
        self.ui.sd_gcomboBoxxxx_03 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_01)
        self.ui.sd_gcomboBoxxxx_04 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_01)
        self.ui.sd_gcomboBoxxxx_05 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_01)
        self.ui.sd_gcomboBoxxxx_06 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_01)
        self.ui.sd_gcomboBoxxxx_07 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_01)
        self.ui.sd_gcomboBoxxxx_08 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_01)
        self.ui.sd_gcomboBoxxxx_09 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_01)
        self.ui.sd_gcomboBoxxxx_10 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_01)
        self.ui.sd_gcomboBoxxxx_11 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_01)
        self.ui.sd_gcomboBoxxxx_12 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_01)
        self.ui.sd_gcomboBoxxxx_13 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_01)
        self.ui.sd_gcomboBoxxxx_14 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_01)
        self.ui.sd_gcomboBoxxxx_15 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_01)
        self.ui.sd_gcomboBoxxxx_16 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_01)

        self.ui.list_gcomboBoxxxxx = [
            self.ui.sd_gcomboBoxxxx_01, self.ui.sd_gcomboBoxxxx_02, self.ui.sd_gcomboBoxxxx_03, self.ui.sd_gcomboBoxxxx_04,
            self.ui.sd_gcomboBoxxxx_05, self.ui.sd_gcomboBoxxxx_06, self.ui.sd_gcomboBoxxxx_07, self.ui.sd_gcomboBoxxxx_08,
            self.ui.sd_gcomboBoxxxx_09, self.ui.sd_gcomboBoxxxx_10, self.ui.sd_gcomboBoxxxx_11, self.ui.sd_gcomboBoxxxx_12,
            self.ui.sd_gcomboBoxxxx_13, self.ui.sd_gcomboBoxxxx_14, self.ui.sd_gcomboBoxxxx_15, self.ui.sd_gcomboBoxxxx_16
        ]

        if self.ui.dict_set['백테날짜고정']:
            self.ui.sd_sdateEditttt_01 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, qday=QDate.fromString(self.ui.dict_set['백테날짜'], 'yyyyMMdd'), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_02 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, qday=QDate.fromString(self.ui.dict_set['백테날짜'], 'yyyyMMdd'), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_03 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, qday=QDate.fromString(self.ui.dict_set['백테날짜'], 'yyyyMMdd'), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_04 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, qday=QDate.fromString(self.ui.dict_set['백테날짜'], 'yyyyMMdd'), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_05 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, qday=QDate.fromString(self.ui.dict_set['백테날짜'], 'yyyyMMdd'), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_06 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, qday=QDate.fromString(self.ui.dict_set['백테날짜'], 'yyyyMMdd'), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_07 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, qday=QDate.fromString(self.ui.dict_set['백테날짜'], 'yyyyMMdd'), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_08 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, qday=QDate.fromString(self.ui.dict_set['백테날짜'], 'yyyyMMdd'), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_09 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, qday=QDate.fromString(self.ui.dict_set['백테날짜'], 'yyyyMMdd'), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_10 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, qday=QDate.fromString(self.ui.dict_set['백테날짜'], 'yyyyMMdd'), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_11 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, qday=QDate.fromString(self.ui.dict_set['백테날짜'], 'yyyyMMdd'), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_12 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, qday=QDate.fromString(self.ui.dict_set['백테날짜'], 'yyyyMMdd'), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_13 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, qday=QDate.fromString(self.ui.dict_set['백테날짜'], 'yyyyMMdd'), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_14 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, qday=QDate.fromString(self.ui.dict_set['백테날짜'], 'yyyyMMdd'), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_15 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, qday=QDate.fromString(self.ui.dict_set['백테날짜'], 'yyyyMMdd'), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_16 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, qday=QDate.fromString(self.ui.dict_set['백테날짜'], 'yyyyMMdd'), changed=self.ui.ChangeBacksDate)
        else:
            self.ui.sd_sdateEditttt_01 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, addday=-int(self.ui.dict_set['백테날짜']), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_02 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, addday=-int(self.ui.dict_set['백테날짜']), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_03 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, addday=-int(self.ui.dict_set['백테날짜']), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_04 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, addday=-int(self.ui.dict_set['백테날짜']), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_05 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, addday=-int(self.ui.dict_set['백테날짜']), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_06 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, addday=-int(self.ui.dict_set['백테날짜']), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_07 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, addday=-int(self.ui.dict_set['백테날짜']), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_08 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, addday=-int(self.ui.dict_set['백테날짜']), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_09 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, addday=-int(self.ui.dict_set['백테날짜']), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_10 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, addday=-int(self.ui.dict_set['백테날짜']), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_11 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, addday=-int(self.ui.dict_set['백테날짜']), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_12 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, addday=-int(self.ui.dict_set['백테날짜']), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_13 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, addday=-int(self.ui.dict_set['백테날짜']), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_14 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, addday=-int(self.ui.dict_set['백테날짜']), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_15 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, addday=-int(self.ui.dict_set['백테날짜']), changed=self.ui.ChangeBacksDate)
            self.ui.sd_sdateEditttt_16 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, addday=-int(self.ui.dict_set['백테날짜']), changed=self.ui.ChangeBacksDate)

        self.ui.list_sdateEdittttt = [
            self.ui.sd_sdateEditttt_01, self.ui.sd_sdateEditttt_02, self.ui.sd_sdateEditttt_03, self.ui.sd_sdateEditttt_04,
            self.ui.sd_sdateEditttt_05, self.ui.sd_sdateEditttt_06, self.ui.sd_sdateEditttt_07, self.ui.sd_sdateEditttt_08,
            self.ui.sd_sdateEditttt_09, self.ui.sd_sdateEditttt_10, self.ui.sd_sdateEditttt_11, self.ui.sd_sdateEditttt_12,
            self.ui.sd_sdateEditttt_13, self.ui.sd_sdateEditttt_14, self.ui.sd_sdateEditttt_15, self.ui.sd_sdateEditttt_16
        ]

        self.ui.sd_edateEditttt_01 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, changed=self.ui.ChangeBackeDate)
        self.ui.sd_edateEditttt_02 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, changed=self.ui.ChangeBackeDate)
        self.ui.sd_edateEditttt_03 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, changed=self.ui.ChangeBackeDate)
        self.ui.sd_edateEditttt_04 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, changed=self.ui.ChangeBackeDate)
        self.ui.sd_edateEditttt_05 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, changed=self.ui.ChangeBackeDate)
        self.ui.sd_edateEditttt_06 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, changed=self.ui.ChangeBackeDate)
        self.ui.sd_edateEditttt_07 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, changed=self.ui.ChangeBackeDate)
        self.ui.sd_edateEditttt_08 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, changed=self.ui.ChangeBackeDate)
        self.ui.sd_edateEditttt_09 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, changed=self.ui.ChangeBackeDate)
        self.ui.sd_edateEditttt_10 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, changed=self.ui.ChangeBackeDate)
        self.ui.sd_edateEditttt_11 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, changed=self.ui.ChangeBackeDate)
        self.ui.sd_edateEditttt_12 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, changed=self.ui.ChangeBackeDate)
        self.ui.sd_edateEditttt_13 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, changed=self.ui.ChangeBackeDate)
        self.ui.sd_edateEditttt_14 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, changed=self.ui.ChangeBackeDate)
        self.ui.sd_edateEditttt_15 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, changed=self.ui.ChangeBackeDate)
        self.ui.sd_edateEditttt_16 = self.wc.setDateEdit(self.ui.sd_groupBoxxxxx_02, changed=self.ui.ChangeBackeDate)

        self.ui.list_edateEdittttt = [
            self.ui.sd_edateEditttt_01, self.ui.sd_edateEditttt_02, self.ui.sd_edateEditttt_03, self.ui.sd_edateEditttt_04,
            self.ui.sd_edateEditttt_05, self.ui.sd_edateEditttt_06, self.ui.sd_edateEditttt_07, self.ui.sd_edateEditttt_08,
            self.ui.sd_edateEditttt_09, self.ui.sd_edateEditttt_10, self.ui.sd_edateEditttt_11, self.ui.sd_edateEditttt_12,
            self.ui.sd_edateEditttt_13, self.ui.sd_edateEditttt_14, self.ui.sd_edateEditttt_15, self.ui.sd_edateEditttt_16
        ]

        self.ui.sd_slineEditttt_01 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='90000', style=style_bc_dk, change=self.ui.TextChanged_01)
        self.ui.sd_slineEditttt_02 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='90000', style=style_bc_dk, change=self.ui.TextChanged_01)
        self.ui.sd_slineEditttt_03 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='90000', style=style_bc_dk, change=self.ui.TextChanged_01)
        self.ui.sd_slineEditttt_04 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='90000', style=style_bc_dk, change=self.ui.TextChanged_01)
        self.ui.sd_slineEditttt_05 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='90000', style=style_bc_dk, change=self.ui.TextChanged_01)
        self.ui.sd_slineEditttt_06 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='90000', style=style_bc_dk, change=self.ui.TextChanged_01)
        self.ui.sd_slineEditttt_07 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='90000', style=style_bc_dk, change=self.ui.TextChanged_01)
        self.ui.sd_slineEditttt_08 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='90000', style=style_bc_dk, change=self.ui.TextChanged_01)
        self.ui.sd_slineEditttt_09 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='90000', style=style_bc_dk, change=self.ui.TextChanged_01)
        self.ui.sd_slineEditttt_10 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='90000', style=style_bc_dk, change=self.ui.TextChanged_01)
        self.ui.sd_slineEditttt_11 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='90000', style=style_bc_dk, change=self.ui.TextChanged_01)
        self.ui.sd_slineEditttt_12 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='90000', style=style_bc_dk, change=self.ui.TextChanged_01)
        self.ui.sd_slineEditttt_13 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='90000', style=style_bc_dk, change=self.ui.TextChanged_01)
        self.ui.sd_slineEditttt_14 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='90000', style=style_bc_dk, change=self.ui.TextChanged_01)
        self.ui.sd_slineEditttt_15 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='90000', style=style_bc_dk, change=self.ui.TextChanged_01)
        self.ui.sd_slineEditttt_16 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='90000', style=style_bc_dk, change=self.ui.TextChanged_01)

        self.ui.list_slineEdittttt = [
            self.ui.sd_slineEditttt_01, self.ui.sd_slineEditttt_02, self.ui.sd_slineEditttt_03, self.ui.sd_slineEditttt_04,
            self.ui.sd_slineEditttt_05, self.ui.sd_slineEditttt_06, self.ui.sd_slineEditttt_07, self.ui.sd_slineEditttt_08,
            self.ui.sd_slineEditttt_09, self.ui.sd_slineEditttt_10, self.ui.sd_slineEditttt_11, self.ui.sd_slineEditttt_12,
            self.ui.sd_slineEditttt_13, self.ui.sd_slineEditttt_14, self.ui.sd_slineEditttt_15, self.ui.sd_slineEditttt_16
        ]

        self.ui.sd_elineEditttt_01 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='93000', style=style_bc_dk, change=self.ui.TextChanged_02)
        self.ui.sd_elineEditttt_02 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='93000', style=style_bc_dk, change=self.ui.TextChanged_02)
        self.ui.sd_elineEditttt_03 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='93000', style=style_bc_dk, change=self.ui.TextChanged_02)
        self.ui.sd_elineEditttt_04 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='93000', style=style_bc_dk, change=self.ui.TextChanged_02)
        self.ui.sd_elineEditttt_05 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='93000', style=style_bc_dk, change=self.ui.TextChanged_02)
        self.ui.sd_elineEditttt_06 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='93000', style=style_bc_dk, change=self.ui.TextChanged_02)
        self.ui.sd_elineEditttt_07 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='93000', style=style_bc_dk, change=self.ui.TextChanged_02)
        self.ui.sd_elineEditttt_08 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='93000', style=style_bc_dk, change=self.ui.TextChanged_02)
        self.ui.sd_elineEditttt_09 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='93000', style=style_bc_dk, change=self.ui.TextChanged_02)
        self.ui.sd_elineEditttt_10 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='93000', style=style_bc_dk, change=self.ui.TextChanged_02)
        self.ui.sd_elineEditttt_11 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='93000', style=style_bc_dk, change=self.ui.TextChanged_02)
        self.ui.sd_elineEditttt_12 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='93000', style=style_bc_dk, change=self.ui.TextChanged_02)
        self.ui.sd_elineEditttt_13 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='93000', style=style_bc_dk, change=self.ui.TextChanged_02)
        self.ui.sd_elineEditttt_14 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='93000', style=style_bc_dk, change=self.ui.TextChanged_02)
        self.ui.sd_elineEditttt_15 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='93000', style=style_bc_dk, change=self.ui.TextChanged_02)
        self.ui.sd_elineEditttt_16 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='93000', style=style_bc_dk, change=self.ui.TextChanged_02)

        self.ui.list_elineEdittttt = [
            self.ui.sd_elineEditttt_01, self.ui.sd_elineEditttt_02, self.ui.sd_elineEditttt_03, self.ui.sd_elineEditttt_04,
            self.ui.sd_elineEditttt_05, self.ui.sd_elineEditttt_06, self.ui.sd_elineEditttt_07, self.ui.sd_elineEditttt_08,
            self.ui.sd_elineEditttt_09, self.ui.sd_elineEditttt_10, self.ui.sd_elineEditttt_11, self.ui.sd_elineEditttt_12,
            self.ui.sd_elineEditttt_13, self.ui.sd_elineEditttt_14, self.ui.sd_elineEditttt_15, self.ui.sd_elineEditttt_16
        ]

        self.ui.sd_blineEditttt_01 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='20', style=style_bc_dk, change=self.ui.TextChanged_03)
        self.ui.sd_blineEditttt_02 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='20', style=style_bc_dk, change=self.ui.TextChanged_03)
        self.ui.sd_blineEditttt_03 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='20', style=style_bc_dk, change=self.ui.TextChanged_03)
        self.ui.sd_blineEditttt_04 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='20', style=style_bc_dk, change=self.ui.TextChanged_03)
        self.ui.sd_blineEditttt_05 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='20', style=style_bc_dk, change=self.ui.TextChanged_03)
        self.ui.sd_blineEditttt_06 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='20', style=style_bc_dk, change=self.ui.TextChanged_03)
        self.ui.sd_blineEditttt_07 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='20', style=style_bc_dk, change=self.ui.TextChanged_03)
        self.ui.sd_blineEditttt_08 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='20', style=style_bc_dk, change=self.ui.TextChanged_03)
        self.ui.sd_blineEditttt_09 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='20', style=style_bc_dk, change=self.ui.TextChanged_03)
        self.ui.sd_blineEditttt_10 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='20', style=style_bc_dk, change=self.ui.TextChanged_03)
        self.ui.sd_blineEditttt_11 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='20', style=style_bc_dk, change=self.ui.TextChanged_03)
        self.ui.sd_blineEditttt_12 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='20', style=style_bc_dk, change=self.ui.TextChanged_03)
        self.ui.sd_blineEditttt_13 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='20', style=style_bc_dk, change=self.ui.TextChanged_03)
        self.ui.sd_blineEditttt_14 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='20', style=style_bc_dk, change=self.ui.TextChanged_03)
        self.ui.sd_blineEditttt_15 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='20', style=style_bc_dk, change=self.ui.TextChanged_03)
        self.ui.sd_blineEditttt_16 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='20', style=style_bc_dk, change=self.ui.TextChanged_03)

        self.ui.list_blineEdittttt = [
            self.ui.sd_blineEditttt_01, self.ui.sd_blineEditttt_02, self.ui.sd_blineEditttt_03, self.ui.sd_blineEditttt_04,
            self.ui.sd_blineEditttt_05, self.ui.sd_blineEditttt_06, self.ui.sd_blineEditttt_07, self.ui.sd_blineEditttt_08,
            self.ui.sd_blineEditttt_09, self.ui.sd_blineEditttt_10, self.ui.sd_blineEditttt_11, self.ui.sd_blineEditttt_12,
            self.ui.sd_blineEditttt_13, self.ui.sd_blineEditttt_14, self.ui.sd_blineEditttt_15, self.ui.sd_blineEditttt_16
        ]

        self.ui.sd_alineEditttt_01 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='30', style=style_bc_dk, change=self.ui.TextChanged_04)
        self.ui.sd_alineEditttt_02 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='30', style=style_bc_dk, change=self.ui.TextChanged_04)
        self.ui.sd_alineEditttt_03 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='30', style=style_bc_dk, change=self.ui.TextChanged_04)
        self.ui.sd_alineEditttt_04 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='30', style=style_bc_dk, change=self.ui.TextChanged_04)
        self.ui.sd_alineEditttt_05 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='30', style=style_bc_dk, change=self.ui.TextChanged_04)
        self.ui.sd_alineEditttt_06 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='30', style=style_bc_dk, change=self.ui.TextChanged_04)
        self.ui.sd_alineEditttt_07 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='30', style=style_bc_dk, change=self.ui.TextChanged_04)
        self.ui.sd_alineEditttt_08 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='30', style=style_bc_dk, change=self.ui.TextChanged_04)
        self.ui.sd_alineEditttt_09 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='30', style=style_bc_dk, change=self.ui.TextChanged_04)
        self.ui.sd_alineEditttt_10 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='30', style=style_bc_dk, change=self.ui.TextChanged_04)
        self.ui.sd_alineEditttt_11 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='30', style=style_bc_dk, change=self.ui.TextChanged_04)
        self.ui.sd_alineEditttt_12 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='30', style=style_bc_dk, change=self.ui.TextChanged_04)
        self.ui.sd_alineEditttt_13 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='30', style=style_bc_dk, change=self.ui.TextChanged_04)
        self.ui.sd_alineEditttt_14 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='30', style=style_bc_dk, change=self.ui.TextChanged_04)
        self.ui.sd_alineEditttt_15 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='30', style=style_bc_dk, change=self.ui.TextChanged_04)
        self.ui.sd_alineEditttt_16 = self.wc.setLineedit(self.ui.sd_groupBoxxxxx_02, ltext='30', style=style_bc_dk, change=self.ui.TextChanged_04)

        self.ui.list_alineEdittttt = [
            self.ui.sd_alineEditttt_01, self.ui.sd_alineEditttt_02, self.ui.sd_alineEditttt_03, self.ui.sd_alineEditttt_04,
            self.ui.sd_alineEditttt_05, self.ui.sd_alineEditttt_06, self.ui.sd_alineEditttt_07, self.ui.sd_alineEditttt_08,
            self.ui.sd_alineEditttt_09, self.ui.sd_alineEditttt_10, self.ui.sd_alineEditttt_11, self.ui.sd_alineEditttt_12,
            self.ui.sd_alineEditttt_13, self.ui.sd_alineEditttt_14, self.ui.sd_alineEditttt_15, self.ui.sd_alineEditttt_16
        ]

        self.ui.sd_p1comboBoxxx_01 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p1comboBoxxx_02 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p1comboBoxxx_03 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p1comboBoxxx_04 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p1comboBoxxx_05 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p1comboBoxxx_06 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p1comboBoxxx_07 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p1comboBoxxx_08 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p1comboBoxxx_09 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p1comboBoxxx_10 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p1comboBoxxx_11 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p1comboBoxxx_12 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p1comboBoxxx_13 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p1comboBoxxx_14 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p1comboBoxxx_15 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p1comboBoxxx_16 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)

        self.ui.list_p1comboBoxxxx = [
            self.ui.sd_p1comboBoxxx_01, self.ui.sd_p1comboBoxxx_02, self.ui.sd_p1comboBoxxx_03, self.ui.sd_p1comboBoxxx_04,
            self.ui.sd_p1comboBoxxx_05, self.ui.sd_p1comboBoxxx_06, self.ui.sd_p1comboBoxxx_07, self.ui.sd_p1comboBoxxx_08,
            self.ui.sd_p1comboBoxxx_09, self.ui.sd_p1comboBoxxx_10, self.ui.sd_p1comboBoxxx_11, self.ui.sd_p1comboBoxxx_12,
            self.ui.sd_p1comboBoxxx_13, self.ui.sd_p1comboBoxxx_14, self.ui.sd_p1comboBoxxx_15, self.ui.sd_p1comboBoxxx_16
        ]

        self.ui.sd_p2comboBoxxx_01 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p2comboBoxxx_02 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p2comboBoxxx_03 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p2comboBoxxx_04 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p2comboBoxxx_05 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p2comboBoxxx_06 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p2comboBoxxx_07 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p2comboBoxxx_08 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p2comboBoxxx_09 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p2comboBoxxx_10 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p2comboBoxxx_11 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p2comboBoxxx_12 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p2comboBoxxx_13 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p2comboBoxxx_14 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p2comboBoxxx_15 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p2comboBoxxx_16 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)

        self.ui.list_p2comboBoxxxx = [
            self.ui.sd_p2comboBoxxx_01, self.ui.sd_p2comboBoxxx_02, self.ui.sd_p2comboBoxxx_03, self.ui.sd_p2comboBoxxx_04,
            self.ui.sd_p2comboBoxxx_05, self.ui.sd_p2comboBoxxx_06, self.ui.sd_p2comboBoxxx_07, self.ui.sd_p2comboBoxxx_08,
            self.ui.sd_p2comboBoxxx_09, self.ui.sd_p2comboBoxxx_10, self.ui.sd_p2comboBoxxx_11, self.ui.sd_p2comboBoxxx_12,
            self.ui.sd_p2comboBoxxx_13, self.ui.sd_p2comboBoxxx_14, self.ui.sd_p2comboBoxxx_15, self.ui.sd_p2comboBoxxx_16
        ]

        self.ui.sd_p3comboBoxxx_01 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p3comboBoxxx_02 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p3comboBoxxx_03 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p3comboBoxxx_04 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p3comboBoxxx_05 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p3comboBoxxx_06 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p3comboBoxxx_07 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p3comboBoxxx_08 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p3comboBoxxx_09 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p3comboBoxxx_10 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p3comboBoxxx_11 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p3comboBoxxx_12 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p3comboBoxxx_13 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p3comboBoxxx_14 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p3comboBoxxx_15 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p3comboBoxxx_16 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)

        self.ui.list_p3comboBoxxxx = [
            self.ui.sd_p3comboBoxxx_01, self.ui.sd_p3comboBoxxx_02, self.ui.sd_p3comboBoxxx_03, self.ui.sd_p3comboBoxxx_04,
            self.ui.sd_p3comboBoxxx_05, self.ui.sd_p3comboBoxxx_06, self.ui.sd_p3comboBoxxx_07, self.ui.sd_p3comboBoxxx_08,
            self.ui.sd_p3comboBoxxx_09, self.ui.sd_p3comboBoxxx_10, self.ui.sd_p3comboBoxxx_11, self.ui.sd_p3comboBoxxx_12,
            self.ui.sd_p3comboBoxxx_13, self.ui.sd_p3comboBoxxx_14, self.ui.sd_p3comboBoxxx_15, self.ui.sd_p3comboBoxxx_16
        ]

        self.ui.sd_p4comboBoxxx_01 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p4comboBoxxx_02 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p4comboBoxxx_03 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p4comboBoxxx_04 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p4comboBoxxx_05 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p4comboBoxxx_06 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p4comboBoxxx_07 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p4comboBoxxx_08 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p4comboBoxxx_09 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p4comboBoxxx_10 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p4comboBoxxx_11 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p4comboBoxxx_12 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p4comboBoxxx_13 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p4comboBoxxx_14 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p4comboBoxxx_15 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_p4comboBoxxx_16 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)

        self.ui.list_p4comboBoxxxx = [
            self.ui.sd_p4comboBoxxx_01, self.ui.sd_p4comboBoxxx_02, self.ui.sd_p4comboBoxxx_03, self.ui.sd_p4comboBoxxx_04,
            self.ui.sd_p4comboBoxxx_05, self.ui.sd_p4comboBoxxx_06, self.ui.sd_p4comboBoxxx_07, self.ui.sd_p4comboBoxxx_08,
            self.ui.sd_p4comboBoxxx_09, self.ui.sd_p4comboBoxxx_10, self.ui.sd_p4comboBoxxx_11, self.ui.sd_p4comboBoxxx_12,
            self.ui.sd_p4comboBoxxx_13, self.ui.sd_p4comboBoxxx_14, self.ui.sd_p4comboBoxxx_15, self.ui.sd_p4comboBoxxx_16
        ]

        self.ui.sd_tcomboBoxxxx_01 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_tcomboBoxxxx_02 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_tcomboBoxxxx_03 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_tcomboBoxxxx_04 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_tcomboBoxxxx_05 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_tcomboBoxxxx_06 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_tcomboBoxxxx_07 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_tcomboBoxxxx_08 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_tcomboBoxxxx_09 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_tcomboBoxxxx_10 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_tcomboBoxxxx_11 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_tcomboBoxxxx_12 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_tcomboBoxxxx_13 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_tcomboBoxxxx_14 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_tcomboBoxxxx_15 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_tcomboBoxxxx_16 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)

        self.ui.list_tcomboBoxxxxx = [
            self.ui.sd_tcomboBoxxxx_01, self.ui.sd_tcomboBoxxxx_02, self.ui.sd_tcomboBoxxxx_03, self.ui.sd_tcomboBoxxxx_04,
            self.ui.sd_tcomboBoxxxx_05, self.ui.sd_tcomboBoxxxx_06, self.ui.sd_tcomboBoxxxx_07, self.ui.sd_tcomboBoxxxx_08,
            self.ui.sd_tcomboBoxxxx_09, self.ui.sd_tcomboBoxxxx_10, self.ui.sd_tcomboBoxxxx_11, self.ui.sd_tcomboBoxxxx_12,
            self.ui.sd_tcomboBoxxxx_13, self.ui.sd_tcomboBoxxxx_14, self.ui.sd_tcomboBoxxxx_15, self.ui.sd_tcomboBoxxxx_16
        ]

        self.ui.sd_bcomboBoxxxx_01 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_bcomboBoxxxx_02 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_bcomboBoxxxx_03 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_bcomboBoxxxx_04 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_bcomboBoxxxx_05 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_bcomboBoxxxx_06 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_bcomboBoxxxx_07 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_bcomboBoxxxx_08 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_bcomboBoxxxx_09 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_bcomboBoxxxx_10 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_bcomboBoxxxx_11 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_bcomboBoxxxx_12 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_bcomboBoxxxx_13 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_bcomboBoxxxx_14 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_bcomboBoxxxx_15 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_bcomboBoxxxx_16 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)

        self.ui.list_bcomboBoxxxxx = [
            self.ui.sd_bcomboBoxxxx_01, self.ui.sd_bcomboBoxxxx_02, self.ui.sd_bcomboBoxxxx_03, self.ui.sd_bcomboBoxxxx_04,
            self.ui.sd_bcomboBoxxxx_05, self.ui.sd_bcomboBoxxxx_06, self.ui.sd_bcomboBoxxxx_07, self.ui.sd_bcomboBoxxxx_08,
            self.ui.sd_bcomboBoxxxx_09, self.ui.sd_bcomboBoxxxx_10, self.ui.sd_bcomboBoxxxx_11, self.ui.sd_bcomboBoxxxx_12,
            self.ui.sd_bcomboBoxxxx_13, self.ui.sd_bcomboBoxxxx_14, self.ui.sd_bcomboBoxxxx_15, self.ui.sd_bcomboBoxxxx_16
        ]

        self.ui.sd_scomboBoxxxx_01 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_scomboBoxxxx_02 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_scomboBoxxxx_03 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_scomboBoxxxx_04 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_scomboBoxxxx_05 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_scomboBoxxxx_06 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_scomboBoxxxx_07 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_scomboBoxxxx_08 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_scomboBoxxxx_09 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_scomboBoxxxx_10 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_scomboBoxxxx_11 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_scomboBoxxxx_12 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_scomboBoxxxx_13 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_scomboBoxxxx_14 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_scomboBoxxxx_15 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_scomboBoxxxx_16 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)

        self.ui.list_scomboBoxxxxx = [
            self.ui.sd_scomboBoxxxx_01, self.ui.sd_scomboBoxxxx_02, self.ui.sd_scomboBoxxxx_03, self.ui.sd_scomboBoxxxx_04,
            self.ui.sd_scomboBoxxxx_05, self.ui.sd_scomboBoxxxx_06, self.ui.sd_scomboBoxxxx_07, self.ui.sd_scomboBoxxxx_08,
            self.ui.sd_scomboBoxxxx_09, self.ui.sd_scomboBoxxxx_10, self.ui.sd_scomboBoxxxx_11, self.ui.sd_scomboBoxxxx_12,
            self.ui.sd_scomboBoxxxx_13, self.ui.sd_scomboBoxxxx_14, self.ui.sd_scomboBoxxxx_15, self.ui.sd_scomboBoxxxx_16
        ]

        self.ui.sd_vcomboBoxxxx_01 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_vcomboBoxxxx_02 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_vcomboBoxxxx_03 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_vcomboBoxxxx_04 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_vcomboBoxxxx_05 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_vcomboBoxxxx_06 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_vcomboBoxxxx_07 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_vcomboBoxxxx_08 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_vcomboBoxxxx_09 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_vcomboBoxxxx_10 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_vcomboBoxxxx_11 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_vcomboBoxxxx_12 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_vcomboBoxxxx_13 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_vcomboBoxxxx_14 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_vcomboBoxxxx_15 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)
        self.ui.sd_vcomboBoxxxx_16 = self.wc.setCombobox(self.ui.sd_groupBoxxxxx_02, activated=self.ui.bActivated_02)

        self.ui.list_vcomboBoxxxxx = [
            self.ui.sd_vcomboBoxxxx_01, self.ui.sd_vcomboBoxxxx_02, self.ui.sd_vcomboBoxxxx_03, self.ui.sd_vcomboBoxxxx_04,
            self.ui.sd_vcomboBoxxxx_05, self.ui.sd_vcomboBoxxxx_06, self.ui.sd_vcomboBoxxxx_07, self.ui.sd_vcomboBoxxxx_08,
            self.ui.sd_vcomboBoxxxx_09, self.ui.sd_vcomboBoxxxx_10, self.ui.sd_vcomboBoxxxx_11, self.ui.sd_vcomboBoxxxx_12,
            self.ui.sd_vcomboBoxxxx_13, self.ui.sd_vcomboBoxxxx_14, self.ui.sd_vcomboBoxxxx_15, self.ui.sd_vcomboBoxxxx_16
        ]

        self.ui.sd_progressBarr_01 = self.wc.setProgressBar(self.ui.sd_groupBoxxxxx_02, style=style_pgbar)
        self.ui.sd_progressBarr_02 = self.wc.setProgressBar(self.ui.sd_groupBoxxxxx_02, style=style_pgbar)
        self.ui.sd_progressBarr_03 = self.wc.setProgressBar(self.ui.sd_groupBoxxxxx_02, style=style_pgbar)
        self.ui.sd_progressBarr_04 = self.wc.setProgressBar(self.ui.sd_groupBoxxxxx_02, style=style_pgbar)
        self.ui.sd_progressBarr_05 = self.wc.setProgressBar(self.ui.sd_groupBoxxxxx_02, style=style_pgbar)
        self.ui.sd_progressBarr_06 = self.wc.setProgressBar(self.ui.sd_groupBoxxxxx_02, style=style_pgbar)
        self.ui.sd_progressBarr_07 = self.wc.setProgressBar(self.ui.sd_groupBoxxxxx_02, style=style_pgbar)
        self.ui.sd_progressBarr_08 = self.wc.setProgressBar(self.ui.sd_groupBoxxxxx_02, style=style_pgbar)
        self.ui.sd_progressBarr_09 = self.wc.setProgressBar(self.ui.sd_groupBoxxxxx_02, style=style_pgbar)
        self.ui.sd_progressBarr_10 = self.wc.setProgressBar(self.ui.sd_groupBoxxxxx_02, style=style_pgbar)
        self.ui.sd_progressBarr_11 = self.wc.setProgressBar(self.ui.sd_groupBoxxxxx_02, style=style_pgbar)
        self.ui.sd_progressBarr_12 = self.wc.setProgressBar(self.ui.sd_groupBoxxxxx_02, style=style_pgbar)
        self.ui.sd_progressBarr_13 = self.wc.setProgressBar(self.ui.sd_groupBoxxxxx_02, style=style_pgbar)
        self.ui.sd_progressBarr_14 = self.wc.setProgressBar(self.ui.sd_groupBoxxxxx_02, style=style_pgbar)
        self.ui.sd_progressBarr_15 = self.wc.setProgressBar(self.ui.sd_groupBoxxxxx_02, style=style_pgbar)
        self.ui.sd_progressBarr_16 = self.wc.setProgressBar(self.ui.sd_groupBoxxxxx_02, style=style_pgbar)

        self.ui.list_progressBarrr = [
            self.ui.sd_progressBarr_01, self.ui.sd_progressBarr_02, self.ui.sd_progressBarr_03, self.ui.sd_progressBarr_04,
            self.ui.sd_progressBarr_05, self.ui.sd_progressBarr_06, self.ui.sd_progressBarr_07, self.ui.sd_progressBarr_08,
            self.ui.sd_progressBarr_09, self.ui.sd_progressBarr_10, self.ui.sd_progressBarr_11, self.ui.sd_progressBarr_12,
            self.ui.sd_progressBarr_13, self.ui.sd_progressBarr_14, self.ui.sd_progressBarr_15, self.ui.sd_progressBarr_16
        ]
        self.ui.dialog_backengine.setFixedSize(480, 600)
        if self.ui.dict_set['창위치기억'] and self.ui.dict_set['창위치'] is not None:
            try:
                self.ui.dialog_backengine.move(self.ui.dict_set['창위치'][18], self.ui.dict_set['창위치'][19])
            except:
                pass
        self.ui.be_groupBoxxxxx_01.setGeometry(5, 5, 470, 590)
        self.ui.be_labellllllll_04.setGeometry(10, 5, 450, 30)
        self.ui.be_comboBoxxxxx_01.setGeometry(15, 40, 220, 30)
        self.ui.be_comboBoxxxxx_02.setGeometry(245, 40, 220, 30)
        self.ui.be_labellllllll_01.setGeometry(10, 70, 450, 30)
        self.ui.be_dateEdittttt_01.setGeometry(10, 105, 220, 30)
        self.ui.be_dateEdittttt_02.setGeometry(240, 105, 220, 30)
        self.ui.be_lineEdittttt_01.setGeometry(10, 140, 220, 30)
        self.ui.be_lineEdittttt_02.setGeometry(240, 140, 220, 30)
        self.ui.be_labellllllll_02.setGeometry(10, 175, 450, 30)
        self.ui.be_lineEdittttt_03.setGeometry(10, 210, 220, 30)
        self.ui.be_lineEdittttt_04.setGeometry(240, 210, 220, 30)
        self.ui.be_labellllllll_03.setGeometry(10, 245, 450, 80)
        self.ui.be_pushButtonnn_01.setGeometry(10, 335, 450, 30)
        self.ui.be_textEditxxxx_01.setGeometry(10, 375, 450, 205)

        self.ui.dialog_scheduler.setFixedSize(1403, 575)
        if self.ui.dict_set['창위치기억'] and self.ui.dict_set['창위치'] is not None:
            try:
                self.ui.dialog_scheduler.move(self.ui.dict_set['창위치'][4], self.ui.dict_set['창위치'][5])
            except:
                pass
        self.ui.sd_groupBoxxxxx_01.setGeometry(5, 5, 1390, 40)
        self.ui.sd_groupBoxxxxx_02.setGeometry(5, 50, 1390, 520)

        self.ui.sd_labellllllll_00.setGeometry(10, 7, 400, 30)
        self.ui.sd_oclineEdittt_01.setGeometry(85, 12, 45, 20)
        self.ui.sd_oclineEdittt_02.setGeometry(205, 12, 45, 20)
        self.ui.sd_oclineEdittt_03.setGeometry(320, 12, 45, 20)
        self.ui.sd_scheckBoxxxx_01.setGeometry(410, 7, 70, 30)
        self.ui.sd_scheckBoxxxx_02.setGeometry(490, 7, 120, 30)

        self.ui.sd_dcomboBoxxxx_01.setGeometry(620, 7, 140, 30)
        self.ui.sd_dpushButtonn_01.setGeometry(770, 7, 80, 30)
        self.ui.sd_dlineEditttt_01.setGeometry(860, 7, 140, 30)
        self.ui.sd_dpushButtonn_02.setGeometry(1010, 7, 80, 30)

        self.ui.sd_pushButtonnn_01.setGeometry(1100, 7, 88, 30)
        self.ui.sd_pushButtonnn_02.setGeometry(1198, 7, 89, 30)
        self.ui.sd_pushButtonnn_03.setGeometry(1297, 7, 89, 30)

        self.ui.sd_labellllllll_01.setGeometry(10, 8, 1380, 30)
        self.ui.sd_checkBoxxxxx_01.setGeometry(10, 40, 40, 25)
        self.ui.sd_checkBoxxxxx_02.setGeometry(10, 70, 40, 25)
        self.ui.sd_checkBoxxxxx_03.setGeometry(10, 100, 40, 25)
        self.ui.sd_checkBoxxxxx_04.setGeometry(10, 130, 40, 25)
        self.ui.sd_checkBoxxxxx_05.setGeometry(10, 160, 40, 25)
        self.ui.sd_checkBoxxxxx_06.setGeometry(10, 190, 40, 25)
        self.ui.sd_checkBoxxxxx_07.setGeometry(10, 220, 40, 25)
        self.ui.sd_checkBoxxxxx_08.setGeometry(10, 250, 40, 25)
        self.ui.sd_checkBoxxxxx_09.setGeometry(10, 280, 40, 25)
        self.ui.sd_checkBoxxxxx_10.setGeometry(10, 310, 40, 25)
        self.ui.sd_checkBoxxxxx_11.setGeometry(10, 340, 40, 25)
        self.ui.sd_checkBoxxxxx_12.setGeometry(10, 370, 40, 25)
        self.ui.sd_checkBoxxxxx_13.setGeometry(10, 400, 40, 25)
        self.ui.sd_checkBoxxxxx_14.setGeometry(10, 430, 40, 25)
        self.ui.sd_checkBoxxxxx_15.setGeometry(10, 460, 40, 25)
        self.ui.sd_checkBoxxxxx_16.setGeometry(10, 490, 40, 25)

        self.ui.sd_gcomboBoxxxx_01.setGeometry(35, 40, 160, 25)
        self.ui.sd_gcomboBoxxxx_02.setGeometry(35, 70, 160, 25)
        self.ui.sd_gcomboBoxxxx_03.setGeometry(35, 100, 160, 25)
        self.ui.sd_gcomboBoxxxx_04.setGeometry(35, 130, 160, 25)
        self.ui.sd_gcomboBoxxxx_05.setGeometry(35, 160, 160, 25)
        self.ui.sd_gcomboBoxxxx_06.setGeometry(35, 190, 160, 25)
        self.ui.sd_gcomboBoxxxx_07.setGeometry(35, 220, 160, 25)
        self.ui.sd_gcomboBoxxxx_08.setGeometry(35, 250, 160, 25)
        self.ui.sd_gcomboBoxxxx_09.setGeometry(35, 280, 160, 25)
        self.ui.sd_gcomboBoxxxx_10.setGeometry(35, 310, 160, 25)
        self.ui.sd_gcomboBoxxxx_11.setGeometry(35, 340, 160, 25)
        self.ui.sd_gcomboBoxxxx_12.setGeometry(35, 370, 160, 25)
        self.ui.sd_gcomboBoxxxx_13.setGeometry(35, 400, 160, 25)
        self.ui.sd_gcomboBoxxxx_14.setGeometry(35, 430, 160, 25)
        self.ui.sd_gcomboBoxxxx_15.setGeometry(35, 460, 160, 25)
        self.ui.sd_gcomboBoxxxx_16.setGeometry(35, 490, 160, 25)

        self.ui.sd_sdateEditttt_01.setGeometry(200, 40, 95, 25)
        self.ui.sd_sdateEditttt_02.setGeometry(200, 70, 95, 25)
        self.ui.sd_sdateEditttt_03.setGeometry(200, 100, 95, 25)
        self.ui.sd_sdateEditttt_04.setGeometry(200, 130, 95, 25)
        self.ui.sd_sdateEditttt_05.setGeometry(200, 160, 95, 25)
        self.ui.sd_sdateEditttt_06.setGeometry(200, 190, 95, 25)
        self.ui.sd_sdateEditttt_07.setGeometry(200, 220, 95, 25)
        self.ui.sd_sdateEditttt_08.setGeometry(200, 250, 95, 25)
        self.ui.sd_sdateEditttt_09.setGeometry(200, 280, 95, 25)
        self.ui.sd_sdateEditttt_10.setGeometry(200, 310, 95, 25)
        self.ui.sd_sdateEditttt_11.setGeometry(200, 340, 95, 25)
        self.ui.sd_sdateEditttt_12.setGeometry(200, 370, 95, 25)
        self.ui.sd_sdateEditttt_13.setGeometry(200, 400, 95, 25)
        self.ui.sd_sdateEditttt_14.setGeometry(200, 430, 95, 25)
        self.ui.sd_sdateEditttt_15.setGeometry(200, 460, 95, 25)
        self.ui.sd_sdateEditttt_16.setGeometry(200, 490, 95, 25)

        self.ui.sd_edateEditttt_01.setGeometry(300, 40, 95, 25)
        self.ui.sd_edateEditttt_02.setGeometry(300, 70, 95, 25)
        self.ui.sd_edateEditttt_03.setGeometry(300, 100, 95, 25)
        self.ui.sd_edateEditttt_04.setGeometry(300, 130, 95, 25)
        self.ui.sd_edateEditttt_05.setGeometry(300, 160, 95, 25)
        self.ui.sd_edateEditttt_06.setGeometry(300, 190, 95, 25)
        self.ui.sd_edateEditttt_07.setGeometry(300, 220, 95, 25)
        self.ui.sd_edateEditttt_08.setGeometry(300, 250, 95, 25)
        self.ui.sd_edateEditttt_09.setGeometry(300, 280, 95, 25)
        self.ui.sd_edateEditttt_10.setGeometry(300, 310, 95, 25)
        self.ui.sd_edateEditttt_11.setGeometry(300, 340, 95, 25)
        self.ui.sd_edateEditttt_12.setGeometry(300, 370, 95, 25)
        self.ui.sd_edateEditttt_13.setGeometry(300, 400, 95, 25)
        self.ui.sd_edateEditttt_14.setGeometry(300, 430, 95, 25)
        self.ui.sd_edateEditttt_15.setGeometry(300, 460, 95, 25)
        self.ui.sd_edateEditttt_16.setGeometry(300, 490, 95, 25)

        self.ui.sd_slineEditttt_01.setGeometry(400, 40, 55, 25)
        self.ui.sd_slineEditttt_02.setGeometry(400, 70, 55, 25)
        self.ui.sd_slineEditttt_03.setGeometry(400, 100, 55, 25)
        self.ui.sd_slineEditttt_04.setGeometry(400, 130, 55, 25)
        self.ui.sd_slineEditttt_05.setGeometry(400, 160, 55, 25)
        self.ui.sd_slineEditttt_06.setGeometry(400, 190, 55, 25)
        self.ui.sd_slineEditttt_07.setGeometry(400, 220, 55, 25)
        self.ui.sd_slineEditttt_08.setGeometry(400, 250, 55, 25)
        self.ui.sd_slineEditttt_09.setGeometry(400, 280, 55, 25)
        self.ui.sd_slineEditttt_10.setGeometry(400, 310, 55, 25)
        self.ui.sd_slineEditttt_11.setGeometry(400, 340, 55, 25)
        self.ui.sd_slineEditttt_12.setGeometry(400, 370, 55, 25)
        self.ui.sd_slineEditttt_13.setGeometry(400, 400, 55, 25)
        self.ui.sd_slineEditttt_14.setGeometry(400, 430, 55, 25)
        self.ui.sd_slineEditttt_15.setGeometry(400, 460, 55, 25)
        self.ui.sd_slineEditttt_16.setGeometry(400, 490, 55, 25)

        self.ui.sd_elineEditttt_01.setGeometry(460, 40, 55, 25)
        self.ui.sd_elineEditttt_02.setGeometry(460, 70, 55, 25)
        self.ui.sd_elineEditttt_03.setGeometry(460, 100, 55, 25)
        self.ui.sd_elineEditttt_04.setGeometry(460, 130, 55, 25)
        self.ui.sd_elineEditttt_05.setGeometry(460, 160, 55, 25)
        self.ui.sd_elineEditttt_06.setGeometry(460, 190, 55, 25)
        self.ui.sd_elineEditttt_07.setGeometry(460, 220, 55, 25)
        self.ui.sd_elineEditttt_08.setGeometry(460, 250, 55, 25)
        self.ui.sd_elineEditttt_09.setGeometry(460, 280, 55, 25)
        self.ui.sd_elineEditttt_10.setGeometry(460, 310, 55, 25)
        self.ui.sd_elineEditttt_11.setGeometry(460, 340, 55, 25)
        self.ui.sd_elineEditttt_12.setGeometry(460, 370, 55, 25)
        self.ui.sd_elineEditttt_13.setGeometry(460, 400, 55, 25)
        self.ui.sd_elineEditttt_14.setGeometry(460, 430, 55, 25)
        self.ui.sd_elineEditttt_15.setGeometry(460, 460, 55, 25)
        self.ui.sd_elineEditttt_16.setGeometry(460, 490, 55, 25)

        self.ui.sd_blineEditttt_01.setGeometry(520, 40, 30, 25)
        self.ui.sd_blineEditttt_02.setGeometry(520, 70, 30, 25)
        self.ui.sd_blineEditttt_03.setGeometry(520, 100, 30, 25)
        self.ui.sd_blineEditttt_04.setGeometry(520, 130, 30, 25)
        self.ui.sd_blineEditttt_05.setGeometry(520, 160, 30, 25)
        self.ui.sd_blineEditttt_06.setGeometry(520, 190, 30, 25)
        self.ui.sd_blineEditttt_07.setGeometry(520, 220, 30, 25)
        self.ui.sd_blineEditttt_08.setGeometry(520, 250, 30, 25)
        self.ui.sd_blineEditttt_09.setGeometry(520, 280, 30, 25)
        self.ui.sd_blineEditttt_10.setGeometry(520, 310, 30, 25)
        self.ui.sd_blineEditttt_11.setGeometry(520, 340, 30, 25)
        self.ui.sd_blineEditttt_12.setGeometry(520, 370, 30, 25)
        self.ui.sd_blineEditttt_13.setGeometry(520, 400, 30, 25)
        self.ui.sd_blineEditttt_14.setGeometry(520, 430, 30, 25)
        self.ui.sd_blineEditttt_15.setGeometry(520, 460, 30, 25)
        self.ui.sd_blineEditttt_16.setGeometry(520, 490, 30, 25)

        self.ui.sd_alineEditttt_01.setGeometry(555, 40, 30, 25)
        self.ui.sd_alineEditttt_02.setGeometry(555, 70, 30, 25)
        self.ui.sd_alineEditttt_03.setGeometry(555, 100, 30, 25)
        self.ui.sd_alineEditttt_04.setGeometry(555, 130, 30, 25)
        self.ui.sd_alineEditttt_05.setGeometry(555, 160, 30, 25)
        self.ui.sd_alineEditttt_06.setGeometry(555, 190, 30, 25)
        self.ui.sd_alineEditttt_07.setGeometry(555, 220, 30, 25)
        self.ui.sd_alineEditttt_08.setGeometry(555, 250, 30, 25)
        self.ui.sd_alineEditttt_09.setGeometry(555, 280, 30, 25)
        self.ui.sd_alineEditttt_10.setGeometry(555, 310, 30, 25)
        self.ui.sd_alineEditttt_11.setGeometry(555, 340, 30, 25)
        self.ui.sd_alineEditttt_12.setGeometry(555, 370, 30, 25)
        self.ui.sd_alineEditttt_13.setGeometry(555, 400, 30, 25)
        self.ui.sd_alineEditttt_14.setGeometry(555, 430, 30, 25)
        self.ui.sd_alineEditttt_15.setGeometry(555, 460, 30, 25)
        self.ui.sd_alineEditttt_16.setGeometry(555, 490, 30, 25)

        self.ui.sd_p1comboBoxxx_01.setGeometry(590, 40, 45, 25)
        self.ui.sd_p1comboBoxxx_02.setGeometry(590, 70, 45, 25)
        self.ui.sd_p1comboBoxxx_03.setGeometry(590, 100, 45, 25)
        self.ui.sd_p1comboBoxxx_04.setGeometry(590, 130, 45, 25)
        self.ui.sd_p1comboBoxxx_05.setGeometry(590, 160, 45, 25)
        self.ui.sd_p1comboBoxxx_06.setGeometry(590, 190, 45, 25)
        self.ui.sd_p1comboBoxxx_07.setGeometry(590, 220, 45, 25)
        self.ui.sd_p1comboBoxxx_08.setGeometry(590, 250, 45, 25)
        self.ui.sd_p1comboBoxxx_09.setGeometry(590, 280, 45, 25)
        self.ui.sd_p1comboBoxxx_10.setGeometry(590, 310, 45, 25)
        self.ui.sd_p1comboBoxxx_11.setGeometry(590, 340, 45, 25)
        self.ui.sd_p1comboBoxxx_12.setGeometry(590, 370, 45, 25)
        self.ui.sd_p1comboBoxxx_13.setGeometry(590, 400, 45, 25)
        self.ui.sd_p1comboBoxxx_14.setGeometry(590, 430, 45, 25)
        self.ui.sd_p1comboBoxxx_15.setGeometry(590, 460, 45, 25)
        self.ui.sd_p1comboBoxxx_16.setGeometry(590, 490, 45, 25)

        self.ui.sd_p2comboBoxxx_01.setGeometry(640, 40, 45, 25)
        self.ui.sd_p2comboBoxxx_02.setGeometry(640, 70, 45, 25)
        self.ui.sd_p2comboBoxxx_03.setGeometry(640, 100, 45, 25)
        self.ui.sd_p2comboBoxxx_04.setGeometry(640, 130, 45, 25)
        self.ui.sd_p2comboBoxxx_05.setGeometry(640, 160, 45, 25)
        self.ui.sd_p2comboBoxxx_06.setGeometry(640, 190, 45, 25)
        self.ui.sd_p2comboBoxxx_07.setGeometry(640, 220, 45, 25)
        self.ui.sd_p2comboBoxxx_08.setGeometry(640, 250, 45, 25)
        self.ui.sd_p2comboBoxxx_09.setGeometry(640, 280, 45, 25)
        self.ui.sd_p2comboBoxxx_10.setGeometry(640, 310, 45, 25)
        self.ui.sd_p2comboBoxxx_11.setGeometry(640, 340, 45, 25)
        self.ui.sd_p2comboBoxxx_12.setGeometry(640, 370, 45, 25)
        self.ui.sd_p2comboBoxxx_13.setGeometry(640, 400, 45, 25)
        self.ui.sd_p2comboBoxxx_14.setGeometry(640, 430, 45, 25)
        self.ui.sd_p2comboBoxxx_15.setGeometry(640, 460, 45, 25)
        self.ui.sd_p2comboBoxxx_16.setGeometry(640, 490, 45, 25)

        self.ui.sd_p3comboBoxxx_01.setGeometry(690, 40, 45, 25)
        self.ui.sd_p3comboBoxxx_02.setGeometry(690, 70, 45, 25)
        self.ui.sd_p3comboBoxxx_03.setGeometry(690, 100, 45, 25)
        self.ui.sd_p3comboBoxxx_04.setGeometry(690, 130, 45, 25)
        self.ui.sd_p3comboBoxxx_05.setGeometry(690, 160, 45, 25)
        self.ui.sd_p3comboBoxxx_06.setGeometry(690, 190, 45, 25)
        self.ui.sd_p3comboBoxxx_07.setGeometry(690, 220, 45, 25)
        self.ui.sd_p3comboBoxxx_08.setGeometry(690, 250, 45, 25)
        self.ui.sd_p3comboBoxxx_09.setGeometry(690, 280, 45, 25)
        self.ui.sd_p3comboBoxxx_10.setGeometry(690, 310, 45, 25)
        self.ui.sd_p3comboBoxxx_11.setGeometry(690, 340, 45, 25)
        self.ui.sd_p3comboBoxxx_12.setGeometry(690, 370, 45, 25)
        self.ui.sd_p3comboBoxxx_13.setGeometry(690, 400, 45, 25)
        self.ui.sd_p3comboBoxxx_14.setGeometry(690, 430, 45, 25)
        self.ui.sd_p3comboBoxxx_15.setGeometry(690, 460, 45, 25)
        self.ui.sd_p3comboBoxxx_16.setGeometry(690, 490, 45, 25)

        self.ui.sd_p4comboBoxxx_01.setGeometry(740, 40, 45, 25)
        self.ui.sd_p4comboBoxxx_02.setGeometry(740, 70, 45, 25)
        self.ui.sd_p4comboBoxxx_03.setGeometry(740, 100, 45, 25)
        self.ui.sd_p4comboBoxxx_04.setGeometry(740, 130, 45, 25)
        self.ui.sd_p4comboBoxxx_05.setGeometry(740, 160, 45, 25)
        self.ui.sd_p4comboBoxxx_06.setGeometry(740, 190, 45, 25)
        self.ui.sd_p4comboBoxxx_07.setGeometry(740, 220, 45, 25)
        self.ui.sd_p4comboBoxxx_08.setGeometry(740, 250, 45, 25)
        self.ui.sd_p4comboBoxxx_09.setGeometry(740, 280, 45, 25)
        self.ui.sd_p4comboBoxxx_10.setGeometry(740, 310, 45, 25)
        self.ui.sd_p4comboBoxxx_11.setGeometry(740, 340, 45, 25)
        self.ui.sd_p4comboBoxxx_12.setGeometry(740, 370, 45, 25)
        self.ui.sd_p4comboBoxxx_13.setGeometry(740, 400, 45, 25)
        self.ui.sd_p4comboBoxxx_14.setGeometry(740, 430, 45, 25)
        self.ui.sd_p4comboBoxxx_15.setGeometry(740, 460, 45, 25)
        self.ui.sd_p4comboBoxxx_16.setGeometry(740, 490, 45, 25)

        self.ui.sd_tcomboBoxxxx_01.setGeometry(790, 40, 55, 25)
        self.ui.sd_tcomboBoxxxx_02.setGeometry(790, 70, 55, 25)
        self.ui.sd_tcomboBoxxxx_03.setGeometry(790, 100, 55, 25)
        self.ui.sd_tcomboBoxxxx_04.setGeometry(790, 130, 55, 25)
        self.ui.sd_tcomboBoxxxx_05.setGeometry(790, 160, 55, 25)
        self.ui.sd_tcomboBoxxxx_06.setGeometry(790, 190, 55, 25)
        self.ui.sd_tcomboBoxxxx_07.setGeometry(790, 220, 55, 25)
        self.ui.sd_tcomboBoxxxx_08.setGeometry(790, 250, 55, 25)
        self.ui.sd_tcomboBoxxxx_09.setGeometry(790, 280, 55, 25)
        self.ui.sd_tcomboBoxxxx_10.setGeometry(790, 310, 55, 25)
        self.ui.sd_tcomboBoxxxx_11.setGeometry(790, 340, 55, 25)
        self.ui.sd_tcomboBoxxxx_12.setGeometry(790, 370, 55, 25)
        self.ui.sd_tcomboBoxxxx_13.setGeometry(790, 400, 55, 25)
        self.ui.sd_tcomboBoxxxx_14.setGeometry(790, 430, 55, 25)
        self.ui.sd_tcomboBoxxxx_15.setGeometry(790, 460, 55, 25)
        self.ui.sd_tcomboBoxxxx_16.setGeometry(790, 490, 55, 25)

        self.ui.sd_bcomboBoxxxx_01.setGeometry(850, 40, 120, 25)
        self.ui.sd_bcomboBoxxxx_02.setGeometry(850, 70, 120, 25)
        self.ui.sd_bcomboBoxxxx_03.setGeometry(850, 100, 120, 25)
        self.ui.sd_bcomboBoxxxx_04.setGeometry(850, 130, 120, 25)
        self.ui.sd_bcomboBoxxxx_05.setGeometry(850, 160, 120, 25)
        self.ui.sd_bcomboBoxxxx_06.setGeometry(850, 190, 120, 25)
        self.ui.sd_bcomboBoxxxx_07.setGeometry(850, 220, 120, 25)
        self.ui.sd_bcomboBoxxxx_08.setGeometry(850, 250, 120, 25)
        self.ui.sd_bcomboBoxxxx_09.setGeometry(850, 280, 120, 25)
        self.ui.sd_bcomboBoxxxx_10.setGeometry(850, 310, 120, 25)
        self.ui.sd_bcomboBoxxxx_11.setGeometry(850, 340, 120, 25)
        self.ui.sd_bcomboBoxxxx_12.setGeometry(850, 370, 120, 25)
        self.ui.sd_bcomboBoxxxx_13.setGeometry(850, 400, 120, 25)
        self.ui.sd_bcomboBoxxxx_14.setGeometry(850, 430, 120, 25)
        self.ui.sd_bcomboBoxxxx_15.setGeometry(850, 460, 120, 25)
        self.ui.sd_bcomboBoxxxx_16.setGeometry(850, 490, 120, 25)

        self.ui.sd_scomboBoxxxx_01.setGeometry(975, 40, 120, 25)
        self.ui.sd_scomboBoxxxx_02.setGeometry(975, 70, 120, 25)
        self.ui.sd_scomboBoxxxx_03.setGeometry(975, 100, 120, 25)
        self.ui.sd_scomboBoxxxx_04.setGeometry(975, 130, 120, 25)
        self.ui.sd_scomboBoxxxx_05.setGeometry(975, 160, 120, 25)
        self.ui.sd_scomboBoxxxx_06.setGeometry(975, 190, 120, 25)
        self.ui.sd_scomboBoxxxx_07.setGeometry(975, 220, 120, 25)
        self.ui.sd_scomboBoxxxx_08.setGeometry(975, 250, 120, 25)
        self.ui.sd_scomboBoxxxx_09.setGeometry(975, 280, 120, 25)
        self.ui.sd_scomboBoxxxx_10.setGeometry(975, 310, 120, 25)
        self.ui.sd_scomboBoxxxx_11.setGeometry(975, 340, 120, 25)
        self.ui.sd_scomboBoxxxx_12.setGeometry(975, 370, 120, 25)
        self.ui.sd_scomboBoxxxx_13.setGeometry(975, 400, 120, 25)
        self.ui.sd_scomboBoxxxx_14.setGeometry(975, 430, 120, 25)
        self.ui.sd_scomboBoxxxx_15.setGeometry(975, 460, 120, 25)
        self.ui.sd_scomboBoxxxx_16.setGeometry(975, 490, 120, 25)

        self.ui.sd_vcomboBoxxxx_01.setGeometry(1100, 40, 120, 25)
        self.ui.sd_vcomboBoxxxx_02.setGeometry(1100, 70, 120, 25)
        self.ui.sd_vcomboBoxxxx_03.setGeometry(1100, 100, 120, 25)
        self.ui.sd_vcomboBoxxxx_04.setGeometry(1100, 130, 120, 25)
        self.ui.sd_vcomboBoxxxx_05.setGeometry(1100, 160, 120, 25)
        self.ui.sd_vcomboBoxxxx_06.setGeometry(1100, 190, 120, 25)
        self.ui.sd_vcomboBoxxxx_07.setGeometry(1100, 220, 120, 25)
        self.ui.sd_vcomboBoxxxx_08.setGeometry(1100, 250, 120, 25)
        self.ui.sd_vcomboBoxxxx_09.setGeometry(1100, 280, 120, 25)
        self.ui.sd_vcomboBoxxxx_10.setGeometry(1100, 310, 120, 25)
        self.ui.sd_vcomboBoxxxx_11.setGeometry(1100, 340, 120, 25)
        self.ui.sd_vcomboBoxxxx_12.setGeometry(1100, 370, 120, 25)
        self.ui.sd_vcomboBoxxxx_13.setGeometry(1100, 400, 120, 25)
        self.ui.sd_vcomboBoxxxx_14.setGeometry(1100, 430, 120, 25)
        self.ui.sd_vcomboBoxxxx_15.setGeometry(1100, 460, 120, 25)
        self.ui.sd_vcomboBoxxxx_16.setGeometry(1100, 490, 120, 25)

        self.ui.sd_progressBarr_01.setGeometry(1225, 40, 160, 25)
        self.ui.sd_progressBarr_02.setGeometry(1225, 70, 160, 25)
        self.ui.sd_progressBarr_03.setGeometry(1225, 100, 160, 25)
        self.ui.sd_progressBarr_04.setGeometry(1225, 130, 160, 25)
        self.ui.sd_progressBarr_05.setGeometry(1225, 160, 160, 25)
        self.ui.sd_progressBarr_06.setGeometry(1225, 190, 160, 25)
        self.ui.sd_progressBarr_07.setGeometry(1225, 220, 160, 25)
        self.ui.sd_progressBarr_08.setGeometry(1225, 250, 160, 25)
        self.ui.sd_progressBarr_09.setGeometry(1225, 280, 160, 25)
        self.ui.sd_progressBarr_10.setGeometry(1225, 310, 160, 25)
        self.ui.sd_progressBarr_11.setGeometry(1225, 340, 160, 25)
        self.ui.sd_progressBarr_12.setGeometry(1225, 370, 160, 25)
        self.ui.sd_progressBarr_13.setGeometry(1225, 400, 160, 25)
        self.ui.sd_progressBarr_14.setGeometry(1225, 430, 160, 25)
        self.ui.sd_progressBarr_15.setGeometry(1225, 460, 160, 25)
        self.ui.sd_progressBarr_16.setGeometry(1225, 490, 160, 25)
