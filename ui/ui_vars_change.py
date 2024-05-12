from traceback import print_exc
from ui.set_text import stock_buy_signal, coin_buy_signal, coin_future_buy_signal, stock_sell_signal, coin_sell_signal, \
    coin_future_sell_signal


def get_fix_strategy(ui, strategy, gubun):
    if gubun == '매수':
        if ui.focusWidget() in (ui.svjb_pushButon_02, ui.svc_pushButton_02, ui.ss_textEditttt_01, ui.ss_textEditttt_03, ui.ss_textEditttt_07):
            if '\nif 매수:' in strategy:
                strategy = strategy.split('\nif 매수:')[0] + stock_buy_signal
            elif 'self.tickdata' not in strategy and stock_buy_signal not in strategy:
                strategy += '\n' + stock_buy_signal
        else:
            if ui.dict_set['거래소'] == '업비트':
                if '\nif 매수:' in strategy:
                    strategy = strategy.split('\nif 매수:')[0] + coin_buy_signal
                elif coin_buy_signal not in strategy:
                    strategy += '\n' + coin_buy_signal
            else:
                if '\nif BUY_LONG or SELL_SHORT:' in strategy:
                    strategy = strategy.split('\nif BUY_LONG or SELL_SHORT:')[0] + coin_future_buy_signal
                elif coin_future_buy_signal not in strategy:
                    strategy += '\n' + coin_future_buy_signal
    else:
        if ui.focusWidget() in (ui.svjs_pushButon_02, ui.svc_pushButton_10, ui.ss_textEditttt_02, ui.ss_textEditttt_04, ui.ss_textEditttt_08):
            if '\nif 매도:' in strategy:
                strategy = strategy.split('\nif 매도:')[0] + stock_sell_signal
            elif 'self.tickdata' not in strategy and stock_sell_signal not in strategy:
                strategy += '\n' + stock_sell_signal
        else:
            if ui.dict_set['거래소'] == '업비트':
                if '\nif 매도:' in strategy:
                    strategy = strategy.split('\nif 매도:')[0] + coin_sell_signal
                elif coin_sell_signal not in strategy:
                    strategy += '\n' + coin_sell_signal
            else:
                if "\nif (포지션 == 'LONG' and SELL_LONG) or (포지션 == 'SHORT' and BUY_SHORT):" in strategy:
                    strategy = strategy.split("\nif (포지션 == 'LONG' and SELL_LONG) or (포지션 == 'SHORT' and BUY_SHORT):")[
                                   0] + coin_future_sell_signal
                elif coin_future_sell_signal not in strategy:
                    strategy += '\n' + coin_future_sell_signal
    return strategy


def get_optivars_to_gavars(opti_vars_text):
    ga_vars_text = ''
    try:
        vars_ = {}
        opti_vars_text = opti_vars_text.replace('self.vars', 'vars_')
        exec(compile(opti_vars_text, '<string>', 'exec'))
        for i in range(len(vars_)):
            ga_vars_text = f'{ga_vars_text}self.vars[{i}] = [['
            vars_start, vars_last, vars_gap = vars_[i][0]
            vars_high = vars_[i][1]
            vars_curr = vars_start
            if vars_start == vars_last:
                ga_vars_text = f'{ga_vars_text}{vars_curr}], {vars_curr}]\n'
            elif vars_start < vars_last:
                while vars_curr <= vars_last:
                    ga_vars_text = f'{ga_vars_text}{vars_curr}, '
                    vars_curr += vars_gap
                    if vars_gap < 0:
                        vars_curr = round(vars_curr, 2)
                ga_vars_text = f'{ga_vars_text[:-2]}], {vars_high}]\n'
            else:
                while vars_curr >= vars_last:
                    ga_vars_text = f'{ga_vars_text}{vars_curr}, '
                    vars_curr += vars_gap
                    if vars_gap < 0:
                        vars_curr = round(vars_curr, 2)
                ga_vars_text = f'{ga_vars_text[:-2]}], {vars_high}]\n'
    except:
        print_exc()

    return ga_vars_text[:-1]


def get_gavars_to_optivars(ga_vars_text):
    opti_vars_text = ''
    try:
        vars_ = {}
        ga_vars_text = ga_vars_text.replace('self.vars', 'vars_')
        exec(compile(ga_vars_text, '<string>', 'exec'))
        for i in range(len(vars_)):
            if len(vars_[i][0]) == 1:
                vars_high = vars_[i][1]
                vars_gap = 0
                vars_start = vars_high
                vars_end = vars_high
            else:
                vars_high, vars_gap = vars_[i][1], vars_[i][0][1] - vars_[i][0][0]
                if type(vars_gap) == float: vars_gap = round(vars_gap, 2)
                vars_start = vars_[i][0][0]
                vars_end = vars_[i][0][-1]
            opti_vars_text = f'{opti_vars_text}vars_[{i}] = [[{vars_start}, {vars_end}, {vars_gap}], {vars_high}]\n'
    except:
        print_exc()

    return opti_vars_text[:-1]


