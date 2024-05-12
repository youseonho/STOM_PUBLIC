import os
import sqlite3
import pandas as pd
from static import read_key, write_key

DB_SETTING   = './_database/setting.db'
DB_TRADELIST = './_database/tradelist.db'
DB_STRATEGY  = './_database/strategy.db'
DB_BACKTEST  = './_database/backtest.db'

try:
    read_key()
    print('시스템 명령 실행 알림 - 암호화키 확인 완료')
except:
    write_key()
    print('시스템 명령 실행 알림 - 암호화키 생성 완료')

delete_file_list = [
    './update.txt',
    './licence.txt',
    './license.txt',
    './stom_32.bat',
    './stom_32.bat.lnk',
    './stom_32_stocklogin.bat',
    './stom_64.bat',
    './stom_64.bat.lnk',
    './stom_64_backscheduler.bat',
    './stom_backscheduler.bat',
    './stock/collector_kiwoom.py',
    './coin/collector_coin.py',
    './utility/static_numba.py',
    './utility/db_update_20220529.py',
    './utility/db_update_20220713.py',
    './utility/db_update_20230126.py',
    './db_update_20220529.bat',
    './db_update_20220713.bat',
    './db_update_20230126.bat',
    './db_update_20240503.bat',
    './backtester/backengine_coin_future3.py',
    './backtester/backengine_coin_future4.py',
    './backtester/backengine_coin_upbit3.py',
    './backtester/backengine_coin_upbit4.py',
    './backtester/backengine_stock3.py',
    './backtester/backengine_stock4.py',
    './download_kiwoom.py',
    './stock/strategy_kiwoom_.py',
    './ui/ui_draw_chart_daymin.py',
    './ui/event_filter.py',
    './kiwoom_manager.py',
    './db_update_day_20240504.bat',
    './db_update_back_20240504.bat',
    './db_distinct.bat'
]

for file in delete_file_list:
    if os.path.isfile(file):
        os.remove(file)

con = sqlite3.connect(DB_SETTING)
df  = pd.read_sql("SELECT name FROM sqlite_master WHERE TYPE = 'table'", con)
table_list = df['name'].to_list()

if 'main' not in table_list:
    columns = [
        'index', '증권사', '주식리시버', '주식트레이더', '주식틱데이터저장', '거래소', '코인리시버', '코인트레이더', '코인틱데이터저장',
        '장중전략조건검색식사용', '주식순위시간', '주식순위선정', '코인순위시간', '코인순위선정', '리시버실행시간', '트레이더실행시간',
        '바이낸스선물고정레버리지', '바이낸스선물고정레버리지값', '바이낸스선물변동레버리지값', '바이낸스선물마진타입', '바이낸스선물포지션',
        '버전업', '리시버공유'
    ]
    data = [0, '키움증권1', 0, 0, 0, '바이낸스선물', 0, 0, 0, 0, 5, 50, 5, 10, 84000, 84500, 1, 1, '0;5;1^5;10;2^10;20;3^20;30;4^30;100;5', 'ISOLATED', 'false', 1, 0]
    df = pd.DataFrame([data], columns=columns).set_index('index')
    df.to_sql('main', con)

