import random
import sqlite3
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QApplication
from utility.setting import DB_STRATEGY
from utility.static import text_not_in_special_characters
from ui.set_text import famous_saying, example_stock_buy, example_stock_sell, example_stockopti_buy1, \
    example_stockopti_buy2, example_stockopti_sell1, example_stockopti_sell2, example_opti_vars, example_vars, \
    example_buyconds, example_sellconds


def svc_button_clicked_01(ui):
    if ui.ss_textEditttt_03.isVisible():
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql('SELECT * FROM stockoptibuy', con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.svc_comboBoxxx_01.clear()
            indexs = list(df.index)
            indexs.sort()
            for i, index in enumerate(indexs):
                ui.svc_comboBoxxx_01.addItem(index)
                if i == 0:
                    ui.svc_lineEdittt_01.setText(index)


def svc_button_clicked_02(ui, proc_query, queryQ):
    if ui.ss_textEditttt_03.isVisible():
        strategy_name = ui.svc_lineEdittt_01.text()
        strategy = ui.ss_textEditttt_03.toPlainText()
        strategy = ui.GetFixStrategy(strategy, '매수')

        if strategy_name == '':
            QMessageBox.critical(ui, '오류 알림', '최적화 매수전략의 이름이 공백 상태입니다.\n이름을 입력하십시오.\n')
        elif not text_not_in_special_characters(strategy_name):
            QMessageBox.critical(ui, '오류 알림', '최적화 매수전략의 이름에 특문이 포함되어 있습니다.\n언더바(_)를 제외한 특문을 제거하십시오.\n')
        elif strategy == '':
            QMessageBox.critical(ui, '오류 알림', '최적화 매수전략의 코드가 공백 상태입니다.\n코드를 작성하십시오.\n')
        else:
            if 'self.tickcols' in strategy or (
                    QApplication.keyboardModifiers() & Qt.ControlModifier) or ui.BackCodeTest1(strategy):
                con = sqlite3.connect(DB_STRATEGY)
                df = pd.read_sql(f"SELECT * FROM stockoptibuy WHERE `index` = '{strategy_name}'", con)
                con.close()
                if proc_query.is_alive():
                    if len(df) > 0:
                        query = f"UPDATE stockoptibuy SET 전략코드 = '{strategy}' WHERE `index` = '{strategy_name}'"
                        queryQ.put(('전략디비', query))
                    else:
                        data = [
                            strategy,
                            9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999.,
                            9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999.,
                            9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999.,
                            9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999.,
                            9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999.,
                            9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999.,
                            9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999.,
                            9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999.,
                            9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999.,
                            9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999.,
                            9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999.,
                            9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999.,
                            9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999.,
                            9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999.,
                            9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999.,
                            9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999.,
                            9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999.,
                            9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999.,
                            9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999.,
                            9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999., 9999.
                        ]
                        columns = [
                            '전략코드',
                            '변수0', '변수1', '변수2', '변수3', '변수4', '변수5', '변수6', '변수7', '변수8', '변수9',
                            '변수10', '변수11', '변수12', '변수13', '변수14', '변수15', '변수16', '변수17', '변수18', '변수19',
                            '변수20', '변수21', '변수22', '변수23', '변수24', '변수25', '변수26', '변수27', '변수28', '변수29',
                            '변수30', '변수31', '변수32', '변수33', '변수34', '변수35', '변수36', '변수37', '변수38', '변수39',
                            '변수40', '변수41', '변수42', '변수43', '변수44', '변수45', '변수46', '변수47', '변수48', '변수49',
                            '변수50', '변수51', '변수52', '변수53', '변수54', '변수55', '변수56', '변수57', '변수58', '변수59',
                            '변수60', '변수61', '변수62', '변수63', '변수64', '변수65', '변수66', '변수67', '변수68', '변수69',
                            '변수70', '변수71', '변수72', '변수73', '변수74', '변수75', '변수76', '변수77', '변수78', '변수79',
                            '변수80', '변수81', '변수82', '변수83', '변수84', '변수85', '변수86', '변수87', '변수88', '변수89',
                            '변수90', '변수91', '변수92', '변수93', '변수94', '변수95', '변수96', '변수97', '변수98', '변수99',
                            '변수100', '변수101', '변수102', '변수103', '변수104', '변수105', '변수106', '변수107', '변수108', '변수109',
                            '변수110', '변수111', '변수112', '변수113', '변수114', '변수115', '변수116', '변수117', '변수118', '변수119',
                            '변수120', '변수121', '변수122', '변수123', '변수124', '변수125', '변수126', '변수127', '변수128', '변수129',
                            '변수130', '변수131', '변수132', '변수133', '변수134', '변수135', '변수136', '변수137', '변수138', '변수139',
                            '변수140', '변수141', '변수142', '변수143', '변수144', '변수145', '변수146', '변수147', '변수148', '변수149',
                            '변수150', '변수151', '변수152', '변수153', '변수154', '변수155', '변수156', '변수157', '변수158', '변수159',
                            '변수160', '변수161', '변수162', '변수163', '변수164', '변수165', '변수166', '변수167', '변수168', '변수169',
                            '변수170', '변수171', '변수172', '변수173', '변수174', '변수175', '변수176', '변수177', '변수178', '변수179',
                            '변수180', '변수181', '변수182', '변수183', '변수184', '변수185', '변수186', '변수187', '변수188', '변수189',
                            '변수190', '변수191', '변수192', '변수193', '변수194', '변수195', '변수196', '변수197', '변수198', '변수199'
                        ]
                        df = pd.DataFrame([data], columns=columns, index=[strategy_name])
                        queryQ.put(('전략디비', df, 'stockoptibuy', 'append'))
                    QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))


