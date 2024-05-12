import pyqtgraph as pg
from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QPicture, QPainter
from ui.set_style import color_bg_dk, color_ma05, color_ma10, color_ma20, color_ma60, color_ma120, color_ma240, \
    color_pluss, color_minus


class ChuseItem(pg.GraphicsObject):
    def __init__(self, ar, ymin, ymax, xticks):
        pg.GraphicsObject.__init__(self)
        self.picture = QPicture()
        self.Chuse(ar, ymin, ymax, xticks)

    def Chuse(self, ar, ymin, ymax, xticks):
        p = QPainter(self.picture)
        height = ymax - ymin
        start = 0
        p.setBrush(pg.mkBrush(color_bg_dk))
        p.setPen(pg.mkPen(color_bg_dk))
        last = len(ar) - 1
        for i, mt in enumerate(ar):
            if i != last:
                if mt == 1 and start == 0:
                    start = xticks[i]
                elif mt == 0 and start != 0:
                    p.drawRect(QRectF(start, ymin, xticks[i] - start, height))
                    start = 0
            elif start != 0:
                p.drawRect(QRectF(start, ymin, xticks[-1] - start, height))
        p.end()

    def paint(self, p, *args):
        if args is None:
            return
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QRectF(self.picture.boundingRect())


class MoveavgItem(pg.GraphicsObject):
    def __init__(self, ar, last=False):
        pg.GraphicsObject.__init__(self)
        self.picture = QPicture()
        self.Movwavg(ar, last)

    def Movwavg(self, ar, last):
        p = QPainter(self.picture)
        count = len(ar)
        if last:
            ma050 = ar[-2, 6]
            ma051 = ar[-1, 6]
            ma100 = ar[-2, 7]
            ma101 = ar[-1, 7]
            ma200 = ar[-2, 8]
            ma201 = ar[-1, 8]
            ma600 = ar[-2, 9]
            ma601 = ar[-1, 9]
            ma120 = ar[-2, 10]
            ma121 = ar[-1, 10]
            ma240 = ar[-2, 11]
            ma241 = ar[-1, 11]
            p.setPen(pg.mkPen(color_ma05))
            p.drawLine(QPointF(count - 2, ma050), QPointF(count - 1, ma051))
            p.setPen(pg.mkPen(color_ma10))
            p.drawLine(QPointF(count - 2, ma100), QPointF(count - 1, ma101))
            p.setPen(pg.mkPen(color_ma20))
            p.drawLine(QPointF(count - 2, ma200), QPointF(count - 1, ma201))
            p.setPen(pg.mkPen(color_ma60))
            p.drawLine(QPointF(count - 2, ma600), QPointF(count - 1, ma601))
            p.setPen(pg.mkPen(color_ma120))
            p.drawLine(QPointF(count - 2, ma120), QPointF(count - 1, ma121))
            p.setPen(pg.mkPen(color_ma240))
            p.drawLine(QPointF(count - 2, ma240), QPointF(count - 1, ma241))
        else:
            for i in range(count):
                if i < count - 2:
                    ma050 = ar[i, 6]
                    ma051 = ar[i + 1, 6]
                    ma100 = ar[i, 7]
                    ma101 = ar[i + 1, 7]
                    ma200 = ar[i, 8]
                    ma201 = ar[i + 1, 8]
                    ma600 = ar[i, 9]
                    ma601 = ar[i + 1, 9]
                    ma120 = ar[i, 10]
                    ma121 = ar[i + 1, 10]
                    ma240 = ar[i, 11]
                    ma241 = ar[i + 1, 11]
                    p.setPen(pg.mkPen(color_ma05))
                    p.drawLine(QPointF(i, ma050), QPointF(i + 1, ma051))
                    p.setPen(pg.mkPen(color_ma10))
                    p.drawLine(QPointF(i, ma100), QPointF(i + 1, ma101))
                    p.setPen(pg.mkPen(color_ma20))
                    p.drawLine(QPointF(i, ma200), QPointF(i + 1, ma201))
                    p.setPen(pg.mkPen(color_ma60))
                    p.drawLine(QPointF(i, ma600), QPointF(i + 1, ma601))
                    p.setPen(pg.mkPen(color_ma120))
                    p.drawLine(QPointF(i, ma120), QPointF(i + 1, ma121))
                    p.setPen(pg.mkPen(color_ma240))
                    p.drawLine(QPointF(i, ma240), QPointF(i + 1, ma241))
        p.end()

    def paint(self, p, *args):
        if args is None:
            return
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QRectF(self.picture.boundingRect())


