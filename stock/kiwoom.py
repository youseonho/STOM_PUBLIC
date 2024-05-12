import os
import sys
import zipfile
import datetime
import pythoncom
import pandas as pd
from PyQt5.QAxContainer import QAxWidget
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utility.setting import OPENAPI_PATH


sn_brrq = 1000
sn_brrd = 1001
sn_cond = 1002
sn_oper = 1003
sn_gsjm = 2000


def parseDat(trcode):
    enc   = zipfile.ZipFile(f'{OPENAPI_PATH}/data/{trcode}.enc')
    lines = enc.read(trcode.upper() + '.dat').decode('cp949')
    lines = lines.split('\n')
    start = [i for i, x in enumerate(lines) if x.startswith('@START')]
    end   = [i for i, x in enumerate(lines) if x.startswith('@END')]
    block = zip(start, end)
    enc_data = {'trcode': trcode, 'input': [], 'output': []}
    for start, end in block:
        block_data = lines[start - 1:end + 1]
        record = block_data[1].split('_')[1].strip().split('=')[0]
        field_name = [line.split('=')[0].strip() for line in block_data[2:-1]]
        fields = {record: field_name}
        enc_data['input'].append(fields) if 'INPUT' in block_data[0] else enc_data['output'].append(fields)
    return enc_data


