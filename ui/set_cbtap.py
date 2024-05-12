from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QLabel
from ui.set_style import qfont12, qfont13, qfont14, style_pgbar, style_bc_dk
from ui.set_text import optistandard, optitext, train_period, valid_period, test_period, optimized_count, opti_standard
from utility.setting import columns_bt


class SetCoinBack:
    def __init__(self, ui_class, wc):
        self.ui = ui_class
        self.wc = wc
        self.set()

    def set(self):
        self.ui.cs_textEditttt_01 = self.wc.setTextEdit(self.ui.cs_tab, filter_=True, font=qfont14)
        self.ui.cs_textEditttt_02 = self.wc.setTextEdit(self.ui.cs_tab, filter_=True, font=qfont14)
        self.ui.cs_textEditttt_03 = self.wc.setTextEdit(self.ui.cs_tab, visible=False, filter_=True, font=qfont14)
        self.ui.cs_textEditttt_04 = self.wc.setTextEdit(self.ui.cs_tab, visible=False, filter_=True, font=qfont14)
        self.ui.cs_textEditttt_05 = self.wc.setTextEdit(self.ui.cs_tab, visible=False, filter_=True, font=qfont14)
        self.ui.cs_textEditttt_06 = self.wc.setTextEdit(self.ui.cs_tab, visible=False, filter_=True, font=qfont14)
        self.ui.cs_textEditttt_07 = self.wc.setTextEdit(self.ui.cs_tab, visible=False, filter_=True, font=qfont14)
        self.ui.cs_textEditttt_08 = self.wc.setTextEdit(self.ui.cs_tab, visible=False, filter_=True, font=qfont14)

    # =================================================================================================================

        self.ui.czoo_pushButon_01 = self.wc.setPushbutton('확대(esc)', box=self.ui.cs_tab, click=self.ui.czooButtonClicked_01)
        self.ui.czoo_pushButon_02 = self.wc.setPushbutton('확대(esc)', box=self.ui.cs_tab, click=self.ui.czooButtonClicked_02)

        self.ui.coin_esczom_list = [self.ui.czoo_pushButon_01, self.ui.czoo_pushButon_02]

    # =================================================================================================================

        self.ui.cs_tableWidget_01 = self.wc.setTablewidget(self.ui.cs_tab, columns_bt, 32, vscroll=True, clicked=self.ui.CellClicked_06)
        self.ui.cs_comboBoxxxx_01 = self.wc.setCombobox(self.ui.cs_tab, font=qfont12, activated=self.ui.Activated_01)
        self.ui.cs_pushButtonn_01 = self.wc.setPushbutton('백테스트상세기록', box=self.ui.cs_tab, click=self.ui.csButtonClicked_01, tip='백테스트 상세기록을 불러온다.')
        self.ui.cs_pushButtonn_02 = self.wc.setPushbutton('그래프', box=self.ui.cs_tab, click=self.ui.csButtonClicked_04, tip='선택된 상세기록의 그래프를 표시한다.')
        self.ui.cs_comboBoxxxx_02 = self.wc.setCombobox(self.ui.cs_tab, font=qfont12, activated=self.ui.Activated_01)
        self.ui.cs_pushButtonn_03 = self.wc.setPushbutton('최적화상세기록', box=self.ui.cs_tab, click=self.ui.csButtonClicked_02, tip='최적화 상세기록을 불러온다.')
        self.ui.cs_pushButtonn_04 = self.wc.setPushbutton('그래프', box=self.ui.cs_tab, click=self.ui.csButtonClicked_04, tip='선택된 상세기록의 그래프를 표시한다.')
        self.ui.cs_comboBoxxxx_03 = self.wc.setCombobox(self.ui.cs_tab, font=qfont12, activated=self.ui.Activated_01)
        self.ui.cs_pushButtonn_05 = self.wc.setPushbutton('분석상세기록', box=self.ui.cs_tab, click=self.ui.csButtonClicked_03, tip='최적화 테스트 및 전진분석 상세기록을 불러온다.')
        self.ui.cs_pushButtonn_06 = self.wc.setPushbutton('그래프', box=self.ui.cs_tab, click=self.ui.csButtonClicked_04, tip='선택된 상세기록의 그래프를 표시한다.')
        self.ui.cs_pushButtonn_07 = self.wc.setPushbutton('비교', box=self.ui.cs_tab, click=self.ui.csButtonClicked_05, tip='두개 이상의 그래프를 선택 비교한다.')

        self.ui.coin_detail_list = [
            self.ui.cs_tableWidget_01, self.ui.cs_comboBoxxxx_01, self.ui.cs_pushButtonn_01, self.ui.cs_pushButtonn_02,
            self.ui.cs_comboBoxxxx_02, self.ui.cs_pushButtonn_03, self.ui.cs_pushButtonn_04, self.ui.cs_comboBoxxxx_03,
            self.ui.cs_pushButtonn_05, self.ui.cs_pushButtonn_06, self.ui.cs_pushButtonn_07
        ]

        for widget in self.ui.coin_detail_list:
            widget.setVisible(False)

    # =================================================================================================================

        self.ui.cs_textEditttt_09 = self.wc.setTextEdit(self.ui.cs_tab, visible=False, vscroll=True)
        self.ui.cs_progressBar_01 = self.wc.setProgressBar(self.ui.cs_tab, style=style_pgbar, visible=False)
        self.ui.cs_pushButtonn_08 = self.wc.setPushbutton('백테스트 중지', box=self.ui.cs_tab, click=self.ui.csButtonClicked_06, color=2, visible=False, tip='(Alt+Enter) 실행중인 백테스트를 중지한다.')

        self.ui.coin_baklog_list = [self.ui.cs_textEditttt_09, self.ui.cs_progressBar_01, self.ui.cs_pushButtonn_08]

    # =================================================================================================================

        self.ui.cvjb_comboBoxx_01 = self.wc.setCombobox(self.ui.cs_tab, font=qfont14, activated=self.ui.cActivated_01)
        self.ui.cvjb_lineEditt_01 = self.wc.setLineedit(self.ui.cs_tab, font=qfont14, aleft=True, ltext='F2, F3', style=style_bc_dk)
        self.ui.cvjb_pushButon_01 = self.wc.setPushbutton('매수전략 로딩(F1)', box=self.ui.cs_tab, click=self.ui.cvjbButtonClicked_01, color=1)
        self.ui.cvjb_pushButon_02 = self.wc.setPushbutton('매수전략 저장(F4)', box=self.ui.cs_tab, click=self.ui.cvjbButtonClicked_02, color=1, tip='작성된 매수전략을 저장한다.\nCtrl 키와 함께 누르면 코드 테스트 과정을 생략한다.')
        self.ui.cvjb_pushButon_03 = self.wc.setPushbutton('매수변수 로딩', box=self.ui.cs_tab, click=self.ui.cvjbButtonClicked_03, color=1, tip='매수전략에 사용할 수 있는 변수목록을 불러온다.')
        self.ui.cvjb_pushButon_04 = self.wc.setPushbutton('매수전략 시작', box=self.ui.cs_tab, click=self.ui.cvjbButtonClicked_04, color=1, tip='작성한 전략을 저장 후 콤보박스에서 선택해야 적용된다.')
        self.ui.cvjb_pushButon_05 = self.wc.setPushbutton('등락율제한', box=self.ui.cs_tab, click=self.ui.cvjbButtonClicked_05)
        self.ui.cvjb_pushButon_06 = self.wc.setPushbutton('고저평균등락율', box=self.ui.cs_tab, click=self.ui.cvjbButtonClicked_06)
        self.ui.cvjb_pushButon_07 = self.wc.setPushbutton('현재가시가비교', box=self.ui.cs_tab, click=self.ui.cvjbButtonClicked_07)
        self.ui.cvjb_pushButon_08 = self.wc.setPushbutton('체결강도하한', box=self.ui.cs_tab, click=self.ui.cvjbButtonClicked_08)
        self.ui.cvjb_pushButon_09 = self.wc.setPushbutton('체결강도평균차이', box=self.ui.cs_tab, click=self.ui.cvjbButtonClicked_09)
        self.ui.cvjb_pushButon_10 = self.wc.setPushbutton('최고체결강도', box=self.ui.cs_tab, click=self.ui.cvjbButtonClicked_10)
        self.ui.cvjb_pushButon_11 = self.wc.setPushbutton('매수시그널', box=self.ui.cs_tab, click=self.ui.cvjbButtonClicked_11, color=3)
        self.ui.cvjb_pushButon_12 = self.wc.setPushbutton('매수전략 중지', box=self.ui.cs_tab, click=self.ui.cvjbButtonClicked_12, color=1, tip='실행중인 매수전략을 중지한다.')

        self.ui.cvj_pushButton_01 = self.wc.setPushbutton('백테스트', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_11, color=2, tip='(Alt+Enter) 기본전략을 백테스팅한다.\nCtrl키와 함께 누르면 백테스트 엔진을 재시작할 수 있습니다.\nCtrl + Alt 키와 함계 누르면 백테 완료 후 변수목록이 포함된 그래프가 저장됩니다.')
        self.ui.cvj_pushButton_02 = self.wc.setPushbutton('백파인더', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_12, color=2, tip='구간등락율을 기준으로 변수를 탐색한다.')
        self.ui.cvj_pushButton_03 = self.wc.setPushbutton('패턴 테스트', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_24, color=2, tip='선택한 전략과 패턴을 테스트한다.\n패턴 학습한 일자 외의 기간을 테스트해야합니다.')
        self.ui.cvj_pushButton_04 = self.wc.setPushbutton('패턴 학습', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_23, color=2, tip='선택한 일자에서 패턴을 학습시킨다.\n패턴 테스트할 일자와 중복되지 않게 일자를 선택해야합니다.')
        self.ui.cvj_pushButton_05 = self.wc.setPushbutton('백파인더 예제', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_13, color=3)
        self.ui.cvj_pushButton_06 = self.wc.setPushbutton('패턴 설정', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_25, color=3)

        self.ui.cvjs_comboBoxx_01 = self.wc.setCombobox(self.ui.cs_tab, font=qfont14, activated=self.ui.cActivated_02)
        self.ui.cvjs_lineEditt_01 = self.wc.setLineedit(self.ui.cs_tab, font=qfont14, aleft=True, ltext='F6, F7', style=style_bc_dk)
        self.ui.cvjs_pushButon_01 = self.wc.setPushbutton('매도전략 로딩(F5)', box=self.ui.cs_tab, click=self.ui.cvjsButtonClicked_01, color=1)
        self.ui.cvjs_pushButon_02 = self.wc.setPushbutton('매도전략 저장(F8)', box=self.ui.cs_tab, click=self.ui.cvjsButtonClicked_02, color=1, tip='작성된 매도전략을 저장한다.\nCtrl 키와 함께 누르면 코드 테스트 과정을 생략한다.')
        self.ui.cvjs_pushButon_03 = self.wc.setPushbutton('매도변수 로딩', box=self.ui.cs_tab, click=self.ui.cvjsButtonClicked_03, color=1, tip='매도전략에 사용할 수 있는 변수목록을 불러온다.')
        self.ui.cvjs_pushButon_04 = self.wc.setPushbutton('매도전략 시작', box=self.ui.cs_tab, click=self.ui.cvjsButtonClicked_04, color=1, tip='작성한 전략을 저장 후 콤보박스에서 선택해야 적용된다.')
        self.ui.cvjs_pushButon_05 = self.wc.setPushbutton('손절라인청산', box=self.ui.cs_tab, click=self.ui.cvjsButtonClicked_05)
        self.ui.cvjs_pushButon_06 = self.wc.setPushbutton('익절라인청산', box=self.ui.cs_tab, click=self.ui.cvjsButtonClicked_06)
        self.ui.cvjs_pushButon_07 = self.wc.setPushbutton('수익율보존청산', box=self.ui.cs_tab, click=self.ui.cvjsButtonClicked_07)
        self.ui.cvjs_pushButon_08 = self.wc.setPushbutton('보유시간기준청산', box=self.ui.cs_tab, click=self.ui.cvjsButtonClicked_08)
        self.ui.cvjs_pushButon_09 = self.wc.setPushbutton('체결강도평균비교', box=self.ui.cs_tab, click=self.ui.cvjsButtonClicked_09)
        self.ui.cvjs_pushButon_10 = self.wc.setPushbutton('최고체결강도비교', box=self.ui.cs_tab, click=self.ui.cvjsButtonClicked_10)
        self.ui.cvjs_pushButon_11 = self.wc.setPushbutton('고저평균등락율', box=self.ui.cs_tab, click=self.ui.cvjsButtonClicked_11)
        self.ui.cvjs_pushButon_12 = self.wc.setPushbutton('호가총잔량비교', box=self.ui.cs_tab, click=self.ui.cvjsButtonClicked_12)
        self.ui.cvjs_pushButon_13 = self.wc.setPushbutton('매도시그널', box=self.ui.cs_tab, click=self.ui.cvjsButtonClicked_13, color=3)
        self.ui.cvjs_pushButon_14 = self.wc.setPushbutton('매도전략 중지', box=self.ui.cs_tab, click=self.ui.cvjsButtonClicked_14, color=1, tip='실행중인 매도전략을 당장 중지한다.')

        self.ui.coin_backte_list = [
            self.ui.cvjb_comboBoxx_01, self.ui.cvjb_lineEditt_01, self.ui.cvjb_pushButon_01, self.ui.cvjb_pushButon_02,
            self.ui.cvjb_pushButon_03, self.ui.cvjb_pushButon_04, self.ui.cvjb_pushButon_05, self.ui.cvjb_pushButon_06,
            self.ui.cvjb_pushButon_07, self.ui.cvjb_pushButon_08, self.ui.cvjb_pushButon_09, self.ui.cvjb_pushButon_10,
            self.ui.cvjb_pushButon_11, self.ui.cvjb_pushButon_12, self.ui.cvj_pushButton_01, self.ui.cvj_pushButton_02,
            self.ui.cvj_pushButton_05, self.ui.cvjs_comboBoxx_01, self.ui.cvjs_lineEditt_01, self.ui.cvjs_pushButon_01,
            self.ui.cvjs_pushButon_02, self.ui.cvjs_pushButon_03, self.ui.cvjs_pushButon_04, self.ui.cvjs_pushButon_05,
            self.ui.cvjs_pushButon_06, self.ui.cvjs_pushButon_07, self.ui.cvjs_pushButon_08, self.ui.cvjs_pushButon_09,
            self.ui.cvjs_pushButon_10, self.ui.cvjs_pushButon_11, self.ui.cvjs_pushButon_12, self.ui.cvjs_pushButon_13,
            self.ui.cvjs_pushButon_14
        ]

    # =================================================================================================================

        self.ui.cvjb_labelllll_01 = QLabel('백테스트 기간설정                                         ~', self.ui.cs_tab)
        self.ui.cvjb_labelllll_02 = QLabel('백테스트 시간설정     시작시간                         종료시간', self.ui.cs_tab)
        self.ui.cvjb_labelllll_03 = QLabel('백테스트 기본설정   배팅(백만)                        평균틱수   self.vars[0]', self.ui.cs_tab)
        if self.ui.dict_set['백테날짜고정']:
            self.ui.cvjb_dateEditt_01 = self.wc.setDateEdit(self.ui.cs_tab, qday=QDate.fromString(self.ui.dict_set['백테날짜'], 'yyyyMMdd'))
        else:
            self.ui.cvjb_dateEditt_01 = self.wc.setDateEdit(self.ui.cs_tab, addday=-int(self.ui.dict_set['백테날짜']))
        self.ui.cvjb_dateEditt_02 = self.wc.setDateEdit(self.ui.cs_tab)
        self.ui.cvjb_lineEditt_02 = self.wc.setLineedit(self.ui.cs_tab, ltext='0', style=style_bc_dk)
        self.ui.cvjb_lineEditt_03 = self.wc.setLineedit(self.ui.cs_tab, ltext='235959', style=style_bc_dk)
        self.ui.cvjb_lineEditt_04 = self.wc.setLineedit(self.ui.cs_tab, ltext='20', style=style_bc_dk)
        self.ui.cvjb_lineEditt_05 = self.wc.setLineedit(self.ui.cs_tab, ltext='30', style=style_bc_dk)

        self.ui.coin_datedt_list = [self.ui.cvjb_labelllll_01, self.ui.cvjb_dateEditt_01, self.ui.cvjb_dateEditt_02, self.ui.cvjb_lineEditt_05]

    # =================================================================================================================

        self.ui.cvj_pushButton_07 = self.wc.setPushbutton('전진분석', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_02, color=4, tip='단축키(Ctrl+4)')
        self.ui.cvj_pushButton_08 = self.wc.setPushbutton('GA 편집기', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_03, color=4, tip='단축키(Ctrl+5)')
        self.ui.cvj_pushButton_09 = self.wc.setPushbutton('테스트 편집기', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_01, color=4, tip='단축키(Ctrl+3)')
        self.ui.cvj_pushButton_10 = self.wc.setPushbutton('조건 편집기', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_10, color=4, tip='단축키(Ctrl+6)')
        self.ui.cvj_pushButton_11 = self.wc.setPushbutton('최적화 편집기', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_05, color=4, tip='단축키(Ctrl+2)')
        self.ui.cvj_pushButton_12 = self.wc.setPushbutton('범위 편집기', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_04, color=4, tip='단축키(Ctrl+7)')
        self.ui.cvj_pushButton_13 = self.wc.setPushbutton('백테스트 로그', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_07, color=4, tip='단축키(Ctrl+9)')
        self.ui.cvj_pushButton_14 = self.wc.setPushbutton('상세기록', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_08, color=4, tip='단축키(Ctrl+0)')
        self.ui.cvj_pushButton_15 = self.wc.setPushbutton('전략 편집기', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_09, color=5, tip='단축키(Ctrl+1)')
        self.ui.cvj_pushButton_16 = self.wc.setPushbutton('변수 편집기', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_06, color=4, tip='단축키(Ctrl+8)')

        self.ui.coin_editer_list = [
            self.ui.cvj_pushButton_07, self.ui.cvj_pushButton_08, self.ui.cvj_pushButton_09, self.ui.cvj_pushButton_10,
            self.ui.cvj_pushButton_11, self.ui.cvj_pushButton_12, self.ui.cvj_pushButton_13, self.ui.cvj_pushButton_14,
            self.ui.cvj_pushButton_15, self.ui.cvj_pushButton_16
        ]

    # =================================================================================================================

        self.ui.cvc_comboBoxxx_01 = self.wc.setCombobox(self.ui.cs_tab, font=qfont14, activated=self.ui.cActivated_03)
        self.ui.cvc_lineEdittt_01 = self.wc.setLineedit(self.ui.cs_tab, font=qfont14, aleft=True, ltext='F2, F3', style=style_bc_dk)
        self.ui.cvc_pushButton_01 = self.wc.setPushbutton('최적화 매수전략 로딩(F1)', box=self.ui.cs_tab, click=self.ui.cvcButtonClicked_01, color=1)
        self.ui.cvc_pushButton_02 = self.wc.setPushbutton('최적화 매수전략 저장(F4)', box=self.ui.cs_tab, click=self.ui.cvcButtonClicked_02, color=1, tip='작성된 최적화 매수전략을 저장한다.\nCtrl 키와 함께 누르면 코드 테스트 과정을 생략한다.')

        self.ui.cvc_comboBoxxx_02 = self.wc.setCombobox(self.ui.cs_tab, font=qfont14, activated=self.ui.cActivated_04)
        self.ui.cvc_lineEdittt_02 = self.wc.setLineedit(self.ui.cs_tab, font=qfont14, aleft=True, ltext='F10, F11', style=style_bc_dk)
        self.ui.cvc_pushButton_03 = self.wc.setPushbutton('최적화 변수범위 로딩(F9)', box=self.ui.cs_tab, click=self.ui.cvcButtonClicked_03, color=1)
        self.ui.cvc_pushButton_04 = self.wc.setPushbutton('최적화 변수범위 저장(F12)', box=self.ui.cs_tab, click=self.ui.cvcButtonClicked_04, color=1, tip='작성된 최적화 변수설정을 저장한다.\nCtrl 키와 함께 누르면 코드 테스트 과정을 생략한다.')

        self.ui.cvc_labellllll_01 = QLabel('▣ 분할은 학습기간, 검증은 검증기간, 테스트는 확인기간까지 선택', self.ui.cs_tab)
        self.ui.cvc_labellllll_02 = QLabel('최적화 학습기간                   검증기간                   확인기간', self.ui.cs_tab)
        self.ui.cvc_comboBoxxx_03 = self.wc.setCombobox(self.ui.cs_tab, items=train_period, tip='최적화 학습기간(주단위)을 선택하십시오.')
        self.ui.cvc_comboBoxxx_04 = self.wc.setCombobox(self.ui.cs_tab, items=valid_period, tip='최적화 검증기간(주단위)을 선택하십시오.')
        self.ui.cvc_comboBoxxx_05 = self.wc.setCombobox(self.ui.cs_tab, items=test_period, tip='최적화 확인기간(주단위)을 선택하십시오.')
        self.ui.cvc_labellllll_03 = QLabel('최적화 실행횟수                   기준값', self.ui.cs_tab)
        self.ui.cvc_comboBoxxx_06 = self.wc.setCombobox(self.ui.cs_tab, items=optimized_count, tip='최적화 횟수를 선택하십시오. 0선택 시 최적값이 변하지 않을 때까지 반복됩니다.')
        self.ui.cvc_comboBoxxx_07 = self.wc.setCombobox(self.ui.cs_tab, items=opti_standard, tip=optistandard)
        self.ui.cvc_pushButton_05 = self.wc.setPushbutton('기준값', color=2, box=self.ui.cs_tab, click=self.ui.cvcButtonClicked_10, tip='백테 결과값 중 특정 수치를 만족하지 못하면\n기준값을 0으로 도출하도록 설정한다.')
        self.ui.cvc_pushButton_36 = self.wc.setPushbutton('optuna', color=3, box=self.ui.cs_tab, click=self.ui.cvcButtonClicked_11, tip='옵튜나의 샘플러를 선택하거나 대시보드를 열람한다')

        self.ui.coin_period_list = [
            self.ui.cvc_labellllll_01, self.ui.cvc_labellllll_02, self.ui.cvc_comboBoxxx_03, self.ui.cvc_comboBoxxx_04,
            self.ui.cvc_comboBoxxx_05, self.ui.cvc_comboBoxxx_06, self.ui.cvc_labellllll_03, self.ui.cvc_comboBoxxx_07,
            self.ui.cvc_pushButton_05, self.ui.cvc_pushButton_36
        ]

        for widget in self.ui.coin_period_list:
            widget.setVisible(False)

    # =================================================================================================================

        self.ui.cvc_pushButton_06 = self.wc.setPushbutton('교차검증', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_14, cmd='최적화OVC', color=2, tip='학습기간과 검증기간을 선택하여 진행되며\n검증 최적화는 1회만 검증을 하지만, 교차검증은\n검증기간을 학습기간 / 검증기간 + 1만큼 교차분류하여 그리드 최적화한다.\nAlt키와 함께 누르면 모든 변수의 최적값을 랜덤 변경하여 시작힌다.\nCtrl+Shift와 함께 누르면 매수변수만 최적화한다.\nCtrl+Alt와 함께 누르면 매도변수만 최적화한다.')
        self.ui.cvc_pushButton_07 = self.wc.setPushbutton('검증', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_14, cmd='최적화OV', color=2, tip='학습기간과 검증기간을 선택하여 진행되며\n데이터의 시계열 순서대로 학습, 검증기간을 분류하여 그리드 최적화한다.\nAlt키와 함께 누르면 모든 변수의 최적값을 랜덤 변경하여 시작힌다.\nCtrl+Shift와 함께 누르면 매수변수만 최적화한다.\nCtrl+Alt와 함께 누르면 매도변수만 최적화한다.')
        self.ui.cvc_pushButton_08 = self.wc.setPushbutton('그리드', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_14, cmd='최적화O', color=2, tip='학습기간만 선택하여 진행되며\n데이터 전체를 기반으로 그리드 최적화한다.\nAlt키와 함께 누르면 모든 변수의 최적값을 랜덤 변경하여 시작힌다.\nCtrl+Shift와 함께 누르면 매수변수만 최적화한다.\nCtrl+Alt와 함께 누르면 매도변수만 최적화한다.')
        self.ui.cvc_pushButton_27 = self.wc.setPushbutton('교차검증', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_14, cmd='최적화BVC', color=3, tip='학습기간과 검증기간을 선택하여 진행되며\n검증 최적화는 1회만 검증을 하지만, 교차검증은\n검증기간을 학습기간 / 검증기간 + 1만큼 교차분류하여 베이지안 최적화한다.\nCtrl+Shift와 함께 누르면 매수변수만 최적화한다.\nCtrl+Alt와 함께 누르면 매도변수만 최적화한다.')
        self.ui.cvc_pushButton_28 = self.wc.setPushbutton('검증', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_14, cmd='최적화BV', color=3, tip='학습기간과 검증기간을 선택하여 진행되며\n데이터의 시계열 순서대로 학습, 검증기간을 분류하여 베이지안 최적화한다.\nCtrl+Shift와 함께 누르면 매수변수만 최적화한다.\nCtrl+Alt와 함께 누르면 매도변수만 최적화한다.')
        self.ui.cvc_pushButton_29 = self.wc.setPushbutton('베이지안', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_14, cmd='최적화B', color=3, tip='학습기간만 선택하여 진행되며\n데이터 전체를 기반으로 베이지안 최적화한다.\nCtrl+Shift와 함께 누르면 매수변수만 최적화한다.\nCtrl+Alt와 함께 누르면 매도변수만 최적화한다.')

    # =================================================================================================================

        self.ui.cvc_comboBoxxx_08 = self.wc.setCombobox(self.ui.cs_tab, font=qfont14, activated=self.ui.cActivated_05)
        self.ui.cvc_lineEdittt_03 = self.wc.setLineedit(self.ui.cs_tab, font=qfont14, aleft=True, ltext='F6, F7', style=style_bc_dk)
        self.ui.cvc_pushButton_09 = self.wc.setPushbutton('최적화 매도전략 로딩(F5)', box=self.ui.cs_tab, click=self.ui.cvcButtonClicked_05, color=1)
        self.ui.cvc_pushButton_10 = self.wc.setPushbutton('최적화 매도전략 저장(F8)', box=self.ui.cs_tab, click=self.ui.cvcButtonClicked_06, color=1, tip='작성된 최적화 매도전략을 저장한다.\nCtrl 키와 함께 누르면 코드 테스트 과정을 생략한다.')
        self.ui.cvc_labellllll_04 = QLabel(optitext, self.ui.cs_tab)
        self.ui.cvc_labellllll_04.setFont(qfont13)
        self.ui.cvc_pushButton_11 = self.wc.setPushbutton('예제', box=self.ui.cs_tab, click=self.ui.cvcButtonClicked_07, color=3)

        self.ui.cvc_lineEdittt_04 = self.wc.setLineedit(self.ui.cs_tab, font=qfont14, aleft=True, visible=False, style=style_bc_dk)
        self.ui.cvc_pushButton_13 = self.wc.setPushbutton('매수전략으로 저장', box=self.ui.cs_tab, click=self.ui.cvcButtonClicked_08, color=1, visible=False, tip='최적값으로 백테용 매수전략으로 저장한다.')
        self.ui.cvc_lineEdittt_05 = self.wc.setLineedit(self.ui.cs_tab, font=qfont14, aleft=True, visible=False, style=style_bc_dk)
        self.ui.cvc_pushButton_14 = self.wc.setPushbutton('매도전략으로 저장', box=self.ui.cs_tab, click=self.ui.cvcButtonClicked_09, color=1, visible=False, tip='최적값으로 백테용 매도전략으로 저장한다.')

        self.ui.coin_optimz_list = [
            self.ui.cvc_comboBoxxx_01, self.ui.cvc_comboBoxxx_02, self.ui.cvc_comboBoxxx_03, self.ui.cvc_comboBoxxx_08,
            self.ui.cvc_lineEdittt_01, self.ui.cvc_lineEdittt_02, self.ui.cvc_lineEdittt_03, self.ui.cvc_labellllll_04,
            self.ui.cvc_pushButton_01, self.ui.cvc_pushButton_02, self.ui.cvc_pushButton_03, self.ui.cvc_pushButton_04,
            self.ui.cvc_pushButton_06, self.ui.cvc_pushButton_07, self.ui.cvc_pushButton_08, self.ui.cvc_pushButton_09,
            self.ui.cvc_pushButton_10, self.ui.cvc_pushButton_11, self.ui.cvc_lineEdittt_04, self.ui.cvc_lineEdittt_05,
            self.ui.cvc_pushButton_13, self.ui.cvc_pushButton_14, self.ui.cvc_pushButton_27, self.ui.cvc_pushButton_28,
            self.ui.cvc_pushButton_29
        ]

        for widget in self.ui.coin_optimz_list:
            widget.setVisible(False)

    # =================================================================================================================

        self.ui.cvc_pushButton_15 = self.wc.setPushbutton('교차검증', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_14, cmd='최적화OVCT', color=2, tip='학습기간, 검증기간, 확인기간을 선택하여 진행되며\n그리드 교차검증 최적화로 구한 최적값을 확인기간에 대하여 테스트한다.\nAlt키와 함께 누르면 모든 변수의 최적값을 랜덤 변경하여 시작힌다.')
        self.ui.cvc_pushButton_16 = self.wc.setPushbutton('검증', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_14, cmd='최적화OVT', color=2, tip='학습기간, 검증기간, 확인기간을 선택하여 진행되며\n그리드 검증 최적화로 구한 최적값을 확인기간에 대하여 테스트한다.\nAlt키와 함께 누르면 모든 변수의 최적값을 랜덤 변경하여 시작힌다.')
        self.ui.cvc_pushButton_17 = self.wc.setPushbutton('그리드', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_14, cmd='최적화OT', color=2, tip='학습기간, 확인기간을 선택하여 진행되며\n그리드 최적화로 구한 최적값을 확인기간에 대하여 테스트한다.\nAlt키와 함께 누르면 모든 변수의 최적값을 랜덤 변경하여 시작힌다.')
        self.ui.cvc_pushButton_30 = self.wc.setPushbutton('교차검증', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_14, cmd='최적화BVCT', color=3, tip='학습기간, 검증기간, 확인기간을 선택하여 진행되며\n베이지안 교차검증 최적화로 구한 최적값을 확인기간에 대하여 테스트한다.')
        self.ui.cvc_pushButton_31 = self.wc.setPushbutton('검증', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_14, cmd='최적화BVT', color=3, tip='학습기간, 검증기간, 확인기간을 선택하여 진행되며\n베이지안 검증 최적화로 구한 최적값을 확인기간에 대하여 테스트한다.')
        self.ui.cvc_pushButton_32 = self.wc.setPushbutton('베이지안', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_14, cmd='최적화BT', color=3, tip='학습기간, 확인기간을 선택하여 진행되며\n베이지안 최적화로 구한 최적값을 확인기간에 대하여 테스트한다.')

        self.ui.coin_optest_list = [
            self.ui.cvc_pushButton_15, self.ui.cvc_pushButton_16, self.ui.cvc_pushButton_17, self.ui.cvc_comboBoxxx_02,
            self.ui.cvc_lineEdittt_02, self.ui.cvc_pushButton_03, self.ui.cvc_pushButton_04, self.ui.cvc_pushButton_30,
            self.ui.cvc_pushButton_31, self.ui.cvc_pushButton_32
        ]

        for widget in self.ui.coin_optest_list:
            widget.setVisible(False)

    # =================================================================================================================

        self.ui.cvc_pushButton_18 = self.wc.setPushbutton('교차검증', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_15, cmd='전진분석ORVC', color=2, tip='학습기간, 확인기간, 전체기간을 선택하여 진행되며\n그리드 교차검증 최적화 테스트를 전진분석한다.\nAlt키와 함께 누르면 모든 변수의 최적값을 랜덤 변경하여 시작힌다.')
        self.ui.cvc_pushButton_19 = self.wc.setPushbutton('검증', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_15, cmd='전진분석ORV', color=2, tip='학습기간, 검증기간, 확인기간, 전체기간을 선택하여 진행되며\n그리드 검증 최적화 테스트를 전진분석한다.\nAlt키와 함께 누르면 모든 변수의 최적값을 랜덤 변경하여 시작힌다.')
        self.ui.cvc_pushButton_20 = self.wc.setPushbutton('그리드', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_15, cmd='전진분석OR', color=2, tip='학습기간, 검증기간, 확인기간, 전체기간을 선택하여 진행되며\n그리드 최적화 테스트를 전진분석한다.\nAlt키와 함께 누르면 모든 변수의 최적값을 랜덤 변경하여 시작힌다.')
        self.ui.cvc_pushButton_33 = self.wc.setPushbutton('교차검증', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_15, cmd='전진분석BRVC', color=3, tip='학습기간, 확인기간, 전체기간을 선택하여 진행되며\n베이지안 교차검증 최적화 테스트를 전진분석한다.')
        self.ui.cvc_pushButton_34 = self.wc.setPushbutton('검증', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_15, cmd='전진분석BRV', color=3, tip='학습기간, 검증기간, 확인기간, 전체기간을 선택하여 진행되며\n베이지안 검증 최적화 테스트를 전진분석한다.')
        self.ui.cvc_pushButton_35 = self.wc.setPushbutton('베이지안', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_15, cmd='전진분석BR', color=3, tip='학습기간, 검증기간, 확인기간, 전체기간을 선택하여 진행되며\n베이지안 최적화 테스트를 전진분석한다.')

        self.ui.coin_rwftvd_list = [
            self.ui.cvc_pushButton_18, self.ui.cvc_pushButton_19, self.ui.cvc_pushButton_20, self.ui.cvc_comboBoxxx_02,
            self.ui.cvc_lineEdittt_02, self.ui.cvc_pushButton_03, self.ui.cvc_pushButton_04, self.ui.cvjb_labelllll_01,
            self.ui.cvjb_dateEditt_01, self.ui.cvjb_dateEditt_02, self.ui.cvc_pushButton_33, self.ui.cvc_pushButton_34,
            self.ui.cvc_pushButton_35
        ]

        for widget in self.ui.coin_rwftvd_list:
            if widget not in (self.ui.cvjb_labelllll_01, self.ui.cvjb_dateEditt_01, self.ui.cvjb_dateEditt_02):
                widget.setVisible(False)

    # =================================================================================================================

        self.ui.cva_pushButton_01 = self.wc.setPushbutton('교차검증 GA 최적화', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_16, cmd='최적화OGVC', color=2, tip='학습기간과 검증기간을 선택하여 진행되며\n교차 검증 GA최적화한다.')
        self.ui.cva_pushButton_02 = self.wc.setPushbutton('검증 GA 최적화', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_16, cmd='최적화OGV', color=2, tip='학습기간과 검증기간을 선택하여 진행되며\n검증 GA최적화한다.')
        self.ui.cva_pushButton_03 = self.wc.setPushbutton('GA 최적화', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_16, cmd='최적화OG', color=2, tip='학습기간을 선택하여 진행되며\n데이터 전체를 사용하여 GA최적화한다.')

        self.ui.cva_comboBoxxx_01 = self.wc.setCombobox(self.ui.cs_tab, font=qfont14, activated=self.ui.cActivated_06)
        self.ui.cva_lineEdittt_01 = self.wc.setLineedit(self.ui.cs_tab, font=qfont14, aleft=True, ltext='F10, F11', style=style_bc_dk)
        self.ui.cva_pushButton_04 = self.wc.setPushbutton('GA 변수범위 로딩(F9)', box=self.ui.cs_tab, click=self.ui.cvaButtonClicked_01, color=1)
        self.ui.cva_pushButton_05 = self.wc.setPushbutton('GA 변수범위 저장(F12)', box=self.ui.cs_tab, click=self.ui.cvaButtonClicked_02, color=1, tip='작성된 변수범위를 저장한다.\nCtrl 키와 함께 누르면 코드 테스트 과정을 생략한다.')

        self.ui.coin_gaopti_list = [
            self.ui.cva_pushButton_01, self.ui.cva_pushButton_02, self.ui.cva_pushButton_03, self.ui.cva_comboBoxxx_01,
            self.ui.cva_lineEdittt_01, self.ui.cva_pushButton_04, self.ui.cva_pushButton_05, self.ui.cvc_labellllll_04
        ]

        for widget in self.ui.coin_gaopti_list:
            widget.setVisible(False)

    # =================================================================================================================

        self.ui.cvc_pushButton_21 = self.wc.setPushbutton('최적화 > GA 범위 변환', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_18, color=2, visible=False, tip='최적화용 범위코드를 GA용으로 변환한다.')
        self.ui.cvc_pushButton_22 = self.wc.setPushbutton('GA > 최적화 범위 변환', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_19, color=2, visible=False, tip='GA용 범위코드를 최적화용으로 변환한다.')
        self.ui.cvc_pushButton_23 = self.wc.setPushbutton('변수 키값 재정렬', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_21, color=2, visible=False, tip='범위 변수 self.vars의 키값을 재정렬한다.')

    # =================================================================================================================

        self.ui.cvc_pushButton_24 = self.wc.setPushbutton('최적화 변수 변환(매수우선)', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_20, color=2, visible=False, tip='일반 전략의 각종 변수를 매수우선 최적화용 변수로 변환한다.')
        self.ui.cvc_pushButton_25 = self.wc.setPushbutton('최적화 변수 변환(매도우선)', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_20, color=2, visible=False, tip='일반 전략의 각종 변수를 매도우선 최적화용 변수로 변환한다.')
        self.ui.cvc_pushButton_26 = self.wc.setPushbutton('변수 키값 재정렬', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_22, color=2, visible=False, tip='변수 self.vars의 키값을 재정렬한다.\n매수, 매도 self.vars의 첫번째 키값을 비교해서\n매수가 빠르면 매수우선, 매도가 빠르면 매도우선으로 재정렬된다.')
        self.ui.cvc_labellllll_05 = QLabel('', self.ui.cs_tab)
        self.ui.cvc_labellllll_05.setVisible(False)

    # =================================================================================================================

        self.ui.cvo_comboBoxxx_01 = self.wc.setCombobox(self.ui.cs_tab, font=qfont14, activated=self.ui.cActivated_07)
        self.ui.cvo_lineEdittt_01 = self.wc.setLineedit(self.ui.cs_tab, font=qfont14, aleft=True, ltext='F2, F3', style=style_bc_dk)
        self.ui.cvo_pushButton_01 = self.wc.setPushbutton('매수조건 로딩(F1)', box=self.ui.cs_tab, click=self.ui.cvoButtonClicked_01, color=1)
        self.ui.cvo_pushButton_02 = self.wc.setPushbutton('매수조건 저장(F4)', box=self.ui.cs_tab, click=self.ui.cvoButtonClicked_02, color=1, tip='작성된 매수조건을 저장한다.\nCtrl 키와 함께 누르면 코드 테스트 과정을 생략한다.')
        self.ui.cvo_comboBoxxx_02 = self.wc.setCombobox(self.ui.cs_tab, font=qfont14, activated=self.ui.cActivated_08)
        self.ui.cvo_lineEdittt_02 = self.wc.setLineedit(self.ui.cs_tab, font=qfont14, aleft=True, ltext='F6, F7', style=style_bc_dk)
        self.ui.cvo_pushButton_03 = self.wc.setPushbutton('매도조건 로딩(F5)', box=self.ui.cs_tab, click=self.ui.cvoButtonClicked_03, color=1)
        self.ui.cvo_pushButton_04 = self.wc.setPushbutton('매도조건 저장(F8)', box=self.ui.cs_tab, click=self.ui.cvoButtonClicked_04, color=1, tip='작성된 매도조건을 저장한다.\nCtrl 키와 함께 누르면 코드 테스트 과정을 생략한다.')

        self.ui.cvo_labellllll_04 = QLabel('매수조건수                     매도조건수                    최적화횟수', self.ui.cs_tab)
        self.ui.cvo_lineEdittt_03 = self.wc.setLineedit(self.ui.cs_tab, ltext='10', style=style_bc_dk)
        self.ui.cvo_lineEdittt_04 = self.wc.setLineedit(self.ui.cs_tab, ltext='5', style=style_bc_dk)
        self.ui.cvo_lineEdittt_05 = self.wc.setLineedit(self.ui.cs_tab, ltext='1000', style=style_bc_dk)

        self.ui.cvo_pushButton_05 = self.wc.setPushbutton('교차검증 조건 최적화', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_17, cmd='최적화OCVC', color=2, tip='학습기간과 검증기간을 선택하여 진행되며\n교차 검증 조건최적화한다.')
        self.ui.cvo_pushButton_06 = self.wc.setPushbutton('검증 조건 최적화', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_17, cmd='최적화OCV', color=2, tip='학습기간과 검증기간을 선택하여 진행되며\n검증 조건최적화한다.')
        self.ui.cvo_pushButton_07 = self.wc.setPushbutton('조건 최적화', box=self.ui.cs_tab, click=self.ui.cvjButtonClicked_17, cmd='최적화OC', color=2, tip='학습기간을 선택하여 진행되며\n데이터 전체를 사용하여 조건최적화한다.')

        self.ui.cvo_pushButton_08 = self.wc.setPushbutton('예제', box=self.ui.cs_tab, click=self.ui.cvcButtonClicked_07, color=3)

        self.ui.coin_opcond_list = [
            self.ui.cs_textEditttt_07, self.ui.cs_textEditttt_08, self.ui.cvo_comboBoxxx_01, self.ui.cvo_lineEdittt_01,
            self.ui.cvo_pushButton_01, self.ui.cvo_pushButton_02, self.ui.cvo_comboBoxxx_02, self.ui.cvo_lineEdittt_02,
            self.ui.cvo_pushButton_03, self.ui.cvo_pushButton_04, self.ui.cvo_pushButton_05, self.ui.cvo_pushButton_06,
            self.ui.cvo_pushButton_07, self.ui.cvo_labellllll_04, self.ui.cvo_lineEdittt_03, self.ui.cvo_lineEdittt_04,
            self.ui.cvo_lineEdittt_05, self.ui.cvo_pushButton_08, self.ui.cvc_labellllll_04
        ]

        for widget in self.ui.coin_opcond_list:
            widget.setVisible(False)

    # =================================================================================================================

        self.ui.cs_textEditttt_01.setGeometry(7, 10, 1000, 463)
        self.ui.cs_textEditttt_02.setGeometry(7, 480, 1000, 272)
        self.ui.cs_textEditttt_03.setGeometry(509, 10, 497, 463)
        self.ui.cs_textEditttt_04.setGeometry(509, 480, 497, 272)
        self.ui.cs_textEditttt_05.setGeometry(659, 10, 347, 740)
        self.ui.cs_textEditttt_06.setGeometry(659, 10, 347, 740)
        self.ui.cs_textEditttt_07.setGeometry(7, 10, 497, 740)
        self.ui.cs_textEditttt_08.setGeometry(509, 10, 497, 740)

        self.ui.czoo_pushButon_01.setGeometry(952, 15, 50, 20)
        self.ui.czoo_pushButon_02.setGeometry(952, 483, 50, 20)

        self.ui.cs_tableWidget_01.setGeometry(7, 40, 1000, 713)
        self.ui.cs_comboBoxxxx_01.setGeometry(7, 10, 150, 25)
        self.ui.cs_pushButtonn_01.setGeometry(162, 10, 100, 25)
        self.ui.cs_pushButtonn_02.setGeometry(267, 10, 55, 25)
        self.ui.cs_comboBoxxxx_02.setGeometry(327, 10, 150, 25)
        self.ui.cs_pushButtonn_03.setGeometry(482, 10, 100, 25)
        self.ui.cs_pushButtonn_04.setGeometry(587, 10, 55, 25)
        self.ui.cs_comboBoxxxx_03.setGeometry(647, 10, 150, 25)
        self.ui.cs_pushButtonn_05.setGeometry(802, 10, 100, 25)
        self.ui.cs_pushButtonn_06.setGeometry(907, 10, 55, 25)
        self.ui.cs_pushButtonn_07.setGeometry(967, 10, 40, 25)

        self.ui.cs_textEditttt_09.setGeometry(7, 10, 1000, 703)
        self.ui.cs_progressBar_01.setGeometry(7, 718, 830, 30)
        self.ui.cs_pushButtonn_08.setGeometry(842, 718, 165, 30)

        self.ui.cvjb_comboBoxx_01.setGeometry(1012, 10, 165, 25)
        self.ui.cvjb_lineEditt_01.setGeometry(1182, 10, 165, 25)
        self.ui.cvjb_pushButon_01.setGeometry(1012, 40, 165, 30)
        self.ui.cvjb_pushButon_02.setGeometry(1182, 40, 165, 30)
        self.ui.cvjb_pushButon_03.setGeometry(1012, 75, 165, 30)
        self.ui.cvjb_pushButon_04.setGeometry(1182, 75, 165, 30)
        self.ui.cvjb_pushButon_05.setGeometry(1012, 110, 165, 30)
        self.ui.cvjb_pushButon_06.setGeometry(1182, 110, 165, 30)
        self.ui.cvjb_pushButon_07.setGeometry(1012, 145, 165, 30)
        self.ui.cvjb_pushButon_08.setGeometry(1182, 145, 165, 30)
        self.ui.cvjb_pushButon_09.setGeometry(1012, 180, 165, 30)
        self.ui.cvjb_pushButon_10.setGeometry(1182, 180, 165, 30)
        self.ui.cvjb_pushButon_11.setGeometry(1012, 215, 165, 30)
        self.ui.cvjb_pushButon_12.setGeometry(1182, 215, 165, 30)

        self.ui.cvj_pushButton_01.setGeometry(1012, 335, 80, 30)
        self.ui.cvj_pushButton_02.setGeometry(1012, 370, 80, 30)
        self.ui.cvj_pushButton_03.setGeometry(1097, 335, 80, 30)
        self.ui.cvj_pushButton_04.setGeometry(1097, 370, 80, 30)
        self.ui.cvj_pushButton_05.setGeometry(1012, 405, 80, 30)
        self.ui.cvj_pushButton_06.setGeometry(1097, 405, 80, 30)

        self.ui.cvjs_comboBoxx_01.setGeometry(1012, 478, 165, 25)
        self.ui.cvjs_lineEditt_01.setGeometry(1182, 478, 165, 25)
        self.ui.cvjs_pushButon_01.setGeometry(1012, 508, 165, 30)
        self.ui.cvjs_pushButon_02.setGeometry(1182, 508, 165, 30)
        self.ui.cvjs_pushButon_03.setGeometry(1012, 543, 165, 30)
        self.ui.cvjs_pushButon_04.setGeometry(1182, 543, 165, 30)
        self.ui.cvjs_pushButon_05.setGeometry(1012, 578, 165, 30)
        self.ui.cvjs_pushButon_06.setGeometry(1182, 578, 165, 30)
        self.ui.cvjs_pushButon_07.setGeometry(1012, 613, 165, 30)
        self.ui.cvjs_pushButon_08.setGeometry(1182, 613, 165, 30)
        self.ui.cvjs_pushButon_09.setGeometry(1012, 648, 165, 30)
        self.ui.cvjs_pushButon_10.setGeometry(1182, 648, 165, 30)
        self.ui.cvjs_pushButon_11.setGeometry(1012, 683, 165, 30)
        self.ui.cvjs_pushButon_12.setGeometry(1182, 683, 165, 30)
        self.ui.cvjs_pushButon_13.setGeometry(1012, 718, 165, 30)
        self.ui.cvjs_pushButon_14.setGeometry(1182, 718, 165, 30)

        self.ui.cvjb_labelllll_01.setGeometry(1012, 255, 340, 20)
        self.ui.cvjb_labelllll_02.setGeometry(1012, 280, 340, 20)
        self.ui.cvjb_labelllll_03.setGeometry(1012, 305, 335, 20)

        self.ui.cvjb_dateEditt_01.setGeometry(1112, 255, 110, 20)
        self.ui.cvjb_dateEditt_02.setGeometry(1237, 255, 110, 20)
        self.ui.cvjb_lineEditt_02.setGeometry(1167, 280, 60, 20)
        self.ui.cvjb_lineEditt_03.setGeometry(1287, 280, 60, 20)
        self.ui.cvjb_lineEditt_04.setGeometry(1167, 305, 60, 20)
        self.ui.cvjb_lineEditt_05.setGeometry(1287, 305, 60, 20)

        self.ui.cvj_pushButton_07.setGeometry(1182, 335, 80, 30)
        self.ui.cvj_pushButton_08.setGeometry(1267, 335, 80, 30)
        self.ui.cvj_pushButton_09.setGeometry(1182, 370, 80, 30)
        self.ui.cvj_pushButton_10.setGeometry(1267, 370, 80, 30)
        self.ui.cvj_pushButton_11.setGeometry(1182, 405, 80, 30)
        self.ui.cvj_pushButton_12.setGeometry(1267, 405, 80, 30)
        self.ui.cvj_pushButton_13.setGeometry(1012, 440, 80, 30)
        self.ui.cvj_pushButton_14.setGeometry(1097, 440, 80, 30)
        self.ui.cvj_pushButton_15.setGeometry(1182, 440, 80, 30)
        self.ui.cvj_pushButton_16.setGeometry(1267, 440, 80, 30)

        self.ui.cvc_comboBoxxx_01.setGeometry(1012, 45, 165, 30)
        self.ui.cvc_lineEdittt_01.setGeometry(1182, 45, 165, 30)
        self.ui.cvc_pushButton_01.setGeometry(1012, 80, 165, 30)
        self.ui.cvc_pushButton_02.setGeometry(1182, 80, 165, 30)

        self.ui.cvc_comboBoxxx_02.setGeometry(1012, 115, 165, 30)
        self.ui.cvc_lineEdittt_02.setGeometry(1182, 115, 165, 30)
        self.ui.cvc_pushButton_03.setGeometry(1012, 150, 165, 30)
        self.ui.cvc_pushButton_04.setGeometry(1182, 150, 165, 30)

        self.ui.cvc_labellllll_01.setGeometry(1012, 250, 335, 25)
        self.ui.cvc_labellllll_02.setGeometry(1012, 190, 335, 25)
        self.ui.cvc_comboBoxxx_03.setGeometry(1097, 190, 45, 25)
        self.ui.cvc_comboBoxxx_04.setGeometry(1197, 190, 45, 25)
        self.ui.cvc_comboBoxxx_05.setGeometry(1302, 190, 45, 25)

        self.ui.cvc_labellllll_03.setGeometry(1012, 220, 335, 25)
        self.ui.cvc_comboBoxxx_06.setGeometry(1097, 220, 45, 25)
        self.ui.cvc_comboBoxxx_07.setGeometry(1187, 220, 55, 25)
        self.ui.cvc_pushButton_05.setGeometry(1247, 220, 47, 25)
        self.ui.cvc_pushButton_36.setGeometry(1299, 220, 48, 25)

        self.ui.cvc_pushButton_06.setGeometry(1012, 335, 80, 30)
        self.ui.cvc_pushButton_07.setGeometry(1012, 370, 80, 30)
        self.ui.cvc_pushButton_08.setGeometry(1012, 405, 80, 30)
        self.ui.cvc_pushButton_27.setGeometry(1097, 335, 80, 30)
        self.ui.cvc_pushButton_28.setGeometry(1097, 370, 80, 30)
        self.ui.cvc_pushButton_29.setGeometry(1097, 405, 80, 30)

        self.ui.cvc_comboBoxxx_08.setGeometry(1012, 513, 165, 30)
        self.ui.cvc_lineEdittt_03.setGeometry(1182, 513, 165, 30)
        self.ui.cvc_pushButton_09.setGeometry(1012, 548, 165, 30)
        self.ui.cvc_pushButton_10.setGeometry(1182, 548, 165, 30)
        self.ui.cvc_labellllll_04.setGeometry(1012, 583, 335, 130)
        self.ui.cvc_pushButton_11.setGeometry(1012, 718, 335, 30)

        self.ui.cvc_lineEdittt_04.setGeometry(1012, 10, 165, 30)
        self.ui.cvc_pushButton_13.setGeometry(1182, 10, 165, 30)
        self.ui.cvc_lineEdittt_05.setGeometry(1012, 478, 165, 30)
        self.ui.cvc_pushButton_14.setGeometry(1182, 478, 165, 30)

        self.ui.cvc_pushButton_15.setGeometry(1012, 335, 80, 30)
        self.ui.cvc_pushButton_16.setGeometry(1012, 370, 80, 30)
        self.ui.cvc_pushButton_17.setGeometry(1012, 405, 80, 30)
        self.ui.cvc_pushButton_30.setGeometry(1097, 335, 80, 30)
        self.ui.cvc_pushButton_31.setGeometry(1097, 370, 80, 30)
        self.ui.cvc_pushButton_32.setGeometry(1097, 405, 80, 30)

        self.ui.cvc_pushButton_18.setGeometry(1012, 335, 80, 30)
        self.ui.cvc_pushButton_19.setGeometry(1012, 370, 80, 30)
        self.ui.cvc_pushButton_20.setGeometry(1012, 405, 80, 30)
        self.ui.cvc_pushButton_33.setGeometry(1097, 335, 80, 30)
        self.ui.cvc_pushButton_34.setGeometry(1097, 370, 80, 30)
        self.ui.cvc_pushButton_35.setGeometry(1097, 405, 80, 30)

        self.ui.cva_pushButton_01.setGeometry(1012, 335, 165, 30)
        self.ui.cva_pushButton_02.setGeometry(1012, 370, 165, 30)
        self.ui.cva_pushButton_03.setGeometry(1012, 405, 165, 30)

        self.ui.cva_comboBoxxx_01.setGeometry(1012, 115, 165, 30)
        self.ui.cva_lineEdittt_01.setGeometry(1182, 115, 165, 30)
        self.ui.cva_pushButton_04.setGeometry(1012, 150, 165, 30)
        self.ui.cva_pushButton_05.setGeometry(1182, 150, 165, 30)

        self.ui.cvc_pushButton_21.setGeometry(1012, 335, 165, 30)
        self.ui.cvc_pushButton_22.setGeometry(1012, 370, 165, 30)
        self.ui.cvc_pushButton_23.setGeometry(1012, 405, 165, 30)
        self.ui.cvc_pushButton_24.setGeometry(1012, 335, 165, 30)
        self.ui.cvc_pushButton_25.setGeometry(1012, 370, 165, 30)
        self.ui.cvc_pushButton_26.setGeometry(1012, 405, 165, 30)
        self.ui.cvc_labellllll_05.setGeometry(1012, 150, 335, 40)

        self.ui.cvo_comboBoxxx_01.setGeometry(1012, 10, 165, 30)
        self.ui.cvo_lineEdittt_01.setGeometry(1182, 10, 165, 30)
        self.ui.cvo_pushButton_01.setGeometry(1012, 45, 165, 30)
        self.ui.cvo_pushButton_02.setGeometry(1182, 45, 165, 30)
        self.ui.cvo_comboBoxxx_02.setGeometry(1012, 80, 165, 30)
        self.ui.cvo_lineEdittt_02.setGeometry(1182, 80, 165, 30)
        self.ui.cvo_pushButton_03.setGeometry(1012, 115, 165, 30)
        self.ui.cvo_pushButton_04.setGeometry(1182, 115, 165, 30)

        self.ui.cvo_labellllll_04.setGeometry(1012, 255, 335, 20)
        self.ui.cvo_lineEdittt_03.setGeometry(1072, 255, 45, 20)
        self.ui.cvo_lineEdittt_04.setGeometry(1197, 255, 45, 20)
        self.ui.cvo_lineEdittt_05.setGeometry(1302, 255, 45, 20)

        self.ui.cvo_pushButton_05.setGeometry(1012, 335, 165, 30)
        self.ui.cvo_pushButton_06.setGeometry(1012, 370, 165, 30)
        self.ui.cvo_pushButton_07.setGeometry(1012, 405, 165, 30)

        self.ui.cvo_pushButton_08.setGeometry(1012, 718, 335, 30)
