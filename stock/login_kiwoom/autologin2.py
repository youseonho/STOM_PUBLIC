import time
import telegram
import pythoncom
from manuallogin import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from multiprocessing import Process
from PyQt5.QAxContainer import QAxWidget
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from utility.static import opstarter_kill
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
        self.AutoLoginOn()

    def AutoLoginOn(self):
        print('자동 로그인 설정 대기 중 ...')
        QTimer.singleShot(1000, lambda: auto_on(2))
        self.ocx.dynamicCall('KOA_Functions(QString, QString)', 'ShowAccountWindow', '')
        opstarter_kill()


if __name__ == '__main__':
    opstarter_kill()
    autologin_dat = f'{OPENAPI_PATH}/system/Autologin.dat'
    if os.path.isfile(autologin_dat): os.remove(autologin_dat)
    print('자동 로그인 설정 파일 삭제 완료')

    Process(target=Window, daemon=True).start()
    print('자동 로그인 설정용 프로세스 시작')

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

    while find_window('Open API login') != 0:
        try:
            hwnd = find_window('인증서 만료공지')
            if hwnd != 0:
                click_button(win32gui.GetDlgItem(hwnd, 0x7F3))
                click_button(win32gui.GetDlgItem(hwnd, 0x1))
                TelegramMassage('인증서 만료기간이 얼마남지 않았습니다.\n인증서를 갱신하십시오.')
        except:
            pass

    time.sleep(5)
    sys.exit()