def svc_button_clicked_03(ui):
    if ui.ss_textEditttt_05.isVisible():
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql('SELECT * FROM stockoptivars', con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.svc_comboBoxxx_02.clear()
            indexs = list(df.index)
            indexs.sort()
            for i, index in enumerate(indexs):
                ui.svc_comboBoxxx_02.addItem(index)
                if i == 0:
                    ui.svc_lineEdittt_02.setText(index)


def svc_button_clicked_04(ui, proc_query, queryQ):
    if ui.ss_textEditttt_05.isVisible():
        strategy_name = ui.svc_lineEdittt_02.text()
        strategy = ui.ss_textEditttt_05.toPlainText()
        if strategy_name == '':
            QMessageBox.critical(ui, '오류 알림', '변수범위의 이름이 공백 상태입니다.\n이름을 입력하십시오.\n')
        elif not text_not_in_special_characters(strategy_name):
            QMessageBox.critical(ui, '오류 알림', '변수범위의 이름에 특문이 포함되어 있습니다.\n언더바(_)를 제외한 특문을 제거하십시오.\n')
        elif strategy == '':
            QMessageBox.critical(ui, '오류 알림', '변수범위의 코드가 공백 상태입니다.\n코드를 작성하십시오.\n')
        else:
            if (QApplication.keyboardModifiers() & Qt.ControlModifier) or ui.BackCodeTest2(strategy):
                if proc_query.is_alive():
                    queryQ.put(('전략디비', f"DELETE FROM stockoptivars WHERE `index` = '{strategy_name}'"))
                    df = pd.DataFrame({'전략코드': [strategy]}, index=[strategy_name])
                    queryQ.put(('전략디비', df, 'stockoptivars', 'append'))
                    QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))


def svc_button_clicked_05(ui):
    if ui.ss_textEditttt_04.isVisible():
        con = sqlite3.connect(DB_STRATEGY)
        df = pd.read_sql('SELECT * FROM stockoptisell', con).set_index('index')
        con.close()
        if len(df) > 0:
            ui.svc_comboBoxxx_08.clear()
            indexs = list(df.index)
            indexs.sort()
            for i, index in enumerate(indexs):
                ui.svc_comboBoxxx_08.addItem(index)
                if i == 0:
                    ui.svc_lineEdittt_03.setText(index)


