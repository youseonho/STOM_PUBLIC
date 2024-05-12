import win32gui
import pyqtgraph as pg
from PyQt5.QtWidgets import QMessageBox
from ui.ui_crosshair import CrossHair
from ui.ui_get_label_text import get_label_text
from utility.chart_items import ChuseItem
from ui.set_style import qfont12, color_fg_bt, color_bg_bt, color_bg_ld
from stock.login_kiwoom.manuallogin import leftClick, enter_keys, press_keys
from utility.setting import list_stock, list_coin
from utility.static import error_decorator, strf_time, from_timestamp, thread_decorator


class DrawChart:
    def __init__(self, ui):
        self.ui = ui
        self.crosshair = CrossHair(self.ui)

    @error_decorator
    def draw_chart(self, data):
        def ci(fname):
            return list_stock.index(fname) if not coin else list_coin.index(fname)

        self.ui.ChartClear()
        if not self.ui.dialog_chart.isVisible():
            return

        coin, self.ui.ctpg_tik_xticks, self.ui.ctpg_tik_arry, self.ui.buy_index, self.ui.sell_index = data[1:]
        if coin == '차트오류':
            QMessageBox.critical(self.ui.dialog_chart, '오류 알림', '해당 날짜의 데이터가 존재하지 않습니다.\n')
            return

        xmin, xmax = self.ui.ctpg_tik_xticks[0], self.ui.ctpg_tik_xticks[-1]
        hms  = from_timestamp(xmax).strftime('%H:%M:%S')
        code = self.ui.ct_lineEdittttt_04.text()
        date = strf_time('%Y%m%d', from_timestamp(xmin))
        if not coin: self.KiwoomHTSChart(code, date)

        if self.ui.ct_pushButtonnn_04.text() == 'CHART 8':
            chart_count = 8
        elif self.ui.ct_pushButtonnn_04.text() == 'CHART 12':
            chart_count = 12
        else:
            chart_count = 16

        self.ui.ctpg_tik_factors = []
        if self.ui.ct_checkBoxxxxx_01.isChecked():     self.ui.ctpg_tik_factors.append('현재가')
        if self.ui.ct_checkBoxxxxx_02.isChecked():     self.ui.ctpg_tik_factors.append('체결강도')
        if self.ui.ct_checkBoxxxxx_03.isChecked():     self.ui.ctpg_tik_factors.append('초당거래대금')
        if self.ui.ct_checkBoxxxxx_04.isChecked():     self.ui.ctpg_tik_factors.append('초당체결수량')
        if self.ui.ct_checkBoxxxxx_05.isChecked():     self.ui.ctpg_tik_factors.append('등락율')
        if self.ui.ct_checkBoxxxxx_06.isChecked():     self.ui.ctpg_tik_factors.append('고저평균대비등락율')
        if self.ui.ct_checkBoxxxxx_07.isChecked():     self.ui.ctpg_tik_factors.append('호가총잔량')
        if self.ui.ct_checkBoxxxxx_08.isChecked():     self.ui.ctpg_tik_factors.append('1호가잔량')
        if self.ui.ct_checkBoxxxxx_09.isChecked():     self.ui.ctpg_tik_factors.append('매도수5호가잔량합')
        if self.ui.ct_checkBoxxxxx_10.isChecked():     self.ui.ctpg_tik_factors.append('당일거래대금')
        if self.ui.ct_checkBoxxxxx_11.isChecked():     self.ui.ctpg_tik_factors.append('누적초당매도수수량')
        if self.ui.ct_checkBoxxxxx_12.isChecked():     self.ui.ctpg_tik_factors.append('등락율각도')
        if self.ui.ct_checkBoxxxxx_13.isChecked():     self.ui.ctpg_tik_factors.append('당일거래대금각도')
        if not coin:
            if self.ui.ct_checkBoxxxxx_14.isChecked(): self.ui.ctpg_tik_factors.append('거래대금증감')
            if self.ui.ct_checkBoxxxxx_15.isChecked(): self.ui.ctpg_tik_factors.append('전일비')
            if self.ui.ct_checkBoxxxxx_16.isChecked(): self.ui.ctpg_tik_factors.append('회전율')
            if self.ui.ct_checkBoxxxxx_17.isChecked(): self.ui.ctpg_tik_factors.append('전일동시간비')
            if self.ui.ct_checkBoxxxxx_18.isChecked(): self.ui.ctpg_tik_factors.append('전일비각도')
        if self.ui.ct_checkBoxxxxx_19.isChecked():     self.ui.ctpg_tik_factors.append('BBAND')
        if self.ui.ct_checkBoxxxxx_20.isChecked():     self.ui.ctpg_tik_factors.append('MACD')
        if self.ui.ct_checkBoxxxxx_21.isChecked():     self.ui.ctpg_tik_factors.append('APO')
        if self.ui.ct_checkBoxxxxx_22.isChecked():     self.ui.ctpg_tik_factors.append('KAMA')
        if self.ui.ct_checkBoxxxxx_23.isChecked():     self.ui.ctpg_tik_factors.append('RSI')
        if self.ui.ct_checkBoxxxxx_24.isChecked():     self.ui.ctpg_tik_factors.append('HT_SINE, HT_LSINE')
        if self.ui.ct_checkBoxxxxx_25.isChecked():     self.ui.ctpg_tik_factors.append('HT_PHASE, HT_QUDRA')
        if self.ui.ct_checkBoxxxxx_26.isChecked():     self.ui.ctpg_tik_factors.append('OBV')

        for i in range(len(self.ui.ctpg_tik_arry[0, :])):
            tick_arry = self.ui.ctpg_tik_arry[:, i]
            if i in (ci('등락율'), ci('초당매수수량'), ci('초당매도수량'), ci('고저평균대비등락율'), ci('초당거래대금'),
                     ci('초당거래대금평균'), ci('등락율각도'), ci('당일거래대금각도'), ci('전일비각도'), ci('관심종목'),
                     ci('APO'), ci('HT_SINE'), ci('HT_LSINE'), ci('HT_PHASE'), ci('HT_QUDRA'), ci('OBV')):
                self.ui.ctpg_tik_data[i] = tick_arry
            else:
                self.ui.ctpg_tik_data[i] = tick_arry[tick_arry != 0]

        len_list = []
        tlen = len(self.ui.ctpg_tik_xticks)
        for data in list(self.ui.ctpg_tik_data.values()):
            len_list.append(tlen - len(data))
        gsjm_arry   = self.ui.ctpg_tik_arry[:, ci('관심종목')]
        chuse_exist = True if len(gsjm_arry[gsjm_arry > 0]) > 0 else False

        for i, factor in enumerate(self.ui.ctpg_tik_factors):
            self.ui.ctpg[i].clear()
            if factor == '현재가':
                ymax = self.ui.ctpg_tik_data[ci('현재가')].max()
                ymin = self.ui.ctpg_tik_data[ci('현재가')].min()
                if chuse_exist: self.ui.ctpg[i].addItem(ChuseItem(self.ui.ctpg_tik_arry[:, ci('관심종목')], ymin, ymax, self.ui.ctpg_tik_xticks))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('이동평균60')]:], y=self.ui.ctpg_tik_data[ci('이동평균60')], pen=(180, 180, 180))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('이동평균300')]:], y=self.ui.ctpg_tik_data[ci('이동평균300')], pen=(140, 140, 140))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('이동평균600')]:], y=self.ui.ctpg_tik_data[ci('이동평균600')], pen=(100, 100, 100))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('이동평균1200')]:], y=self.ui.ctpg_tik_data[ci('이동평균1200')], pen=(60, 60, 60))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('현재가')]:], y=self.ui.ctpg_tik_data[ci('현재가')], pen=(200, 100, 100))
                for j, price in enumerate(self.ui.ctpg_tik_arry[:, ci('매수가')]):
                    if price > 0:
                        arrow = pg.ArrowItem(angle=-180, tipAngle=60, headLen=10, pen='w', brush='r')
                        arrow.setPos(self.ui.ctpg_tik_xticks[j], price)
                        self.ui.ctpg[i].addItem(arrow)
                for j, price in enumerate(self.ui.ctpg_tik_arry[:, ci('매도가')]):
                    if price > 0:
                        arrow = pg.ArrowItem(angle=0, tipAngle=60, headLen=10, pen='w', brush='b')
                        arrow.setPos(self.ui.ctpg_tik_xticks[j], price)
                        self.ui.ctpg[i].addItem(arrow)
                if 'USDT' in code:
                    for j, price in enumerate(self.ui.ctpg_tik_arry[:, ci('매수가2')]):
                        if price > 0:
                            arrow = pg.ArrowItem(angle=-180, tipAngle=60, headLen=10, pen='w', brush='m')
                            arrow.setPos(self.ui.ctpg_tik_xticks[j], price)
                            self.ui.ctpg[i].addItem(arrow)
                    for j, price in enumerate(self.ui.ctpg_tik_arry[:, ci('매도가2')]):
                        if price > 0:
                            arrow = pg.ArrowItem(angle=0, tipAngle=60, headLen=10, pen='w', brush='b')
                            arrow.setPos(self.ui.ctpg_tik_xticks[j], price)
                            self.ui.ctpg[i].addItem(arrow)
            elif factor == '체결강도':
                ymax = max(self.ui.ctpg_tik_data[ci('체결강도')].max(), self.ui.ctpg_tik_data[ci('최고체결강도')].max())
                ymin = min(self.ui.ctpg_tik_data[ci('체결강도')].min(), self.ui.ctpg_tik_data[ci('최저체결강도')].min())
                if chuse_exist: self.ui.ctpg[i].addItem(ChuseItem(self.ui.ctpg_tik_arry[:, ci('관심종목')], ymin, ymax, self.ui.ctpg_tik_xticks))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('체결강도평균')]:], y=self.ui.ctpg_tik_data[ci('체결강도평균')], pen=(100, 200, 100))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('최저체결강도')]:], y=self.ui.ctpg_tik_data[ci('최저체결강도')], pen=(100, 100, 200))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('최고체결강도')]:], y=self.ui.ctpg_tik_data[ci('최고체결강도')], pen=(200, 100, 100))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('체결강도')]:], y=self.ui.ctpg_tik_data[ci('체결강도')], pen=(100, 200, 100))
            elif factor == '초당거래대금':
                ymax = self.ui.ctpg_tik_data[ci('초당거래대금')].max()
                ymin = self.ui.ctpg_tik_data[ci('초당거래대금평균')].min()
                if chuse_exist: self.ui.ctpg[i].addItem(ChuseItem(self.ui.ctpg_tik_arry[:, ci('관심종목')], ymin, ymax, self.ui.ctpg_tik_xticks))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('초당거래대금')]:], y=self.ui.ctpg_tik_data[ci('초당거래대금')], pen=(200, 100, 100))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('초당거래대금평균')]:], y=self.ui.ctpg_tik_data[ci('초당거래대금평균')], pen=(100, 200, 100))
            elif factor == '초당체결수량':
                ymax = max(self.ui.ctpg_tik_data[ci('초당매수수량')].max(), self.ui.ctpg_tik_data[ci('초당매도수량')].max())
                ymin = min(self.ui.ctpg_tik_data[ci('초당매수수량')].min(), self.ui.ctpg_tik_data[ci('초당매도수량')].min())
                if chuse_exist: self.ui.ctpg[i].addItem(ChuseItem(self.ui.ctpg_tik_arry[:, ci('관심종목')], ymin, ymax, self.ui.ctpg_tik_xticks))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('초당매도수량')]:], y=self.ui.ctpg_tik_data[ci('초당매도수량')], pen=(100, 100, 200))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('초당매수수량')]:], y=self.ui.ctpg_tik_data[ci('초당매수수량')], pen=(200, 100, 100))
            elif factor == '호가총잔량':
                ymax = max(self.ui.ctpg_tik_data[ci('매수총잔량')].max(), self.ui.ctpg_tik_data[ci('매도총잔량')].max())
                ymin = min(self.ui.ctpg_tik_data[ci('매수총잔량')].min(), self.ui.ctpg_tik_data[ci('매도총잔량')].min())
                if chuse_exist: self.ui.ctpg[i].addItem(ChuseItem(self.ui.ctpg_tik_arry[:, ci('관심종목')], ymin, ymax, self.ui.ctpg_tik_xticks))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('매수총잔량')]:], y=self.ui.ctpg_tik_data[ci('매수총잔량')], pen=(200, 100, 100))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('매도총잔량')]:], y=self.ui.ctpg_tik_data[ci('매도총잔량')], pen=(100, 100, 200))
            elif factor == '1호가잔량':
                ymax = max(self.ui.ctpg_tik_data[ci('매수잔량1')].max(), self.ui.ctpg_tik_data[ci('매도잔량1')].max())
                ymin = min(self.ui.ctpg_tik_data[ci('매수잔량1')].min(), self.ui.ctpg_tik_data[ci('매도잔량1')].min())
                if chuse_exist: self.ui.ctpg[i].addItem(ChuseItem(self.ui.ctpg_tik_arry[:, ci('관심종목')], ymin, ymax, self.ui.ctpg_tik_xticks))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('매수잔량1')]:], y=self.ui.ctpg_tik_data[ci('매수잔량1')], pen=(200, 100, 100))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('매도잔량1')]:], y=self.ui.ctpg_tik_data[ci('매도잔량1')], pen=(100, 100, 200))
            elif factor == '누적초당매도수수량':
                ymax = max(self.ui.ctpg_tik_data[ci('누적초당매수수량')].max(), self.ui.ctpg_tik_data[ci('누적초당매도수량')].max())
                ymin = min(self.ui.ctpg_tik_data[ci('누적초당매수수량')].min(), self.ui.ctpg_tik_data[ci('누적초당매도수량')].min())
                if chuse_exist: self.ui.ctpg[i].addItem(ChuseItem(self.ui.ctpg_tik_arry[:, ci('관심종목')], ymin, ymax, self.ui.ctpg_tik_xticks))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('누적초당매도수량')]:], y=self.ui.ctpg_tik_data[ci('누적초당매도수량')], pen=(100, 100, 200))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('누적초당매수수량')]:], y=self.ui.ctpg_tik_data[ci('누적초당매수수량')], pen=(200, 100, 100))
            elif factor == 'BBAND':
                ymax = max(self.ui.ctpg_tik_data[ci('BBU')].max(), self.ui.ctpg_tik_data[ci('현재가')].max())
                ymin = min(self.ui.ctpg_tik_data[ci('BBL')].min(), self.ui.ctpg_tik_data[ci('현재가')].min())
                if chuse_exist: self.ui.ctpg[i].addItem(ChuseItem(self.ui.ctpg_tik_arry[:, ci('관심종목')], ymin, ymax, self.ui.ctpg_tik_xticks))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('BBM')]:], y=self.ui.ctpg_tik_data[ci('BBM')], pen=(100, 100, 100))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('BBL')]:], y=self.ui.ctpg_tik_data[ci('BBL')], pen=(100, 100, 200))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('BBU')]:], y=self.ui.ctpg_tik_data[ci('BBU')], pen=(100, 200, 100))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('현재가')]:], y=self.ui.ctpg_tik_data[ci('현재가')], pen=(200, 100, 100))
            elif factor == 'MACD':
                ymax = self.ui.ctpg_tik_data[ci('MACD')].max()
                ymin = self.ui.ctpg_tik_data[ci('MACD')].min()
                if chuse_exist: self.ui.ctpg[i].addItem(ChuseItem(self.ui.ctpg_tik_arry[:, ci('관심종목')], ymin, ymax, self.ui.ctpg_tik_xticks))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('MACDH')]:], y=self.ui.ctpg_tik_data[ci('MACDH')], pen=(100, 100, 100))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('MACDS')]:], y=self.ui.ctpg_tik_data[ci('MACDS')], pen=(100, 100, 200))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('MACD')]:], y=self.ui.ctpg_tik_data[ci('MACD')], pen=(100, 200, 100))
            elif factor == 'HT_SINE, HT_LSINE':
                ymax = max(self.ui.ctpg_tik_data[ci('HT_SINE')].max(), self.ui.ctpg_tik_data[ci('HT_LSINE')].max())
                ymin = min(self.ui.ctpg_tik_data[ci('HT_SINE')].min(), self.ui.ctpg_tik_data[ci('HT_LSINE')].min())
                if chuse_exist: self.ui.ctpg[i].addItem(ChuseItem(self.ui.ctpg_tik_arry[:, ci('관심종목')], ymin, ymax, self.ui.ctpg_tik_xticks))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('HT_LSINE')]:], y=self.ui.ctpg_tik_data[ci('HT_LSINE')], pen=(100, 50, 200))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('HT_SINE')]:], y=self.ui.ctpg_tik_data[ci('HT_SINE')], pen=(100, 200, 100))
            elif factor == 'HT_PHASE, HT_QUDRA':
                ymax = max(self.ui.ctpg_tik_data[ci('HT_PHASE')].max(), self.ui.ctpg_tik_data[ci('HT_QUDRA')].max())
                ymin = min(self.ui.ctpg_tik_data[ci('HT_PHASE')].min(), self.ui.ctpg_tik_data[ci('HT_QUDRA')].min())
                if chuse_exist: self.ui.ctpg[i].addItem(ChuseItem(self.ui.ctpg_tik_arry[:, ci('관심종목')], ymin, ymax, self.ui.ctpg_tik_xticks))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('HT_QUDRA')]:], y=self.ui.ctpg_tik_data[ci('HT_QUDRA')], pen=(100, 100, 200))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('HT_PHASE')]:], y=self.ui.ctpg_tik_data[ci('HT_PHASE')], pen=(100, 200, 100))
            else:
                pen  = (100, 200, 100) if (not coin and ci(factor) < 63) or (coin and ci(factor) < 53) else (100, 200, 200)
                ymax = self.ui.ctpg_tik_data[ci(factor)].max()
                ymin = self.ui.ctpg_tik_data[ci(factor)].min()
                if chuse_exist: self.ui.ctpg[i].addItem(ChuseItem(self.ui.ctpg_tik_arry[:, ci('관심종목')], ymin, ymax, self.ui.ctpg_tik_xticks))
                self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci(factor)]:], y=self.ui.ctpg_tik_data[ci(factor)], pen=pen)
                if factor == 'KAMA':
                    self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('현재가')]:], y=self.ui.ctpg_tik_data[ci('현재가')], pen=(200, 100, 100))

            if self.ui.ct_checkBoxxxxx_22.isChecked():
                legend = pg.TextItem(anchor=(1, 0), color=color_fg_bt, border=color_bg_bt, fill=color_bg_ld)
                legend.setText(get_label_text(coin, self.ui.ctpg_tik_arry, -1, self.ui.ctpg_tik_factors[i], hms))
                legend.setFont(qfont12)
                legend.setPos(xmax, ymax)
                self.ui.ctpg[i].addItem(legend)
                self.ui.ctpg_tik_legend[i] = legend

            if i != 0: self.ui.ctpg[i].setXLink(self.ui.ctpg[0])
            self.SetRangeCtpg(i, xmin, xmax, ymin, ymax)
            if self.ui.ct_checkBoxxxxx_22.isChecked():
                self.ui.ctpg_tik_legend[i].setPos(self.ui.ctpg_cvb[i].state['viewRange'][0][1], self.ui.ctpg_cvb[i].state['viewRange'][1][1])
            if i == chart_count - 1: break

        if self.ui.ct_checkBoxxxxx_31.isChecked():
            if chart_count == 8:
                self.crosshair.crosshair(
                    False, coin, self.ui.ctpg[0], self.ui.ctpg[1], self.ui.ctpg[2], self.ui.ctpg[3], self.ui.ctpg[4],
                    self.ui.ctpg[5], self.ui.ctpg[6], self.ui.ctpg[7])
            elif chart_count == 12:
                self.crosshair.crosshair(
                    False, coin, self.ui.ctpg[0], self.ui.ctpg[1], self.ui.ctpg[2], self.ui.ctpg[3], self.ui.ctpg[4],
                    self.ui.ctpg[5], self.ui.ctpg[6], self.ui.ctpg[7], self.ui.ctpg[8], self.ui.ctpg[9],
                    self.ui.ctpg[10], self.ui.ctpg[11])
            elif chart_count == 16:
                self.crosshair.crosshair(
                    False, coin, self.ui.ctpg[0], self.ui.ctpg[1], self.ui.ctpg[2], self.ui.ctpg[3], self.ui.ctpg[4],
                    self.ui.ctpg[5], self.ui.ctpg[6], self.ui.ctpg[7], self.ui.ctpg[8], self.ui.ctpg[9],
                    self.ui.ctpg[10], self.ui.ctpg[11], self.ui.ctpg[12], self.ui.ctpg[13], self.ui.ctpg[14],
                    self.ui.ctpg[15])

        self.ui.ctpg_tik_name = self.ui.ct_lineEdittttt_05.text()
        if not self.ui.database_chart: self.ui.database_chart = True

        if self.ui.dialog_hoga.isVisible() and self.ui.hg_labellllllll_01.text() != '':
            self.ui.hgButtonClicked_02('매수')

    def SetRangeCtpg(self, i, xmin, xmax, ymin, ymax):
        self.ui.ctpg_cvb[i].set_range(xmin, xmax, ymin, ymax)
        self.ui.ctpg[i].setRange(xRange=(xmin, xmax), yRange=(ymin, ymax))

    @thread_decorator
    def KiwoomHTSChart(self, code, date):
        try:
            hwnd_mult = win32gui.FindWindowEx(None, None, None, "[0607] 멀티차트")
            if hwnd_mult != 0:
                win32gui.SetForegroundWindow(hwnd_mult)
                self.HTSControl(code, date, hwnd_mult)
            else:
                hwnd_main = win32gui.FindWindowEx(None, None, '_NKHeroMainClass', None)
                if hwnd_main != 0:
                    win32gui.SetForegroundWindow(hwnd_main)
                    hwnd_mult = win32gui.FindWindowEx(hwnd_main, None, "MDIClient", None)
                    hwnd_mult = win32gui.FindWindowEx(hwnd_mult, None, None, "[0607] 멀티차트")
                    self.HTSControl(code, date, hwnd_mult)
        except:
            pass

    def HTSControl(self, code, date, hwnd_mult):
        try:
            hwnd_part = win32gui.FindWindowEx(hwnd_mult, None, "AfxFrameOrView110", None)
            hwnd_prev = win32gui.FindWindowEx(hwnd_part, None, "AfxWnd110", None)
            hwnd_prev = win32gui.FindWindowEx(hwnd_part, hwnd_prev, "AfxWnd110", None)
            hwnd_part = win32gui.FindWindowEx(hwnd_part, hwnd_prev, "AfxWnd110", None)

            hwnd_prev = win32gui.FindWindowEx(hwnd_part, None, "AfxWnd110", None)
            hwnd_part = win32gui.FindWindowEx(hwnd_part, hwnd_prev, "AfxWnd110", None)

            hwnd_prev = win32gui.FindWindowEx(hwnd_part, None, "AfxWnd110", None)
            hwnd_mid1 = win32gui.FindWindowEx(hwnd_part, hwnd_prev, "AfxWnd110", None)
            hwnd_mid2 = win32gui.FindWindowEx(hwnd_part, hwnd_mid1, "AfxWnd110", None)
            hwnd_mid3 = win32gui.FindWindowEx(hwnd_part, hwnd_mid2, "AfxWnd110", None)

            hwnd_prev = win32gui.FindWindowEx(hwnd_mid2, None, "AfxWnd110", None)
            hwnd_prev = win32gui.FindWindowEx(hwnd_mid2, hwnd_prev, "AfxWnd110", None)
            hwnd_prev = win32gui.FindWindowEx(hwnd_mid2, hwnd_prev, "AfxWnd110", None)
            hwnd_code = win32gui.FindWindowEx(hwnd_mid2, hwnd_prev, "AfxWnd110", None)

            leftClick(15, 15, win32gui.GetDlgItem(hwnd_code, 0x01))
            enter_keys(win32gui.GetDlgItem(hwnd_code, 0x01), code)

            leftClick(15, 15, win32gui.GetDlgItem(hwnd_mid3, 0x834))
            hwnd_prev = win32gui.FindWindowEx(hwnd_mid1, None, "AfxWnd110", None)
            hwnd_part = win32gui.FindWindowEx(hwnd_mid1, hwnd_prev, "AfxWnd110", None)
            hwnd_date = win32gui.FindWindowEx(hwnd_part, None, "AfxWnd110", None)

            leftClick(15, 15, win32gui.GetDlgItem(hwnd_date, 0x7D1))
            press_keys(int(date[0]))
            press_keys(int(date[1]))
            press_keys(int(date[2]))
            press_keys(int(date[3]))
            press_keys(int(date[4]))
            press_keys(int(date[5]))
            press_keys(int(date[6]))
            press_keys(int(date[7]))
            # noinspection PyUnresolvedReferences
            win32api.Sleep(200)

            leftClick(15, 15, win32gui.GetDlgItem(hwnd_mid3, 0x838))
            hwnd_prev = win32gui.FindWindowEx(hwnd_mid1, None, "AfxWnd110", None)
            hwnd_part = win32gui.FindWindowEx(hwnd_mid1, hwnd_prev, "AfxWnd110", None)
            hwnd_date = win32gui.FindWindowEx(hwnd_part, None, "AfxWnd110", None)

            leftClick(15, 15, win32gui.GetDlgItem(hwnd_date, 0x7D1))
            press_keys(int(date[4]))
            press_keys(int(date[5]))
            press_keys(int(date[6]))
            press_keys(int(date[7]))
        except:
            print('키움HTS에 멀티차트가 없거나 일봉, 분봉 차트 두개로 설정되어 있지 않습니다.')
            print('2x1로 좌측은 일봉, 우측은 분봉, 종목일괄변경으로 설정하신 다음 실행하십시오.')

        win32gui.SetForegroundWindow(int(self.ui.winId()))
