from oci import get_data
from brain import sma_method_old_data, buy_in_time_sma, sell_in_time_profit

import pytz
import json

from datetime import datetime
from binance.client import Client

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

all_transmisions = []

raw_data = get_data("BTCUSDT", "26 May, 2020", "27 May, 2020")

closeprices = raw_data.get('close', None)
print(closeprices[-1])
print(closeprices.index[-1])
a = sma_method_old_data(closeprices)
zisk = 0

for i in a:
    i.show_profit()
    zisk += i.real_profit
    myFile = open('data_1.txt', 'a') 
    myFile.write('\n'
    + str(i.bought_at) + str('  ') + str(i.sold_at) + str('  ') 
    + str(i.buy_price) + str('  ') + str(i.sell_price) + str('  ')
    + str(i.profit) + str('  ') + str(i.real_profit) + str('  ')
    + str(i.status) + str('  ') + str(i.volume) + str('  '))
    myFile.close()



print(zisk)
    