def svc_button_clicked_06(ui, proc_query, queryQ):
    if ui.ss_textEditttt_04.isVisible():
        strategy_name = ui.svc_lineEdittt_03.text()
        strategy = ui.ss_textEditttt_04.toPlainText()
        strategy = ui.GetFixStrategy(strategy, '매도')

        if strategy_name == '':
            QMessageBox.critical(ui, '오류 알림', '최적화 매도전략의 이름이 공백 상태입니다.\n이름을 입력하십시오.\n')
        elif not text_not_in_special_characters(strategy_name):
            QMessageBox.critical(ui, '오류 알림', '최적화 매도전략의 이름에 특문이 포함되어 있습니다.\n언더바(_)를 제외한 특문을 제거하십시오.\n')
        elif strategy == '':
            QMessageBox.critical(ui, '오류 알림', '최적화 매도전략의 코드가 공백 상태입니다.\n코드를 작성하십시오.\n')
        else:
            if 'self.tickcols' in strategy or (
                    QApplication.keyboardModifiers() & Qt.ControlModifier) or ui.BackCodeTest1(strategy):
                if proc_query.is_alive():
                    queryQ.put(('전략디비', f"DELETE FROM stockoptisell WHERE `index` = '{strategy_name}'"))
                    df = pd.DataFrame({'전략코드': [strategy]}, index=[strategy_name])
                    queryQ.put(('전략디비', df, 'stockoptisell', 'append'))
                    QMessageBox.information(ui, '저장 완료', random.choice(famous_saying))


def svc_button_clicked_07(ui):
    if ui.ss_textEditttt_01.isVisible():
        ui.ss_textEditttt_01.clear()
        ui.ss_textEditttt_01.append(example_stock_buy)
    if ui.ss_textEditttt_02.isVisible():
        ui.ss_textEditttt_02.clear()
        ui.ss_textEditttt_02.append(example_stock_sell)
    if ui.ss_textEditttt_03.isVisible():
        ui.ss_textEditttt_03.clear()
        if ui.svc_pushButton_24.isVisible():
            ui.ss_textEditttt_03.append(example_stockopti_buy1)
        else:
            ui.ss_textEditttt_03.append(example_stockopti_buy2)
    if ui.ss_textEditttt_04.isVisible():
        ui.ss_textEditttt_04.clear()
        if ui.svc_pushButton_24.isVisible():
            ui.ss_textEditttt_04.append(example_stockopti_sell1)
        else:
            ui.ss_textEditttt_04.append(example_stockopti_sell2)
    if ui.ss_textEditttt_05.isVisible():
        ui.ss_textEditttt_05.clear()
        ui.ss_textEditttt_05.append(example_opti_vars)
    if ui.ss_textEditttt_06.isVisible():
        ui.ss_textEditttt_06.clear()
        ui.ss_textEditttt_06.append(example_vars)
    if ui.ss_textEditttt_07.isVisible():
        ui.ss_textEditttt_07.clear()
        ui.ss_textEditttt_07.append(example_buyconds)
    if ui.ss_textEditttt_08.isVisible():
        ui.ss_textEditttt_08.clear()
        ui.ss_textEditttt_08.append(example_sellconds)


