import os
import re
from PyQt5.QtCore import QTimer
from ui.set_style import color_fg_rt, color_fg_dk, color_fg_bt
from utility.setting import ui_num
from utility.static import error_decorator, now, qtest_qwait, timedelta_sec, int_hms


class UpdateTextedit:
    def __init__(self, ui, qlist):
        """
        windowQ, soundQ, queryQ, teleQ, chartQ, hogaQ, webcQ, backQ, creceivQ, ctraderQ,  cstgQ, liveQ, kimpQ, wdzservQ
           0        1       2      3       4      5      6      7       8         9         10     11    12      13
        """
        self.ui       = ui
        self.soundQ   = qlist[1]
        self.teleQ    = qlist[3]
        self.wdzservQ = qlist[13]

    @error_decorator
    def update_texedit(self, data):
        if len(data) == 2:
            if '시스템 명령 오류 알림' in data[1]:
                self.ui.lgicon_alert = True
    
            time_ = str(now())[:-7] if data[0] in (ui_num['S백테스트'], ui_num['C백테스트'], ui_num['CF백테스트']) else str(now())
            log_  = f'<font color=#FF32FF>{data[1]}</font>' if '오류' in data[1] else data[1]
            text  = f'[{time_}] {log_}' if '</font>' not in log_ else f'<font color=white>[{time_}]</font> {log_}'
    
            if data[0] == ui_num['백테엔진']:
                self.ui.be_textEditxxxx_01.append(text)
                if data[1] == '백테엔진 준비 완료' and self.ui.auto_mode:
                    if self.ui.dialog_backengine.isVisible():
                        self.ui.dialog_backengine.close()
                    qtest_qwait(2)
                    self.ui.AutoBackSchedule(2)
            elif data[0] == ui_num['S로그텍스트']:
                self.ui.sst_textEditttt_01.append(text)
                self.ui.log1.info(text)
            elif data[0] == ui_num['S단순텍스트']:
                self.ui.src_textEditttt_01.append(text)
                self.ui.log2.info(text)
                if '전략연산 프로세스 틱데이터 저장 중 ... [8]' in text:
                    self.ui.tickdata_save = True
            elif data[0] == ui_num['S오더텍스트']:
                self.ui.log3.info(text)
            elif data[0] == ui_num['C로그텍스트']:
                self.ui.cst_textEditttt_01.append(text)
                self.ui.log4.info(text)
            elif data[0] == ui_num['C단순텍스트']:
                self.ui.crc_textEditttt_01.append(text)
                self.ui.log5.info(text)
            elif data[0] == ui_num['S백테스트']:
                if '배팅금액' in data[1] or 'OUT' in data[1] or '결과' in data[1] or '최적값' in data[1] or \
                        '벤치점수' in data[1] or '백테스트 시작' in data[1] or ']단계' in data[1]:
                    color = color_fg_rt
                elif ('AP' in data[1] and '-' in data[1].split('AP')[1]) or \
                        ('수익률' in data[1] and '-' in data[1].split('수익률')[1]):
                    color = color_fg_dk
                else:
                    color = color_fg_bt
                self.ui.ss_textEditttt_09.setTextColor(color)
                self.ui.ss_textEditttt_09.append(text)
                self.ui.log6.info(re.sub('(<([^>]+)>)', '', text))
                if '백테스트를 중지합니다' in data[1] and self.ui.back_condition: self.ui.BacktestProcessKill(0)
                if data[1] in ('백테스트 완료', '백파인더 완료', '벤치테스트 완료', '최적화O 완료', '최적화OV 완료', '최적화OVC 완료',
                               '최적화B 완료', '최적화BV 완료', '최적화BVC 완료', '최적화OT 완료', '최적화OVT 완료', '최적화OVCT 완료',
                               '최적화BT 완료', '최적화BVT 완료', '최적화BVCT 완료', '전진분석OR 완료', '전진분석ORV 완료', '전진분석ORVC 완료',
                               '전진분석BR 완료', '전진분석BRV 완료', '전진분석BRVC 완료', '최적화OG 완료', '최적화OGV 완료', '최적화OGVC 완료',
                               '최적화OC 완료', '최적화OCV 완료', '최적화OCVC 완료', '패턴 학습 완료', '패턴 테스트 완료'):
                    if data[1] in ('최적화O 완료', '최적화OV 완료', '최적화OVC 완료', '최적화B 완료', '최적화BV 완료', '최적화BVC 완료'):
                        self.ui.sActivated_04()
                    if data[1] in ('최적화OG 완료', '최적화OGV 완료', '최적화OGVC 완료'):
                        self.ui.sActivated_06()
                    if not self.ui.dict_set['그래프띄우지않기'] and data[1] not in ('백파인더 완료', '벤치테스트 완료', '최적화OG 완료', '최적화OGV 완료', '최적화OGVC 완료', '최적화OC 완료', '최적화OCV 완료', '최적화OCVC 완료'):
                        self.ui.svjButtonClicked_08()
                    self.ui.BacktestProcessKill(0)
                    self.ui.ssicon_alert = False
                    self.ui.main_btn_list[2].setIcon(self.ui.icon_stocks)
                    if self.ui.back_schedul:
                        qtest_qwait(3)
                        self.ui.sdButtonClicked_02()
            elif data[0] in (ui_num['C백테스트'], ui_num['CF백테스트']):
                if '배팅금액' in data[1] or 'OUT' in data[1] or '결과' in data[1] or '최적값' in data[1] or \
                        '벤치점수' in data[1] or '백테스트 시작' in data[1] or ']단계' in data[1]:
                    color = color_fg_rt
                elif ('AP' in data[1] and '-' in data[1].split('AP')[1]) or \
                        ('수익률' in data[1] and '-' in data[1].split('수익률')[1].split('KRW')[0]):
                    color = color_fg_dk
                else:
                    color = color_fg_bt
                self.ui.cs_textEditttt_09.setTextColor(color)
                self.ui.cs_textEditttt_09.append(text)
                self.ui.log6.info(re.sub('(<([^>]+)>)', '', text))
                if '백테스트를 중지합니다' in data[1] and self.ui.back_condition: self.ui.BacktestProcessKill(0)
                if data[1] in ('백테스트 완료', '백파인더 완료', '벤치테스트 완료', '최적화O 완료', '최적화OV 완료', '최적화OVC 완료',
                               '최적화B 완료', '최적화BV 완료', '최적화BVC 완료', '최적화OT 완료', '최적화OVT 완료', '최적화OVCT 완료',
                               '최적화BT 완료', '최적화BVT 완료', '최적화BVCT 완료', '전진분석OR 완료', '전진분석ORV 완료', '전진분석ORVC 완료',
                               '전진분석BR 완료', '전진분석BRV 완료', '전진분석BRVC 완료', '최적화OG 완료', '최적화OGV 완료', '최적화OGVC 완료',
                               '최적화OC 완료', '최적화OCV 완료', '최적화OCVC 완료', '패턴 학습 완료', '패턴 테스트 완료'):
                    if data[1] in ('최적화O 완료', '최적화OV 완료', '최적화OVC 완료', '최적화B 완료', '최적화BV 완료', '최적화BVC 완료'):
                        self.ui.cActivated_04()
                    if data[1] in ('최적화OG 완료', '최적화OGV 완료', '최적화OGVC 완료'):
                        self.ui.cActivated_06()
                    if not self.ui.dict_set['그래프띄우지않기'] and data[1] not in ('백파인더 완료', '벤치테스트 완료', '최적화OG 완료', '최적화OGV 완료', '최적화OGVC 완료', '최적화OC 완료', '최적화OCV 완료', '최적화OCVC 완료'):
                        self.ui.cvjButtonClicked_08()
                    self.ui.BacktestProcessKill(0)
                    self.ui.csicon_alert = False
                    self.ui.main_btn_list[3].setIcon(self.ui.icon_coins)
                    if self.ui.back_schedul:
                        qtest_qwait(3)
                        self.ui.sdButtonClicked_02()
            elif data[0] == ui_num['기업개요']:
                self.ui.gg_textEdittttt_01.clear()
                self.ui.gg_textEdittttt_01.append(data[1])
    
            if data[0] == ui_num['S단순텍스트'] and '리시버 종료' in data[1]:
                self.wdzservQ.put(('manager', '리시버 종료'))
            elif data[0] == ui_num['S로그텍스트'] and '전략연산 종료' in data[1]:
                self.wdzservQ.put(('manager', '전략연산 종료'))
                if self.ui.tickdata_save and self.ui.dict_set['디비자동관리']:
                    self.AutoDataBase(1)
                else:
                    self.StockShutDownCheck()
            elif data[0] == ui_num['S로그텍스트'] and '트레이더 종료' in data[1]:
                self.wdzservQ.put(('manager', '트레이더 종료'))
            elif data[0] == ui_num['C단순텍스트'] and '리시버 종료' in data[1]:
                if self.ui.CoinReceiverProcessAlive():
                    self.ui.proc_receiver_coin.kill()
            elif data[0] == ui_num['C로그텍스트'] and '전략연산 종료' in data[1]:
                if self.ui.CoinStrategyProcessAlive():
                    self.ui.proc_strategy_coin.kill()
                self.CoinShutDownCheck()
            elif data[0] == ui_num['C로그텍스트'] and '트레이더 종료' in data[1]:
                if self.ui.CoinTraderProcessAlive():
                    self.ui.proc_trader_coin.kill()
            elif data[0] == ui_num['DB관리']:
                if data[1] == 'DB업데이트완료':
                    self.ui.database_control = False
                else:
                    self.ui.db_textEdittttt_01.append(text)
                if self.ui.auto_mode:
                    if data[1] == '날짜별 DB 생성 완료':
                        self.AutoDataBase(2)
                    elif data[1] == '당일 데이터 백테디비로 추가 완료':
                        self.AutoDataBase(3)
        elif len(data) == 5:
            self.ui.dict_name = data[1]
            self.ui.dict_code = data[2]
            self.ui.dict_sgbn = data[3]
        elif len(data) == 4:
            if data[1] <= data[2]:
                curr_time = now()
                try:
                    left_backtime  = curr_time - data[3]
                    left_total_sec = left_backtime.total_seconds()
                    remain_backtime = timedelta_sec(left_total_sec / data[1] * (data[2] - data[1])) - curr_time
                except:
                    self.ui.ss_progressBar_01.setFormat('%p%')
                    self.ui.ss_progressBar_01.setValue(0)
                else:
                    if self.ui.back_schedul:
                        self.ui.list_progressBarrr[self.ui.back_scount].setFormat('%p%')
                        self.ui.list_progressBarrr[self.ui.back_scount].setValue(data[1])
                        self.ui.list_progressBarrr[self.ui.back_scount].setRange(0, data[2])
                    if data[0] == ui_num['S백테바']:
                        self.ui.ss_progressBar_01.setFormat(f'%p% | 경과 시간 {left_backtime} | 남은 시간 {remain_backtime}')
                        self.ui.ss_progressBar_01.setValue(data[1])
                        self.ui.ss_progressBar_01.setRange(0, data[2])
                    elif data[0] in (ui_num['C백테바'], ui_num['CF백테바']):
                        self.ui.cs_progressBar_01.setFormat(f'%p% | 경과 시간 {left_backtime} | 남은 시간 {remain_backtime}')
                        self.ui.cs_progressBar_01.setValue(data[1])
                        self.ui.cs_progressBar_01.setRange(0, data[2])

    def AutoDataBase(self, gubun):
        if gubun == 1:
            self.ui.auto_mode = True
            if self.ui.dict_set['주식알림소리'] or self.ui.dict_set['코인알림소리']:
                self.soundQ.put('데이터베이스 자동관리를 시작합니다.')
            if not self.ui.dialog_db.isVisible():
                self.ui.dialog_db.show()
            qtest_qwait(2)
            self.ui.dbButtonClicked_08()
        elif gubun == 2:
            if not self.ui.dialog_db.isVisible():
                self.ui.dialog_db.show()
            qtest_qwait(2)
            self.ui.dbButtonClicked_07()
        elif gubun == 3:
            if self.ui.dialog_db.isVisible():
                self.ui.dialog_db.close()
            self.teleQ.put('데이터베이스 자동관리 완료')
            qtest_qwait(2)
            self.ui.auto_mode = False
            self.StockShutDownCheck()

    def StockShutDownCheck(self):
        if not self.ui.dict_set['백테스케쥴실행'] or now().weekday() != self.ui.dict_set['백테스케쥴요일']:
            if self.ui.dict_set['프로그램종료']:
                QTimer.singleShot(180 * 1000, self.ui.ProcessKill)
        elif self.ui.dict_set['주식알림소리']:
            self.soundQ.put('오늘은 백테 스케쥴러의 실행이 예약되어 있어 프로그램을 종료하지 않습니다.')

    def CoinShutDownCheck(self):
        if not self.ui.dict_set['백테스케쥴실행'] or now().weekday() != self.ui.dict_set['백테스케쥴요일']:
            if self.ui.dict_set['프로그램종료']:
                QTimer.singleShot(180 * 1000, self.ui.ProcessKill)
        elif self.ui.dict_set['코인알림소리']:
            self.soundQ.put('오늘은 백테 스케쥴러의 실행이 예약되어 있어 프로그램을 종료하지 않습니다.')
