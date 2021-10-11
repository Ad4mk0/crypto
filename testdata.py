from w import akey , skey

from datetime import datetime
import time
from binance.client import Client

import pandas as pd
import numpy as np
import copy
import math








currency = "BTCUSDT"
api_key = akey
api_secret = skey
client = Client(api_key, api_secret)
klines = client.get_historical_klines(currency, Client.KLINE_INTERVAL_6HOUR, "8 hour ago UTC")
df = pd.DataFrame(klines)
df.columns = ['open_time',
                'open', 'high', 'low', 'close', 'volume',
                'close_time', 'qav', 'num_trades', 'tb_base_av','tb_quote_av','ignore']

df.index = pd.to_datetime(df.open_time, unit='ms')
df['close'] = pd.to_numeric(df['close'])
print(df)



