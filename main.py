# -*- coding: utf-8 -*-
import ccxt
import ccxtpro
import asyncio
import operator
from datetime import datetime, timedelta

binance = ccxt.binance()
markets = binance.load_markets()

usdt_ticker = []
busd_ticker = []
btc_ticker = []

# usdt 마켓
for ticker in markets:
    pair = ticker.split('/')[-1]
    main_ticker = ticker.split('/')[0]
    if pair != 'USDT': continue
    if main_ticker in ['TUSD', 'USDSB', 'BUSD', 'EUR', 'DAI', 'GBP', 'TRB', 'SUSD', 'UST', 'USDP', 'BTCST', 'BZRX', 'BULL', 'BEAR',
                       'WBTC', 'BKRW', 'PAX', 'USDC', 'USDS', 'AUD', 'PAXG']: continue
    if main_ticker[-2:] == 'UP' or main_ticker[-4:] == 'DOWN' or main_ticker[-4:] == 'BEAR' or main_ticker[-4:] == 'BULL': continue

    usdt_ticker.append(main_ticker)
"""# busd 마켓
for ticker in markets:
    pair = ticker.split('/')[-1]
    main_ticker = ticker.split('/')[0]
    if pair != 'BUSD': continue
    if main_ticker in usdt_ticker: continue # 중복된 티커를 제거
    if main_ticker in ['TUSD', 'USDSB', 'BUSD', 'EUR', 'DAI', 'GBP', 'TRB', 'SUSD', 'UST', 'USDP', 'BTCST', 'BZRX',
                       'BULL', 'BEAR','WBTC']: continue
    if main_ticker[-2:] == 'UP' or main_ticker[-4:] == 'DOWN' or main_ticker[-4:] == 'BEAR' or main_ticker[-4:] == 'BULL': continue

    busd_ticker.append(main_ticker)
# btc 마켓
for ticker in markets:
    pair = ticker.split('/')[-1]
    main_ticker = ticker.split('/')[0]
    if pair != 'BTC': continue
    if main_ticker in usdt_ticker: continue # 중복된 티커를 제거
    if main_ticker in busd_ticker: continue # 중복된 티커를 제거
    if main_ticker in ['TUSD', 'USDSB', 'BUSD', 'EUR', 'DAI', 'GBP', 'TRB', 'SUSD', 'UST', 'USDP', 'BTCST', 'BZRX',
                       'BULL', 'BEAR','WBTC']: continue
    if main_ticker[-2:] == 'UP' or main_ticker[-4:] == 'DOWN' or main_ticker[-4:] == 'BEAR' or main_ticker[-4:] == 'BULL': continue

    btc_ticker.append(main_ticker)"""

print(usdt_ticker)
print(busd_ticker)
print(btc_ticker)


timeframe = '1d'

# date = '2021-12-04'
date = '2021-05-19'
date = '2022-02-01'
date = '2022-02-14'

date_start = '2022-02-01'
date_end = '2022-02-10'

today_date = datetime.now()
today9am = today_date.replace(hour=9, minute=0, second=0, microsecond=0)
date_to_compare = datetime.strptime(date, "%Y-%m-%d")
date_diff = today_date - date_to_compare
date_difference = date_diff.days

if today_date < today9am: date_difference -= 1 # 0시 기준으로 시간차를 계산해서 9시 이전은 +1상태니까 1을 뺀다

print(date_difference)

# each ohlcv candle is a list of [ timestamp, open, high, low, close, volume ]
close_index = 4
low_index = 3
high_index = 2


yc_h_change_p_dict = {}
yc_l_change_p_dict = {}

#TODO

for symbol in usdt_ticker:
    try:
        ohlcv = binance.fetch_ohlcv(symbol+'/USDT', timeframe)
        # 기본적으로 len이 1칸초과여서 1을 빼는게 맨뒤 인덱스다
        yesterday_close = ohlcv[len(ohlcv)-1 - date_difference - 1][close_index]
        low_last = ohlcv[len(ohlcv)-1 - date_difference][low_index]
        high_last = ohlcv[len(ohlcv)-1 - date_difference][high_index]
        # 전날 종가, 당일 저가 계산 - 최대 낙폭 구하기
        yc_l_change_p = round((low_last - yesterday_close) / yesterday_close * 100, 2)
        yc_h_change_p = round((high_last - yesterday_close) / yesterday_close * 100, 2)

        if not yc_h_change_p >= 6 : continue

        # print(symbol, yesterday_close, high_last, yc_h_change_p)
        yc_l_change_p_dict[symbol] = yc_l_change_p
        yc_h_change_p_dict[symbol] = yc_h_change_p
    except Exception as e:
        print(e);pass

a = sorted(yc_h_change_p_dict.items(), key=operator.itemgetter(1), reverse=True)

for i in a: print(i)
