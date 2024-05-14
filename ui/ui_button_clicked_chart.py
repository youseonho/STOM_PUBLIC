import random
import sqlite3
import pandas as pd
from multiprocessing import Process
from PyQt5.QtWidgets import QMessageBox
from coin.strategy_upbit import StrategyUpbit
from coin.simulator_upbit import ReceiverUpbit2, TraderUpbit2
from coin.strategy_binance_future import StrategyBinanceFuture
from coin.simulator_binance import ReceiverBinanceFuture2, TraderBinanceFuture2
from ui.set_text import famous_saying
from utility.setting import DB_PATH, DB_SETTING
from utility.static import qtest_qwait, threading_timer


def ct_button_clicked_01(ui, wdzservQ, qlist):
    if not ui.SimulatorProcessAlive():
        code = ui.ct_lineEdittttt_04.text()
        gubun = '업비트' if 'KRW' in code else '바이낸스선물' if 'USDT' in code else '주식'
        if gubun == '업비트':
            if ui.CoinStrategyProcessAlive():
                QMessageBox.critical(ui.dialog_test, '오류 알림', '코인 전략연산 프로세스가 실행중입니다.\n 트레이더을 작동 중지 설정하여 프로그램을 재구동하십시오.')
                return
        elif gubun == '바이낸스선물':
            if ui.CoinStrategyProcessAlive():
                QMessageBox.critical(ui.dialog_test, '오류 알림', '코인 전략연산 프로세스가 실행중입니다.\n 트레이더을 작동 중지 설정하여 프로그램을 재구동하십시오.')
                return

        elif gubun == '업비트':
            ui.proc_simulator_rv = Process(target=ReceiverUpbit2, args=(qlist,), daemon=True)
            ui.proc_simulator_td = Process(target=TraderUpbit2, args=(qlist,), daemon=True)
            ui.proc_strategy_coin = Process(target=StrategyUpbit, args=(qlist,), daemon=True)
        else:
            ui.proc_simulator_rv = Process(target=ReceiverBinanceFuture2, args=(qlist,), daemon=True)
            ui.proc_simulator_td = Process(target=TraderBinanceFuture2, args=(qlist,), daemon=True)
            ui.proc_strategy_coin = Process(target=StrategyBinanceFuture, args=(qlist,), daemon=True)

        if gubun == '주식':
            wdzservQ.put(('manager', '시뮬레이터구동'))
            ui.stock_simulator_alive = True
        else:
            ui.proc_strategy_coin.start()
            ui.proc_simulator_td.start()
            ui.proc_simulator_rv.start()
        qtest_qwait(2)
        QMessageBox.information(ui.dialog_test, '알림', '시뮬레이터 엔진 구동 완료')
    else:
        buttonReply = QMessageBox.question(
            ui.dialog_test, '시뮬엔진', '이미 시뮬레이터 엔진이 구동중입니다.\n엔진을 재시작하시겠습니까?\n',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if buttonReply == QMessageBox.Yes:
            ui.ctButtonClicked_02()
            ui.ctButtonClicked_01()


def ct_button_clicked_02(ui, wdzservQ):
    if ui.SimulatorProcessAlive():
        if ui.proc_simulator_rv is not None and ui.proc_simulator_rv.is_alive():
            ui.proc_simulator_rv.kill()
        if ui.proc_simulator_td is not None and ui.proc_simulator_td.is_alive():
            ui.proc_simulator_td.kill()
        if ui.CoinStrategyProcessAlive():
            ui.proc_strategy_coin.kill()
        wdzservQ.put(('manager', '시뮬레이터종료'))
        ui.stock_simulator_alive = False
    qtest_qwait(3)
    QMessageBox.information(ui.dialog_test, '알림', '시뮬레이터 엔진 종료 완료')


def ct_button_clicked_03(ui, windowQ, wdzservQ, cstgQ):
    code = ui.ct_lineEdittttt_04.text()
    if code == '':
        QMessageBox.critical(ui.dialog_test, '오류 알림', '종목코드가 입력되지 않았습니다.\n')
        return
    if ui.tt_lineEdittttt_01.text() == '':
        QMessageBox.critical(ui.dialog_test, '오류 알림', '시작시간이 입력되지 않았습니다.\n')
        return
    if ui.tt_lineEdittttt_02.text() == '':
        QMessageBox.critical(ui.dialog_test, '오류 알림', '종료시간 입력되지 않았습니다.\n')
        return
    if not ui.SimulatorProcessAlive():
        QMessageBox.critical(ui.dialog_test, '오류 알림', '시뮬레이터용 엔진이 미실행중입니다.\n')
        return

    gubun = '업비트' if 'KRW' in code else '바이낸스선물' if 'USDT' in code else '주식'
    date = ui.ct_dateEdittttt_01.date().toString('yyyyMMdd')
    start_time = int(ui.tt_lineEdittttt_01.text())
    end_time = int(ui.tt_lineEdittttt_02.text())
    qtest_qwait(1)

    ui.ChartClear()
    if gubun == '주식':
        wdzservQ.put(('simul_strategy', ('차트종목코드', code)))
        wdzservQ.put(('simul_strategy', ('관심목록', (code,))))
    else:
        cstgQ.put(('차트종목코드', code))
        cstgQ.put(('관심목록', (code,), (code,)))
    windowQ.put('복기모드시작')

    try:
        file_first_name = 'stock_tick_' if gubun == '주식' else 'coin_tick_'
        con = sqlite3.connect(f'{DB_PATH}/{file_first_name}{date}.db')
        df = pd.read_sql(f'SELECT * FROM "{code}" WHERE "index" LIKE "{date}%"', con)
        con.close()
    except:
        print('일자별 디비에 해당 종목의 데이터가 존재하지 않습니다.')
    else:
        df['구분시간'] = df['index'].apply(lambda x: int(str(x)[8:]))
        df = df[(df['구분시간'] >= start_time) & (df['구분시간'] <= end_time)]
        df.set_index('index', inplace=True)
        ui.df_test = df.drop(columns=['구분시간'])
        ui.ct_test = 0
        ui.TickInput(code, gubun)


def ct_button_clicked_04(ui):
    if not ui.test_pause:
        ui.test_pause = True
        ui.tt_pushButtonnn_04.setText('재시작')
    else:
        ui.test_pause = False
        ui.tt_pushButtonnn_04.setText('일시정지')
        code = ui.ct_lineEdittttt_04.text()
        gubun = '업비트' if 'KRW' in code else '바이낸스선물' if 'USDT' in code else '주식'
        ui.TickInput(code, gubun)


def ct_button_clicked_05(ui):
    ui.df_test = None


def ct_button_clicked_06(ui):
    ui.dialog_test.close()


def ct_button_clicked_07(ui):
    k = ['5', '2', '2', '0', '12', '26', '9', '12', '26', '0', '12', '26', '0', '5', '0.7', '0.5', '0.05', '30', '14',
         '10', '10']
    for i, linedit in enumerate(ui.factor_linedit_list):
        linedit.setText(k[i])


def ct_button_clicked_08(ui):
    con = sqlite3.connect(DB_SETTING)
    df = pd.read_sql('SELECT * FROM back', con)
    k_list = df['보조지표설정'][0]
    k_list = k_list.split(';')
    con.close()
    for i, linedit in enumerate(ui.factor_linedit_list):
        linedit.setText(k_list[i])


def ct_button_clicked_09(ui, proc_query, queryQ):
    k_list = []
    for linedit in ui.factor_linedit_list:
        k_list.append(linedit.text())
    k_list = ';'.join(k_list)
    if proc_query.is_alive():
        query = f"UPDATE back SET 보조지표설정 = '{k_list}'"
        queryQ.put(('설정디비', query))
    QMessageBox.information(ui.dialog_factor, '저장 완료', random.choice(famous_saying))


def get_k_list(ui):
    k_list = []
    for linedit in ui.factor_linedit_list:
        k_list.append(linedit.text())
    k_list = [int(x) if '.' not in x else float(x) for x in k_list]
    return k_list


def tick_put(ui, code, gubun, windowQ, wdzservQ, ctraderQ, creceivQ, cstgQ):
    try:
        dt = ui.df_test.index[ui.ct_test]
        data = tuple(ui.df_test.iloc[ui.ct_test])
        if gubun == '주식':
            wdzservQ.put(('trader', ('복기모드시간', str(dt))))
            wdzservQ.put(('receiver', (dt,) + data + (code,)))
        else:
            ctraderQ.put(('복기모드시간', str(dt)))
            creceivQ.put((dt,) + data + (code,))
        ui.ct_test += 1
        speed = int(ui.tt_comboBoxxxxx_01.currentText())
        if not ui.test_pause:
            data = [ui, code, gubun, windowQ, wdzservQ, ctraderQ, creceivQ, cstgQ]
            threading_timer(round(1 / speed, 2), tick_put, data)
    except:
        if gubun == '주식':
            wdzservQ.put(('simul_strategy', ('관심목록', ())))
            wdzservQ.put(('simul_strategy', '복기모드종료'))
        else:
            cstgQ.put(('관심목록', ()))
            cstgQ.put('복기모드종료')
        windowQ.put('복기모드종료')
        ui.ct_test = 0
        ui.test_pause = False
        qtest_qwait(2)
        ui.ChartClear()
