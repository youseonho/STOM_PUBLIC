import sys
from utility.static import qtest_qwait


def process_kill(ui, wdzservQ, queryQ, kimpQ, creceivQ, ctraderQ):
    if ui.dict_set['리시버프로파일링']:
        wdzservQ.put(('receiver', '프로파일링결과'))
        qtest_qwait(3)
    if ui.dict_set['트레이더프로파일링']:
        wdzservQ.put(('trader', '프로파일링결과'))
        qtest_qwait(3)
    if ui.dict_set['전략연산프로파일링']:
        wdzservQ.put(('strategy', '프로파일링결과'))
        qtest_qwait(3)

    wdzservQ.put(('manager', '통신종료'))
    factor_choice = ''
    for checkbox in ui.factor_checkbox_list:
        factor_choice = f"{factor_choice}{'1' if checkbox.isChecked() else '0'};"
    query = f"UPDATE etc SET 팩터선택 = '{factor_choice[:-1]}'"
    queryQ.put(('설정디비', query))
    divid_mode = ui.be_comboBoxxxxx_01.currentText()
    optuna_sampler = ui.op_comboBoxxxx_01.currentText()
    optuna_fixvars = ui.op_lineEditttt_01.text()
    optuna_count = int(ui.op_lineEditttt_02.text())
    optuna_autostep = 1 if ui.op_checkBoxxxx_01.isChecked() else 0
    query = f"UPDATE back SET 백테엔진분류방법 = '{divid_mode}', '옵튜나샘플러' = '{optuna_sampler}', '옵튜나고정변수' = '{optuna_fixvars}', '옵튜나실행횟수' = {optuna_count}, '옵튜나자동스탭' = {optuna_autostep}"
    queryQ.put(('설정디비', query))

    if ui.dict_set['창위치기억']:
        geo_len = len(ui.dict_set['창위치']) if ui.dict_set['창위치'] is not None else 0
        geometry = f"{ui.x()};{ui.y()};"
        geometry += f"{ui.dialog_chart.x()};{ui.dialog_chart.y() - 31 if geo_len > 3 and ui.dict_set['창위치'][3] + 31 == ui.dialog_chart.y() else ui.dialog_chart.y()};"
        geometry += f"{ui.dialog_scheduler.x()};{ui.dialog_scheduler.y() - 31 if geo_len > 5 and ui.dict_set['창위치'][5] + 31 == ui.dialog_scheduler.y() else ui.dialog_scheduler.y()};"
        geometry += f"{ui.dialog_jisu.x()};{ui.dialog_jisu.y() - 31 if geo_len > 7 and ui.dict_set['창위치'][7] + 31 == ui.dialog_jisu.y() else ui.dialog_jisu.y()};"
        geometry += f"{ui.dialog_info.x()};{ui.dialog_info.y() - 31 if geo_len > 9 and ui.dict_set['창위치'][9] + 31 == ui.dialog_info.y() else ui.dialog_info.y()};"
        geometry += f"{ui.dialog_web.x()};{ui.dialog_web.y() - 31 if geo_len > 11 and ui.dict_set['창위치'][11] + 31 == ui.dialog_web.y() else ui.dialog_web.y()};"
        geometry += f"{ui.dialog_tree.x()};{ui.dialog_tree.y() - 31 if geo_len > 13 and ui.dict_set['창위치'][13] + 31 == ui.dialog_tree.y() else ui.dialog_tree.y()};"
        geometry += f"{ui.dialog_kimp.x()};{ui.dialog_kimp.y() - 31 if geo_len > 15 and ui.dict_set['창위치'][15] + 31 == ui.dialog_kimp.y() else ui.dialog_kimp.y()};"
        geometry += f"{ui.dialog_hoga.x()};{ui.dialog_hoga.y() - 31 if geo_len > 17 and ui.dict_set['창위치'][17] + 31 == ui.dialog_hoga.y() else ui.dialog_hoga.y()};"
        geometry += f"{ui.dialog_backengine.x()};{ui.dialog_backengine.y() - 31 if geo_len > 19 and ui.dict_set['창위치'][19] + 31 == ui.dialog_backengine.y() else ui.dialog_backengine.y()};"
        geometry += f"{ui.dialog_order.x()};{ui.dialog_order.y() - 31 if geo_len > 21 and ui.dict_set['창위치'][21] + 31 == ui.dialog_order.y() else ui.dialog_order.y()};"
        geometry += f"{ui.dialog_pattern.x()};{ui.dialog_pattern.y() - 31 if geo_len > 23 and ui.dict_set['창위치'][23] + 31 == ui.dialog_pattern.y() else ui.dialog_pattern.y()}"
        query = f"UPDATE etc SET 창위치 = '{geometry}'"
        queryQ.put(('설정디비', query))
    queryQ.put('프로세스종료')

    if ui.writer.isRunning(): ui.writer.terminate()
    if ui.qtimer1.isActive(): ui.qtimer1.stop()
    if ui.qtimer2.isActive(): ui.qtimer2.stop()
    if ui.qtimer3.isActive(): ui.qtimer3.stop()

    if ui.dialog_chart.isVisible():     ui.dialog_chart.close()
    if ui.dialog_scheduler.isVisible(): ui.dialog_scheduler.close()
    if ui.dialog_jisu.isVisible():      ui.dialog_jisu.close()
    if ui.dialog_info.isVisible():      ui.dialog_info.close()
    if ui.dialog_web.isVisible():       ui.dialog_web.close()
    if ui.dialog_tree.isVisible():      ui.dialog_tree.close()
    if ui.dialog_graph.isVisible():     ui.dialog_graph.close()
    if ui.dialog_kimp.isVisible():      ui.dialog_kimp.close()
    if ui.StomLiveProcessAlive():       ui.proc_stomlive.kill()

    if ui.CoinKimpProcessAlive():
        kimpQ.put('프로세스종료')
    if ui.CoinReceiverProcessAlive():
        creceivQ.put('프로세스종료')
        ui.proc_receiver_coin.kill()
    if ui.CoinTraderProcessAlive():
        if ui.dict_set['거래소'] == '바이낸스선물':
            ctraderQ.put('프로세스종료')
        ui.proc_trader_coin.kill()
    if ui.CoinStrategyProcessAlive():
        ui.proc_strategy_coin.kill()

    if ui.SimulatorProcessAlive():
        try:
            ui.proc_simulator_rv.kill()
            ui.proc_simulator_td.kill()
        except:
            pass
    if ui.BacktestProcessAlive():
        ui.BacktestProcessKill(1)

    qtest_qwait(3)
    sys.exit()
