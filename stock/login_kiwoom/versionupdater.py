import time
import telegram
import pythoncom
from manuallogin import *
from PyQt5 import QtWidgets
from multiprocessing import Process
from PyQt5.QAxContainer import QAxWidget
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from utility.static import now, timedelta_sec, opstarter_kill
from utility.setting import OPENAPI_PATH, DICT_SET


def TelegramMassage(txt):
    try:
        bot = telegram.Bot(DICT_SET['텔레그램봇토큰'])
        bot.sendMessage(chat_id=DICT_SET['텔레그램사용자아이디'], text=txt)
    except:
        print(txt)


class Window(QtWidgets.QMainWindow):
    app = QtWidgets.QApplication(sys.argv)

    def __init__(self):
        super().__init__()
        self.bool_connected = False
        self.ocx = QAxWidget('KHOPENAPI.KHOpenAPICtrl.1')
        self.ocx.OnEventConnect.connect(self.OnEventConnect)
        self.CommConnect()

    def CommConnect(self):
        self.ocx.dynamicCall('CommConnect()')
        while not self.bool_connected:
            pythoncom.PumpWaitingMessages()

    def OnEventConnect(self, err_code):
        if err_code == 0:
            self.bool_connected = True
            sys.exit()


if __name__ == '__main__':
    opstarter_kill()
    autologin_dat = f'{OPENAPI_PATH}/system/Autologin.dat'
    if os.path.isfile(autologin_dat): os.remove(autologin_dat)
    print('자동 로그인 설정 파일 삭제 완료')

    proc = Process(target=Window, daemon=True)
    proc.start()

    print('버전처리용 로그인 프로세스 시작')
    while find_window('Open API login') == 0:
        print('로그인창 열림 대기 중 ...')
        time.sleep(1)

    print('아이디 및 패스워드 입력 대기 중 ...')
    time.sleep(2)

    if DICT_SET['증권사'] == '키움증권1':
        manual_login(4)
    elif DICT_SET['증권사'] == '키움증권2':
        manual_login(8)
    print('아이디 및 패스워드 입력 완료')

    update = False
    endtime = timedelta_sec(90)
    while find_window('Open API login') != 0:
        hwnd = find_window('인증서 만료공지')
        if hwnd != 0:
            try:
                click_button(win32gui.GetDlgItem(hwnd, 0x7F3))
                click_button(win32gui.GetDlgItem(hwnd, 0x1))
                TelegramMassage('인증서 만료기간이 얼마남지 않았습니다.\n인증서를 갱신하십시오.')
            except:
                pass

        hwnd = find_window('opstarter')
        if hwnd != 0:
            try:
                static_hwnd = win32gui.GetDlgItem(hwnd, 0xFFFF)
                text = win32gui.GetWindowText(static_hwnd)
                if '버전처리' in text:
                    if proc.is_alive(): proc.kill()
                    click_button(win32gui.GetDlgItem(hwnd, 0x2))
                    print('버전 업그레이드 완료')
                    update = True
            except:
                pass

        if not proc.is_alive():
            break

        print('버전처리 및 로그인창 닫힘 대기 중 ...')
        time.sleep(1)
        if now() > endtime:
            opstarter_kill()
            break

    if update:
        time.sleep(5)
        hwnd = find_window('업그레이드 확인')
        if hwnd != 0:
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        print('버전 업그레이드 확인 완료')

    opstarter_kill()
    sys.exit()
