from utility.setting import list_stock, list_coin


def get_label_text(coin, arry, xpoint, factor, hms):
    def ci(fname):
        return list_stock.index(fname) if not coin else list_coin.index(fname)

    if factor == '현재가':
        if coin:
            text = f"시간 {hms}\n" \
                   f"이평0060 {arry[xpoint, ci('이동평균60')]:,.8f}\n" \
                   f"이평0300 {arry[xpoint, ci('이동평균300')]:,.8f}\n" \
                   f"이평0600 {arry[xpoint, ci('이동평균600')]:,.8f}\n" \
                   f"이평1200 {arry[xpoint, ci('이동평균1200')]:,.8f}\n" \
                   f"현재가       {arry[xpoint, ci('현재가')]:,.4f}"
        else:
            text = f"시간 {hms}\n" \
                   f"이평0060 {arry[xpoint, ci('이동평균60')]:,.3f}\n" \
                   f"이평0300 {arry[xpoint, ci('이동평균300')]:,.3f}\n" \
                   f"이평0600 {arry[xpoint, ci('이동평균600')]:,.3f}\n" \
                   f"이평1200 {arry[xpoint, ci('이동평균1200')]:,.3f}\n" \
                   f"현재가       {arry[xpoint, ci('현재가')]:,.0f}"
    elif factor == '체결강도':
        text =     f"체결강도        {arry[xpoint, ci('체결강도')]:,.2f}\n" \
                   f"체결강도평균 {arry[xpoint, ci('체결강도평균')]:,.2f}\n" \
                   f"최고체결강도 {arry[xpoint, ci('최고체결강도')]:,.2f}\n" \
                   f"최저체결강도 {arry[xpoint, ci('최저체결강도')]:,.2f}"
    elif factor == '초당거래대금':
        text =     f"초당거래대금        {arry[xpoint, ci('초당거래대금')]:,.0f}\n" \
                   f"초당거래대금평균 {arry[xpoint, ci('초당거래대금평균')]:,.0f}"
    elif factor == '초당체결수량':
        if coin:
            text = f"초당매수수량 {arry[xpoint, ci('초당매수수량')]:,.8f}\n" \
                   f"초당매도수량 {arry[xpoint, ci('초당매도수량')]:,.8f}"
        else:
            text = f"초당매수수량 {arry[xpoint, ci('초당매수수량')]:,.0f}\n" \
                   f"초당매도수량 {arry[xpoint, ci('초당매도수량')]:,.0f}"
    elif factor == '호가총잔량':
        if coin:
            text = f"매도총잔량 {arry[xpoint, ci('매도총잔량')]:,.8f}\n" \
                   f"매수총잔량 {arry[xpoint, ci('매수총잔량')]:,.8f}"
        else:
            text = f"매도총잔량 {arry[xpoint, ci('매도총잔량')]:,.0f}\n" \
                   f"매수총잔량 {arry[xpoint, ci('매수총잔량')]:,.0f}"
    elif factor == '1호가잔량':
        if coin:
            text = f"매도1잔량 {arry[xpoint, ci('매도잔량1')]:,.8f}\n" \
                   f"매수1잔량 {arry[xpoint, ci('매수잔량1')]:,.8f}"
        else:
            text = f"매도1잔량 {arry[xpoint, ci('매도잔량1')]:,.0f}\n" \
                   f"매수1잔량 {arry[xpoint, ci('매수잔량1')]:,.0f}"
    elif factor == '매도수5호가잔량합':
        if coin:
            text = f"매도수5호가잔량합 {arry[xpoint, ci('매도수5호가잔량합')]:,.8f}"
        else:
            text = f"5호가잔량합 {arry[xpoint, ci('매도수5호가잔량합')]:,.0f}"
    elif factor == '누적초당매도수수량':
        if coin:
            text = f"누적초당매수수량 {arry[xpoint, ci('누적초당매수수량')]:,.8f}\n" \
                   f"누적초당매도수량 {arry[xpoint, ci('누적초당매도수량')]:,.8f}"
        else:
            text = f"누적초당매수수량 {arry[xpoint, ci('누적초당매수수량')]:,.0f}\n" \
                   f"누적초당매도수량 {arry[xpoint, ci('누적초당매도수량')]:,.0f}"
    elif factor == 'BBAND':
        text =     f"BBU  {arry[xpoint, ci('BBU')]:,.2f}\n" \
                   f"BBM {arry[xpoint, ci('BBM')]:,.2f}\n" \
                   f"BBL   {arry[xpoint, ci('BBL')]:,.2f}"
    elif factor == 'MACD':
        text =     f"MACD     {arry[xpoint, ci('MACD')]:,.2f}\n" \
                   f"MACDS  {arry[xpoint, ci('MACDS')]:,.2f}\n" \
                   f"MACDH {arry[xpoint, ci('MACDH')]:,.2f}"
    elif factor == 'HT_SINE, HT_LSINE':
        text =     f"HT_SINE   {arry[xpoint, ci('HT_SINE')]:,.2f}\n" \
                   f"HT_LSINE {arry[xpoint, ci('HT_LSINE')]:,.2f}"
    elif factor == 'HT_PHASE, HT_QUDRA':
        text =     f"HT_PHASE  {arry[xpoint, ci('HT_PHASE')]:,.2f}\n" \
                   f"HT_QUDRA {arry[xpoint, ci('HT_QUDRA')]:,.2f}"
    else:
        text =     f"{factor} {arry[xpoint, ci(factor)]:,.2f}"
        if factor == 'KAMA':
            if coin:
                text = f"{text}\n현재가   {arry[xpoint, ci('현재가')]:,.4f}"
            else:
                text = f"{text}\n현재가   {arry[xpoint, ci('현재가')]:,.0f}"

    return text
