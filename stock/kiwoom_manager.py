import os
import sys
import zmq
import win32gui
import subprocess
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, QTimer, pyqtSignal
from multiprocessing import Process, Queue
from trader_kiwoom import TraderKiwoom
from receiver_kiwoom import ReceiverKiwoom
from strategy_kiwoom import StrategyKiwoom
from stock.simulator_kiwoom import ReceiverKiwoom2, TraderKiwoom2
from login_kiwoom.manuallogin import find_window
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utility.setting import DICT_SET, LOGIN_PATH
from utility.static import now, timedelta_sec, int_hms, qtest_qwait, opstarter_kill, get_port_number


class ZmqRecv(QThread):
    signal1 = pyqtSignal(str)
    signal2 = pyqtSignal(tuple)

    def __init__(self, main, qlist, port_num):
        super().__init__()
        self.main     =  main
        self.sreceivQ = qlist[1]
        self.straderQ = qlist[2]
        self.sstgQs   = qlist[3]

        self.zctx = zmq.Context()
        self.sock = self.zctx.socket(zmq.SUB)
        self.sock.connect(f'tcp://localhost:{port_num}')
        self.sock.setsockopt_string(zmq.SUBSCRIBE, '')

    def run(self):
        while True:
            msg  = self.sock.recv_string()
            data = self.sock.recv_pyobj()
            if msg == 'receiver':
                self.sreceivQ.put(data)
            elif msg == 'trader':
                self.straderQ.put(data)
            elif msg == 'strategy':
                if data[0] == '차트종목코드':
                    count = data[-1]
                    for i, q in enumerate(self.sstgQs):
                        if i == count:
                            q.put(data[:2])
                        else:
                            q.put(data[:2])
                else:
                    for q in self.sstgQs:
                        q.put(data)
            elif msg == 'manager':
                if type(data) == str:
                    # noinspection PyUnresolvedReferences
                    self.signal1.emit(data)
                elif type(data) == tuple:
                    # noinspection PyUnresolvedReferences
                    self.signal2.emit(data)
                if data == '통신종료':
                    QThread.sleep(1)
                    break
            elif msg == 'simul_strategy':
                self.sstgQs[0].put(data)
        self.sock.close()
        self.zctx.term()


class ZmqServ(QThread):
    def __init__(self, qlist, port_num):
        super().__init__()
        self.kwzservQ = qlist[0]
        self.sreceivQ = qlist[1]
        self.straderQ = qlist[2]
        self.sstgQs   = qlist[3]

        self.zctx = zmq.Context()
        self.sock = self.zctx.socket(zmq.PUB)
        self.sock.bind(f'tcp://*:{port_num}')

    def run(self):
        int_hms_ = int_hms()
        while True:
            msg, data = self.kwzservQ.get()
            self.sock.send_string(msg, zmq.SNDMORE)
            self.sock.send_pyobj(data)
            if int_hms() > int_hms_:
                sstgQs_size = sum([q.qsize() for q in self.sstgQs])
                qsize_data  = ('qsize', (self.sreceivQ.qsize(), self.straderQ.qsize(), sstgQs_size))
                self.sock.send_string('qsize', zmq.SNDMORE)
                self.sock.send_pyobj(qsize_data)
                int_hms_ = int_hms()
            if type(data) == str and data == '통신종료':
                QThread.sleep(1)
                break
        self.sock.close()
        self.zctx.term()


