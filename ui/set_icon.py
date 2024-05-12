from PyQt5.QtGui import QIcon
from utility.setting import ICON_PATH


class SetIcon:
    def __init__(self, ui_class):
        self.ui = ui_class
        self.set()

    def set(self):
        self.ui.icon_main    = QIcon(f'{ICON_PATH}/python.png')
        self.ui.icon_stock   = QIcon(f'{ICON_PATH}/stock.png')
        self.ui.icon_coin    = QIcon(f'{ICON_PATH}/coin.png')
        self.ui.icon_set     = QIcon(f'{ICON_PATH}/set.png')
        self.ui.icon_live    = QIcon(f'{ICON_PATH}/live.png')
        self.ui.icon_log     = QIcon(f'{ICON_PATH}/log.png')
        self.ui.icon_log2    = QIcon(f'{ICON_PATH}/log2.png')
        self.ui.icon_total   = QIcon(f'{ICON_PATH}/total.png')
        self.ui.icon_start   = QIcon(f'{ICON_PATH}/start.png')
        self.ui.icon_dbdel   = QIcon(f'{ICON_PATH}/dbdel.png')
        self.ui.icon_stocks  = QIcon(f'{ICON_PATH}/stocks.png')
        self.ui.icon_stocks2 = QIcon(f'{ICON_PATH}/stocks2.png')
        self.ui.icon_coins   = QIcon(f'{ICON_PATH}/coins.png')
        self.ui.icon_coins2  = QIcon(f'{ICON_PATH}/coins2.png')

        self.ui.icon_open    = QIcon(f'{ICON_PATH}/open.bmp')
        self.ui.icon_high    = QIcon(f'{ICON_PATH}/high.bmp')
        self.ui.icon_low     = QIcon(f'{ICON_PATH}/low.bmp')
        self.ui.icon_up      = QIcon(f'{ICON_PATH}/up.bmp')
        self.ui.icon_down    = QIcon(f'{ICON_PATH}/down.bmp')
        self.ui.icon_vi      = QIcon(f'{ICON_PATH}/vi.bmp')
        self.ui.icon_totals  = QIcon(f'{ICON_PATH}/totals.bmp')
        self.ui.icon_totalb  = QIcon(f'{ICON_PATH}/totalb.bmp')
