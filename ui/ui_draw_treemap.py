import squarify
from utility.setting import ui_num
from utility.static import error_decorator


class DrawTremap:
    def __init__(self, ui, qlist):
        """
        windowQ, soundQ, queryQ, teleQ, chartQ, hogaQ, webcQ, backQ, creceivQ, ctraderQ,  cstgQ, liveQ, kimpQ, wdzservQ
           0        1       2      3       4      5      6      7       8         9         10     11    12      13
        """
        self.ui = ui
        self.webcQ = qlist[6]

    @error_decorator
    def draw_treemap(self, data):
        if not self.ui.dialog_tree.isVisible():
            self.webcQ.put(('트리맵중단', ''))
            return

        gubun, df1, df2, cl1, cl2 = data
        if gubun == ui_num['트리맵'] and self.ui.tm_dt:
            return

        def mouse_press(event):
            if event.inaxes == self.ui.tm_ax1 and self.ui.df_tm1 is not None:
                if event.button == 1 and event.button != self.ui.tm_mc1:
                    self.ui.tm_mc1 = 1
                    df_ = self.ui.df_tm1[(self.ui.df_tm1['x'] < event.xdata) & (event.xdata < self.ui.df_tm1['x2']) &
                                         (self.ui.df_tm1['y'] < event.ydata) & (event.ydata < self.ui.df_tm1['y2'])]
                    if len(df_) == 1:
                        self.ui.tm_dt = True
                        url = df_['url'].iloc[0]
                        self.webcQ.put(('트리맵1', url))
                elif event.button == 3 and event.button != self.ui.tm_mc1:
                    self.ui.tm_mc1 = 3
                    self.ui.tm_dt = False
                    self.ui.tm_ax1.clear()
                    self.ui.tm_ax1.axis('off')
                    squarify.plot(sizes=self.ui.df_tm1['등락율'], label=self.ui.df_tm1['업종명'], alpha=.9,
                                  value=self.ui.df_tm1['등락율%'], color=self.ui.tm_cl1, ax=self.ui.tm_ax1,
                                  bar_kwargs=dict(linewidth=1, edgecolor='#000000'))
                    self.ui.canvas.figure.tight_layout()
                    self.ui.canvas.mpl_connect('button_press_event', mouse_press)
                    self.ui.canvas.draw()
            elif event.inaxes == self.ui.tm_ax2 and self.ui.df_tm2 is not None:
                if event.button == 1 and event.button != self.ui.tm_mc2:
                    self.ui.tm_mc2 = 1
                    df_ = self.ui.df_tm2[(self.ui.df_tm2['x'] < event.xdata) & (event.xdata < self.ui.df_tm2['x2']) &
                                         (self.ui.df_tm2['y'] < event.ydata) & (event.ydata < self.ui.df_tm2['y2'])]
                    if len(df_) == 1:
                        self.ui.tm_dt = True
                        url = df_['url'].iloc[0]
                        self.webcQ.put(('트리맵2', url))
                elif event.button == 3 and event.button != self.ui.tm_mc2:
                    self.ui.tm_mc2 = 3
                    self.ui.tm_dt = False
                    self.ui.tm_ax2.clear()
                    self.ui.tm_ax2.axis('off')
                    squarify.plot(sizes=self.ui.df_tm2['등락율'], label=self.ui.df_tm2['테마명'], alpha=.9,
                                  value=self.ui.df_tm2['등락율%'], color=self.ui.tm_cl2, ax=self.ui.tm_ax2,
                                  bar_kwargs=dict(linewidth=1, edgecolor='#000000'))
                    self.ui.canvas.figure.tight_layout()
                    self.ui.canvas.mpl_connect('button_press_event', mouse_press)
                    self.ui.canvas.draw()

        if gubun == ui_num['트리맵']:
            self.ui.df_tm1 = df1
            self.ui.df_tm2 = df2
            self.ui.tm_cl1 = cl1
            self.ui.tm_cl2 = cl2

            normed = squarify.normalize_sizes(self.ui.df_tm1['등락율'], 100, 100)
            rects = squarify.squarify(normed, 0, 0, 100, 100)
            self.ui.df_tm1['x']  = [rect["x"] for rect in rects]
            self.ui.df_tm1['y']  = [rect["y"] for rect in rects]
            self.ui.df_tm1['dx'] = [rect["dx"] for rect in rects]
            self.ui.df_tm1['dy'] = [rect["dy"] for rect in rects]
            self.ui.df_tm1['x2'] = self.ui.df_tm1['x'] + self.ui.df_tm1['dx']
            self.ui.df_tm1['y2'] = self.ui.df_tm1['y'] + self.ui.df_tm1['dy']

            normed = squarify.normalize_sizes(self.ui.df_tm2['등락율'], 100, 100)
            rects = squarify.squarify(normed, 0, 0, 100, 100)
            self.ui.df_tm2['x']  = [rect["x"] for rect in rects]
            self.ui.df_tm2['y']  = [rect["y"] for rect in rects]
            self.ui.df_tm2['dx'] = [rect["dx"] for rect in rects]
            self.ui.df_tm2['dy'] = [rect["dy"] for rect in rects]
            self.ui.df_tm2['x2'] = self.ui.df_tm2['x'] + self.ui.df_tm2['dx']
            self.ui.df_tm2['y2'] = self.ui.df_tm2['y'] + self.ui.df_tm2['dy']

            if self.ui.tm_ax1 is None:
                self.ui.tm_ax1 = self.ui.canvas.figure.add_subplot(211)
                self.ui.tm_ax2 = self.ui.canvas.figure.add_subplot(212)
            else:
                self.ui.tm_ax1.clear()
                self.ui.tm_ax2.clear()
            self.ui.tm_ax1.axis('off')
            self.ui.tm_ax2.axis('off')
            squarify.plot(sizes=self.ui.df_tm1['등락율'], label=self.ui.df_tm1['업종명'], alpha=.9, value=self.ui.df_tm1['등락율%'],
                          color=self.ui.tm_cl1, ax=self.ui.tm_ax1, bar_kwargs=dict(linewidth=1, edgecolor='#000000'))
            squarify.plot(sizes=self.ui.df_tm2['등락율'], label=self.ui.df_tm2['테마명'], alpha=.9, value=self.ui.df_tm2['등락율%'],
                          color=self.ui.tm_cl2, ax=self.ui.tm_ax2, bar_kwargs=dict(linewidth=1, edgecolor='#000000'))
        elif gubun == ui_num['트리맵1']:
            self.ui.tm_ax1.clear()
            self.ui.tm_ax1.axis('off')
            squarify.plot(sizes=df1['등락율'], label=df1['종목명'], alpha=.9, value=df1['등락율%'],
                          color=cl1, ax=self.ui.tm_ax1, bar_kwargs=dict(linewidth=1, edgecolor='#000000'))
        elif gubun == ui_num['트리맵2']:
            self.ui.tm_ax2.clear()
            self.ui.tm_ax2.axis('off')
            squarify.plot(sizes=df2['등락율'], label=df2['종목명'], alpha=.9, value=df2['등락율%'],
                          color=cl2, ax=self.ui.tm_ax2, bar_kwargs=dict(linewidth=1, edgecolor='#000000'))

        self.ui.canvas.figure.tight_layout()
        self.ui.canvas.mpl_connect('button_press_event', mouse_press)
        self.ui.canvas.draw()