def get_stgtxt_to_varstxt(ui, buystg, sellstg):
    cnt = 1
    sellstg_str, buystg_str = '', ''
    if ui.focusWidget() == ui.svc_pushButton_24:
        if buystg != '' and '변수' in buystg:
            buystg = buystg.split('\n')
            for line in buystg:
                if '변수' in line:
                    for text in line:
                        buystg_str += text
                        if buystg_str[-2:] == '변수':
                            buystg_str = buystg_str.replace('변수', f'self.vars[{cnt}]')
                            cnt += 1
                    buystg_str += '\n'
                else:
                    buystg_str += line + '\n'
        if sellstg != '' and '변수' in sellstg:
            sellstg = sellstg.split('\n')
            for line in sellstg:
                if '변수' in line:
                    for text in line:
                        sellstg_str += text
                        if sellstg_str[-2:] == '변수':
                            sellstg_str = sellstg_str.replace('변수', f'self.vars[{cnt}]')
                            cnt += 1
                    sellstg_str += '\n'
                else:
                    sellstg_str += line + '\n'
    else:
        if sellstg != '' and '변수' in sellstg:
            sellstg = sellstg.split('\n')
            for line in sellstg:
                if '변수' in line:
                    for text in line:
                        sellstg_str += text
                        if sellstg_str[-2:] == '변수':
                            sellstg_str = sellstg_str.replace('변수', f'self.vars[{cnt}]')
                            cnt += 1
                    sellstg_str += '\n'
                else:
                    sellstg_str += line + '\n'
        if buystg != '' and '변수' in buystg:
            buystg = buystg.split('\n')
            for line in buystg:
                if '변수' in line:
                    for text in line:
                        buystg_str += text
                        if buystg_str[-2:] == '변수':
                            buystg_str = buystg_str.replace('변수', f'self.vars[{cnt}]')
                            cnt += 1
                    buystg_str += '\n'
                else:
                    buystg_str += line + '\n'

    return buystg_str[:-1], sellstg_str[:-1]


def get_stgtxt_sort(buystg, sellstg):
    buystg_str, sellstg_str = '', ''
    if buystg != '' and sellstg != '' and 'self.vars' in buystg and 'self.vars' in sellstg:
        buy_num = int(buystg.split('self.vars[')[1].split(']')[0])
        sell_num = int(sellstg.split('self.vars[')[1].split(']')[0])
        cnt = 1
        buystg = buystg.split('\n')
        sellstg = sellstg.split('\n')
        if buy_num < sell_num:
            for line in buystg:
                if 'self.vars' in line and '#' not in line:
                    str_pass = False
                    for text in line:
                        if str_pass:
                            if text == ']':
                                str_pass = False
                            else:
                                continue
                        else:
                            buystg_str += text

                        if buystg_str[-5:] == 'vars[':
                            buystg_str += f'{cnt}]'
                            str_pass = True
                            cnt += 1
                    buystg_str += '\n'
                else:
                    buystg_str += line + '\n'
            for line in sellstg:
                if 'self.vars' in line and '#' not in line:
                    str_pass = False
                    for text in line:
                        if str_pass:
                            if text == ']':
                                str_pass = False
                            else:
                                continue
                        else:
                            sellstg_str += text

                        if sellstg_str[-5:] == 'vars[':
                            sellstg_str += f'{cnt}]'
                            str_pass = True
                            cnt += 1
                    sellstg_str += '\n'
                else:
                    sellstg_str += line + '\n'
        else:
            for line in sellstg:
                if 'self.vars' in line and '#' not in line:
                    str_pass = False
                    for text in line:
                        if str_pass:
                            if text == ']':
                                str_pass = False
                            else:
                                continue
                        else:
                            sellstg_str += text

                        if sellstg_str[-5:] == 'vars[':
                            sellstg_str += f'{cnt}]'
                            str_pass = True
                            cnt += 1
                    sellstg_str += '\n'
                else:
                    sellstg_str += line + '\n'
            for line in buystg:
                if 'self.vars' in line and '#' not in line:
                    str_pass = False
                    for text in line:
                        if str_pass:
                            if text == ']':
                                str_pass = False
                            else:
                                continue
                        else:
                            buystg_str += text

                        if buystg_str[-5:] == 'vars[':
                            buystg_str += f'{cnt}]'
                            str_pass = True
                            cnt += 1
                    buystg_str += '\n'
                else:
                    buystg_str += line + '\n'

    return buystg_str[:-1], sellstg_str[:-1]


def get_stgtxt_sort2(optivars, gavars):
    optivars_str, gavars_str = '', ''
    if optivars != '' and 'self.vars' in optivars:
        cnt = 0
        optivars = optivars.split('\n')
        for line in optivars:
            if 'self.vars' in line and '#' not in line:
                str_pass = False
                for text in line:
                    if str_pass:
                        if text == ']':
                            str_pass = False
                        else:
                            continue
                    else:
                        optivars_str += text

                    if optivars_str[-5:] == 'vars[':
                        optivars_str += f'{cnt}]'
                        str_pass = True
                        cnt += 1
                optivars_str += '\n'
            else:
                optivars_str += line + '\n'
    if gavars != '' and 'self.vars' in gavars:
        cnt = 0
        gavars = gavars.split('\n')
        for line in gavars:
            if 'self.vars' in line and '#' not in line:
                str_pass = False
                for text in line:
                    if str_pass:
                        if text == ']':
                            str_pass = False
                        else:
                            continue
                    else:
                        gavars_str += text

                    if gavars_str[-5:] == 'vars[':
                        gavars_str += f'{cnt}]'
                        str_pass = True
                        cnt += 1
                gavars_str += '\n'
            else:
                gavars_str += line + '\n'

    return optivars_str[:-1], gavars_str[:-1]
