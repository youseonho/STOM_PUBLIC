import pyqtgraph as pg
from ui.ui_crosshair import CrossHair
from ui.ui_get_label_text import get_label_text
from ui.set_style import qfont12, color_fg_bt, color_bg_bt, color_bg_ld
from utility.setting import list_stock_real, list_coin_real
from utility.static import error_decorator, from_timestamp, strp_time


class DrawRealChart:
    def __init__(self, ui):
        self.ui = ui
        self.crosshair = CrossHair(self.ui)
        self.chart_item_index = 0

    @error_decorator
    def draw_realchart(self, data):
        def ci(fname):
            return list_stock_real.index(fname) if not coin else list_coin_real.index(fname)

        def cii():
            self.chart_item_index += 1
            return self.chart_item_index

        if not self.ui.dialog_chart.isVisible():
            self.ui.ChartClear()
            return

        self.chart_item_index = 0
        name, self.ui.ctpg_tik_arry = data[1:]
        coin = True if 'KRW' in name or 'USDT' in name else False
        self.ui.ctpg_tik_xticks = [strp_time('%Y%m%d%H%M%S', str(int(x))).timestamp() for x in self.ui.ctpg_tik_data[0]]
        xmin, xmax = self.ui.ctpg_tik_xticks[0], self.ui.ctpg_tik_xticks[-1]
        hms = from_timestamp(xmax).strftime('%H:%M:%S')

        if self.ui.ct_pushButtonnn_04.text() == 'CHART 8':
            chart_count = 8
        elif self.ui.ct_pushButtonnn_04.text() == 'CHART 12':
            chart_count = 12
        else:
            chart_count = 16

        if self.ui.ctpg_tik_name != name:
            self.ui.ctpg_tik_item    = {}
            self.ui.ctpg_tik_data    = {}
            self.ui.ctpg_tik_legend  = {}
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

        if self.ui.ctpg_tik_name != name:
            for i, factor in enumerate(self.ui.ctpg_tik_factors):
                self.ui.ctpg[i].clear()
                if factor == '현재가':
                    ymax = self.ui.ctpg_tik_data[ci('현재가')].max()
                    ymin = min(self.ui.ctpg_tik_data[ci('이동평균1200')].min(), self.ui.ctpg_tik_data[ci('현재가')].min())
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('이동평균60')]:], y=self.ui.ctpg_tik_data[ci('이동평균60')], pen=(180, 180, 180))
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('이동평균300')]:], y=self.ui.ctpg_tik_data[ci('이동평균300')], pen=(140, 140, 140))
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('이동평균600')]:], y=self.ui.ctpg_tik_data[ci('이동평균600')], pen=(100, 100, 100))
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('이동평균1200')]:], y=self.ui.ctpg_tik_data[ci('이동평균1200')], pen=(60, 60, 60))
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('현재가')]:], y=self.ui.ctpg_tik_data[ci('현재가')], pen=(200, 50, 50))
                    self.ui.ctpg_tik_cline = pg.InfiniteLine(angle=0)
                    self.ui.ctpg_tik_cline.setPen(pg.mkPen(color_fg_bt))
                    self.ui.ctpg_tik_cline.setPos(self.ui.ctpg_tik_data[ci(5)][-1])
                    self.ui.ctpg[i].addItem(self.ui.ctpg_tik_cline)
                elif factor == '체결강도':
                    ymax = max(self.ui.ctpg_tik_data[ci('체결강도')].max(), self.ui.ctpg_tik_data[ci('최고체결강도')].max())
                    ymin = min(self.ui.ctpg_tik_data[ci('체결강도')].min(), self.ui.ctpg_tik_data[ci('최저체결강도')].min())
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('체결강도평균')]:], y=self.ui.ctpg_tik_data[ci('체결강도평균')], pen=(50, 200, 50))
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('최저체결강도')]:], y=self.ui.ctpg_tik_data[ci('최저체결강도')], pen=(50, 50, 200))
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('최고체결강도')]:], y=self.ui.ctpg_tik_data[ci('최고체결강도')], pen=(200, 50, 50))
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('체결강도')]:], y=self.ui.ctpg_tik_data[ci('체결강도')], pen=(50, 200, 50))
                elif factor == '초당거래대금':
                    ymax = self.ui.ctpg_tik_data[ci('초당거래대금')].max()
                    ymin = self.ui.ctpg_tik_data[ci('초당거래대금평균')].min()
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('초당거래대금')]:], y=self.ui.ctpg_tik_data[ci('초당거래대금')], pen=(200, 50, 50))
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('초당거래대금평균')]:], y=self.ui.ctpg_tik_data[ci('초당거래대금평균')], pen=(50, 200, 50))
                elif factor == '초당체결수량':
                    ymax = max(self.ui.ctpg_tik_data[ci('초당매수수량')].max(), self.ui.ctpg_tik_data[ci('초당매도수량')].max())
                    ymin = min(self.ui.ctpg_tik_data[ci('초당매수수량')].min(), self.ui.ctpg_tik_data[ci('초당매도수량')].min())
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('초당매도수량')]:], y=self.ui.ctpg_tik_data[ci('초당매도수량')], pen=(50, 50, 200))
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('초당매수수량')]:], y=self.ui.ctpg_tik_data[ci('초당매수수량')], pen=(200, 50, 50))
                elif factor == '호가총잔량':
                    ymax = max(self.ui.ctpg_tik_data[ci('매수총잔량')].max(), self.ui.ctpg_tik_data[ci('매도총잔량')].max())
                    ymin = min(self.ui.ctpg_tik_data[ci('매수총잔량')].min(), self.ui.ctpg_tik_data[ci('매도총잔량')].min())
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('매수총잔량')]:], y=self.ui.ctpg_tik_data[ci('매수총잔량')], pen=(200, 50, 50))
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('매도총잔량')]:], y=self.ui.ctpg_tik_data[ci('매도총잔량')], pen=(50, 50, 200))
                elif factor == '1호가잔량':
                    ymax = max(self.ui.ctpg_tik_data[ci('매수잔량1')].max(), self.ui.ctpg_tik_data[ci('매도잔량1')].max())
                    ymin = min(self.ui.ctpg_tik_data[ci('매수잔량1')].min(), self.ui.ctpg_tik_data[ci('매도잔량1')].min())
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('매수잔량1')]:], y=self.ui.ctpg_tik_data[ci('매수잔량1')], pen=(200, 50, 50))
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('매도잔량1')]:], y=self.ui.ctpg_tik_data[ci('매도잔량1')], pen=(50, 50, 200))
                elif factor == '누적초당매도수수량':
                    ymax = max(self.ui.ctpg_tik_data[ci('누적초당매수수량')].max(), self.ui.ctpg_tik_data[ci('누적초당매도수량')].max())
                    ymin = min(self.ui.ctpg_tik_data[ci('누적초당매수수량')].min(), self.ui.ctpg_tik_data[ci('누적초당매도수량')].min())
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('누적초당매도수량')]:], y=self.ui.ctpg_tik_data[ci('누적초당매도수량')], pen=(50, 50, 200))
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('누적초당매수수량')]:], y=self.ui.ctpg_tik_data[ci('누적초당매수수량')], pen=(200, 50, 50))
                elif factor == 'BBAND':
                    ymax = max(self.ui.ctpg_tik_data[ci('BBU')].max(), self.ui.ctpg_tik_data[ci('현재가')].max())
                    ymin = min(self.ui.ctpg_tik_data[ci('BBL')].min(), self.ui.ctpg_tik_data[ci('현재가')].min())
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('BBM')]:], y=self.ui.ctpg_tik_data[ci('BBM')], pen=(140, 140, 140))
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('BBL')]:], y=self.ui.ctpg_tik_data[ci('BBL')], pen=(50, 50, 200))
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('BBU')]:], y=self.ui.ctpg_tik_data[ci('BBU')], pen=(50, 200, 50))
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('현재가')]:], y=self.ui.ctpg_tik_data[ci('현재가')], pen=(200, 50, 50))
                elif factor == 'MACD':
                    ymax = self.ui.ctpg_tik_data[ci('MACD')].max()
                    ymin = self.ui.ctpg_tik_data[ci('MACD')].min()
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('MACDH')]:], y=self.ui.ctpg_tik_data[ci('MACDH')], pen=(140, 140, 140))
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('MACDS')]:], y=self.ui.ctpg_tik_data[ci('MACDS')], pen=(50, 50, 200))
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('MACD')]:], y=self.ui.ctpg_tik_data[ci('MACD')], pen=(50, 200, 50))
                elif factor == 'HT_SINE, HT_LSINE':
                    ymax = max(self.ui.ctpg_tik_data[ci('HT_SINE')].max(), self.ui.ctpg_tik_data[ci('HT_LSINE')].max())
                    ymin = min(self.ui.ctpg_tik_data[ci('HT_SINE')].min(), self.ui.ctpg_tik_data[ci('HT_LSINE')].min())
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('HT_LSINE')]:], y=self.ui.ctpg_tik_data[ci('HT_LSINE')], pen=(50, 50, 200))
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('HT_SINE')]:], y=self.ui.ctpg_tik_data[ci('HT_SINE')], pen=(50, 200, 50))
                elif factor == 'HT_PHASE, HT_QUDRA':
                    ymax = max(self.ui.ctpg_tik_data[ci('HT_PHASE')].max(), self.ui.ctpg_tik_data[ci('HT_QUDRA')].max())
                    ymin = min(self.ui.ctpg_tik_data[ci('HT_PHASE')].min(), self.ui.ctpg_tik_data[ci('HT_QUDRA')].min())
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('HT_QUDRA')]:], y=self.ui.ctpg_tik_data[ci('HT_QUDRA')], pen=(50, 50, 200))
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('HT_PHASE')]:], y=self.ui.ctpg_tik_data[ci('HT_PHASE')], pen=(50, 200, 50))
                else:
                    if factor == 'KAMA':
                        self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci('현재가')]:], y=self.ui.ctpg_tik_data[ci('현재가')], pen=(200, 50, 50))
                    pen = (200, 200, 50) if (not coin and ci(factor) < 62) or (coin and ci(factor) < 52) else (50, 200, 200)
                    ymax = self.ui.ctpg_tik_data[ci(factor)].max()
                    ymin = self.ui.ctpg_tik_data[ci(factor)].min()
                    self.ui.ctpg_tik_item[cii()] = self.ui.ctpg[i].plot(x=self.ui.ctpg_tik_xticks[len_list[ci(factor)]:], y=self.ui.ctpg_tik_data[ci(factor)], pen=pen)

                if self.ui.ct_checkBoxxxxx_22.isChecked():
                    legend = pg.TextItem(anchor=(0, 0), color=color_fg_bt, border=color_bg_bt, fill=color_bg_ld)
                    legend.setFont(qfont12)
                    legend.setText(get_label_text(coin, self.ui.ctpg_tik_arry, -1, self.ui.ctpg_tik_factors[i], hms))
                    self.ui.ctpg[i].addItem(legend)
                    self.ui.ctpg_tik_legend[i] = legend

                if i != 0: self.ui.ctpg[i].setXLink(self.ui.ctpg[0])
                self.SetRangeCtpg(i, xmin, xmax, ymin, ymax)
                if self.ui.ct_checkBoxxxxx_22.isChecked():
                    self.ui.ctpg_tik_legend[i].setPos(self.ui.ctpg_cvb[i].state['viewRange'][0][0], self.ui.ctpg_cvb[i].state['viewRange'][1][1])
                if i == chart_count - 1: break

            self.ui.ctpg_tik_name = name
            if self.ui.ct_checkBoxxxxx_31.isChecked():
                if chart_count == 8:
                    self.crosshair.crosshair(True, coin, self.ui.ctpg[0], self.ui.ctpg[1], self.ui.ctpg[2],
                                             self.ui.ctpg[3], self.ui.ctpg[4], self.ui.ctpg[5], self.ui.ctpg[6],
                                             self.ui.ctpg[7])
                elif chart_count == 12:
                    self.crosshair.crosshair(True, coin, self.ui.ctpg[0], self.ui.ctpg[1], self.ui.ctpg[2],
                                             self.ui.ctpg[3], self.ui.ctpg[4], self.ui.ctpg[5], self.ui.ctpg[6],
                                             self.ui.ctpg[7], self.ui.ctpg[8], self.ui.ctpg[9], self.ui.ctpg[10],
                                             self.ui.ctpg[11])
                elif chart_count == 16:
                    self.crosshair.crosshair(True, coin, self.ui.ctpg[0], self.ui.ctpg[1], self.ui.ctpg[2],
                                             self.ui.ctpg[3], self.ui.ctpg[4], self.ui.ctpg[5], self.ui.ctpg[6],
                                             self.ui.ctpg[7], self.ui.ctpg[8], self.ui.ctpg[9], self.ui.ctpg[10],
                                             self.ui.ctpg[11], self.ui.ctpg[12], self.ui.ctpg[13], self.ui.ctpg[14],
                                             self.ui.ctpg[15])
        else:
            for i, factor in enumerate(self.ui.ctpg_tik_factors):
                if factor == '현재가':
                    ymax = self.ui.ctpg_tik_data[ci('현재가')].max()
                    ymin = self.ui.ctpg_tik_data[ci('현재가')].min()
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('이동평균60')]:], y=self.ui.ctpg_tik_data[ci('이동평균60')])
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('이동평균300')]:], y=self.ui.ctpg_tik_data[ci('이동평균300')])
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('이동평균600')]:], y=self.ui.ctpg_tik_data[ci('이동평균600')])
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('이동평균1200')]:], y=self.ui.ctpg_tik_data[ci('이동평균1200')])
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('현재가')]:], y=self.ui.ctpg_tik_data[ci('현재가')])
                    self.ui.ctpg_tik_cline.setPos(self.ui.ctpg_tik_data[ci('현재가')][-1])
                elif factor == '체결강도':
                    ymax = max(self.ui.ctpg_tik_data[ci('체결강도')].max(), self.ui.ctpg_tik_data[ci('최고체결강도')].max())
                    ymin = min(self.ui.ctpg_tik_data[ci('체결강도')].min(), self.ui.ctpg_tik_data[ci('최저체결강도')].min())
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('체결강도평균')]:], y=self.ui.ctpg_tik_data[ci('체결강도평균')])
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('최저체결강도')]:], y=self.ui.ctpg_tik_data[ci('최저체결강도')])
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('최고체결강도')]:], y=self.ui.ctpg_tik_data[ci('최고체결강도')])
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('체결강도')]:], y=self.ui.ctpg_tik_data[ci('체결강도')])
                elif factor == '초당거래대금':
                    ymax = self.ui.ctpg_tik_data[ci('초당거래대금')].max()
                    ymin = self.ui.ctpg_tik_data[ci('초당거래대금평균')].min()
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('초당거래대금')]:], y=self.ui.ctpg_tik_data[ci('초당거래대금')])
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('초당거래대금평균')]:], y=self.ui.ctpg_tik_data[ci('초당거래대금평균')])
                elif factor == '초당체결수량':
                    ymax = max(self.ui.ctpg_tik_data[ci('초당매수수량')].max(), self.ui.ctpg_tik_data[ci('초당매도수량')].max())
                    ymin = min(self.ui.ctpg_tik_data[ci('초당매수수량')].min(), self.ui.ctpg_tik_data[ci('초당매도수량')].min())
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('초당매도수량')]:], y=self.ui.ctpg_tik_data[ci('초당매도수량')])
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('초당매수수량')]:], y=self.ui.ctpg_tik_data[ci('초당매수수량')])
                elif factor == '호가총잔량':
                    ymax = max(self.ui.ctpg_tik_data[ci('매수총잔량')].max(), self.ui.ctpg_tik_data[ci('매도총잔량')].max())
                    ymin = min(self.ui.ctpg_tik_data[ci('매수총잔량')].min(), self.ui.ctpg_tik_data[ci('매도총잔량')].min())
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('매수총잔량')]:], y=self.ui.ctpg_tik_data[ci('매수총잔량')])
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('매도총잔량')]:], y=self.ui.ctpg_tik_data[ci('매도총잔량')])
                elif factor == '1호가잔량':
                    ymax = max(self.ui.ctpg_tik_data[ci('매수잔량1')].max(), self.ui.ctpg_tik_data[ci('매도잔량1')].max())
                    ymin = min(self.ui.ctpg_tik_data[ci('매수잔량1')].min(), self.ui.ctpg_tik_data[ci('매도잔량1')].min())
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('매수잔량1')]:], y=self.ui.ctpg_tik_data[ci('매수잔량1')])
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('매도잔량1')]:], y=self.ui.ctpg_tik_data[ci('매도잔량1')])
                elif factor == '누적초당매도수수량':
                    ymax = max(self.ui.ctpg_tik_data[ci('누적초당매수수량')].max(), self.ui.ctpg_tik_data[ci('누적초당매도수량')].max())
                    ymin = min(self.ui.ctpg_tik_data[ci('누적초당매수수량')].min(), self.ui.ctpg_tik_data[ci('누적초당매도수량')].min())
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('누적초당매도수량')]:], y=self.ui.ctpg_tik_data[ci('누적초당매도수량')])
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('누적초당매수수량')]:], y=self.ui.ctpg_tik_data[ci('누적초당매수수량')])
                elif factor == 'BBAND':
                    ymax = max(self.ui.ctpg_tik_data[ci('BBU')].max(), self.ui.ctpg_tik_data[ci('현재가')].max())
                    ymin = min(self.ui.ctpg_tik_data[ci('BBL')].min(), self.ui.ctpg_tik_data[ci('현재가')].min())
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('BBM')]:], y=self.ui.ctpg_tik_data[ci('BBM')])
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('BBL')]:], y=self.ui.ctpg_tik_data[ci('BBL')])
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('BBU')]:], y=self.ui.ctpg_tik_data[ci('BBU')])
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('현재가')]:], y=self.ui.ctpg_tik_data[ci('현재가')])
                elif factor == 'MACD':
                    ymax = self.ui.ctpg_tik_data[ci('MACD')].max()
                    ymin = self.ui.ctpg_tik_data[ci('MACD')].min()
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('MACDH')]:], y=self.ui.ctpg_tik_data[ci('MACDH')])
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('MACDS')]:], y=self.ui.ctpg_tik_data[ci('MACDS')])
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('MACD')]:], y=self.ui.ctpg_tik_data[ci('MACD')])
                elif factor == 'HT_SINE, HT_LSINE':
                    ymax = max(self.ui.ctpg_tik_data[ci('HT_SINE')].max(), self.ui.ctpg_tik_data[ci('HT_LSINE')].max())
                    ymin = min(self.ui.ctpg_tik_data[ci('HT_SINE')].min(), self.ui.ctpg_tik_data[ci('HT_LSINE')].min())
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('HT_LSINE')]:], y=self.ui.ctpg_tik_data[ci('HT_LSINE')])
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('HT_SINE')]:], y=self.ui.ctpg_tik_data[ci('HT_SINE')])
                elif factor == 'HT_PHASE, HT_QUDRA':
                    ymax = max(self.ui.ctpg_tik_data[ci('HT_PHASE')].max(), self.ui.ctpg_tik_data[ci('HT_QUDRA')].max())
                    ymin = min(self.ui.ctpg_tik_data[ci('HT_PHASE')].min(), self.ui.ctpg_tik_data[ci('HT_QUDRA')].min())
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('HT_QUDRA')]:], y=self.ui.ctpg_tik_data[ci('HT_QUDRA')])
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('HT_PHASE')]:], y=self.ui.ctpg_tik_data[ci('HT_PHASE')])
                else:
                    if factor == 'KAMA':
                        self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci('현재가')]:], y=self.ui.ctpg_tik_data[ci('현재가')])
                    ymax = self.ui.ctpg_tik_data[ci(factor)].max()
                    ymin = self.ui.ctpg_tik_data[ci(factor)].min()
                    self.ui.ctpg_tik_item[cii()].setData(x=self.ui.ctpg_tik_xticks[len_list[ci(factor)]:], y=self.ui.ctpg_tik_data[ci(factor)])

                self.SetRangeCtpg(i, xmin, xmax, ymin, ymax)
                self.SetPosLegendLabel(i, coin, hms)
                if i == chart_count - 1: break

        if self.ui.database_chart: self.ui.database_chart = False

    def SetRangeCtpg(self, i, xmin, xmax, ymin, ymax):
        self.ui.ctpg_cvb[i].set_range(xmin, xmax, ymin, ymax)
        self.ui.ctpg[i].setRange(xRange=(xmin, xmax), yRange=(ymin, ymax))

    def SetPosLegendLabel(self, i, coin, hms):
        if self.ui.ct_checkBoxxxxx_31.isChecked():
            self.ui.ctpg_tik_labels[i].setPos(self.ui.ctpg_cvb[i].state['viewRange'][0][0], self.ui.ctpg_cvb[i].state['viewRange'][1][0])
        if self.ui.ct_checkBoxxxxx_22.isChecked():
            self.ui.ctpg_tik_legend[i].setPos(self.ui.ctpg_cvb[i].state['viewRange'][0][0], self.ui.ctpg_cvb[i].state['viewRange'][1][1])
            self.ui.ctpg_tik_legend[i].setText(get_label_text(coin, self.ui.ctpg_tik_arry, -1, self.ui.ctpg_tik_factors[i], hms))
