import time
import json
import uuid
import pyupbit
import asyncio
import operator
import websockets
import numpy as np
import pandas as pd
from multiprocessing import Process, Queue
from utility.setting import ui_num, DICT_SET
from utility.static import now, strf_time, strp_time, timedelta_sec, from_timestamp, int_hms_utc, threading_timer


class ReceiverUpbit:
    def __init__(self, qlist):
        """
        windowQ, soundQ, queryQ, teleQ, chartQ, hogaQ, webcQ, backQ, creceivQ, ctraderQ,  cstgQ, liveQ, kimpQ, wdzservQ
           0        1       2      3       4      5      6      7       8         9         10     11    12      13
        """
        self.windowQ  = qlist[0]
        self.soundQ   = qlist[1]
        self.queryQ   = qlist[2]
        self.teleQ    = qlist[3]
        self.hogaQ    = qlist[5]
        self.creceivQ = qlist[8]
        self.ctraderQ = qlist[9]
        self.cstgQ    = qlist[10]
        self.dict_set = DICT_SET

        self.dict_bool = {
            '프로세스종료': False
        }
        self.dict_tick = {}
        self.dict_hgdt = {}
        self.dict_tm5m = {}
        self.dict_arry = {}
        self.dict_mtop = {}
        self.dict_hgbs = {}

        curr_time = now()
        self.dict_time = {
            '티커리스트재조회': timedelta_sec(600),
            '거래대금순위기록': curr_time,
            '거래대금순위저장': curr_time
        }

        self.list_prmt   = []
        self.list_gsjm1  = []
        self.list_gsjm2  = []
        self.tuple_jang  = ()
        self.tuple_order = ()

        self.int_logt         = int(strf_time('%Y%m%d%H%M', timedelta_sec(-32400)))
        self.int_jcct         = int(strf_time('%Y%m%d%H%M%S', timedelta_sec(-32400)))
        self.dt_mtct          = None
        self.hoga_code        = None
        self.proc_webs        = None
        self.proc_webs_orderb = None
        self.codes            = None
        self.MainLoop()

    def MainLoop(self):
        text = '코인 리시버를 시작하였습니다.'
        if self.dict_set['코인알림소리']: self.soundQ.put(text)
        self.teleQ.put(text)
        self.windowQ.put((ui_num['C단순텍스트'], '시스템 명령 실행 알림 - 리시버 시작'))
        self.GetTickers()
        wsq = Queue()
        while True:
            curr_time = now()
            inthmsutc = int_hms_utc()

            if self.proc_webs is None or not self.proc_webs.is_alive():
                self.WebSocketsStart(wsq)

            if not self.creceivQ.empty():
                data = self.creceivQ.get()
                if type(data) == tuple:
                    self.UpdateTuple(data)
                if data == '프로세스종료':
                    self.ctraderQ.put('프로세스종료')
                    self.cstgQ.put('프로세스종료')
                    self.WebProcessKill()
                    break

            if not wsq.empty():
                data = wsq.get()
                if data == 'ConnectionClosedError':
                    self.windowQ.put((ui_num['C단순텍스트'], '시스템 명령 오류 알림 - 웹소켓 연결 끊김으로 다시 연결합니다.'))
                    self.WebProcessKill()
                elif data[0] == 'ticker':
                    try:
                        data      = data[1]
                        code      = data['code']
                        c         = data['trade_price']
                        o         = data['opening_price']
                        h         = data['high_price']
                        low       = data['low_price']
                        per = round(data['signed_change_rate'] * 100, 2)
                        tbids     = data['acc_bid_volume']
                        tasks     = data['acc_ask_volume']
                        dm        = data['acc_trade_price']
                        dt        = int(strf_time('%Y%m%d%H%M%S', from_timestamp(int(data['timestamp'] / 1000 - 32400))))
                    except Exception as e:
                        self.windowQ.put((ui_num['C단순텍스트'], f'시스템 명령 오류 알림 - 웹소켓 ticker {e}'))
                    else:
                        self.UpdateTickData(code, c, o, h, low, per, dm, tbids, tasks, dt)
                elif data[0] == 'orderbook':
                    try:
                        data = data[1]
                        code = data['code']
                        dt = int(strf_time('%Y%m%d%H%M%S', from_timestamp(int(data['timestamp'] / 1000 - 32400))))
                        hoga_tamount = (
                            data['total_ask_size'], data['total_bid_size']
                        )
                        data = data['orderbook_units']
                        hoga_seprice = (
                            data[9]['ask_price'], data[8]['ask_price'], data[7]['ask_price'], data[6]['ask_price'], data[5]['ask_price'],
                            data[4]['ask_price'], data[3]['ask_price'], data[2]['ask_price'], data[1]['ask_price'], data[0]['ask_price']
                        )
                        hoga_buprice = (
                            data[0]['bid_price'], data[1]['bid_price'], data[2]['bid_price'], data[3]['bid_price'], data[4]['bid_price'],
                            data[5]['bid_price'], data[6]['bid_price'], data[7]['bid_price'], data[8]['bid_price'], data[9]['bid_price']
                        )
                        hoga_samount = (
                            data[9]['ask_size'], data[8]['ask_size'], data[7]['ask_size'], data[6]['ask_size'], data[5]['ask_size'],
                            data[4]['ask_size'], data[3]['ask_size'], data[2]['ask_size'], data[1]['ask_size'], data[0]['ask_size']
                        )
                        hoga_bamount = (
                            data[0]['bid_size'], data[1]['bid_size'], data[2]['bid_size'], data[3]['bid_size'], data[4]['bid_size'],
                            data[5]['bid_size'], data[6]['bid_size'], data[7]['bid_size'], data[8]['bid_size'], data[9]['bid_size']
                        )
                    except Exception as e:
                        self.windowQ.put((ui_num['C단순텍스트'], f'시스템 명령 오류 알림 - 웹소켓 orderbook {e}'))
                    else:
                        self.UpdateHogaData(dt, hoga_tamount, hoga_seprice, hoga_buprice, hoga_samount, hoga_bamount, code, curr_time)

            if curr_time > self.dict_time['거래대금순위기록']:
                self.UpdateMoneyTop()
                self.dict_time['거래대금순위기록'] = timedelta_sec(1)

            if curr_time > self.dict_time['거래대금순위저장']:
                self.MoneyTopSearch()
                df = pd.DataFrame(self.dict_mtop.values(), columns=['거래대금순위'], index=list(self.dict_mtop.keys()))
                self.queryQ.put(('코인디비', df, 'moneytop', 'append'))
                self.dict_mtop = {}
                self.dict_time['거래대금순위저장'] = timedelta_sec(10)

            if self.dict_set['코인장초전략종료시간'] < inthmsutc < self.dict_set['코인장초전략종료시간'] + 10:
                if self.dict_set['코인장초프로세스종료'] and not self.dict_bool['프로세스종료']:
                    self.ReceiverProcKill()

            if self.dict_set['코인장중전략종료시간'] < inthmsutc < self.dict_set['코인장중전략종료시간'] + 10:
                if self.dict_set['코인장중프로세스종료'] and not self.dict_bool['프로세스종료']:
                    self.ReceiverProcKill()

            if curr_time > self.dict_time['티커리스트재조회']:
                codes = pyupbit.get_tickers(fiat="KRW")
                if len(codes) > len(self.codes):
                    self.codes = codes
                    self.ctraderQ.put('코인명갱신')
                    self.WebProcessKill()
                self.dict_time['티커리스트재조회'] = timedelta_sec(600)

            if self.creceivQ.empty() and wsq.empty():
                time.sleep(0.001)

        self.windowQ.put((ui_num['C단순텍스트'], '시스템 명령 실행 알림 - 리시버 종료'))
        time.sleep(1)

    def ReceiverProcKill(self):
        self.dict_bool['프로세스종료'] = True
        threading_timer(180, self.creceivQ.put, '프로세스종료')

    def WebSocketsStart(self, wsq):
        self.proc_webs = Process(target=WebSocketManager, args=(self.codes, wsq), daemon=True)
        self.proc_webs.start()

    def WebProcessKill(self):
        if self.proc_webs.is_alive(): self.proc_webs.kill()
        time.sleep(3)

    def GetTickers(self):
        self.codes = pyupbit.get_tickers(fiat="KRW")
        for i, code in enumerate(self.codes):
            self.dict_hgbs[code] = [0, 0]

        last = len(self.codes)
        for i, code in enumerate(self.codes):
            time.sleep(0.05)
            df = pyupbit.get_ohlcv(ticker=code, interval='minutes5')
            if df is not None:
                self.dict_tm5m[code] = df['value'].iloc[-1]
            print(f'분봉 데이터 조회 중 ... [{i+1}/{last}][{code}]')

        self.list_prmt = [x for x, y in sorted(self.dict_tm5m.items(), key=operator.itemgetter(1), reverse=True)[:self.dict_set['코인순위선정']]]
        for code in self.list_prmt:
            self.InsertGsjmlist(code)
        self.list_gsjm1 = self.list_prmt[:-3]
        self.list_gsjm2 = self.list_prmt
        data = tuple(self.list_gsjm2)
        self.cstgQ.put(('관심목록', data))

    def UpdateTuple(self, data):
        gubun, data = data
        if gubun == '잔고목록':
            self.tuple_jang = data
        elif gubun == '주문목록':
            self.tuple_order = data
        elif gubun == '호가종목코드':
            self.hoga_code = data
        elif gubun == '설정변경':
            self.dict_set = data
            if not self.dict_set['코인리시버'] and not self.dict_set['코인트레이더']:
                self.creceivQ.put('프로세스종료')

    def UpdateTickData(self, code, c, o, h, low, per, dm, tbids, tasks, dt):
        if dt != self.int_jcct and dt > self.int_jcct:
            self.int_jcct = dt

        try:
            ch = round(tbids / tasks * 100, 2)
        except:
            ch = 500.
        ch = 500. if ch > 500 else ch

        if code in self.dict_tick.keys():
            prebids, preasks, pretbids, pretasks = self.dict_tick[code][7:]
        else:
            prebids, preasks, pretbids, pretasks = 0, 0, tbids, tasks

        bids_ = round(tbids - pretbids, 8) if tbids >= pretbids else tbids
        asks_ = round(tasks - pretasks, 8) if tasks >= pretasks else tasks
        bids  = round(prebids + bids_, 8)  if tbids >= pretbids else bids_
        asks  = round(preasks + asks_, 8)  if tasks >= pretasks else asks_
        self.dict_tick[code] = [c, o, h, low, per, dm, ch, bids, asks, tbids, tasks]

        if tbids > pretbids:
            self.dict_hgbs[code] = (0, c)
        elif tasks > pretasks:
            self.dict_hgbs[code] = (c, 2147483648)

        dt_ = int(str(dt)[:13])
        if code not in self.dict_arry.keys():
            self.dict_arry[code] = np.array([[dt_, dm]])
        elif dt_ != self.dict_arry[code][-1, 0]:
            self.dict_arry[code] = np.r_[self.dict_arry[code], np.array([[dt_, dm]])]
            if len(self.dict_arry[code]) == self.dict_set['코인순위시간'] * 6:
                self.dict_tm5m[code] = dm - self.dict_arry[code][0, 1]
                self.dict_arry[code] = np.delete(self.dict_arry[code], 0, 0)

    def UpdateHogaData(self, dt, hoga_tamount, hoga_seprice, hoga_buprice, hoga_samount, hoga_bamount, code, receivetime):
        sm = 0
        int_logt = int(str(dt)[:12])
        ticksend = False
        if code in self.dict_tick.keys():
            if code in self.dict_hgdt.keys():
                if dt > self.dict_hgdt[code][0]:
                    if self.dict_tick[code][5] >= self.dict_hgdt[code][1]:
                        sm = self.dict_tick[code][5] - self.dict_hgdt[code][1]
                    else:
                        sm = self.dict_tick[code][5]
                    ticksend = True
            else:
                ticksend = True

        if ticksend:
            csp, cbp = self.dict_hgbs[code]

            if hoga_seprice[-1] < csp:
                index = 0
                for i, price in enumerate(hoga_seprice[::-1]):
                    if price >= csp:
                        index = i
                        break
                if index <= 5:
                    hoga_seprice = hoga_seprice[5 - index:10 - index]
                    hoga_samount = hoga_samount[5 - index:10 - index]
                else:
                    hoga_seprice = tuple(np.zeros(index - 5)) + hoga_seprice[:10 - index]
                    hoga_samount = tuple(np.zeros(index - 5)) + hoga_samount[:10 - index]
            else:
                hoga_seprice = hoga_seprice[-5:]
                hoga_samount = hoga_samount[-5:]

            if hoga_buprice[0] > cbp:
                index = 0
                for i, price in enumerate(hoga_buprice):
                    if price <= cbp:
                        index = i
                        break
                hoga_buprice = hoga_buprice[index:index + 5]
                hoga_bamount = hoga_bamount[index:index + 5]
                if index > 5:
                    hoga_buprice = hoga_buprice + tuple(np.zeros(index - 5))
                    hoga_bamount = hoga_bamount + tuple(np.zeros(index - 5))
            else:
                hoga_buprice = hoga_buprice[:5]
                hoga_bamount = hoga_bamount[:5]

            c     = self.dict_tick[code][0]
            hlp   = round((c / ((self.dict_tick[code][2] + self.dict_tick[code][3]) / 2) - 1) * 100, 2)
            hgjrt = sum(hoga_samount + hoga_bamount)
            logt  = now() if self.int_logt < int_logt else 0
            gsjm  = 1 if code in self.list_gsjm1 else 0
            data  = (dt,) + tuple(self.dict_tick[code][:9]) + (sm, hlp) + hoga_tamount + hoga_seprice + hoga_buprice + hoga_samount + hoga_bamount + (hgjrt, gsjm, code, logt)

            self.cstgQ.put(data)
            if code in self.tuple_order or code in self.tuple_jang:
                self.ctraderQ.put((code, c))

            if self.hoga_code == code:
                c, o, h, low, per, _, ch, bids, asks, _, _ = self.dict_tick[code]
                self.hogaQ.put((code, c, per, 0, 0, o, h, low))
                self.hogaQ.put((-asks, ch))
                self.hogaQ.put((bids, ch))
                self.hogaQ.put((code,) + hoga_tamount + hoga_seprice[-5:] + hoga_buprice[:5] + hoga_samount[-5:] + hoga_bamount[:5])

            self.dict_hgdt[code] = [dt, self.dict_tick[code][5]]
            self.dict_tick[code][7:9] = [0, 0]

        if self.int_logt < int_logt:
            gap = (now() - receivetime).total_seconds()
            self.windowQ.put((ui_num['C단순텍스트'], f'리시버 연산 시간 알림 - 수신시간과 연산시간의 차이는 [{gap:.6f}]초입니다.'))
            self.int_logt = int_logt

    def UpdateMoneyTop(self):
        data = tuple(self.list_gsjm2)
        self.cstgQ.put(('관심목록', data))

        text_gsjm = ';'.join(self.list_gsjm1)
        curr_strtime = str(self.int_jcct)
        curr_datetime = strp_time('%Y%m%d%H%M%S', curr_strtime)

        if self.dt_mtct is not None:
            gap_seconds = (curr_datetime - self.dt_mtct).total_seconds()
            while gap_seconds > 1:
                gap_seconds -= 1
                pre_time = strf_time('%Y%m%d%H%M%S', timedelta_sec(-gap_seconds, curr_datetime))
                self.dict_mtop[int(pre_time)] = text_gsjm

        if curr_datetime != self.dt_mtct:
            self.dict_mtop[int(curr_strtime)] = text_gsjm
            self.dt_mtct = curr_datetime

    def MoneyTopSearch(self):
        if len(self.dict_tm5m) > 0:
            list_mtop = [x for x, y in sorted(self.dict_tm5m.items(), key=operator.itemgetter(1), reverse=True)[:self.dict_set['코인순위선정']]]
            self.list_gsjm1 = list_mtop[:-3]

            insert_list = list(set(list_mtop) - set(self.list_prmt))
            if len(insert_list) > 0:
                for code in insert_list:
                    self.InsertGsjmlist(code)

            delete_list = list(set(self.list_prmt) - set(list_mtop))
            if len(delete_list) > 0:
                for code in delete_list:
                    self.DeleteGsjmlist(code)

            self.list_prmt = list_mtop

    def InsertGsjmlist(self, code):
        if code not in self.list_gsjm2:
            self.list_gsjm2.append(code)
            if self.dict_set['코인매도취소관심진입']:
                self.ctraderQ.put(('관심진입', code))

    def DeleteGsjmlist(self, code):
        if code in self.list_gsjm2:
            self.list_gsjm2.remove(code)
            if self.dict_set['코인매수취소관심이탈']:
                self.ctraderQ.put(('관심이탈', code))


