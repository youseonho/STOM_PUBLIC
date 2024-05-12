import zmq
from PyQt5.QtCore import QThread


class ZmqServ(QThread):
    def __init__(self, wdzservQ_, port_num):
        super().__init__()
        self.wdzservQ_ = wdzservQ_
        self.zctx = zmq.Context()
        self.sock = self.zctx.socket(zmq.PUB)
        self.sock.bind(f'tcp://*:{port_num}')

    def run(self):
        while True:
            msg, data = self.wdzservQ_.get()
            self.sock.send_string(msg, zmq.SNDMORE)
            self.sock.send_pyobj(data)
            if data == '통신종료':
                QThread.sleep(1)
                break
        self.sock.close()
        self.zctx.term()


class ZmqRecv(QThread):
    def __init__(self, qlist_, port_num):
        super().__init__()
        """
        windowQ, soundQ, queryQ, teleQ, chartQ, hogaQ, webcQ, backQ, creceivQ, ctraderQ,  cstgQ, liveQ, kimpQ, wdzservQ
           0        1       2      3       4      5      6      7       8         9         10     11    12      13
        """
        self.windowQ = qlist_[0]
        self.soundQ  = qlist_[1]
        self.queryQ  = qlist_[2]
        self.teleQ   = qlist_[3]
        self.chartQ  = qlist_[4]
        self.hogaQ   = qlist_[5]
        self.liveQ   = qlist_[11]

        self.zctx = zmq.Context()
        self.sock = self.zctx.socket(zmq.SUB)
        self.sock.connect(f'tcp://localhost:{port_num}')
        self.sock.setsockopt_string(zmq.SUBSCRIBE, '')

    def run(self):
        while True:
            msg  = self.sock.recv_string()
            data = self.sock.recv_pyobj()
            if msg == 'window':
                self.windowQ.put(data)
                if data == '통신종료':
                    QThread.sleep(1)
                    break
            elif msg == 'sound':
                self.soundQ.put(data)
            elif msg == 'query':
                self.queryQ.put(data)
            elif msg == 'tele':
                self.teleQ.put(data)
            elif msg == 'chart':
                self.chartQ.put(data)
            elif msg == 'hoga':
                self.hogaQ.put(data)
            elif msg == 'live':
                self.liveQ.put(data)
            elif msg == 'qsize':
                self.windowQ.put(data)
        self.sock.close()
        self.zctx.term()
