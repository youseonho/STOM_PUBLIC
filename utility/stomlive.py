import sys
import time
import socket
import pandas as pd
from threading import Thread
from utility.static import timedelta_sec, now
from utility.setting import ui_num, columns_tt, columns_sb, columns_sd, columns_nd

HOST = '139.150.82.209'
PORT = 5728


class StomLiveSender(Thread):
    def __init__(self, s, liveQ):
        super().__init__()
        self.csock = s
        self.liveQ = liveQ

    def run(self):
        send_time = timedelta_sec(5)
        while True:
            try:
                data = self.liveQ.get()
                if type(data) == tuple:
                    time.sleep(1)
                    if self.liveQ.empty() and now() > send_time:
                        gubun, df = data
                        data = list(df.iloc[0])
                        data = [str(int(x)) if i != 5 else str(float(x)) for i, x in enumerate(data)]
                        text = f"{gubun};{';'.join(data)}"
                        self.csock.sendall(text.encode('utf-8'))
                        send_time = timedelta_sec(5)
                else:
                    self.csock.sendall(data.encode('utf-8'))
            except:
                pass


class StomLiveClient:
    def __init__(self, qlist):
        """
        windowQ, soundQ, queryQ, teleQ, chartQ, hogaQ, webcQ, backQ, creceivQ, ctraderQ,  cstgQ, liveQ, kimpQ, wdzservQ
           0        1       2      3       4      5      6      7       8         9         10     11    12      13
        """
        self.windowQ = qlist[0]
        self.liveQ   = qlist[11]
        self.Start()

    def Start(self):
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((HOST, PORT))
                sender = StomLiveSender(s, self.liveQ)
                sender.start()
                print('스톰라이브 서버에 연결되었습니다.')
                while True:
                    data = s.recv(1024000).decode('utf-8')
                    self.UpdateStomLiveData(data)
                    time.sleep(0.1)
            except:
                print('스톰라이브 서버 연결이 해제되었습니다. 10초 후 재연결합니다.')
                time.sleep(10)
                break

        sys.exit()

    def UpdateStomLiveData(self, data):
        data1, data2, data3, data4, data5, data6 = None, None, None, None, None, None
        df1, df2, df3, df4, df5, df6, df7, df8 = None, None, None, None, None, None, None, None

        if '주식당일시작' in data:
            data1 = data.split('주식당일시작')[1].split('주식당일종료')[0].split('^')
        if '주식통계시작' in data:
            data2 = data.split('주식통계시작')[1].split('주식통계종료')[0].split('^')
        if '코인당일시작' in data:
            data3 = data.split('코인당일시작')[1].split('코인당일종료')[0].split('^')
        if '코인통계시작' in data:
            data4 = data.split('코인통계시작')[1].split('코인통계종료')[0].split('^')
        if '백테당일시작' in data:
            data5 = data.split('백테당일시작')[1].split('백테당일종료')[0].split('^')
        if '백테통계시작' in data:
            data6 = data.split('백테통계시작')[1].split('백테통계종료')[0].split('^')

        if data1 is not None:
            data1 = [[int(x) if '.' not in x else float(x) for x in d.split(';')] for i, d in enumerate(data1)]
            df1 = pd.DataFrame(dict(zip(columns_tt, data1)))
            df1.sort_values(by=['수익금합계'], ascending=False, inplace=True)

        if data2 is not None:
            data2 = [[self.tatal_text_conv(i, x) for x in d.split(';')] for i, d in enumerate(data2)]
            df3 = pd.DataFrame(dict(zip(columns_nd, data2)))
            df3 = df3[::-1]

            df2 = pd.DataFrame({
                '기간': [len(df3)],
                '누적매수금액': [df3['총매수금액'].sum()],
                '누적매도금액': [df3['총매도금액'].sum()],
                '누적수익금액': [df3['총수익금액'].sum()],
                '누적손실금액': [df3['총손실금액'].sum()],
                '누적수익률': [round(df3['수익금합계'].sum() / df3['총매수금액'].sum() * 100, 2)],
                '누적수익금': [df3['수익금합계'].sum()]
            })

        if data3 is not None:
            data3 = [[int(x) if '.' not in x else float(x) for x in d.split(';')] for i, d in enumerate(data3)]
            df4 = pd.DataFrame(dict(zip(columns_tt, data3)))

        if data4 is not None:
            data4 = [[self.tatal_text_conv(i, x) for x in d.split(';')] for i, d in enumerate(data4)]
            df6 = pd.DataFrame(dict(zip(columns_nd, data4)))
            df6 = df6[::-1]

            df5 = pd.DataFrame({
                '기간': [len(df6)],
                '누적매수금액': [df6['총매수금액'].sum()],
                '누적매도금액': [df6['총매도금액'].sum()],
                '누적수익금액': [df6['총수익금액'].sum()],
                '누적손실금액': [df6['총손실금액'].sum()],
                '누적수익률': [round(df6['수익금합계'].sum() / df6['총매수금액'].sum() * 100, 2)],
                '누적수익금': [df6['수익금합계'].sum()]
            })

        if data5 is not None:
            data5 = [[self.back_text_conv(i, x) for x in d.split(';')] for i, d in enumerate(data5)]
            df7 = pd.DataFrame(dict(zip(columns_sd, data5)))
            df7.sort_values(by=['cagr'], ascending=False, inplace=True)

        if data6 is not None:
            df8 = pd.DataFrame(columns=['백테스트', '백파인더', '최적화', '최적화V', '최적화VC', '최적화T', '최적화VT', '최적화VCT',
                                        '최적화OG', '최적화OGV', '최적화OGVC', '최적화OC', '최적화OCV', '최적화OCVC', '전진분석', '전진분석V', '전진분석VC'])
            for i, d in enumerate(data6):
                df8.loc[i] = [int(x) for x in d.split(';')]

            tbk   = df8['백테스트'].iloc[:-1].sum()
            tbf   = df8['백파인더'].iloc[:-1].sum()
            toh   = df8['최적화'].iloc[:-1].sum()
            tov   = df8['최적화V'].iloc[:-1].sum()
            tovc  = df8['최적화VC'].iloc[:-1].sum()
            toht  = df8['최적화T'].iloc[:-1].sum()
            tovt  = df8['최적화VT'].iloc[:-1].sum()
            tovct = df8['최적화VCT'].iloc[:-1].sum()
            tog   = df8['최적화OG'].iloc[:-1].sum()
            togv  = df8['최적화OGV'].iloc[:-1].sum()
            togvc = df8['최적화OGVC'].iloc[:-1].sum()
            toc   = df8['최적화OC'].iloc[:-1].sum()
            tocv  = df8['최적화OCV'].iloc[:-1].sum()
            tocvc = df8['최적화OCVC'].iloc[:-1].sum()
            trh   = df8['전진분석'].iloc[:-1].sum()
            trv   = df8['전진분석V'].iloc[:-1].sum()
            trvc  = df8['전진분석VC'].iloc[:-1].sum()
            ttb = tbk + tbf + toh + tov + tovc + toht + tovt + tovct + tog + togv + togvc + toc + tocv + tocvc + trh + trv + trvc
            abk   = df8['백테스트'].iloc[:-1].mean()
            abf   = df8['백파인더'].iloc[:-1].mean()
            aoh   = df8['최적화'].iloc[:-1].mean()
            aov   = df8['최적화V'].iloc[:-1].mean()
            aovc  = df8['최적화VC'].iloc[:-1].mean()
            aoht  = df8['최적화T'].iloc[:-1].mean()
            aovt  = df8['최적화VT'].iloc[:-1].mean()
            aovct = df8['최적화VCT'].iloc[:-1].mean()
            aog   = df8['최적화OG'].iloc[:-1].mean()
            aogv  = df8['최적화OGV'].iloc[:-1].mean()
            aogvc = df8['최적화OGVC'].iloc[:-1].mean()
            aoc   = df8['최적화OC'].iloc[:-1].mean()
            aocv  = df8['최적화OCV'].iloc[:-1].mean()
            aocvc = df8['최적화OCVC'].iloc[:-1].mean()
            arh   = df8['전진분석'].iloc[:-1].mean()
            arv   = df8['전진분석V'].iloc[:-1].mean()
            arvc  = df8['전진분석VC'].iloc[:-1].mean()
            tta = abk + abf + aoh + aov + aovc + aoht + aovt + aovct + aog + aogv + aogvc + aoc + aocv + aocvc + arh + arv + arvc
            mbk, mbf, moh, mov, movc, moht, movt, movct, mog, mogv, mogvc, moc, mocv, mocvc, mrh, mrv, mrvc = df8.iloc[-1]
            ttm = mbk + mbf + moh + mov + movc + moht + movt + movct + mog + mogv + mogvc + moc + mocv + mocvc + mrh + mrv + mrvc
            df8 = pd.DataFrame(columns=columns_sb)
            df8.loc[0] = '합계', tbk, tbf, toh, tov, tovc, toht, tovt, tovct, tog, togv, togvc, toc, tocv, tocvc, trh, trv, trvc, ttb
            df8.loc[1] = '평균', abk, abf, aoh, aov, aovc, aoht, aovt, aovct, aog, aogv, aogvc, aoc, aocv, aocvc, arh, arv, arvc, tta
            df8.loc[2] = 'MY', mbk, mbf, moh, mov, movc, moht, movt, movct, mog, mogv, mogvc, moc, mocv, mocvc, mrh, mrv, mrvc, ttm

        if df1 is not None:
            self.windowQ.put((ui_num['스톰라이브1'], df1))
        if df2 is not None:
            self.windowQ.put((ui_num['스톰라이브2'], df2))
        if df3 is not None:
            self.windowQ.put((ui_num['스톰라이브3'], df3))
        if df4 is not None:
            self.windowQ.put((ui_num['스톰라이브4'], df4))
        if df5 is not None:
            self.windowQ.put((ui_num['스톰라이브5'], df5))
        if df6 is not None:
            self.windowQ.put((ui_num['스톰라이브6'], df6))
        if df7 is not None:
            self.windowQ.put((ui_num['스톰라이브7'], df7))
        if df8 is not None:
            self.windowQ.put((ui_num['스톰라이브8'], df8))

    @staticmethod
    def tatal_text_conv(i, t):
        try:
            if i == 0:
                return t
            elif i == 5:
                return float(t)
            else:
                return int(float(t))
        except:
            return 0

    @staticmethod
    def back_text_conv(i, t):
        try:
            if i in (0, 1):
                return str(t)
            elif i in (2, 3, 4, 5, 6, 7, 8, 10, 11, 16):
                return int(float(t))
            else:
                return float(t)
        except:
            return 0
