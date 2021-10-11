from binance.client import Client

from w import akey , skey

import pandas as pd
import numpy as np
import datetime

import pandas

import matplotlib.pyplot as plt

# Window length for moving average
window_length = 14


api_key = akey
api_secret = skey


# Get data

client = Client(api_key, api_secret)
klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
df = pd.DataFrame(klines)
df.columns = ['open_time','open', 'high', 'low', 'close', 'volume','close_time', 'qav', 'num_trades', 'tb_base_av','tb_quote_av','ignore']

df.index = pd.to_datetime(df.open_time, unit='ms')
df['close'] = pd.to_numeric(df['close'])
print(df)
# Get just the adjusted close
close = df['close']
# Get the difference in price from previous step
delta = close.diff()
# Get rid of the first row, which is NaN since it did not have a previous 
# row to calculate the differences
delta = delta[1:] 

# Make the positive gains (up) and negative gains (down) Series
up, down = delta.copy(), delta.copy()
up[up < 0] = 0
down[down > 0] = 0

# Calculate the EWMA
roll_up1 = up.ewm(span=window_length).mean()
roll_down1 = down.abs().ewm(span=window_length).mean()

# Calculate the RSI based on EWMA
RS1 = roll_up1 / roll_down1
RSI1 = 100.0 - (100.0 / (1.0 + RS1))

# Calculate the SMA
roll_up2 = up.rolling(window_length).mean()
roll_down2 = down.abs().rolling(window_length).mean()

# Calculate the RSI based on SMA
RS2 = roll_up2 / roll_down2
RSI2 = 100.0 - (100.0 / (1.0 + RS2))

# Compare graphically
plt.figure(figsize=(8, 6))
RSI1.plot()
RSI2.plot()
plt.legend(['RSI via EWMA', 'RSI via SMA'])
plt.show()


#https://stackoverflow.com/questions/20526414/relative-strength-index-in-python-pandas