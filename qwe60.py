from w import akey , skey

from datetime import datetime
import time
from binance.client import Client

import pandas as pd
import numpy as np
import copy
import math


def floatPrecision(f, n):
	n = int(math.log10(1 / float(n)))
	f = math.floor(float(f) * 10 ** n) / 10 ** n
	f = "{:0.0{}f}".format(float(f), n)
	return str(int(f)) if int(n) == 0 else f





def buy_in_time_sma(sma20, sma50, current_price):   
    if sma20[1] > sma50[1] and sma50[0] > sma20[0]:
        
        api_key = akey
        api_secret = skey
        client = Client(api_key, api_secret)

        symbol_info = client.get_symbol_info('BTCUSDT')

        tick_size = float(list(filter(lambda f: f['filterType'] == 'PRICE_FILTER', symbol_info['filters']))[0]['tickSize'])
        step_size = float(list(filter(lambda f: f['filterType'] == 'LOT_SIZE', symbol_info['filters']))[0]['stepSize'])
        price = float(list(filter(lambda x: x['symbol'] == 'BTCUSDT', client.get_all_tickers()))[0]['price'])

        price = floatPrecision(price, tick_size)
        usdt_balance = float(client.get_asset_balance(asset='USDT')['free'])          #make money go shoppin'
        quantity = floatPrecision(usdt_balance / float(price), step_size)

        buy = client.order_limit_buy(symbol='BTCUSDT',quantity=quantity,price=price)

        print("K U P I L O")
        
        global buy_prize
        buy_prize = current_price

        global status
        status = False
        
    else:
        return None

def sell_in_time(current_price, buy_prize):

    profit = (current_price - buy_prize) / buy_prize
    print(profit)
    if profit < -0.03 or profit > 0.035:
        
        api_key = akey
        api_secret = skey
        client = Client(api_key, api_secret)

        lol = client.get_asset_balance(asset='BTC')
        juj = (float(lol.get('free'))*0.995)
        juj = round(juj,6)
        
        sorder = client.create_order(
            symbol='BTCUSDT',                       #hustlin' like a robocop
            side=Client.SIDE_SELL,   
            type=Client.ORDER_TYPE_MARKET,
            quantity = juj
            )

        print("P R E D A L O")
        
        global status
        status = True

def get_data(currency):

    api_key = akey
    api_secret = skey
    client = Client(api_key, api_secret)
    klines = client.get_historical_klines(currency, Client.KLINE_INTERVAL_6HOUR, "300 hours ago UTC")
    df = pd.DataFrame(klines)
    df.columns = ['open_time',
                'open', 'high', 'low', 'close', 'volume',
                'close_time', 'qav', 'num_trades', 'tb_base_av','tb_quote_av','ignore']

    df.index = pd.to_datetime(df.open_time, unit='ms')
    df['close'] = pd.to_numeric(df['close'])
    return df

def update_data(data_frame, currency):

    api_key = akey
    api_secret = skey
    client = Client(api_key, api_secret)
    klines = client.get_historical_klines(currency, Client.KLINE_INTERVAL_6HOUR, "1 min ago UTC")
    df = pd.DataFrame(klines)
    if df.empty:
        return pd.concat([data_frame, data_frame[len(data_frame)-1:len(data_frame):1]])

    else:
        df.columns = ['open_time',
                    'open', 'high', 'low', 'close', 'volume',
                    'close_time', 'qav', 'num_trades', 'tb_base_av','tb_quote_av','ignore']

        df.index = pd.to_datetime(df.open_time, unit='ms')
        df['close'] = pd.to_numeric(df['close'])
    
        print(df.get('close', None))

        return pd.concat([data_frame, df])

datetime.now()

data = get_data("BTCUSDT")


status = True
buy_prize = 10

var = 1
while var == 1:
    
    if (datetime.now().hour == 0) or (datetime.now().hour == 6) or (datetime.now().hour == 12) or (datetime.now().hour == 18):
    #if datetime.now().second == 0:
        time.sleep(2)

        data = update_data(data, "BTCUSDT")        
        data = copy.deepcopy(data[len(data)-60:len(data):1])
         

        
        if status == True:


            closeprices = data.get('close', None)
            sma50 = closeprices.rolling(window=50).mean()
            sma20 = closeprices.rolling(window=21).mean()

            q = sma20[len(sma20)-2:len(sma20):1]
            w = sma50[len(sma50)-2:len(sma50):1]
            e = closeprices[len(closeprices)-1:len(closeprices):1]

            buy_in_time_sma(q, w, e[0])
    
        if status == False:
            closeprices = data.get('close', None)
            e = closeprices[len(closeprices)-1:len(closeprices):1]
            sell_in_time(e[0], buy_prize)

    continue

