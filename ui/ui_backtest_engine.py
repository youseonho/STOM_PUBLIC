import sqlite3
import pandas as pd
from utility.setting import DB_STOCK_BACK, DB_COIN_BACK
from utility.static import thread_decorator, timedelta_sec, now, qtest_qwait


def backtest_engine_show(ui, gubun):
    table_list = []
    BACK_FILE = DB_STOCK_BACK if gubun == '주식' else DB_COIN_BACK
    con = sqlite3.connect(BACK_FILE)
    try:
        df = pd.read_sql("SELECT name FROM sqlite_master WHERE TYPE = 'table'", con)
        table_list = df['name'].to_list()
        table_list.remove('codename')
        table_list.remove('moneytop')
    except:
        pass
    con.close()
    if table_list:
        name_list = [ui.dict_name[code] if code in ui.dict_name.keys() else code for code in table_list]
        name_list.sort()
        ui.be_comboBoxxxxx_02.clear()
        for name in name_list:
            ui.be_comboBoxxxxx_02.addItem(name)
    ui.be_lineEdittttt_01.setText('90000' if gubun == '주식' else '0')
    ui.be_lineEdittttt_02.setText('93000' if gubun == '주식' else '235959')
    if not ui.backengin_window_open:
        ui.be_comboBoxxxxx_01.setCurrentText(ui.dict_set['백테엔진분류방법'])
    ui.dialog_backengine.show()
    ui.backengin_window_open = True


# noinspection PyUnusedLocal
@thread_decorator
def start_backtest_engine(ui, gubun, windowQ, wdzservQ, backQ, totalQ, webcQ):
    pass


# noinspection PyUnusedLocal
def back_code_test1(stg_code, testQ):
    return True


# noinspection PyUnusedLocal
def back_code_test2(vars_code, testQ, ga):
    pass


# noinspection PyUnusedLocal
def back_code_test3(gubun, conds_code, testQ):
    pass


def back_code_test_wait(gubun, testQ):
    test_ok = False
    test_time = timedelta_sec(3)

    while now() < test_time:
        if not testQ.empty():
            testQ.get()
            print(f'{gubun} 코드 오류 테스트 완료')
            test_ok = True
            break
        qtest_qwait(0.1)

    if not test_ok:
        print(f'{gubun}에 오류가 있어 저장하지 못하였습니다.')

    return test_ok


def clear_backtestQ(backQ, totalQ):
    if not backQ.empty():
        while not backQ.empty():
            backQ.get()
    if not totalQ.empty():
        while not totalQ.empty():
            totalQ.get()


# noinspection PyUnusedLocal
def backtest_process_kill(ui, gubun, totalQ):
    pass
