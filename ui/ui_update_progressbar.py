from ui.set_style import style_bc_bb, style_bc_bt, style_bc_by, style_bc_sl


def update_progressbar(ui, soundQ, webcQ):
    ui.progressBarrr.setValue(ui.cpu_per)
    ui.counter = 0 if ui.counter == 599 else ui.counter + 1

    ui.kp_pushButton.setStyleSheet(style_bc_bb if not ui.dialog_kimp.isVisible() else style_bc_bt)
    ui.dd_pushButton.setStyleSheet(style_bc_bb if not ui.dialog_db.isVisible() else style_bc_bt)
    ui.js_pushButton.setStyleSheet(style_bc_bb if not ui.dialog_jisu.isVisible() else style_bc_bt)
    ui.uj_pushButton.setStyleSheet(style_bc_bb if not ui.dialog_tree.isVisible() else style_bc_bt)
    ui.gu_pushButton.setStyleSheet(style_bc_bb if not ui.dialog_info.isVisible() else style_bc_bt)
    ui.hg_pushButton.setStyleSheet(style_bc_bb if not ui.dialog_hoga.isVisible() else style_bc_bt)
    ui.ct_pushButton.setStyleSheet(style_bc_bb if not ui.dialog_chart.isVisible() else style_bc_bt)
    ui.ct_pushButtonnn_02.setStyleSheet(style_bc_bt if not ui.dialog_factor.isVisible() else style_bc_bb)
    ui.ct_pushButtonnn_05.setStyleSheet(style_bc_bt if not ui.dialog_test.isVisible() else style_bc_bb)
    ui.bs_pushButton.setStyleSheet(style_bc_bb if not ui.dialog_scheduler.isVisible() else style_bc_bt)
    ui.tt_pushButton.setStyleSheet(style_bc_bb if not ui.s_calendarWidgett.isVisible() and not ui.c_calendarWidgett.isVisible() else style_bc_bt)

    style_ = style_bc_bt if ui.proc_backtester_bb is not None and ui.proc_backtester_bb.is_alive() and ui.counter % 2 != 0 else style_bc_by
    ui.svj_pushButton_01.setStyleSheet(style_)
    ui.cvj_pushButton_01.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_bf is not None and ui.proc_backtester_bf.is_alive() and ui.counter % 2 != 0 else style_bc_by
    ui.svj_pushButton_02.setStyleSheet(style_)
    ui.cvj_pushButton_02.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_bc is not None and ui.proc_backtester_bc.is_alive() and ui.counter % 2 != 0 else style_bc_by
    ui.svj_pushButton_03.setStyleSheet(style_)
    ui.cvj_pushButton_03.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_bp is not None and ui.proc_backtester_bp.is_alive() and ui.counter % 2 != 0 else style_bc_by
    ui.svj_pushButton_04.setStyleSheet(style_)
    ui.cvj_pushButton_04.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_ovc is not None and ui.proc_backtester_ovc.is_alive() and ui.counter % 2 != 0 else style_bc_by
    ui.svc_pushButton_06.setStyleSheet(style_)
    ui.cvc_pushButton_06.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_ov is not None and ui.proc_backtester_ov.is_alive() and ui.counter % 2 != 0 else style_bc_by
    ui.svc_pushButton_07.setStyleSheet(style_)
    ui.cvc_pushButton_07.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_o is not None and ui.proc_backtester_o.is_alive() and ui.counter % 2 != 0 else style_bc_by
    ui.svc_pushButton_08.setStyleSheet(style_)
    ui.cvc_pushButton_08.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_ovct is not None and ui.proc_backtester_ovct.is_alive() and ui.counter % 2 != 0 else style_bc_by
    ui.svc_pushButton_15.setStyleSheet(style_)
    ui.cvc_pushButton_15.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_ovt is not None and ui.proc_backtester_ovt.is_alive() and ui.counter % 2 != 0 else style_bc_by
    ui.svc_pushButton_16.setStyleSheet(style_)
    ui.cvc_pushButton_16.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_ot is not None and ui.proc_backtester_ot.is_alive() and ui.counter % 2 != 0 else style_bc_by
    ui.svc_pushButton_17.setStyleSheet(style_)
    ui.cvc_pushButton_17.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_orvc is not None and ui.proc_backtester_orvc.is_alive() and ui.counter % 2 != 0 else style_bc_by
    ui.svc_pushButton_18.setStyleSheet(style_)
    ui.cvc_pushButton_18.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_orv is not None and ui.proc_backtester_orv.is_alive() and ui.counter % 2 != 0 else style_bc_by
    ui.svc_pushButton_19.setStyleSheet(style_)
    ui.cvc_pushButton_19.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_or is not None and ui.proc_backtester_or.is_alive() and ui.counter % 2 != 0 else style_bc_by
    ui.svc_pushButton_20.setStyleSheet(style_)
    ui.cvc_pushButton_20.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_ogvc is not None and ui.proc_backtester_ogvc.is_alive() and ui.counter % 2 != 0 else style_bc_by
    ui.sva_pushButton_01.setStyleSheet(style_)
    ui.cva_pushButton_01.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_ogv is not None and ui.proc_backtester_ogv.is_alive() and ui.counter % 2 != 0 else style_bc_by
    ui.sva_pushButton_02.setStyleSheet(style_)
    ui.cva_pushButton_02.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_og is not None and ui.proc_backtester_og.is_alive() and ui.counter % 2 != 0 else style_bc_by
    ui.sva_pushButton_03.setStyleSheet(style_)
    ui.cva_pushButton_03.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_ocvc is not None and ui.proc_backtester_ocvc.is_alive() and ui.counter % 2 != 0 else style_bc_by
    ui.svo_pushButton_05.setStyleSheet(style_)
    ui.cvo_pushButton_05.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_ocv is not None and ui.proc_backtester_ocv.is_alive() and ui.counter % 2 != 0 else style_bc_by
    ui.svo_pushButton_06.setStyleSheet(style_)
    ui.cvo_pushButton_06.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_oc is not None and ui.proc_backtester_oc.is_alive() and ui.counter % 2 != 0 else style_bc_by
    ui.svo_pushButton_07.setStyleSheet(style_)
    ui.cvo_pushButton_07.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_bvc is not None and ui.proc_backtester_bvc.is_alive() and ui.counter % 2 != 0 else style_bc_sl
    ui.svc_pushButton_27.setStyleSheet(style_)
    ui.cvc_pushButton_27.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_bv is not None and ui.proc_backtester_bv.is_alive() and ui.counter % 2 != 0 else style_bc_sl
    ui.svc_pushButton_28.setStyleSheet(style_)
    ui.cvc_pushButton_28.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_b is not None and ui.proc_backtester_b.is_alive() and ui.counter % 2 != 0 else style_bc_sl
    ui.svc_pushButton_29.setStyleSheet(style_)
    ui.cvc_pushButton_29.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_bvct is not None and ui.proc_backtester_bvct.is_alive() and ui.counter % 2 != 0 else style_bc_sl
    ui.svc_pushButton_30.setStyleSheet(style_)
    ui.cvc_pushButton_30.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_bvt is not None and ui.proc_backtester_bvt.is_alive() and ui.counter % 2 != 0 else style_bc_sl
    ui.svc_pushButton_31.setStyleSheet(style_)
    ui.cvc_pushButton_31.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_bt is not None and ui.proc_backtester_bt.is_alive() and ui.counter % 2 != 0 else style_bc_sl
    ui.svc_pushButton_32.setStyleSheet(style_)
    ui.cvc_pushButton_32.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_brvc is not None and ui.proc_backtester_brvc.is_alive() and ui.counter % 2 != 0 else style_bc_sl
    ui.svc_pushButton_33.setStyleSheet(style_)
    ui.cvc_pushButton_33.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_brv is not None and ui.proc_backtester_brv.is_alive() and ui.counter % 2 != 0 else style_bc_sl
    ui.svc_pushButton_34.setStyleSheet(style_)
    ui.cvc_pushButton_34.setStyleSheet(style_)

    style_ = style_bc_bt if ui.proc_backtester_br is not None and ui.proc_backtester_br.is_alive() and ui.counter % 2 != 0 else style_bc_sl
    ui.svc_pushButton_35.setStyleSheet(style_)
    ui.cvc_pushButton_35.setStyleSheet(style_)

    style_ = style_bc_bb if ui.ct_test > 0 and ui.counter % 2 != 0 else style_bc_bt
    ui.tt_pushButtonnn_03.setStyleSheet(style_)

    ui.be_pushButtonnn_01.setStyleSheet(style_bc_by if ui.backtest_engine else style_bc_bt)

    if ui.ssicon_alert:
        icon = ui.icon_stocks if ui.counter % 2 == 0 else ui.icon_stocks2
        ui.main_btn_list[2].setIcon(icon)

    if ui.csicon_alert:
        icon = ui.icon_coins if ui.counter % 2 == 0 else ui.icon_coins2
        ui.main_btn_list[3].setIcon(icon)

    if ui.lgicon_alert:
        icon = ui.icon_log if ui.counter % 2 == 0 else ui.icon_log2
        ui.main_btn_list[5].setIcon(icon)
        if ui.counter % 5 == 0 and (ui.dict_set['주식알림소리'] or ui.dict_set['코인알림소리']):
            soundQ.put('오류가 발생하였습니다. 로그탭을 확인하십시오.')

    if not ui.image_search or (ui.counter % 600 == 0 and (ui.image_label1.isVisible() or ui.image_label2.isVisible())):
        if not ui.image_search: ui.image_search = True
        webcQ.put(('풍경사진요청', ''))