class CandlestickItem(pg.GraphicsObject):
    def __init__(self, ar, last=False):
        pg.GraphicsObject.__init__(self)
        self.picture = QPicture()
        self.CandleSticks(ar, last)

    def CandleSticks(self, ar, last):
        p = QPainter(self.picture)
        count = len(ar)
        if last:
            for i in (count - 2, count - 1):
                o = ar[i, 1]
                h = ar[i, 2]
                low = ar[i, 3]
                c = ar[i, 4]
                if c >= o:
                    p.setPen(pg.mkPen(color_pluss))
                    p.setBrush(pg.mkBrush(color_pluss))
                else:
                    p.setPen(pg.mkPen(color_minus))
                    p.setBrush(pg.mkBrush(color_minus))
                if h != low:
                    p.drawLine(QPointF(i, h), QPointF(i, low))
                    p.drawRect(QRectF(i - 0.25, o, 0.5, c - o))
                else:
                    p.drawLine(QPointF(i - 0.25, c), QPointF(i + 0.25, c))
        else:
            for i in range(count):
                if i < count - 2:
                    o   = ar[i, 1]
                    h   = ar[i, 2]
                    low = ar[i, 3]
                    c   = ar[i, 4]
                    if c >= o:
                        p.setPen(pg.mkPen(color_pluss))
                        p.setBrush(pg.mkBrush(color_pluss))
                    else:
                        p.setPen(pg.mkPen(color_minus))
                        p.setBrush(pg.mkBrush(color_minus))
                    if h != low:
                        p.drawLine(QPointF(i, h), QPointF(i, low))
                        p.drawRect(QRectF(i - 0.25, o, 0.5, c - o))
                    else:
                        p.drawLine(QPointF(i - 0.25, c), QPointF(i + 0.25, c))
        p.end()

    def paint(self, p, *args):
        if args is None:
            return
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QRectF(self.picture.boundingRect())


class VolumeBarsItem(pg.GraphicsObject):
    def __init__(self, ar, last=False):
        pg.GraphicsObject.__init__(self)
        self.picture = QPicture()
        self.MoneyBars(ar, last)

    def MoneyBars(self, ar, last):
        p = QPainter(self.picture)
        count = len(ar)
        if last:
            x = count - 1
            c = ar[-1, 4]
            o = ar[-1, 1]
            m = ar[-1, 5]
            if c >= o:
                p.setPen(pg.mkPen(color_pluss))
                p.setBrush(pg.mkBrush(color_pluss))
            else:
                p.setPen(pg.mkPen(color_minus))
                p.setBrush(pg.mkBrush(color_minus))
            p.drawRect(QRectF(x - 0.25, 0, 0.25 * 2, m))
        else:
            for i in range(count):
                if i < count - 1:
                    o = ar[i, 1]
                    c = ar[i, 4]
                    m = ar[i, 5]
                    if c >= o:
                        p.setPen(pg.mkPen(color_pluss))
                        p.setBrush(pg.mkBrush(color_pluss))
                    else:
                        p.setPen(pg.mkPen(color_minus))
                        p.setBrush(pg.mkBrush(color_minus))
                    p.drawRect(QRectF(i - 0.25, 0, 0.25 * 2, m))
        p.end()

    def paint(self, p, *args):
        if args is None:
            return
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QRectF(self.picture.boundingRect())
