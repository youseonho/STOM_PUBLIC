import os
import re
import psutil
import _pickle
import datetime
import numpy as np
import winreg as reg
from io import BytesIO
from threading import Thread, Timer
from PyQt5.QtTest import QTest
from traceback import print_exc
from cryptography.fernet import Fernet


def threading_timer(sec, func, args=None):
    if args is None:
        Timer(int(sec), func).start()
    elif type(args) == list:
        Timer(int(sec), func, args=args).start()
    else:
        Timer(int(sec), func, args=[args]).start()


def get_port_number():
    port_number = 5500
    run_count = 0
    for proc in psutil.process_iter():
        if 'cmd' in proc.name():
            run_count += 1
    port_number += run_count * 10
    return port_number


def win_proc_alive(name):
    alive = False
    for proc in psutil.process_iter():
        if name in proc.name():
            alive = True
    return alive


def opstarter_kill():
    if win_proc_alive('opstarter'):
        os.system('C:/Windows/System32/taskkill /f /im opstarter.exe')


def array_to_bytes(x: np.ndarray) -> bytes:
    np_bytes = BytesIO()
    # noinspection PyTypeChecker
    np.save(np_bytes, x, allow_pickle=True)
    return np_bytes.getvalue()


def bytes_to_array(b: bytes) -> np.ndarray:
    np_bytes = BytesIO(b)
    return np.load(np_bytes, allow_pickle=True)


def pickle_write(file, data):
    with open(f'{file}.pkl', "wb") as f:
        _pickle.dump(data, f, protocol=-1)


def pickle_read(file):
    data = None
    if os.path.isfile(f'{file}.pkl'):
        with open(f'{file}.pkl', "rb") as f:
            data = _pickle.load(f)
    return data


def pickle_delete(file):
    if os.path.isfile(file):
        os.remove(file)


def thread_decorator(func):
    def wrapper(*args):
        Thread(target=func, args=args, daemon=True).start()

    return wrapper


def error_decorator(func):
    def wrapper(*args):
        try:
            func(*args)
        except:
            print_exc()

    return wrapper


def qtest_qwait(sec):
    # noinspection PyArgumentList
    QTest.qWait(int(sec * 1000))


def now():
    return datetime.datetime.now()


def now_utc():
    return timedelta_sec(-32400)


def int_hms():
    return int(strf_time('%H%M%S'))


def int_hms_utc():
    return int(strf_time('%H%M%S', timedelta_sec(-32400)))


def timedelta_sec(second, std_time=None):
    return now() + datetime.timedelta(seconds=float(second)) if std_time is None else std_time + datetime.timedelta(
        seconds=float(second))


def timedelta_day(day, std_time=None):
    return now() + datetime.timedelta(days=float(day)) if std_time is None else std_time + datetime.timedelta(
        days=float(day))


def strp_time(timetype, str_time):
    if timetype == '%Y%m%d%H%M%S':
        str_time = f'{str_time[:4]}-{str_time[4:6]}-{str_time[6:8]} {str_time[8:10]}:{str_time[10:12]}:{str_time[12:14]}'
    elif timetype == '%Y%m%d':
        str_time = f'{str_time[:4]}-{str_time[4:6]}-{str_time[6:8]}'
    else:
        str_time = f'2000-01-01 {str_time[:2]}:{str_time[2:4]}:{str_time[4:6]}'
    return datetime.datetime.fromisoformat(str_time)


def strf_time(timetype, std_time=None):
    return now().strftime(timetype) if std_time is None else std_time.strftime(timetype)


def from_timestamp(time):
    return datetime.datetime.fromtimestamp(time)


def change_format(text, dotdowndel=False, dotdown4=False, dotdown8=False):
    text = str(text)
    try:
        format_data = f'{int(text):,}'
    except:
        if dotdowndel:
            format_data = f'{float(text):,.0f}'
        elif dotdown4:
            format_data = f'{float(text):,.4f}'
        elif dotdown8:
            format_data = f'{float(text):,.8f}'
        else:
            format_data = f'{float(text):,.2f}'
    return format_data


