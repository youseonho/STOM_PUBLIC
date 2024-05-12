import time
import ntplib
import win32api
from dateutil import tz
from datetime import datetime

try:
    ntp_client = ntplib.NTPClient()
    while True:
        response = ntp_client.request('time.windows.com', version=3)
        dt = datetime.utcfromtimestamp(response.tx_time + response.delay)
        localtime = dt.astimezone(tz.tzlocal())
        offset = abs(response.offset)
        if offset >= 0.01:
            # noinspection PyUnresolvedReferences
            win32api.SetSystemTime(
                localtime.year,
                localtime.month,
                localtime.weekday(),
                localtime.day,
                localtime.hour,
                localtime.minute,
                localtime.second,
                localtime.microsecond // 1000
            )
            print(f'표준시간 동기화 중 ... 현재 표준시간과의 차이는 [{offset:.6f}]초입니다.')
        else:
            print(f'표준시간 동기화 완 ... 현재 표준시간과의 차이는 [{offset:.6f}]초입니다.')
            break
        time.sleep(1)
except:
    pass
