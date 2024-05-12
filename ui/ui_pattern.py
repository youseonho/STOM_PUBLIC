import os
import random
import sqlite3
import pandas as pd
from PyQt5.QtWidgets import QMessageBox
from ui.set_text import famous_saying
from utility.setting import DB_STRATEGY, PATTERN_PATH
from utility.static import pickle_read


def pactivated_01(ui):
    name = ui.pt_comboBoxxxxx_00.currentText()
    con = sqlite3.connect(DB_STRATEGY)
    if ui.main_btn == 2:
        df = pd.read_sql(f'SELECT * FROM stockpattern WHERE `index`= "{name}"', con)
    else:
        df = pd.read_sql(f'SELECT * FROM coinpattern WHERE `index`= "{name}"', con)
    con.close()
    if len(df) > 0:
        pattern = df['패턴설정'][0]
        pattern = pattern.split('^')
        ui.pt_comboBoxxxxx_14.setCurrentText(pattern[1])
        ui.pt_comboBoxxxxx_15.setCurrentText(pattern[2])
        ui.pt_checkBoxxxxx_14.setChecked(True if pattern[3] == '1' else False)
        ui.pt_lineEdittttt_01.setText(pattern[4])
        ui.pt_checkBoxxxxx_15.setChecked(True if pattern[5] == '1' else False)
        ui.pt_checkBoxxxxx_34.setChecked(True if pattern[6] == '1' else False)
        ui.pt_lineEdittttt_02.setText(pattern[7])
        ui.pt_checkBoxxxxx_35.setChecked(True if pattern[8] == '1' else False)
        ui.pt_checkBoxxxxx_01.setChecked(True if pattern[9] == '1' else False)
        ui.pt_checkBoxxxxx_02.setChecked(True if pattern[10] == '1' else False)
        ui.pt_checkBoxxxxx_03.setChecked(True if pattern[11] == '1' else False)
        ui.pt_checkBoxxxxx_04.setChecked(True if pattern[12] == '1' else False)
        ui.pt_checkBoxxxxx_05.setChecked(True if pattern[13] == '1' else False)
        ui.pt_checkBoxxxxx_06.setChecked(True if pattern[14] == '1' else False)
        ui.pt_checkBoxxxxx_07.setChecked(True if pattern[15] == '1' else False)
        ui.pt_checkBoxxxxx_08.setChecked(True if pattern[16] == '1' else False)
        ui.pt_checkBoxxxxx_09.setChecked(True if pattern[17] == '1' else False)
        ui.pt_checkBoxxxxx_10.setChecked(True if pattern[18] == '1' else False)
        ui.pt_checkBoxxxxx_11.setChecked(True if pattern[19] == '1' else False)
        ui.pt_checkBoxxxxx_12.setChecked(True if pattern[20] == '1' else False)
        ui.pt_checkBoxxxxx_13.setChecked(True if pattern[21] == '1' else False)
        ui.pt_comboBoxxxxx_01.setCurrentText(pattern[22])
        ui.pt_comboBoxxxxx_02.setCurrentText(pattern[23])
        ui.pt_comboBoxxxxx_03.setCurrentText(pattern[24])
        ui.pt_comboBoxxxxx_04.setCurrentText(pattern[25])
        ui.pt_comboBoxxxxx_05.setCurrentText(pattern[26])
        ui.pt_comboBoxxxxx_06.setCurrentText(pattern[27])
        ui.pt_comboBoxxxxx_07.setCurrentText(pattern[28])
        ui.pt_comboBoxxxxx_08.setCurrentText(pattern[29])
        ui.pt_comboBoxxxxx_09.setCurrentText(pattern[30])
        ui.pt_comboBoxxxxx_10.setCurrentText(pattern[31])
        ui.pt_comboBoxxxxx_11.setCurrentText(pattern[32])
        ui.pt_comboBoxxxxx_12.setCurrentText(pattern[33])
        ui.pt_comboBoxxxxx_13.setCurrentText(pattern[34])
        ui.pt_checkBoxxxxx_21.setChecked(True if pattern[35] == '1' else False)
        ui.pt_checkBoxxxxx_22.setChecked(True if pattern[36] == '1' else False)
        ui.pt_checkBoxxxxx_23.setChecked(True if pattern[37] == '1' else False)
        ui.pt_checkBoxxxxx_24.setChecked(True if pattern[38] == '1' else False)
        ui.pt_checkBoxxxxx_25.setChecked(True if pattern[39] == '1' else False)
        ui.pt_checkBoxxxxx_26.setChecked(True if pattern[40] == '1' else False)
        ui.pt_checkBoxxxxx_27.setChecked(True if pattern[41] == '1' else False)
        ui.pt_checkBoxxxxx_28.setChecked(True if pattern[42] == '1' else False)
        ui.pt_checkBoxxxxx_29.setChecked(True if pattern[43] == '1' else False)
        ui.pt_checkBoxxxxx_30.setChecked(True if pattern[44] == '1' else False)
        ui.pt_checkBoxxxxx_31.setChecked(True if pattern[45] == '1' else False)
        ui.pt_checkBoxxxxx_32.setChecked(True if pattern[46] == '1' else False)
        ui.pt_checkBoxxxxx_33.setChecked(True if pattern[47] == '1' else False)
        ui.pt_comboBoxxxxx_21.setCurrentText(pattern[48])
        ui.pt_comboBoxxxxx_22.setCurrentText(pattern[49])
        ui.pt_comboBoxxxxx_23.setCurrentText(pattern[50])
        ui.pt_comboBoxxxxx_24.setCurrentText(pattern[51])
        ui.pt_comboBoxxxxx_25.setCurrentText(pattern[52])
        ui.pt_comboBoxxxxx_26.setCurrentText(pattern[53])
        ui.pt_comboBoxxxxx_27.setCurrentText(pattern[54])
        ui.pt_comboBoxxxxx_28.setCurrentText(pattern[55])
        ui.pt_comboBoxxxxx_29.setCurrentText(pattern[56])
        ui.pt_comboBoxxxxx_30.setCurrentText(pattern[57])
        ui.pt_comboBoxxxxx_31.setCurrentText(pattern[58])
        ui.pt_comboBoxxxxx_32.setCurrentText(pattern[59])
        ui.pt_comboBoxxxxx_33.setCurrentText(pattern[60])