class Kiwoom:
    def __init__(self, user_class, gubun):
        self.dict_bool = {
            '로그인': False,
            'TR수신': False,
            'TR다음': False,
            'CD로딩': False,
            'CD수신': False
        }
        self.tr_df     = None
        self.tr_name   = None
        self.dict_item = None
        self.list_trcd = None

        self.ocx = QAxWidget('KHOPENAPI.KHOpenAPICtrl.1')
        self.ocx.OnEventConnect.connect(self.OnEventConnect)
        self.ocx.OnReceiveTrData.connect(self.OnReceiveTrData)

        if gubun == 'Receiver':
            self.ocx.OnReceiveTrCondition.connect(self.OnReceiveTrCondition)
            self.ocx.OnReceiveConditionVer.connect(self.OnReceiveConditionVer)
            self.ocx.OnReceiveRealData.connect(user_class.OnReceiveRealData)
            self.ocx.OnReceiveRealCondition.connect(user_class.OnReceiveRealCondition)
        elif gubun == 'Trader':
            self.ocx.OnReceiveMsg.connect(user_class.OnReceiveMsg)
            self.ocx.OnReceiveRealData.connect(user_class.OnReceiveRealData)
            self.ocx.OnReceiveChejanData.connect(user_class.OnReceiveChejanData)
        elif gubun == 'Downloader':
            self.ocx.OnReceiveTrCondition.connect(self.OnReceiveTrCondition)
            self.ocx.OnReceiveConditionVer.connect(self.OnReceiveConditionVer)

    def CommConnect(self):
        self.ocx.dynamicCall('CommConnect()')
        while not self.dict_bool['로그인']:
            pythoncom.PumpWaitingMessages()

    def GetConditionLoad(self):
        self.ocx.dynamicCall('GetConditionLoad()')
        while not self.dict_bool['CD로딩']:
            pythoncom.PumpWaitingMessages()

    def GetConditionNamelist(self):
        data = self.ocx.dynamicCall('GetConditionNameList()')
        conditions = data.split(';')[:-1]
        list_cond = [[int(condition.split('^')[0]), condition.split('^')[1]] for condition in conditions]
        return list_cond

    def Block_Request(self, *args, **kwargs):
        trcode = args[0].lower()
        self.dict_item = parseDat(trcode)
        self.tr_name = kwargs['output']
        nnext = kwargs['next']
        for i in kwargs:
            if i.lower() != 'output' and i.lower() != 'next':
                self.ocx.dynamicCall('SetInputValue(QString, QString)', i, kwargs[i])
        self.dict_bool['TR수신'] = False
        self.dict_bool['TR다음'] = False
        sn_num = sn_brrd if trcode == 'opt10054' else sn_brrq
        self.ocx.dynamicCall('CommRqData(QString, QString, int, QString)', self.tr_name, trcode, nnext, sn_num)
        sleeptime = datetime.datetime.now() + datetime.timedelta(seconds=0.25)
        while not self.dict_bool['TR수신'] or datetime.datetime.now() < sleeptime:
            pythoncom.PumpWaitingMessages()
        if trcode != 'opt10054':
            self.DisconnectRealData(sn_brrq)
        return self.tr_df

    def SendCondition(self, cond):
        self.dict_bool['CD수신'] = False
        self.ocx.dynamicCall('SendCondition(QString, QString, int, int)', cond)
        sleeptime = datetime.datetime.now() + datetime.timedelta(seconds=0.25)
        while not self.dict_bool['CD수신'] or datetime.datetime.now() < sleeptime:
            pythoncom.PumpWaitingMessages()
        return self.list_trcd

    def SendConditionStop(self, cond):
        self.ocx.dynamicCall("SendConditionStop(QString, QString, int)", cond)

    def OnEventConnect(self, err_code):
        if err_code == 0: self.dict_bool['로그인'] = True

    # noinspection PyUnusedLocal
    def OnReceiveConditionVer(self, ret, msg):
        if ret == 1: self.dict_bool['CD로딩'] = True

    # noinspection PyUnusedLocal
    def OnReceiveTrCondition(self, screen, code_list, cond_name, cond_index, nnext):
        codes = code_list.split(';')[:-1]
        self.list_trcd = codes
        self.dict_bool['CD수신'] = True

    # noinspection PyUnusedLocal
    def OnReceiveTrData(self, screen, rqname, trcode, record, nnext):
        if 'ORD' in trcode:
            return

        items = None
        self.dict_bool['TR다음'] = True if nnext == '2' else False
        for output in self.dict_item['output']:
            record = list(output.keys())[0]
            items = list(output.values())[0]
            if record == self.tr_name:
                break
        rows = self.ocx.dynamicCall('GetRepeatCnt(QString, QString)', trcode, rqname)
        if rows == 0:
            rows = 1
        df2 = []
        for row in range(rows):
            row_data = []
            for item in items:
                data = self.ocx.dynamicCall('GetCommData(QString, QString, int, QString)', trcode, rqname, row, item)
                row_data.append(data.strip())
            df2.append(row_data)
        df = pd.DataFrame(df2, columns=items)
        self.tr_df = df
        self.dict_bool['TR수신'] = True

    def GetAccountNumber(self):
        return self.ocx.dynamicCall('GetLoginInfo(QString)', 'ACCNO').split(';')[0]

    def SetRealReg(self, rreg):
        self.ocx.dynamicCall('SetRealReg(QString, QString, QString, QString)', rreg)

    def SetRealRemove(self, rreg):
        self.ocx.dynamicCall('SetRealRemove(QString, QString)', rreg)

    def DisconnectRealData(self, screen):
        self.ocx.dynamicCall('DisconnectRealData(QString)', screen)

    def GetCodeListByMarket(self, market):
        data = self.ocx.dynamicCall('GetCodeListByMarket(QString)', market)
        tokens = data.split(';')[:-1]
        return tokens

    def GetMasterCodeName(self, code):
        return self.ocx.dynamicCall('GetMasterCodeName(QString)', code)

    def GetMasterLastPrice(self, code):
        return int(self.ocx.dynamicCall('GetMasterLastPrice(QString)', code))

    def GetCommRealData(self, code, fid):
        return self.ocx.dynamicCall('GetCommRealData(QString, int)', code, fid)

    def GetChejanData(self, fid):
        return self.ocx.dynamicCall('GetChejanData(int)', fid)

    def SendOrder(self, order):
        return self.ocx.dynamicCall('SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)', order)