class WebSocketManager:
    def __init__(self, codes, q):
        self.codes = codes
        self.q = q
        self.AsyncioLoop()

    async def task_ticker_socket(self):
        uri = "wss://api.upbit.com/websocket/v1"
        async with websockets.connect(uri, ping_interval=60) as websocket:
            data = [{'ticket': str(uuid.uuid4())[:6]}, {'type': 'ticker', 'codes': self.codes, 'isOnlyRealtime': True}]
            await websocket.send(json.dumps(data))
            while True:
                try:
                    recv_data = await websocket.recv()
                    recv_data = json.loads(recv_data.decode('utf8'))
                    self.q.put(('ticker', recv_data))
                except:
                    self.q.put('ConnectionClosedError')

    async def task_orderbook_socket(self):
        uri = "wss://api.upbit.com/websocket/v1"
        async with websockets.connect(uri, ping_interval=60) as websocket:
            data = [{'ticket': str(uuid.uuid4())[:6]}, {'type': 'orderbook', 'codes': self.codes, 'isOnlyRealtime': True}]
            await websocket.send(json.dumps(data))
            while True:
                try:
                    recv_data = await websocket.recv()
                    recv_data = json.loads(recv_data.decode('utf8'))
                    self.q.put(('orderbook', recv_data))
                except:
                    self.q.put('ConnectionClosedError')

    def AsyncioLoop(self):
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.task_ticker_socket())
        asyncio.ensure_future(self.task_orderbook_socket())
        loop.run_forever()