def ptbutton_clicked_01(ui):
    con = sqlite3.connect(DB_STRATEGY)
    if ui.main_btn == 2:
        df = pd.read_sql('SELECT * FROM stockpattern', con).set_index('index')
    else:
        df = pd.read_sql('SELECT * FROM coinpattern', con).set_index('index')
    con.close()
    if len(df) > 0:
        ui.pt_comboBoxxxxx_00.clear()
        for pattern_name in df.index:
            ui.pt_comboBoxxxxx_00.addItem(pattern_name)


def ptbutton_clicked_02(ui, proc_query, queryQ):
    if ui.main_btn == 2:
        name = ui.svjb_comboBoxx_01.currentText()
    else:
        name = ui.cvjb_comboBoxx_01.currentText()

    if name == '':
        QMessageBox.critical(ui.dialog_pattern, '오류 알림', '패턴의 이름은 전략의 이름이 포함되어 저장됩니다.\n전략을 로딩하고 선택하십시오.')
        return
    if not ui.pt_checkBoxxxxx_14.isChecked() and not ui.pt_checkBoxxxxx_15.isChecked():
        QMessageBox.critical(ui.dialog_pattern, '오류 알림', '매수 패턴 인식 조건을 선택하십시오.\n')
        return
    if ui.pt_checkBoxxxxx_14.isChecked() and ui.pt_checkBoxxxxx_15.isChecked():
        QMessageBox.critical(ui.dialog_pattern, '오류 알림', '매수 패턴 인식 조건은 하나만 선택할 수 있습니다.\n')
        return
    if not ui.pt_checkBoxxxxx_34.isChecked() and not ui.pt_checkBoxxxxx_35.isChecked():
        QMessageBox.critical(ui.dialog_pattern, '오류 알림', '매도 패턴 인식 조건을 선택하십시오.\n')
        return
    if ui.pt_checkBoxxxxx_34.isChecked() and ui.pt_checkBoxxxxx_35.isChecked():
        QMessageBox.critical(ui.dialog_pattern, '오류 알림', '매도 패턴 인식 조건은 하나만 선택할 수 있습니다.\n')
        return
    if ui.pt_checkBoxxxxx_14.isChecked() and ui.pt_lineEdittttt_01.text() == '':
        QMessageBox.critical(ui.dialog_pattern, '오류 알림', '매수 패턴 인식 조건 등락율 수치를 입력하십시오.\n')
        return
    if ui.pt_checkBoxxxxx_34.isChecked() and ui.pt_lineEdittttt_02.text() == '':
        QMessageBox.critical(ui.dialog_pattern, '오류 알림', '매도 패턴 인식 조건 등락율 수치를 입력하십시오.\n')
        return
    if ui.pt_lineEdittttt_01.text() == '' or ui.pt_lineEdittttt_02.text() == '':
        QMessageBox.critical(ui.dialog_pattern, '오류 알림', '등락율 수치가 입력되지 않았습니다.\n사용하지 않더라도 입력되어야 합니다.')
        return

    pattern_text = get_pattern_text(ui)
    df = pd.DataFrame({'패턴설정': [pattern_text]}, index=[name])
    if proc_query.is_alive():
        if ui.main_btn == 2:
            queryQ.put(('전략디비', f"DELETE FROM stockpattern WHERE `index` = '{name}'"))
            queryQ.put(('전략디비', df, 'stockpattern', 'append'))
        else:
            queryQ.put(('전략디비', f"DELETE FROM coinpattern WHERE `index` = '{name}'"))
            queryQ.put(('전략디비', df, 'coinpattern', 'append'))
        QMessageBox.information(ui.dialog_pattern, '저장 완료', random.choice(famous_saying))


