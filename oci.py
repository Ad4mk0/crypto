from binance.client import Client

from w import akey , skey

import pandas as pd
import numpy as np
import datetime

api_key = akey
api_secret = skey

def get_data(currency):
    client = Client(api_key, api_secret)
    klines = client.get_historical_klines(currency, Client.KLINE_INTERVAL_1MINUTE, "1 hour ago UTC")
    df = pd.DataFrame(klines)
    df.columns = ['open_time',
                'open', 'high', 'low', 'close', 'volume',
                'close_time', 'qav', 'num_trades', 'tb_base_av','tb_quote_av','ignore']

    df.index = pd.to_datetime(df.open_time, unit='ms')
    df['close'] = pd.to_numeric(df['close'])
    #print(df)
    return df