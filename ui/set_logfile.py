import logging
from utility.static import strf_time


class SetLogFile:
    def __init__(self, ui_class):
        self.ui = ui_class
        self.set()

    def set(self):
        name = strf_time('%Y%m%d')
        if self.ui.dict_set['주식트레이더']:
            self.ui.log1 = self.setLog('TraderStock', f"./_log/ST_{name}.txt")
            self.ui.log2 = self.setLog('ReceiverStock', f"./_log/SR_{name}.txt")
            self.ui.log3 = self.setLog('StockOrder', f"./_log/SO_{name}.txt")
        if self.ui.dict_set['코인트레이더']:
            self.ui.log4 = self.setLog('TraderCoin', f"./_log/CT_{name}.txt")
            self.ui.log5 = self.setLog('ReceiverCoin', f"./_log/CT_{name}.txt")
        self.ui.log6 = self.setLog('Backtester', f"./_log/BK_{name}.txt")

    @staticmethod
    def setLog(name, filename):
        log = logging.getLogger(name)
        log.setLevel(logging.INFO)
        log.addHandler(logging.FileHandler(filename=filename, encoding='utf-8'))
        return log