class KiwoomManager:
    def __init__(self):
        app = QApplication(sys.argv)

        self.kwzservQ, self.sreceivQ, self.straderQ, sstg1Q, sstg2Q, sstg3Q, sstg4Q, sstg5Q, sstg6Q, sstg7Q, sstg8Q = \
            Queue(), Queue(), Queue(), Queue(), Queue(), Queue(), Queue(), Queue(), Queue(), Queue(), Queue()
        self.sstgQs   = [sstg1Q, sstg2Q, sstg3Q, sstg4Q, sstg5Q, sstg6Q, sstg7Q, sstg8Q]
        self.qlist    = [self.kwzservQ, self.sreceivQ, self.straderQ, self.sstgQs]
        self.dict_set = DICT_SET
        self.int_time = int_hms()

        self.backtest_engine      = False
        self.daydata_download     = False
        self.proc_receiver_stock  = None
        self.proc_strategy_stock1 = None
        self.proc_strategy_stock2 = None
        self.proc_strategy_stock3 = None
        self.proc_strategy_stock4 = None
        self.proc_strategy_stock5 = None
        self.proc_strategy_stock6 = None
        self.proc_strategy_stock7 = None
        self.proc_strategy_stock8 = None
        self.proc_trader_stock    = None
        self.proc_simulator_rv    = None
        self.proc_simulator_td    = None

        port_num = get_port_number()
        self.zmqserv = ZmqServ(self.qlist, port_num + 1)
        self.zmqserv.start()

        self.zmqrecv = ZmqRecv(self, self.qlist, port_num)
        # noinspection PyUnresolvedReferences
        self.zmqrecv.signal1.connect(self.UpdateString)
        # noinspection PyUnresolvedReferences
        self.zmqrecv.signal2.connect(self.UpdateTuple)
        self.zmqrecv.start()

        self.qtimer1 = QTimer()
        self.qtimer1.setInterval(1 * 1000)
        # noinspection PyUnresolvedReferences
        self.qtimer1.timeout.connect(self.ProcessStarter)
        self.qtimer1.start()

        app.exec_()

    def UpdateString(self, data):
        if data == '주식수동시작':
            self.StockManualStart()
        elif data == '시뮬레이터구동':
            self.SimulatorStart()
        elif data == '시뮬레이터종료':
            self.SimulatorProcessKill()
        elif data == '리시버 종료':
            self.StockReceiverProcessKill()
        elif data == '전략연산 종료':
            self.StockStrategyProcessKill()
        elif data == '트레이더 종료':
            self.StockTraderProcessKill()
        elif data == '통신종료':
            self.ManagerProcessKill()
        elif data == '백테엔진구동':
            self.backtest_engine = True

    def UpdateTuple(self, data):
        if data[0] == '설정변경':
            self.dict_set = data[1]
            if self.StockStrategyProcessAlive():
                for q in self.sstgQs:
                    q.put(('설정변경', self.dict_set))
            if self.StockReceiverProcessAlive():
                self.sreceivQ.put(('설정변경', self.dict_set))
            if self.StockTraderProcessAlive():
                self.straderQ.put(('설정변경', self.dict_set))

    def StockManualStart(self):
        if self.backtest_engine:
            print('백테엔진 구동 중에는 로그인할 수 없습니다.')
            return
        if self.dict_set['아이디2'] is None:
            print('두번째 계정이 설정되지 않아 리시버를 시작할 수 없습니다. 계정 설정 후 다시 시작하십시오.')
        elif self.dict_set['주식리시버'] and not self.StockReceiverProcessAlive():
            self.StockReceiverStart()
        if self.dict_set['아이디1'] is None:
            print('첫번째 계정이 설정되지 않아 트레이더를 시작할 수 없습니다. 계정 설정 후 다시 시작하십시오.')
        elif self.dict_set['주식트레이더'] and self.StockReceiverProcessAlive() and not self.StockTraderProcessAlive():
            self.StockTraderStart()

    def SimulatorStart(self):
        if self.backtest_engine:
            print('백테엔진 구동 중에는 시뮬레이터를 실행할 수 없습니다.')
            return
        self.proc_simulator_rv    = Process(target=ReceiverKiwoom2, args=(self.qlist,), daemon=True)
        self.proc_simulator_td    = Process(target=TraderKiwoom2, args=(self.qlist,), daemon=True)
        self.proc_strategy_stock1 = Process(target=StrategyKiwoom, args=(0, self.qlist,), daemon=True)
        self.proc_strategy_stock1.start()
        self.proc_simulator_td.start()
        self.proc_simulator_rv.start()

    def SimulatorProcessKill(self):
        if self.SimulatorProcessAlive():
            self.proc_simulator_td.kill()
            self.proc_simulator_rv.kill()
            self.proc_strategy_stock1.kill()

    def StockReceiverProcessKill(self):
        if self.StockReceiverProcessAlive():
            self.proc_receiver_stock.kill()

    def StockStrategyProcessKill(self):
        if self.StockStrategyProcessAlive():
            try:
                self.proc_strategy_stock1.kill()
                self.proc_strategy_stock2.kill()
                self.proc_strategy_stock3.kill()
                self.proc_strategy_stock4.kill()
                self.proc_strategy_stock5.kill()
                self.proc_strategy_stock6.kill()
                self.proc_strategy_stock7.kill()
                self.proc_strategy_stock8.kill()
            except:
                pass

    def StockTraderProcessKill(self):
        if self.StockTraderProcessAlive():
            self.proc_trader_stock.kill()

    def ManagerProcessKill(self):
        self.kwzservQ.put(('window', '통신종료'))
        self.SimulatorProcessKill()
        self.StockReceiverProcessKill()
        self.StockStrategyProcessKill()
        self.StockTraderProcessKill()
        qtest_qwait(3)
        sys.exit()

    def ProcessStarter(self):
        inthms = int_hms()
        if not self.backtest_engine:
            if self.int_time < self.dict_set['리시버실행시간'] <= inthms and self.dict_set['주식리시버'] and not self.StockReceiverProcessAlive():
                self.StockReceiverStart()
            if self.int_time < self.dict_set['트레이더실행시간'] <= inthms and self.dict_set['주식트레이더'] and self.StockReceiverProcessAlive() and not self.StockTraderProcessAlive():
                self.StockTraderStart()
        self.int_time = inthms

    @staticmethod
    def OpenapiLoginWait():
        result = True
        lwopen = True
        update = False

        time_out_open = timedelta_sec(10)
        while find_window('Open API login') == 0:
            if now() > time_out_open:
                result = False
                lwopen = False
                print('로그인 오류 알림 : 로그인창이 열리지 않아 잠시 후 재시도합니다.')
                break
            qtest_qwait(0.1)

        if lwopen:
            time_out_update = timedelta_sec(30)
            time_out_close  = timedelta_sec(90)
            while find_window('Open API login') != 0:
                if not update:
                    try:
                        text = win32gui.GetWindowText(win32gui.GetDlgItem(find_window('Open API login'), 0x40D))
                        if '다운로드' in text or '분석' in text or '기동' in text:
                            update = True
                    except:
                        pass
                    if now() > time_out_update:
                        result = False
                        print('로그인 오류 알림 : 업데이트가 확인되지 않아 잠시 후 재시도합니다.')
                        break
                if now() > time_out_close:
                    result = False
                    print('로그인 오류 알림 : 업데이트 제한 시간 초과로 잠시 후 재시도합니다.')
                    break
                qtest_qwait(0.01)

        if not result: opstarter_kill()

        return result

    def StockVersionUp(self):
        subprocess.Popen(f'python {LOGIN_PATH}/versionupdater.py')
        while not self.OpenapiLoginWait():
            qtest_qwait(0.1)
            subprocess.Popen(f'python {LOGIN_PATH}/versionupdater.py')
        qtest_qwait(10)

    def StockAutoLogin1(self):
        subprocess.Popen(f'python {LOGIN_PATH}/autologin1.py')
        while not self.OpenapiLoginWait():
            qtest_qwait(0.1)
            subprocess.Popen(f'python {LOGIN_PATH}/autologin1.py')
        qtest_qwait(5)

    def StockAutoLogin2(self):
        subprocess.Popen(f'python {LOGIN_PATH}/autologin2.py')
        while not self.OpenapiLoginWait():
            qtest_qwait(0.1)
            subprocess.Popen(f'python {LOGIN_PATH}/autologin2.py')
        qtest_qwait(5)

    def StockReceiverStart(self):
        if self.dict_set['아이디2'] is not None:
            if self.dict_set['버전업']:
                self.StockVersionUp()
            self.StockAutoLogin2()

            while True:
                qtest_qwait(0.1)
                if not self.StockReceiverProcessAlive():
                    self.proc_receiver_stock = Process(target=ReceiverKiwoom, args=(self.qlist,), daemon=True)
                    self.proc_receiver_stock.start()
                    if self.OpenapiLoginWait():
                        break
                    else:
                        self.proc_receiver_stock.kill()
                        print('로그인 또는 업데이트 실패, 잠시 후 재접속합니다.')
        else:
            print('두번째 계정이 설정되지 않아 리시버를 시작할 수 없습니다. 계정 설정 후 다시 시작하십시오.')

    def StockTraderStart(self):
        if self.dict_set['아이디1'] is not None:
            self.StockAutoLogin1()
            self.proc_strategy_stock1 = Process(target=StrategyKiwoom, args=(0, self.qlist), daemon=True)
            self.proc_strategy_stock2 = Process(target=StrategyKiwoom, args=(1, self.qlist), daemon=True)
            self.proc_strategy_stock3 = Process(target=StrategyKiwoom, args=(2, self.qlist), daemon=True)
            self.proc_strategy_stock4 = Process(target=StrategyKiwoom, args=(3, self.qlist), daemon=True)
            self.proc_strategy_stock5 = Process(target=StrategyKiwoom, args=(4, self.qlist), daemon=True)
            self.proc_strategy_stock6 = Process(target=StrategyKiwoom, args=(5, self.qlist), daemon=True)
            self.proc_strategy_stock7 = Process(target=StrategyKiwoom, args=(6, self.qlist), daemon=True)
            self.proc_strategy_stock8 = Process(target=StrategyKiwoom, args=(7, self.qlist), daemon=True)
            self.proc_strategy_stock1.start()
            self.proc_strategy_stock2.start()
            self.proc_strategy_stock3.start()
            self.proc_strategy_stock4.start()
            self.proc_strategy_stock5.start()
            self.proc_strategy_stock6.start()
            self.proc_strategy_stock7.start()
            self.proc_strategy_stock8.start()
            while True:
                qtest_qwait(1)
                if not self.StockTraderProcessAlive():
                    self.proc_trader_stock = Process(target=TraderKiwoom, args=(self.qlist,), daemon=True)
                    self.proc_trader_stock.start()
                    if self.OpenapiLoginWait():
                        break
                    else:
                        self.proc_trader_stock.kill()
        else:
            print('첫번째 계정이 설정되지 않아 트레이더를 시작할 수 없습니다. 계정 설정 후 다시 시작하십시오.')

    def StockReceiverProcessAlive(self):
        return self.proc_receiver_stock is not None and self.proc_receiver_stock.is_alive()

    def StockTraderProcessAlive(self):
        return self.proc_trader_stock is not None and self.proc_trader_stock.is_alive()

    def StockStrategyProcessAlive(self):
        return self.proc_strategy_stock1 is not None and self.proc_strategy_stock1.is_alive()

    def SimulatorProcessAlive(self):
        return self.proc_simulator_rv is not None and self.proc_simulator_rv.is_alive() and self.proc_simulator_td is not None and self.proc_simulator_td.is_alive()


if __name__ == '__main__':
    KiwoomManager()
