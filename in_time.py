from oci import get_data
from brain import sma_method_old_data, buy_in_time_sma, sell_in_time_profit

import pytz
import json

from datetime import datetime
import time
from binance.client import Client

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



all_transmisions = []
datetime.now()
var = 1
while var == 1:
    if datetime.now().second == 0:
        time.sleep(1.5)
        raw_data = get_data("BTCUSDT")
        closeprices = raw_data.get('close', None)
        sma50 = closeprices.rolling(window=50).mean()
        sma20 = closeprices.rolling(window=20).mean()
        print('prebehlo')
        
        q = sma20[len(sma20)-3:len(sma20)-1:1]
        w = sma50[len(sma50)-3:len(sma50)-1:1]
        e = closeprices[len(closeprices)-2:len(closeprices)-1:1]
        
        #print(q)
        #print(w)
        #print(e)
        
        x = buy_in_time_sma(q, w, e, "BTCUSDT")
        if x != None:
            all_transmisions.append(x)    

        for i in all_transmisions:
            sell_in_time_profit(i, e)
            #print('spravilo trans')
        
    continue