if 'sacc' not in table_list:
    columns = [
        "index", "아이디1", "비밀번호1", "인증서비밀번호1", "계좌비밀번호1", "아이디2", "비밀번호2", "인증서비밀번호2", "계좌비밀번호2",
        "아이디3", "비밀번호3", "인증서비밀번호3", "계좌비밀번호3", "아이디4", "비밀번호4", "인증서비밀번호4", "계좌비밀번호4"
    ]
    data = [0, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    df = pd.DataFrame([data], columns=columns).set_index('index')
    df.to_sql('sacc', con)

if 'cacc' not in table_list:
    columns = ["index", "Access_key1", "Secret_key1", "Access_key2", "Secret_key2"]
    data = [0, '', '', '', '']
    df = pd.DataFrame([data], columns=columns).set_index('index')
    df.to_sql('cacc', con)


if 'telegram' not in table_list:
    columns = ["index", "str_bot", "int_id"]
    data = [0, '', '']
    df = pd.DataFrame([data], columns=columns).set_index('index')
    df.to_sql('telegram', con)

if 'stock' not in table_list:
    columns = [
        "index", "주식모의투자", "주식알림소리", "주식장초매수전략", "주식장초매도전략", "주식장초평균값계산틱수", "주식장초최대매수종목수",
        "주식장초전략종료시간", "주식장초잔고청산", "주식장초프로세스종료", "주식장초컴퓨터종료", "주식장중매수전략", "주식장중매도전략",
        "주식장중평균값계산틱수", "주식장중최대매수종목수", "주식장중전략종료시간", "주식장중잔고청산", "주식장중프로세스종료", "주식장중컴퓨터종료",
        "주식투자금고정", "주식장초투자금", "주식장중투자금", "주식손실중지", "주식손실중지수익률", "주식수익중지", "주식수익중지수익률",
        "주식장초패턴인식", "주식장중패턴인식"
    ]
    data = [0, 1, 1, '', '', 30, 10, 93000, 1, 1, 0, '', '', 30, 10, 152900, 1, 0, 0, 1, 20.0, 20.0, 0, 2.0, 0, 2.0, 0, 0]
    df = pd.DataFrame([data], columns=columns).set_index('index')
    df.to_sql('stock', con)

if 'coin' not in table_list:
    columns = [
        "index", "코인모의투자", "코인알림소리", "코인장초매수전략", "코인장초매도전략", "코인장초평균값계산틱수", "코인장초최대매수종목수",
        "코인장초전략종료시간", "코인장초잔고청산", "코인장초프로세스종료", "코인장초컴퓨터종료", "코인장중매수전략", "코인장중매도전략",
        "코인장중평균값계산틱수", "코인장중최대매수종목수", "코인장중전략종료시간", "코인장중잔고청산", "코인장중프로세스종료", "코인장중컴퓨터종료",
        "코인투자금고정", "코인장초투자금", "코인장중투자금", "코인손실중지", "코인손실중지수익률", "코인수익중지", "코인수익중지수익률",
        "코인장초패턴인식", "코인장중패턴인식"
    ]
    data = [0, 1, 1, '', '', 30, 10, 100000, 1, 0, 0, '', '', 30, 10, 234500, 1, 0, 0, 1, 1000.0, 1000.0, 0, 2.0, 0, 2.0, 0, 0]
    df = pd.DataFrame([data], columns=columns).set_index('index')
    df.to_sql('coin', con)

if 'back' not in table_list:
    columns = [
        "index", "블랙리스트추가", "백테주문관리적용", "백테매수시간기준", "백테일괄로딩", "그래프저장하지않기", "그래프띄우지않기",
        "디비자동관리", "교차검증가중치", "백테스케쥴실행", "백테스케쥴요일", "백테스케쥴시간", "백테스케쥴구분", "백테스케쥴명",
        "백테날짜고정", "백테날짜", "최적화기준값제한", "백테엔진분류방법", "옵튜나샘플러", "옵튜나고정변수", "옵튜나실행횟수",
        "옵튜나자동스탭", "범위자동관리", "보조지표사용", "보조지표설정"
    ]
    data = [0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 4, 160000, '', '', 1, '20220323',
            '0.0;1000.0;0;100.0;0.0;100.0;-10.0;10.0;0.0;100.0;-10000.0;10000.0;0.0;10.0',
            '종목코드별 분류', 'TPESampler', '', 0, 0, 0, 0,
            '5;2;2;0;12;26;9;12;26;0;30;14']
    df = pd.DataFrame([data], columns=columns).set_index('index')
    df.to_sql('back', con)

if 'etc' not in table_list:
    columns = ["index", "테마", "인트로숨김", "저해상도", "휴무프로세스종료", "휴무컴퓨터종료", "창위치기억", "창위치", "스톰라이브", "프로그램종료", "팩터선택"]
    data = [0, '다크블루', 0, 0, 1, 0, 1, '', 1, 0, '1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1']
    df = pd.DataFrame([data], columns=columns).set_index('index')
    df.to_sql('etc', con)

if 'stockbuyorder' not in table_list:
    columns = [
        'index', '주식매수주문구분', '주식매수분할횟수', '주식매수분할방법', '주식매수분할시그널', '주식매수분할하방', '주식매수분할상방',
        '주식매수분할하방수익률', '주식매수분할상방수익률', '주식매수분할고정수익률', '주식매수지정가기준가격', '주식매수지정가호가번호',
        '주식매수시장가잔량범위', '주식매수취소관심이탈', '주식매수취소매도시그널', '주식매수취소시간', '주식매수취소시간초', '주식매수금지블랙리스트',
        '주식매수금지라운드피겨', '주식매수금지라운드호가', '주식매수금지손절횟수', '주식매수금지손절횟수값', '주식매수금지거래횟수',
        '주식매수금지거래횟수값', '주식매수금지시간', '주식매수금지시작시간', '주식매수금지종료시간', '주식매수금지간격', '주식매수금지간격초',
        '주식매수금지손절간격', '주식매수금지손절간격초', '주식매수정정횟수', '주식매수정정호가차이', '주식매수정정호가'
    ]
    data = [0, '시장가', 1, 2, 1, 0, 1, 0.5, 0.5, 1, '매수1호가', 0, 3, 0, 0, 0, 30, 0, 0, 5, 0, 2, 0, 2, 0, 120000, 130000, 0, 5, 0, 300, 0, 5, 2]
    df = pd.DataFrame([data], columns=columns).set_index('index')
    df.to_sql('stockbuyorder', con)

if 'stocksellorder' not in table_list:
    columns = [
        'index', '주식매도주문구분', '주식매도분할횟수', '주식매도분할방법', '주식매도분할시그널', '주식매도분할하방', '주식매도분할상방',
        '주식매도분할하방수익률', '주식매도분할상방수익률', '주식매도지정가기준가격', '주식매도지정가호가번호', '주식매도시장가잔량범위',
        '주식매도취소관심진입', '주식매도취소매수시그널', '주식매도취소시간', '주식매도취소시간초', '주식매도손절수익률청산', '주식매도손절수익률',
        '주식매도손절수익금청산', '주식매도손절수익금', '주식매도금지매수횟수', '주식매도금지매수횟수값', '주식매도금지라운드피겨',
        '주식매도금지라운드호가', '주식매도금지시간', '주식매도금지시작시간', '주식매도금지종료시간', '주식매도금지간격', '주식매도금지간격초',
        '주식매도정정횟수', '주식매도정정호가차이', '주식매도정정호가'
    ]
    data = [0, '시장가', 1, 1, 1, 0, 1, 0.5, 2.0, '매도1호가', 0, 5, 0, 0, 0, 30, 0, 5, 0, 100, 0, 2, 0, 5, 0, 120000, 130000, 0, 300, 0, 5, 2]
    df = pd.DataFrame([data], columns=columns).set_index('index')
    df.to_sql('stocksellorder', con)

if 'coinbuyorder' not in table_list:
    columns = [
        'index', '코인매수주문구분', '코인매수분할횟수', '코인매수분할방법', '코인매수분할시그널', '코인매수분할하방', '코인매수분할상방',
        '코인매수분할하방수익률', '코인매수분할상방수익률', '코인매수분할고정수익률', '코인매수지정가기준가격', '코인매수지정가호가번호',
        '코인매수시장가잔량범위', '코인매수취소관심이탈', '코인매수취소매도시그널', '코인매수취소시간', '코인매수취소시간초', '코인매수금지블랙리스트',
        '코인매수금지200원이하', '코인매수금지손절횟수', '코인매수금지손절횟수값', '코인매수금지거래횟수', '코인매수금지거래횟수값', '코인매수금지시간',
        '코인매수금지시작시간', '코인매수금지종료시간', '코인매수금지간격', '코인매수금지간격초', '코인매수금지손절간격', '코인매수금지손절간격초',
        '코인매수정정횟수', '코인매수정정호가차이', '코인매수정정호가'
    ]
    data = [0, '시장가', 1, 1, 1, 0, 1, 0.5, 0.5, 1, '매수1호가', 0, 3, 0, 0, 0, 30, 0, 0, 0, 2, 0, 2, 0, 150000, 210000, 0, 5, 0, 300, 0, 5, 2]
    df = pd.DataFrame([data], columns=columns).set_index('index')
    df.to_sql('coinbuyorder', con)

if 'coinsellorder' not in table_list:
    columns = [
        'index', '코인매도주문구분', '코인매도분할횟수', '코인매도분할방법', '코인매도분할시그널', '코인매도분할하방', '코인매도분할상방',
        '코인매도분할하방수익률', '코인매도분할상방수익률', '코인매도지정가기준가격', '코인매도지정가호가번호', '코인매도시장가잔량범위',
        '코인매도취소관심진입', '코인매도취소매수시그널', '코인매도취소시간', '코인매도취소시간초', '코인매도손절수익률청산', '코인매도손절수익률',
        '코인매도손절수익금청산', '코인매도손절수익금', '코인매도금지매수횟수', '코인매도금지매수횟수값', '코인매도금지시간', '코인매도금지시작시간',
        '코인매도금지종료시간', '코인매도금지간격', '코인매도금지간격초', '코인매도정정횟수', '코인매도정정호가차이', '코인매도정정호가'
    ]
    data = [0, '시장가', 1, 1, 1, 0, 1, 0.5, 2.0, '매도1호가', 0, 5, 0, 0, 0, 30, 0, 5, 0, 100, 0, 2, 0, 150000, 210000, 0, 300, 0, 5, 2]
    df = pd.DataFrame([data], columns=columns).set_index('index')
    df.to_sql('coinsellorder', con)

if 'codename' not in table_list:
    columns = ["index", "종목명"]
    data = ['005930', '삼성전자']
    df = pd.DataFrame([data], columns=columns).set_index('index')
    df.to_sql('codename', con)

con.commit()
con.close()

con = sqlite3.connect(DB_STRATEGY)
cur = con.cursor()
df  = pd.read_sql("SELECT name FROM sqlite_master WHERE TYPE = 'table'", con)
table_list = df['name'].to_list()

if 'coinbuy' not in table_list:
    cur.execute('CREATE TABLE "coinbuy" ( "index" TEXT, "전략코드" TEXT )')
    cur.execute('CREATE INDEX "ix_coinbuy_index" ON "coinbuy"("index")')

if 'coinsell' not in table_list:
    cur.execute('CREATE TABLE "coinsell" ( "index" TEXT, "전략코드" TEXT )')
    cur.execute('CREATE INDEX "ix_coinsell_index"ON "coinsell" ("index")')

if 'coinoptibuy' not in table_list:
    query = 'CREATE TABLE "coinoptibuy" ( "index" TEXT, "전략코드" TEXT, ' \
            '"변수0" REAL, "변수1" REAL, "변수2" REAL, "변수3" REAL, "변수4" REAL, "변수5" REAL, "변수6" REAL, "변수7" REAL, "변수8" REAL, "변수9" REAL, ' \
            '"변수10" REAL, "변수11" REAL, "변수12" REAL, "변수13" REAL, "변수14" REAL, "변수15" REAL, "변수16" REAL, "변수17" REAL, "변수18" REAL, "변수19" REAL, ' \
            '"변수20" REAL, "변수21" REAL, "변수22" REAL, "변수23" REAL, "변수24" REAL, "변수25" REAL, "변수26" REAL, "변수27" REAL, "변수28" REAL, "변수29" REAL, ' \
            '"변수30" REAL, "변수31" REAL, "변수32" REAL, "변수33" REAL, "변수34" REAL, "변수35" REAL, "변수36" REAL, "변수37" REAL, "변수38" REAL, "변수39" REAL, ' \
            '"변수40" REAL, "변수41" REAL, "변수42" REAL, "변수43" REAL, "변수44" REAL, "변수45" REAL, "변수46" REAL, "변수47" REAL, "변수48" REAL, "변수49" REAL, ' \
            '"변수50" REAL, "변수51" REAL, "변수52" REAL, "변수53" REAL, "변수54" REAL, "변수55" REAL, "변수56" REAL, "변수57" REAL, "변수58" REAL, "변수59" REAL, ' \
            '"변수60" REAL, "변수61" REAL, "변수62" REAL, "변수63" REAL, "변수64" REAL, "변수65" REAL, "변수66" REAL, "변수67" REAL, "변수68" REAL, "변수69" REAL, ' \
            '"변수70" REAL, "변수71" REAL, "변수72" REAL, "변수73" REAL, "변수74" REAL, "변수75" REAL, "변수76" REAL, "변수77" REAL, "변수78" REAL, "변수79" REAL, ' \
            '"변수80" REAL, "변수81" REAL, "변수82" REAL, "변수83" REAL, "변수84" REAL, "변수85" REAL, "변수86" REAL, "변수87" REAL, "변수88" REAL, "변수89" REAL, ' \
            '"변수90" REAL, "변수91" REAL, "변수92" REAL, "변수93" REAL, "변수94" REAL, "변수95" REAL, "변수96" REAL, "변수97" REAL, "변수98" REAL, "변수99" REAL, ' \
            '"변수100" REAL, "변수101" REAL, "변수102" REAL, "변수103" REAL, "변수104" REAL, "변수105" REAL, "변수106" REAL, "변수107" REAL, "변수108" REAL, "변수109" REAL, ' \
            '"변수110" REAL, "변수111" REAL, "변수112" REAL, "변수113" REAL, "변수114" REAL, "변수115" REAL, "변수116" REAL, "변수117" REAL, "변수118" REAL, "변수119" REAL, ' \
            '"변수120" REAL, "변수121" REAL, "변수122" REAL, "변수123" REAL, "변수124" REAL, "변수125" REAL, "변수126" REAL, "변수127" REAL, "변수128" REAL, "변수129" REAL, ' \
            '"변수130" REAL, "변수131" REAL, "변수132" REAL, "변수133" REAL, "변수134" REAL, "변수135" REAL, "변수136" REAL, "변수137" REAL, "변수138" REAL, "변수139" REAL, ' \
            '"변수140" REAL, "변수141" REAL, "변수142" REAL, "변수143" REAL, "변수144" REAL, "변수145" REAL, "변수146" REAL, "변수147" REAL, "변수148" REAL, "변수149" REAL, ' \
            '"변수150" REAL, "변수151" REAL, "변수152" REAL, "변수153" REAL, "변수154" REAL, "변수155" REAL, "변수156" REAL, "변수157" REAL, "변수158" REAL, "변수159" REAL, ' \
            '"변수160" REAL, "변수161" REAL, "변수162" REAL, "변수163" REAL, "변수164" REAL, "변수165" REAL, "변수166" REAL, "변수167" REAL, "변수168" REAL, "변수169" REAL, ' \
            '"변수170" REAL, "변수171" REAL, "변수172" REAL, "변수173" REAL, "변수174" REAL, "변수175" REAL, "변수176" REAL, "변수177" REAL, "변수178" REAL, "변수179" REAL, ' \
            '"변수180" REAL, "변수181" REAL, "변수182" REAL, "변수183" REAL, "변수184" REAL, "변수185" REAL, "변수186" REAL, "변수187" REAL, "변수188" REAL, "변수189" REAL, ' \
            '"변수190" REAL, "변수191" REAL, "변수192" REAL, "변수193" REAL, "변수194" REAL, "변수195" REAL, "변수196" REAL, "변수197" REAL, "변수198" REAL, "변수199" REAL )'
    cur.execute(query)
    cur.execute('CREATE INDEX "ix_coinoptibuy_index"ON "coinoptibuy" ("index")')

if 'coinoptisell' not in table_list:
    cur.execute('CREATE TABLE "coinoptisell" ( "index" TEXT, "전략코드" TEXT )')
    cur.execute('CREATE INDEX "ix_coinoptisell_index"ON "coinoptisell" ("index")')

if 'coinoptivars' not in table_list:
    cur.execute('CREATE TABLE "coinoptivars" ( "index" TEXT, "전략코드" TEXT )')
    cur.execute('CREATE INDEX "ix_coinoptivars_index"ON "coinoptivars" ("index")')

if 'coinvars' not in table_list:
    cur.execute('CREATE TABLE "coinvars" ( "index" TEXT, "전략코드" TEXT )')
    cur.execute('CREATE INDEX "ix_coinvars_index"ON "coinvars" ("index")')

if 'coinbuyconds' not in table_list:
    cur.execute('CREATE TABLE "coinbuyconds" ( "index" TEXT, "전략코드" TEXT )')
    cur.execute('CREATE INDEX "ix_coinbuyconds_index" ON "coinbuyconds"("index")')

if 'coinsellconds' not in table_list:
    cur.execute('CREATE TABLE "coinsellconds" ( "index" TEXT, "전략코드" TEXT )')
    cur.execute('CREATE INDEX "ix_coinsellconds_index"ON "coinsellconds" ("index")')

if 'coinpattern' not in table_list:
    cur.execute('CREATE TABLE "coinpattern" ( "index" TEXT, "패턴설정" TEXT )')
    cur.execute('CREATE INDEX "ix_coinpattern_index" ON "coinpattern"("index")')

if 'stockbuy' not in table_list:
    cur.execute('CREATE TABLE "stockbuy" ( "index" TEXT, "전략코드" TEXT )')
    cur.execute('CREATE INDEX "ix_stockbuy_index"ON "stockbuy" ("index")')

if 'stocksell' not in table_list:
    cur.execute('CREATE TABLE "stocksell" ( "index" TEXT, "전략코드" TEXT )')
    cur.execute('CREATE INDEX "ix_stocksell_index"ON "stocksell" ("index")')

if 'stockoptibuy' not in table_list:
    query = 'CREATE TABLE "stockoptibuy" ( "index" TEXT, "전략코드" TEXT, ' \
            '"변수0" REAL, "변수1" REAL, "변수2" REAL, "변수3" REAL, "변수4" REAL, "변수5" REAL, "변수6" REAL, "변수7" REAL, "변수8" REAL, "변수9" REAL, ' \
            '"변수10" REAL, "변수11" REAL, "변수12" REAL, "변수13" REAL, "변수14" REAL, "변수15" REAL, "변수16" REAL, "변수17" REAL, "변수18" REAL, "변수19" REAL, ' \
            '"변수20" REAL, "변수21" REAL, "변수22" REAL, "변수23" REAL, "변수24" REAL, "변수25" REAL, "변수26" REAL, "변수27" REAL, "변수28" REAL, "변수29" REAL, ' \
            '"변수30" REAL, "변수31" REAL, "변수32" REAL, "변수33" REAL, "변수34" REAL, "변수35" REAL, "변수36" REAL, "변수37" REAL, "변수38" REAL, "변수39" REAL, ' \
            '"변수40" REAL, "변수41" REAL, "변수42" REAL, "변수43" REAL, "변수44" REAL, "변수45" REAL, "변수46" REAL, "변수47" REAL, "변수48" REAL, "변수49" REAL, ' \
            '"변수50" REAL, "변수51" REAL, "변수52" REAL, "변수53" REAL, "변수54" REAL, "변수55" REAL, "변수56" REAL, "변수57" REAL, "변수58" REAL, "변수59" REAL, ' \
            '"변수60" REAL, "변수61" REAL, "변수62" REAL, "변수63" REAL, "변수64" REAL, "변수65" REAL, "변수66" REAL, "변수67" REAL, "변수68" REAL, "변수69" REAL, ' \
            '"변수70" REAL, "변수71" REAL, "변수72" REAL, "변수73" REAL, "변수74" REAL, "변수75" REAL, "변수76" REAL, "변수77" REAL, "변수78" REAL, "변수79" REAL, ' \
            '"변수80" REAL, "변수81" REAL, "변수82" REAL, "변수83" REAL, "변수84" REAL, "변수85" REAL, "변수86" REAL, "변수87" REAL, "변수88" REAL, "변수89" REAL, ' \
            '"변수90" REAL, "변수91" REAL, "변수92" REAL, "변수93" REAL, "변수94" REAL, "변수95" REAL, "변수96" REAL, "변수97" REAL, "변수98" REAL, "변수99" REAL, ' \
            '"변수100" REAL, "변수101" REAL, "변수102" REAL, "변수103" REAL, "변수104" REAL, "변수105" REAL, "변수106" REAL, "변수107" REAL, "변수108" REAL, "변수109" REAL, ' \
            '"변수110" REAL, "변수111" REAL, "변수112" REAL, "변수113" REAL, "변수114" REAL, "변수115" REAL, "변수116" REAL, "변수117" REAL, "변수118" REAL, "변수119" REAL, ' \
            '"변수120" REAL, "변수121" REAL, "변수122" REAL, "변수123" REAL, "변수124" REAL, "변수125" REAL, "변수126" REAL, "변수127" REAL, "변수128" REAL, "변수129" REAL, ' \
            '"변수130" REAL, "변수131" REAL, "변수132" REAL, "변수133" REAL, "변수134" REAL, "변수135" REAL, "변수136" REAL, "변수137" REAL, "변수138" REAL, "변수139" REAL, ' \
            '"변수140" REAL, "변수141" REAL, "변수142" REAL, "변수143" REAL, "변수144" REAL, "변수145" REAL, "변수146" REAL, "변수147" REAL, "변수148" REAL, "변수149" REAL, ' \
            '"변수150" REAL, "변수151" REAL, "변수152" REAL, "변수153" REAL, "변수154" REAL, "변수155" REAL, "변수156" REAL, "변수157" REAL, "변수158" REAL, "변수159" REAL, ' \
            '"변수160" REAL, "변수161" REAL, "변수162" REAL, "변수163" REAL, "변수164" REAL, "변수165" REAL, "변수166" REAL, "변수167" REAL, "변수168" REAL, "변수169" REAL, ' \
            '"변수170" REAL, "변수171" REAL, "변수172" REAL, "변수173" REAL, "변수174" REAL, "변수175" REAL, "변수176" REAL, "변수177" REAL, "변수178" REAL, "변수179" REAL, ' \
            '"변수180" REAL, "변수181" REAL, "변수182" REAL, "변수183" REAL, "변수184" REAL, "변수185" REAL, "변수186" REAL, "변수187" REAL, "변수188" REAL, "변수189" REAL, ' \
            '"변수190" REAL, "변수191" REAL, "변수192" REAL, "변수193" REAL, "변수194" REAL, "변수195" REAL, "변수196" REAL, "변수197" REAL, "변수198" REAL, "변수199" REAL )'
    cur.execute(query)
    cur.execute('CREATE INDEX "ix_stockoptibuy_index"ON "stockoptibuy" ("index")')

if 'stockoptisell' not in table_list:
    cur.execute('CREATE TABLE "stockoptisell" ( "index" TEXT, "전략코드" TEXT )')
    cur.execute('CREATE INDEX "ix_stockoptisell_index"ON "stockoptisell" ("index")')

if 'stockoptivars' not in table_list:
    cur.execute('CREATE TABLE "stockoptivars" ( "index" TEXT, "전략코드" TEXT )')
    cur.execute('CREATE INDEX "ix_stockoptivars_index"ON "stockoptivars" ("index")')

if 'stockvars' not in table_list:
    cur.execute('CREATE TABLE "stockvars" ( "index" TEXT, "전략코드" TEXT )')
    cur.execute('CREATE INDEX "ix_stockvars_index"ON "stockvars" ("index")')

if 'stockbuyconds' not in table_list:
    cur.execute('CREATE TABLE "stockbuyconds" ( "index" TEXT, "전략코드" TEXT )')
    cur.execute('CREATE INDEX "ix_stockbuyconds_index" ON "stockbuyconds"("index")')

if 'stocksellconds' not in table_list:
    cur.execute('CREATE TABLE "stocksellconds" ( "index" TEXT, "전략코드" TEXT )')
    cur.execute('CREATE INDEX "ix_stocksellconds_index"ON "stocksellconds" ("index")')

if 'stockpattern' not in table_list:
    cur.execute('CREATE TABLE "stockpattern" ( "index" TEXT, "패턴설정" TEXT )')
    cur.execute('CREATE INDEX "ix_stockpattern_index" ON "stockpattern"("index")')

if 'schedule' not in table_list:
    cur.execute('CREATE TABLE "schedule" ( "index" TEXT, "스케쥴" TEXT )')
    cur.execute('CREATE INDEX "ix_schedule_index"ON "schedule" ("index")')

con.commit()
con.close()

con = sqlite3.connect(DB_TRADELIST)
cur = con.cursor()
df  = pd.read_sql("SELECT name FROM sqlite_master WHERE TYPE = 'table'", con)
table_list = df['name'].to_list()

if 'c_chegeollist' not in table_list:
    query = 'CREATE TABLE "c_chegeollist" ( "index"	TEXT, "종목명" TEXT, "주문구분" TEXT, "주문수량" REAL, ' \
            '"체결수량" REAL, "미체결수량" REAL, "체결가" REAL, "체결시간" TEXT, "주문가격" REAL, "주문번호" TEXT )'
    cur.execute(query)
    cur.execute('CREATE INDEX "ix_c_chegeollist_index" ON "c_chegeollist" ( "index" )')

if 'c_jangolist' not in table_list:
    query = 'CREATE TABLE "c_jangolist" ( "index" TEXT, "종목명" TEXT, "매입가" REAL, "현재가" REAL, "수익률" REAL, ' \
            '"평가손익" INTEGER, "매입금액" INTEGER, "평가금액" INTEGER, "보유수량" REAL, "분할매수횟수" INTEGER, "분할매도횟수" INTEGER, "매수시간" TEXT )'
    cur.execute(query)
    cur.execute('CREATE INDEX "ix_c_jangolist_index"ON "c_jangolist" ("index")')

if 'c_jangolist_future' not in table_list:
    query = 'CREATE TABLE "c_jangolist_future" ( "index" TEXT, "종목명" TEXT, "포지션" TEXT, "매입가" REAL, "현재가" REAL, "수익률" REAL, ' \
            '"평가손익" INTEGER, "매입금액" INTEGER, "평가금액" INTEGER, "보유수량" REAL, "레버리지" INTEGER, "분할매수횟수" INTEGER, "분할매도횟수" INTEGER, "매수시간" TEXT )'
    cur.execute(query)
    cur.execute('CREATE INDEX "ix_c_jangolist_future_index"ON "c_jangolist_future" ("index")')

if 'c_totaltradelist' not in table_list:
    query = 'CREATE TABLE "c_totaltradelist" ( "index" TEXT, "총매수금액" INTEGER, "총매도금액" INTEGER, "총수익금액" INTEGER, ' \
            '"총손실금액" INTEGER, "수익률" REAL, "수익금합계" INTEGER )'
    cur.execute(query)
    cur.execute('CREATE INDEX "ix_c_totaltradelist_index" ON "c_totaltradelist" ( "index" )')

if 'c_tradelist' not in table_list:
    query = 'CREATE TABLE "c_tradelist" ( "index" TEXT, "종목명" TEXT, "매수금액" INTEGER, "매도금액" INTEGER, ' \
            '"주문수량" REAL, "수익률" REAL, "수익금" INTEGER, "체결시간" TEXT )'
    cur.execute(query)
    cur.execute('CREATE INDEX "ix_c_tradelist_index" ON "c_tradelist" ( "index" )')

if 'c_tradelist_future' not in table_list:
    query = 'CREATE TABLE "c_tradelist_future" ( "index" TEXT, "종목명" TEXT, "포지션" TEXT, "매수금액" INTEGER, "매도금액" INTEGER, ' \
            '"주문수량" REAL, "수익률" REAL, "수익금" INTEGER, "체결시간" TEXT )'
    cur.execute(query)
    cur.execute('CREATE INDEX "ix_c_tradelist_future_index" ON "c_tradelist_future" ( "index" )')

if 's_chegeollist' not in table_list:
    query = 'CREATE TABLE "s_chegeollist" ( "index" TEXT, "종목명" TEXT, "주문구분" TEXT, "주문수량" INTEGER, ' \
            '"체결수량" INTEGER, "미체결수량" INTEGER, "체결가" INTEGER, "체결시간" TEXT, "주문가격" INTEGER, "주문번호" TEXT )'
    cur.execute(query)
    cur.execute('CREATE INDEX "ix_s_chegeollist_index" ON "s_chegeollist" ( "index" )')

if 's_jangolist' not in table_list:
    query = 'CREATE TABLE "s_jangolist" ( "index" TEXT, "종목명" TEXT, "매입가" INTEGER, "현재가" INTEGER, "수익률" REAL, ' \
            '"평가손익" INTEGER, "매입금액" INTEGER, "평가금액" INTEGER, "보유수량" INTEGER, "분할매수횟수" INTEGER, "분할매도횟수" INTEGER, "매수시간" TEXT )'
    cur.execute(query)
    cur.execute('CREATE INDEX "ix_s_jangolist_index"ON "s_jangolist" ("index")')

if 's_totaltradelist' not in table_list:
    query = 'CREATE TABLE "s_totaltradelist" ( "index" TEXT, "총매수금액" INTEGER, "총매도금액" INTEGER, ' \
            '"총수익금액" INTEGER, "총손실금액" INTEGER, "수익률" REAL, "수익금합계" INTEGER)'
    cur.execute(query)
    cur.execute('CREATE INDEX "ix_s_totaltradelist_index" ON "s_totaltradelist" ( "index" )')

if 's_tradelist' not in table_list:
    query = 'CREATE TABLE "s_tradelist" ( "index" TEXT, "종목명" TEXT, "매수금액" INTEGER, "매도금액" INTEGER, ' \
            '"주문수량" INTEGER, "수익률" REAL, "수익금" INTEGER, "체결시간" TEXT )'
    cur.execute(query)
    cur.execute('CREATE INDEX "ix_s_tradelist_index" ON "s_tradelist" ( "index" )')

con.commit()
con.close()

print('시스템 명령 실행 알림 - 데이터베이스 확인 완료')
