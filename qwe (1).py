from w import akey , skey

from datetime import datetime
import time
from binance.client import Client

import pandas as pd
import numpy as np
import copy


def buy_in_time_sma(sma20, sma50, current_price):   
    if sma20[1] > sma50[1] and sma50[0] > sma20[0]:
        
        api_key = akey
        api_secret = skey
        client = Client(api_key, api_secret)

        lol = Client.get_asset_balance(asset='USDT')
        juj = (lol.get('free'))

        border = Client.create_order(
            symbol='BTCUSDT',
            side=Client.SIDE_BUY,   
            type=Client.ORDER_TYPE_MARKET,
            quantity=juj)

        print("kupilo")
        global status
        status = False
        
    else:
        return None
"""
def buy_in_time_treshold(treshold, current_price):
    if current_price >= treshold:
        print("kupilo")
        global status
        status = False
        global buy_prize
        buy_prize = current_price
"""
def sell_in_time(current_price, buy_prize):

    profit = (current_price - buy_prize) / buy_prize
    print(profit)
    if profit < -0.002 or profit > 0.005:
        
        api_key = akey
        api_secret = skey
        client = Client(api_key, api_secret)

        lul = client.get_asset_balance(asset='BTC')
        joj = (lul.get('free'))

        sorder = client.create_order(
            symbol='BTCUSDT',
            side=Client.SIDE_SELL,   
            type=Client.ORDER_TYPE_MARKET,          #Sell
            quantity=joj)

        print("predalo")
        global status
        status = True

def get_data(currency):

    api_key = akey
    api_secret = skey
    client = Client(api_key, api_secret)
    klines = client.get_historical_klines(currency, Client.KLINE_INTERVAL_1MINUTE, "5 hours ago UTC")
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
    klines = client.get_historical_klines(currency, Client.KLINE_INTERVAL_1MINUTE, "1 min ago UTC")
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
    if datetime.now().second == 0:
        time.sleep(2)

        data = update_data(data, "BTCUSDT")        
        data = copy.deepcopy(data[len(data)-60:len(data):1])
         

        
        if status == True:


            closeprices = data.get('close', None)
            sma50 = closeprices.rolling(window=50).mean()
            sma20 = closeprices.rolling(window=20).mean()

            q = sma20[len(sma20)-2:len(sma20):1]
            w = sma50[len(sma50)-2:len(sma50):1]
            e = closeprices[len(closeprices)-1:len(closeprices):1]

            buy_in_time_sma(q, w, e[0])
        """
        if status == True:
            closeprices = data.get('close', None)
            e = closeprices[len(closeprices)-1:len(closeprices):1]
            buy_in_time_treshold(10000, e[0])
        """
        if status == False:
            closeprices = data.get('close', None)
            e = closeprices[len(closeprices)-1:len(closeprices):1]
            sell_in_time(e[0], buy_prize)

    continue

