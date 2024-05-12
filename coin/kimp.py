import re
import json
import time
import uuid
import asyncio
import pyupbit
import requests
import websockets
import pandas as pd
from multiprocessing import Process, Queue
from binance import AsyncClient, BinanceSocketManager
from utility.setting import ui_num, columns_kp
from utility.static import comma2float, threading_timer


class Kimp:
    def __init__(self, qlist):
        """
        windowQ, soundQ, queryQ, teleQ, chartQ, hogaQ, webcQ, backQ, creceivQ, ctraderQ,  cstgQ, liveQ, kimpQ, wdzservQ
           0        1       2      3       4      5      6      7       8         9         10     11    12      13
        """
        self.windowQ   = qlist[0]
        self.kimpQ     = qlist[12]
        self.usdtokrw  = None
        self.proc_webs = None
        self.codes     = None
        self.threadrun = True
        self.df        = pd.DataFrame(columns=columns_kp)
        self.Start()

    def Start(self):
        wsq = Queue()
        self.codes = pyupbit.get_tickers(fiat="KRW")
        self.ConvertedCurrency()
        self.WebsSocketsStart(wsq)
        while True:
            if not self.kimpQ.empty():
                data = self.kimpQ.get()
                if data == '프로세스종료':
                    self.threadrun = False
                    self.WebProcessKill()
                    break

            if not wsq.empty():
                data = wsq.get()
                if data == 'ConnectionClosedError':
                    self.WebProcessKill()
                    self.WebsSocketsStart(wsq)
                elif data[0] == 'upbit':
                    data = data[1]
                    code = data['code'].replace('KRW-', '')
                    c    = data['trade_price']
                    self.df.loc[code, ['종목명', '업비트(원)']] = code, c
                elif data[0] == 'binance' and self.usdtokrw is not None:
                    data = data[1]
                    for x in data:
                        if re.search('USDT$', x['s']) is not None:
                            code = x['s'].replace('USDT', '')
                            c    = float(x['c'])
                            self.df.loc[code, '바이낸스(달러)'] = c

                    self.df['대비(원)'] = self.df['업비트(원)'] - self.df['바이낸스(달러)'] * self.usdtokrw
                    self.df['대비율(%)'] = self.df['대비(원)'] / self.df['업비트(원)'] * 100
                    self.df.dropna(inplace=True)
                    self.df.sort_values(by=['대비율(%)'], ascending=False, inplace=True)
                    self.windowQ.put((ui_num['김프'], self.usdtokrw, self.df))

            if self.kimpQ.empty() and wsq.empty():
                time.sleep(0.001)

        time.sleep(3)

    def ConvertedCurrency(self):
        try:
            source = requests.get('https://www.google.com/search?q=convert+1+United%20States%20Dollar+to+South%20Korean%20won&hl=en&lr=lang_en').text
            results = re.findall("[\d*,]*\.\d* {currency_to_name}".format(currency_to_name='South Korean won'), source)[0]
            converted_currency = re.findall('[\d*,]*\.\d*', results)[0].replace(',', '')
            self.usdtokrw = comma2float(converted_currency)
        except:
            pass

        if self.threadrun:
            threading_timer(5, self.ConvertedCurrency)

    def WebsSocketsStart(self, wsq):
        self.proc_webs = Process(target=WebSocketManager, args=(self.codes, wsq), daemon=True)
        self.proc_webs.start()

    def WebProcessKill(self):
        if self.proc_webs is not None and self.proc_webs.is_alive():
            self.proc_webs.kill()
        time.sleep(3)


class WebSocketManager:
    def __init__(self, codes, q):
        self.codes = codes
        self.q     = q
        self.AsyncioLoop()

    async def task_upbit_ticker_socket(self):
        uri = "wss://api.upbit.com/websocket/v1"
        async with websockets.connect(uri, ping_interval=60) as websocket:
            data = [{'ticket': str(uuid.uuid4())[:6]}, {'type': 'ticker', 'codes': self.codes, 'isOnlyRealtime': True}]
            await websocket.send(json.dumps(data))
            while True:
                try:
                    recv_data = await websocket.recv()
                    recv_data = json.loads(recv_data.decode('utf8'))
                    self.q.put(('upbit', recv_data))
                except:
                    self.q.put('ConnectionClosedError')

    async def task_binance_ticker_socket(self):
        client = await AsyncClient.create()
        bm = BinanceSocketManager(client)
        ms = bm.miniticker_socket()
        async with ms as ticker_socket:
            while True:
                try:
                    recv_data = await ticker_socket.recv()
                    self.q.put(('binance', recv_data))
                except:
                    self.q.put('ConnectionClosedError')

    def AsyncioLoop(self):
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.task_upbit_ticker_socket())
        asyncio.ensure_future(self.task_binance_ticker_socket())
        loop.run_forever()
