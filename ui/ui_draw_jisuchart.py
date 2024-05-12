from utility.setting import ui_num
from utility.static import error_decorator


class DrawRealJisuChart:
    def __init__(self, ui):
        self.ui = ui

    @error_decorator
    def draw_realjisuchart(self, data):
        if not self.ui.dialog_jisu.isVisible():
            return

        gubun, xticks, ydatas = data
        if gubun == ui_num['코스피']:
            if 40 not in self.ui.ctpg_tik_item.keys():
                self.ui.ctpg_tik_item[40] = self.ui.jspg[1].plot(x=xticks, y=ydatas, pen=(255, 0, 0))
                self.ui.jspg[1].enableAutoRange()
            else:
                self.ui.ctpg_tik_item[40].setData(x=xticks, y=ydatas)
        elif gubun == ui_num['코스닥']:
            if 41 not in self.ui.ctpg_tik_item.keys():
                self.ui.ctpg_tik_item[41] = self.ui.jspg[2].plot(x=xticks, y=ydatas, pen=(0, 0, 255))
                self.ui.jspg[2].enableAutoRange()
            else:
                self.ui.ctpg_tik_item[41].setData(x=xticks, y=ydatas)