def floor_down(float_, decimal_point):
    float_ = int(float_ * (1 / decimal_point))
    float_ = float_ * decimal_point
    return float_


def comma2int(t):
    if '.' in t: t = t.split('.')[0]
    if ':' in t: t = t.replace(':', '')
    if ' ' in t: t = t.replace(' ', '')
    if ',' in t: t = t.replace(',', '')
    return int(t)


def comma2float(t):
    if ' ' in t: t = t.replace(' ', '')
    if ',' in t: t = t.replace(',', '')
    return float(t)


def write_key():
    key = str(Fernet.generate_key(), 'utf-8')
    reg.CreateKey(reg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\STOM')
    reg.CreateKey(reg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\STOM\EN_KEY')
    openkey = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\STOM\EN_KEY', 0, reg.KEY_ALL_ACCESS)
    reg.SetValueEx(openkey, 'EN_KEY', 0, reg.REG_SZ, key)
    reg.CloseKey(openkey)


def read_key():
    openkey = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\STOM\EN_KEY', 0, reg.KEY_ALL_ACCESS)
    key, _ = reg.QueryValueEx(openkey, 'EN_KEY')
    reg.CloseKey(openkey)
    return key


def en_text(key, text):
    fernet = Fernet(bytes(key, 'utf-8'))
    return str(fernet.encrypt(bytes(text, 'utf-8')), 'utf-8')


def de_text(key, text):
    fernet = Fernet(bytes(key, 'utf-8'))
    return str(fernet.decrypt(bytes(text, 'utf-8')), 'utf-8')


def factorial(x):
    return 1 if x <= 1 else factorial(x - 1) * x


def text_not_in_special_characters(t):
    t = t.replace(' ', '')
    if t == re.findall(r'\w+', t)[0]:
        return True
    return False


def roundfigure_upper5(price, index):
    if index < 20230125000000:
        if 1000 <= price <= 1025:
            return True
        if 5000 <= price <= 5050:
            return True
        if 10000 <= price <= 10250:
            return True
        if 50000 <= price <= 50500:
            return True
        if 100000 <= price <= 102500:
            return True
        if 500000 <= price <= 505000:
            return True
    else:
        if 2000 <= price <= 2025:
            return True
        if 5000 <= price <= 5050:
            return True
        if 20000 <= price <= 20250:
            return True
        if 50000 <= price <= 50500:
            return True
        if 200000 <= price <= 202500:
            return True
        if 500000 <= price <= 505000:
            return True
    return False


def roundfigure_upper(price, unit, index):
    if index < 20230125000000:
        if 1000 <= price <= 1000 + 5 * unit:
            return True
        if 5000 <= price <= 5000 + 10 * unit:
            return True
        if 10000 <= price <= 10000 + 50 * unit:
            return True
        if 50000 <= price <= 50000 + 100 * unit:
            return True
        if 100000 <= price <= 100000 + 500 * unit:
            return True
        if 500000 <= price <= 500000 + 1000 * unit:
            return True
    else:
        if 2000 <= price <= 2000 + 5 * unit:
            return True
        if 5000 <= price <= 5000 + 10 * unit:
            return True
        if 20000 <= price <= 20000 + 50 * unit:
            return True
        if 50000 <= price <= 50000 + 100 * unit:
            return True
        if 200000 <= price <= 200000 + 500 * unit:
            return True
        if 500000 <= price <= 500000 + 1000 * unit:
            return True
    return False


def roundfigure_lower(price, unit, index):
    if index < 20230125000000:
        if 1000 - 1 * unit <= price <= 1000:
            return True
        if 5000 - 5 * unit <= price <= 5000:
            return True
        if 10000 - 10 * unit <= price <= 10000:
            return True
        if 50000 - 50 * unit <= price <= 50000:
            return True
        if 100000 - 100 * unit <= price <= 100000:
            return True
        if 500000 - 500 * unit <= price <= 500000:
            return True
    else:
        if 2000 - 1 * unit <= price <= 2000:
            return True
        if 5000 - 5 * unit <= price <= 5000:
            return True
        if 20000 - 10 * unit <= price <= 20000:
            return True
        if 50000 - 50 * unit <= price <= 50000:
            return True
        if 200000 - 100 * unit <= price <= 200000:
            return True
        if 500000 - 500 * unit <= price <= 500000:
            return True
    return False


def GetUpbitHogaunit(price):
    if price < 0.01:
        return 0.0001
    elif price < 1:
        return 0.001
    elif price < 10:
        return 0.01
    elif price < 100:
        return 0.1
    elif price < 1000:
        return 1
    elif price < 10000:
        return 5
    elif price < 100000:
        return 10
    elif price < 500000:
        return 50
    elif price < 1000000:
        return 100
    elif price < 2000000:
        return 500
    else:
        return 1000


try:
    from numba import jit


    @jit(nopython=True, cache=True)
    def GetKiwoomPgSgSp(bg, cg):
        texs = int(cg * 0.0018)
        bfee = int(bg * 0.00015 / 10) * 10
        sfee = int(cg * 0.00015 / 10) * 10
        pg = int(cg - texs - bfee - sfee)
        sg = int(round(pg - bg))
        sp = round(sg / bg * 100, 2)
        return pg, sg, sp


    @jit(nopython=True, cache=True)
    def GetUpbitPgSgSp(bg, cg):
        bfee = bg * 0.0005
        sfee = cg * 0.0005
        pg = int(round(cg - bfee - sfee))
        sg = int(round(pg - bg))
        sp = round(sg / bg * 100, 2)
        return pg, sg, sp


    @jit(nopython=True, cache=True)
    def GetBinanceLongPgSgSp(bg, cg, market1, market2):
        bfee = bg * (0.0004 if market1 else 0.0002)
        sfee = (cg - bfee) * (0.0004 if market2 else 0.0002)
        pg = round(cg - bfee - sfee, 4)
        sg = round(pg - bg, 4)
        sp = round(sg / bg * 100, 2)
        return pg, sg, sp


    @jit(nopython=True, cache=True)
    def GetBinanceShortPgSgSp(bg, cg, market1, market2):
        bfee = bg * (0.0004 if market1 else 0.0002)
        sfee = (cg - bfee) * (0.0004 if market2 else 0.0002)
        pg = round(bg + bg - cg - bfee - sfee, 4)
        sg = round(pg - bg, 4)
        sp = round(sg / bg * 100, 2)
        return pg, sg, sp


    @jit(nopython=True, cache=True)
    def GetVIPrice(kosd, std_price, index):
        uvi = int(std_price * 1.1)
        x = GetHogaunit(kosd, uvi, index)
        if uvi % x != 0:
            uvi += x - uvi % x
        dvi = int(std_price * 0.9)
        y = GetHogaunit(kosd, dvi, index)
        if dvi % y != 0:
            dvi -= dvi % y
        return int(uvi), int(dvi), int(x)


    @jit(nopython=True, cache=True)
    def GetSangHahanga(kosd, predayclose, index):
        uplimitprice = int(predayclose * 1.30)
        x = GetHogaunit(kosd, uplimitprice, index)
        if uplimitprice % x != 0:
            uplimitprice -= uplimitprice % x
        downlimitprice = int(predayclose * 0.70)
        x = GetHogaunit(kosd, downlimitprice, index)
        if downlimitprice % x != 0:
            downlimitprice += x - downlimitprice % x
        return int(uplimitprice), int(downlimitprice)


    @jit(nopython=True, cache=True)
    def GetUvilower5(uvi, hogaunit, index):
        upper5 = uvi - hogaunit * 5
        if GetHogaunit(True, upper5, index) != hogaunit:
            k = 0
            hogaunit2 = 0
            for i in (1, 2, 3, 4, 5):
                hogaunit_ = GetHogaunit(True, uvi - hogaunit * i, index)
                if hogaunit_ != hogaunit:
                    hogaunit2 = hogaunit_
                    break
                k += 1
            upper5 = uvi - hogaunit * k - hogaunit2 * (5 - k)
        return upper5


    @jit(nopython=True, cache=True)
    def GetHogaunit(kosd, price, index):
        if index < 20230125000000:
            if price < 1000:
                x = 1
            elif price < 5000:
                x = 5
            elif price < 10000:
                x = 10
            elif price < 50000:
                x = 50
            elif kosd:
                x = 100
            elif price < 100000:
                x = 100
            elif price < 500000:
                x = 500
            else:
                x = 1000
        else:
            if price < 2000:
                x = 1
            elif price < 5000:
                x = 5
            elif price < 20000:
                x = 10
            elif price < 50000:
                x = 50
            elif price < 200000:
                x = 100
            elif price < 500000:
                x = 500
            else:
                x = 1000
        return x
except:
    def GetKiwoomPgSgSp(bg, cg):
        texs = int(cg * 0.0018)
        bfee = int(bg * 0.00015 / 10) * 10
        sfee = int(cg * 0.00015 / 10) * 10
        pg = int(cg - texs - bfee - sfee)
        sg = int(round(pg - bg))
        sp = round(sg / bg * 100, 2)
        return pg, sg, sp


    def GetUpbitPgSgSp(bg, cg):
        bfee = bg * 0.0005
        sfee = cg * 0.0005
        pg = int(round(cg - bfee - sfee))
        sg = int(round(pg - bg))
        sp = round(sg / bg * 100, 2)
        return pg, sg, sp


    def GetBinanceLongPgSgSp(bg, cg, market1, market2):
        bfee = bg * (0.0004 if market1 else 0.0002)
        sfee = (cg - bfee) * (0.0004 if market2 else 0.0002)
        pg = round(cg - bfee - sfee, 4)
        sg = round(pg - bg, 4)
        sp = round(sg / bg * 100, 2)
        return pg, sg, sp


    def GetBinanceShortPgSgSp(bg, cg, market1, market2):
        bfee = bg * (0.0004 if market1 else 0.0002)
        sfee = (cg - bfee) * (0.0004 if market2 else 0.0002)
        pg = round(bg + bg - cg - bfee - sfee, 4)
        sg = round(pg - bg, 4)
        sp = round(sg / bg * 100, 2)
        return pg, sg, sp


    def GetVIPrice(kosd, std_price, index):
        uvi = int(std_price * 1.1)
        x = GetHogaunit(kosd, uvi, index)
        if uvi % x != 0:
            uvi += x - uvi % x
        dvi = int(std_price * 0.9)
        y = GetHogaunit(kosd, dvi, index)
        if dvi % y != 0:
            dvi -= dvi % y
        return int(uvi), int(dvi), int(x)


    def GetSangHahanga(kosd, predayclose, index):
        uplimitprice = int(predayclose * 1.30)
        x = GetHogaunit(kosd, uplimitprice, index)
        if uplimitprice % x != 0:
            uplimitprice -= uplimitprice % x
        downlimitprice = int(predayclose * 0.70)
        x = GetHogaunit(kosd, downlimitprice, index)
        if downlimitprice % x != 0:
            downlimitprice += x - downlimitprice % x
        return int(uplimitprice), int(downlimitprice)


    def GetUvilower5(uvi, hogaunit, index):
        upper5 = uvi - hogaunit * 5
        if GetHogaunit(True, upper5, index) != hogaunit:
            k = 0
            hogaunit2 = 0
            for i in (1, 2, 3, 4, 5):
                hogaunit_ = GetHogaunit(True, uvi - hogaunit * i, index)
                if hogaunit_ != hogaunit:
                    hogaunit2 = hogaunit_
                    break
                k += 1
            upper5 = uvi - hogaunit * k - hogaunit2 * (5 - k)
        return upper5


    def GetHogaunit(kosd, price, index):
        if index < 20230125000000:
            if price < 1000:
                x = 1
            elif price < 5000:
                x = 5
            elif price < 10000:
                x = 10
            elif price < 50000:
                x = 50
            elif kosd:
                x = 100
            elif price < 100000:
                x = 100
            elif price < 500000:
                x = 500
            else:
                x = 1000
        else:
            if price < 2000:
                x = 1
            elif price < 5000:
                x = 5
            elif price < 20000:
                x = 10
            elif price < 50000:
                x = 50
            elif price < 200000:
                x = 100
            elif price < 500000:
                x = 500
            else:
                x = 1000
        return x