def svc_button_clicked_08(ui, proc_query, queryQ):
    tabl = 'stockoptivars' if not ui.sva_pushButton_01.isVisible() else 'stockvars'
    stgy = ui.svc_comboBoxxx_01.currentText()
    opti = ui.svc_comboBoxxx_02.currentText() if not ui.sva_pushButton_01.isVisible() else ui.sva_comboBoxxx_01.currentText()
    name = ui.svc_lineEdittt_04.text()
    if stgy == '' or opti == '' or name == '':
        QMessageBox.critical(ui, '오류 알림', '전략 및 범위 코드를 선택하거나\n매수전략의 이름을 입력하십시오.\n')
        return
    elif not text_not_in_special_characters(name):
        QMessageBox.critical(ui, '오류 알림', '매수전략의 이름에 특문이 포함되어 있습니다.\n언더바(_)를 제외한 특문을 제거하십시오.\n')
        return

    con = sqlite3.connect(DB_STRATEGY)
    df = pd.read_sql('SELECT * FROM stockoptibuy', con).set_index('index')
    stg = df['전략코드'][stgy]
    df = pd.read_sql(f'SELECT * FROM "{tabl}"', con).set_index('index')
    opt = df['전략코드'][opti]
    con.close()

    try:
        vars_ = {}
        opt = opt.replace('self.vars', 'vars_')
        exec(compile(opt, '<string>', 'exec'))
        for i in range(len(vars_)):
            stg = stg.replace(f'self.vars[{i}]', f'{vars_[i][1]}')
    except Exception as e:
        QMessageBox.critical(ui, '오류 알림', f'{e}')
        return

    if proc_query.is_alive():
        queryQ.put(('전략디비', f"DELETE FROM stockbuy WHERE `index` = '{name}'"))
        df = pd.DataFrame({'전략코드': [stg]}, index=[name])
        queryQ.put(('전략디비', df, 'stockbuy', 'append'))
        QMessageBox.information(ui, '저장 알림', '최적값으로 매수전략을 저장하였습니다.\n')


def svc_button_clicked_09(ui, proc_query, queryQ):
    tabl = 'stockoptivars' if not ui.sva_pushButton_01.isVisible() else 'stockvars'
    stgy = ui.svc_comboBoxxx_08.currentText()
    opti = ui.svc_comboBoxxx_02.currentText() if not ui.sva_pushButton_01.isVisible() else ui.sva_comboBoxxx_01.currentText()
    name = ui.svc_lineEdittt_05.text()
    if stgy == '' or opti == '' or name == '':
        QMessageBox.critical(ui, '오류 알림', '전략 및 범위 코드를 선택하거나\n매도전략의 이름을 입력하십시오.\n')
        return
    elif not text_not_in_special_characters(name):
        QMessageBox.critical(ui, '오류 알림', '매도전략의 이름에 특문이 포함되어 있습니다.\n언더바(_)를 제외한 특문을 제거하십시오.\n')
        return

    con = sqlite3.connect(DB_STRATEGY)
    df = pd.read_sql('SELECT * FROM stockoptisell', con).set_index('index')
    stg = df['전략코드'][stgy]
    df = pd.read_sql(f'SELECT * FROM "{tabl}"', con).set_index('index')
    opt = df['전략코드'][opti]
    con.close()

    try:
        vars_ = {}
        opt = opt.replace('self.vars', 'vars_')
        exec(compile(opt, '<string>', 'exec'))
        for i in range(len(vars_)):
            stg = stg.replace(f'self.vars[{i}]', f'{vars_[i][1]}')
    except Exception as e:
        QMessageBox.critical(ui, '오류 알림', f'{e}')
        return

    if proc_query.is_alive():
        queryQ.put(('전략디비', f"DELETE FROM stocksell WHERE `index` = '{name}'"))
        df = pd.DataFrame({'전략코드': [stg]}, index=[name])
        queryQ.put(('전략디비', df, 'stocksell', 'append'))
        QMessageBox.information(ui, '저장 알림', '최적값으로 매도전략을 저장하였습니다.\n')


def svc_button_clicked_10(ui):
    ui.dialog_std.show() if not ui.dialog_std.isVisible() else ui.dialog_std.close()


def svc_button_clicked_11(ui):
    if not ui.dialog_optuna.isVisible():
        if not ui.optuna_window_open:
            ui.op_lineEditttt_01.setText(ui.dict_set['옵튜나고정변수'])
            ui.op_lineEditttt_02.setText(str(ui.dict_set['옵튜나실행횟수']))
            ui.op_checkBoxxxx_01.setChecked(True) if ui.dict_set['옵튜나자동스탭'] else ui.op_checkBoxxxx_01.setChecked(
                False)
            ui.op_comboBoxxxx_01.setCurrentText(ui.dict_set['옵튜나샘플러'])
        ui.dialog_optuna.show()
        ui.optuna_window_open = True
    else:
        ui.dialog_optuna.close()