def ptbutton_clicked_03(ui):
    if ui.main_btn == 2:
        middle_name = 'stock'
    else:
        middle_name = 'coin'
    last_name = ui.pt_comboBoxxxxx_00.currentText()
    if last_name != '':
        pattern_buy_name = f'{PATTERN_PATH}/pattern_{middle_name}_{last_name}_buy'
        pattern_sell_name = f'{PATTERN_PATH}/pattern_{middle_name}_{last_name}_sell'
        if os.path.isfile(f'{pattern_buy_name}.pkl') and os.path.isfile(f'{pattern_sell_name}.pkl'):
            if ui.backtest_engine:
                for q in ui.back_eques:
                    q.put(('백테유형', '백테스트'))
                dict_pattern, dict_pattern_buy, dict_pattern_sell = get_pattern_setup(get_pattern_text(ui))
                for q in ui.back_eques:
                    q.put(('패턴정보', dict_pattern, dict_pattern_buy, dict_pattern_sell))
                pattern_buy = pickle_read(pattern_buy_name)
                pattern_sell = pickle_read(pattern_sell_name)
                for q in ui.back_eques:
                    q.put(('모델정보', pattern_buy, pattern_sell))
                QMessageBox.information(ui.dialog_pattern, '전송 완료', random.choice(famous_saying))
            else:
                QMessageBox.critical(ui.dialog_pattern, '오류 알림', '백테엔진이 미실행중입니다.\n먼저 백테엔진을 구동하십시오.\n')
        else:
            QMessageBox.critical(ui.dialog_pattern, '오류 알림', '학습 데이터 파일이 존재하지 않습니다.\n')
    else:
        QMessageBox.critical(ui.dialog_pattern, '오류 알림', '전송할 패턴 데이터의 이름을 콤보박스에서 선택하십시오.\n')


def get_pattern_text(ui):
    pattern_text = [
        ui.pt_comboBoxxxxx_00.currentText(),
        ui.pt_comboBoxxxxx_14.currentText(),
        ui.pt_comboBoxxxxx_15.currentText(),
        '1' if ui.pt_checkBoxxxxx_14.isChecked() else '0',
        ui.pt_lineEdittttt_01.text(),
        '1' if ui.pt_checkBoxxxxx_15.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_34.isChecked() else '0',
        ui.pt_lineEdittttt_02.text(),
        '1' if ui.pt_checkBoxxxxx_35.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_01.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_02.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_03.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_04.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_05.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_06.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_07.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_08.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_09.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_10.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_11.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_12.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_13.isChecked() else '0',
        ui.pt_comboBoxxxxx_01.currentText(),
        ui.pt_comboBoxxxxx_02.currentText(),
        ui.pt_comboBoxxxxx_03.currentText(),
        ui.pt_comboBoxxxxx_04.currentText(),
        ui.pt_comboBoxxxxx_05.currentText(),
        ui.pt_comboBoxxxxx_06.currentText(),
        ui.pt_comboBoxxxxx_07.currentText(),
        ui.pt_comboBoxxxxx_08.currentText(),
        ui.pt_comboBoxxxxx_09.currentText(),
        ui.pt_comboBoxxxxx_10.currentText(),
        ui.pt_comboBoxxxxx_11.currentText(),
        ui.pt_comboBoxxxxx_12.currentText(),
        ui.pt_comboBoxxxxx_13.currentText(),
        '1' if ui.pt_checkBoxxxxx_21.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_22.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_23.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_24.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_25.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_26.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_27.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_28.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_29.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_30.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_31.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_32.isChecked() else '0',
        '1' if ui.pt_checkBoxxxxx_33.isChecked() else '0',
        ui.pt_comboBoxxxxx_21.currentText(),
        ui.pt_comboBoxxxxx_22.currentText(),
        ui.pt_comboBoxxxxx_23.currentText(),
        ui.pt_comboBoxxxxx_24.currentText(),
        ui.pt_comboBoxxxxx_25.currentText(),
        ui.pt_comboBoxxxxx_26.currentText(),
        ui.pt_comboBoxxxxx_27.currentText(),
        ui.pt_comboBoxxxxx_28.currentText(),
        ui.pt_comboBoxxxxx_29.currentText(),
        ui.pt_comboBoxxxxx_30.currentText(),
        ui.pt_comboBoxxxxx_31.currentText(),
        ui.pt_comboBoxxxxx_32.currentText(),
        ui.pt_comboBoxxxxx_33.currentText()
    ]
    pattern_text = '^'.join(pattern_text)
    return pattern_text


