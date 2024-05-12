import pandas as pd
from utility.setting import ui_num
from PyQt5.QtCore import QThread, pyqtSignal


class Writer(QThread):
    signal1 = pyqtSignal(tuple)
    signal2 = pyqtSignal(tuple)
    signal3 = pyqtSignal(tuple)
    signal4 = pyqtSignal(tuple)
    signal5 = pyqtSignal(tuple)
    signal6 = pyqtSignal(tuple)
    signal7 = pyqtSignal(tuple)
    signal8 = pyqtSignal(tuple)
    signal9 = pyqtSignal(str)

    def __init__(self, windowQ):
        super().__init__()
        self.windowQ = windowQ
        df           = pd.DataFrame
        self.df_list = [df, df, df, df, df, df, df, df]
        self.test    = None

    def run(self):
        gsjm_count = 0
        while True:
            try:
                data = self.windowQ.get()
                if type(data[0]) != str:
                    if data[0] <= ui_num['DB관리'] or data[0] == ui_num['기업개요']:
                        # noinspection PyUnresolvedReferences
                        self.signal1.emit(data)
                    elif ui_num['S실현손익'] <= data[0] <= ui_num['C상세기록']:
                        if data[0] == ui_num['S관심종목']:
                            if not self.test:
                                index = data[1]
                                self.df_list[index] = data[2]
                                gsjm_count += 1
                                if gsjm_count == 8:
                                    gsjm_count = 0
                                    # noinspection PyTypeChecker
                                    df = pd.concat(self.df_list)
                                    df.sort_values(by=['d_money'], ascending=False, inplace=True)
                                    # noinspection PyUnresolvedReferences
                                    self.signal2.emit((ui_num['S관심종목'], df))
                            else:
                                # noinspection PyUnresolvedReferences
                                self.signal2.emit((ui_num['S관심종목'], data[2]))
                        else:
                            # noinspection PyUnresolvedReferences
                            self.signal2.emit(data)
                    elif data[0] == ui_num['차트']:
                        # noinspection PyUnresolvedReferences
                        self.signal3.emit(data)
                    elif data[0] == ui_num['실시간차트']:
                        # noinspection PyUnresolvedReferences
                        self.signal4.emit(data)
                    elif data[0] == ui_num['풍경사진']:
                        # noinspection PyUnresolvedReferences
                        self.signal7.emit(data)
                    elif data[0] in (ui_num['코스피'], ui_num['코스닥']):
                        # noinspection PyUnresolvedReferences
                        self.signal5.emit(data)
                    elif data[0] >= ui_num['트리맵']:
                        # noinspection PyUnresolvedReferences
                        self.signal6.emit(data)
                else:
                    if data[0] == 'qsize':
                        # noinspection PyUnresolvedReferences
                        self.signal8.emit(data[1])
                    elif '라이브' in data:
                        # noinspection PyUnresolvedReferences
                        self.signal9.emit(data)
                    elif data == '복기모드시작':
                        self.test = True
                    elif data == '복기모드종료':
                        self.test = False
            except:
                pass
