import telegram
import pandas as pd
from utility.setting import DICT_SET
from telegram.ext import Updater, MessageHandler, Filters


class TelegramMsg:
    def __init__(self, qlist):
        """
        windowQ, soundQ, queryQ, teleQ, chartQ, hogaQ, webcQ, backQ, creceivQ, ctraderQ,  cstgQ, liveQ, kimpQ, wdzservQ
           0        1       2      3       4      5      6      7       8         9         10     11    12      13
        """
        self.windowQ  = qlist[0]
        self.teleQ    = qlist[3]
        self.ctraderQ = qlist[9]
        self.cstgQ    = qlist[10]
        self.wdzservQ = qlist[13]
        self.dict_set = None
        self.updater  = None
        self.bot      = None
        self.UpdateBot(DICT_SET)
        self.Start()

    def Start(self):
        while True:
            data = self.teleQ.get()
            if type(data) == str:
                if '.png' not in data:
                    self.SendMsg(data)
                else:
                    self.SendPhoto(data)
            elif type(data) == pd.DataFrame:
                self.UpdateDataframe(data)
            elif data[0] == '설정변경':
                if self.updater is not None:
                    self.updater.stop()
                    self.updater = None
                self.UpdateBot(data[1])

    def __del__(self):
        if self.updater is not None:
            self.updater.stop()

    def UpdateBot(self, dict_set):
        self.dict_set = dict_set
        if self.updater is None and self.dict_set['텔레그램봇토큰'] is not None:
            try:
                self.bot = telegram.Bot(self.dict_set['텔레그램봇토큰'])
            except:
                print('텔레그램 설정 오류 알림 - 텔레그램 봇토큰이 잘못되어 봇을 만들 수 없습니다.')
            else:
                self.SetCustomButton()
        else:
            self.bot = None

    def SetCustomButton(self):
        custum_button = [
            ['S잔고청산', 'S전략중지', 'C잔고청산', 'C전략중지'],
            ['S체결목록', 'S거래목록', 'S잔고평가'],
            ['C체결목록', 'C거래목록', 'C잔고평가'],
            ['S스톰라이브', 'C스톰라이브', '백테라이브']
        ]
        reply_markup = telegram.ReplyKeyboardMarkup(custum_button)
        self.bot.send_message(chat_id=self.dict_set['텔레그램사용자아이디'], text='사용자버튼 설정을 완료하였습니다.', reply_markup=reply_markup)
        self.updater = Updater(self.dict_set['텔레그램봇토큰'])
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.ButtonClicked))
        self.updater.start_polling(drop_pending_updates=True)

    def ButtonClicked(self, update, context):
        if context == '':
            return
        cmd = update.message.text
        if cmd == 'S전략중지':
            self.wdzservQ.put(('strategy', '매수전략중지'))
            self.SendMsg('주식 전략 중지 완료')
        elif cmd == 'C전략중지':
            self.cstgQ.put('매수전략중지')
            self.SendMsg('코인 전략 중지 완료')
        elif '라이브' in cmd:
            self.windowQ.put(cmd)
        elif 'S' in cmd:
            self.wdzservQ.put(('trader', cmd))
        elif 'C' in cmd:
            self.ctraderQ.put(cmd)

    def SendMsg(self, msg):
        if self.bot is not None:
            try:
                self.bot.sendMessage(chat_id=self.dict_set['텔레그램사용자아이디'], text=msg)
            except Exception as e:
                print(f'텔레그램 명령 오류 알림 - sendMessage {e}')
        else:
            print('텔레그램 설정 오류 알림 - 텔레그램 봇이 설정되지 않아 메세지를 보낼 수 없습니다.')

    def SendPhoto(self, path):
        if self.bot is not None:
            try:
                with open(path, 'rb') as image:
                    self.bot.send_photo(chat_id=self.dict_set['텔레그램사용자아이디'], photo=image)
            except Exception as e:
                print(f'텔레그램 명령 오류 알림 - send_photo {e}')
        else:
            print('텔레그램 설정 오류 알림 - 텔레그램 봇이 설정되지 않아 스크린샷를 보낼 수 없습니다.')

    def UpdateDataframe(self, df):
        if df.columns[1] == '매수금액':
            text = ''
            for index in df.index:
                ct    = df['체결시간'][index][8:10] + ':' + df['체결시간'][index][10:12]
                per   = df['수익률'][index]
                sg    = df['수익금'][index]
                name  = df['종목명'][index]
                text += f'{ct} {per:.2f}% {sg:,.0f}원 {name}\n'
            self.SendMsg(text)
        elif df.columns[1] in ('매입가', '포지션'):
            text   = ''
            m_unit = '원' if df.columns[1] == '매입가' else 'USDT'
            for index in df.index:
                per   = df['수익률'][index]
                sg    = df['평가손익'][index]
                name  = df['종목명'][index]
                if df.columns[1] == '매입가':
                    text += f'{per:.2f}% {sg:,.0f}{m_unit} {name}\n'
                else:
                    pos   = df['포지션'][index]
                    text += f'{pos} {per:.2f}% {sg:,.0f}{m_unit} {name}\n'
            tbg   = df['매입금액'].sum()
            tpg   = df['평가금액'].sum()
            tsg   = df['평가손익'].sum()
            tsp   = round(tsg / tbg * 100, 2)
            text += f'{tbg:,.0f}{m_unit} {tpg:,.0f}{m_unit} {tsp:.2f}% {tsg:,.0f}{m_unit}\n'
            self.SendMsg(text)
        elif df.columns[1] == '주문구분':
            text = ''
            for index in df.index:
                ct   = df['체결시간'][index][8:10] + ':' + df['체결시간'][index][10:12]
                bs   = df['주문구분'][index]
                bp   = df['체결가'][index]
                name = df['종목명'][index]
                text += f'{ct} {bs} {bp:,.0f} {name}\n'
            self.SendMsg(text)