def get_pattern_setup(pattern_text):
    pattern_setup = pattern_text.split('^')
    dict_pattern = {
        '패턴이름': pattern_setup[0],
        '인식구간': int(pattern_setup[1]),
        '조건구간': int(pattern_setup[2]),
        '매수조건1': 1 if pattern_setup[3] == '1' else 0,
        '매수조건2': float(pattern_setup[4]),
        '매수조건3': 1 if pattern_setup[5] == '1' else 0,
        '매도조건1': 1 if pattern_setup[6] == '1' else 0,
        '매도조건2': float(pattern_setup[7]),
        '매도조건3': 1 if pattern_setup[8] == '1' else 0
    }
    dict_pattern_buy = {}
    if pattern_setup[9] == '1':
        dict_pattern_buy['등락율'] = float(pattern_setup[22])
    if pattern_setup[10] == '1':
        dict_pattern_buy['당일거래대금'] = float(pattern_setup[23])
    if pattern_setup[11] == '1':
        dict_pattern_buy['체결강도'] = float(pattern_setup[24])
    if pattern_setup[12] == '1':
        dict_pattern_buy['초당매수금액'] = float(pattern_setup[25])
    if pattern_setup[13] == '1':
        dict_pattern_buy['초당매도금액'] = float(pattern_setup[26])
    if pattern_setup[14] == '1':
        dict_pattern_buy['순매수금액'] = float(pattern_setup[27])
    if pattern_setup[15] == '1':
        dict_pattern_buy['초당거래대금'] = float(pattern_setup[28])
    if pattern_setup[16] == '1':
        dict_pattern_buy['고저평균대비등락율'] = float(pattern_setup[29])
    if pattern_setup[17] == '1':
        dict_pattern_buy['매도1잔량금액'] = float(pattern_setup[30])
    if pattern_setup[18] == '1':
        dict_pattern_buy['매수1잔량금액'] = float(pattern_setup[31])
    if pattern_setup[19] == '1':
        dict_pattern_buy['매도총잔량금액'] = float(pattern_setup[32])
    if pattern_setup[20] == '1':
        dict_pattern_buy['매수총잔량금액'] = float(pattern_setup[33])
    if pattern_setup[21] == '1':
        dict_pattern_buy['매도수5호가총금액'] = float(pattern_setup[34])
    dict_pattern_sell = {}
    if pattern_setup[35] == '1':
        dict_pattern_sell['등락율'] = float(pattern_setup[48])
    if pattern_setup[36] == '1':
        dict_pattern_sell['당일거래대금'] = float(pattern_setup[49])
    if pattern_setup[37] == '1':
        dict_pattern_sell['체결강도'] = float(pattern_setup[50])
    if pattern_setup[38] == '1':
        dict_pattern_sell['초당매수금액'] = float(pattern_setup[51])
    if pattern_setup[39] == '1':
        dict_pattern_sell['초당매도금액'] = float(pattern_setup[52])
    if pattern_setup[40] == '1':
        dict_pattern_sell['순매수금액'] = float(pattern_setup[53])
    if pattern_setup[41] == '1':
        dict_pattern_sell['초당거래대금'] = float(pattern_setup[54])
    if pattern_setup[42] == '1':
        dict_pattern_sell['고저평균대비등락율'] = float(pattern_setup[55])
    if pattern_setup[43] == '1':
        dict_pattern_sell['매도1잔량금액'] = float(pattern_setup[56])
    if pattern_setup[44] == '1':
        dict_pattern_sell['매수1잔량금액'] = float(pattern_setup[57])
    if pattern_setup[45] == '1':
        dict_pattern_sell['매도총잔량금액'] = float(pattern_setup[58])
    if pattern_setup[46] == '1':
        dict_pattern_sell['매수총잔량금액'] = float(pattern_setup[59])
    if pattern_setup[47] == '1':
        dict_pattern_sell['매도수5호가총금액'] = float(pattern_setup[60])
    return dict_pattern, dict_pattern_buy, dict_pattern_sell
