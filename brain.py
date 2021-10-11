import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

import time
import copy



class transmision():
    def __init__(self, bought_at, buy_price, sold_at, sell_price, status, volume, stock, profit, real_profit):
        self.bought_at = bought_at
        self.buy_price = buy_price
        self.sold_at = sold_at
        self.sell_price = sell_price
        self.status = status
        self.volume = volume
        self.stock = stock
        self.profit = profit
        self.real_profit = real_profit

    def show(self):
        print(self.bought_at) 
        print(self.buy_price) 
        print(self.sold_at) 
        print(self.status) 
        print(self.volume) 
        print(self.stock) 
        print(self.profit) 
    
    def show_profit(self):
        print(str(self.bought_at) + str('  ') + str(self.sold_at) + str('  ') + str(self.real_profit))


   
def sma_method_old_data(data):
    sma50 = data.rolling(window=50).mean()
    sma20 = data.rolling(window=20).mean()

    idx = np.argwhere(np.diff(np.sign(sma50 - sma20))).flatten()
    idx = idx[49:len(idx):1]

    transmisions = []
    max_spending = 10

    total_investments = 0
    for i in idx:
        if sma20[i+1] > sma50[i+1]:
            bought_at = data.index[i+1]
            buy_price = data[i+1]
            volume = max_spending / buy_price
            total_investments += volume * buy_price
            trans = transmision(bought_at, buy_price, bought_at, buy_price, 'done', volume, 'ahoj', 0, 0)
            a = 0
            while (a > -0.01 and a < 0.015) and i < len(data) - 2 :
                i += 1
                trans.sold_at = data.index[i]
                trans.sell_price = data[i]
                a = -((trans.buy_price - trans.sell_price) / trans.buy_price)
                trans.profit = a
                trans.real_profit = (trans.sell_price - trans.buy_price)*trans.volume

            transmisions.append(trans)


    '''
    plt.rcParams['timezone'] = 'UTC'  #nastavenie time-zony grafu


    plt.figure(figsize = (12,6))
    plt.plot(data, label='SPY Adj Close', linewidth = 2)
    plt.plot(sma50, label='50 day rolling SMA', linewidth = 1.5)
    plt.plot(sma20, label='20 day rolling SMA', linewidth = 1.5)
    plt.show()'''


    return transmisions


def buy_in_time_sma(sma20, sma50, current_price, currency):
    max_spending = 10
    #print(sma20[0])
    #print(sma20[1])
    #print(sma50[0])
    #print(sma50[1])
    if sma20[1] > sma50[1] and sma50[0] > sma20[0]:
        volume = max_spending / current_price.values[0]
        trans = transmision(copy.deepcopy(current_price.index[0]), copy.deepcopy(current_price), None, None, 'active', copy.deepcopy(volume), currency, None, None)
        print('kupilo')
	#print(current_price.values[0])
        return trans
    else:
        return None

        

    
def sell_in_time_profit(transmision, current_price):
    if transmision.status == 'active':
        profit = (current_price.values[0] - transmision.buy_price.values[0]) / transmision.buy_price.values[0]
        if profit < -0.002 or profit > 0.004:
            transmision.sold_at = copy.deepcopy(current_price.index[0])
            transmision.sell_price = copy.deepcopy(current_price)
            transmision.status = 'done'
            transmision.profit = copy.deepcopy(profit)
            transmision.real_profit = copy.deepcopy((transmision.sell_price.values[0] - transmision.buy_price.values[0]) * transmision.volume)
            print('predalo')
            myFile = open('data_1.txt', 'a') 
            myFile.write('\n'
             #+ str(transmision.bought_at) + str('  ') + str(transmision.sold_at) + str('  ') 
             + str(transmision.buy_price) + '\n'  + str(transmision.sell_price) + '\n'
             + str(transmision.profit) + '\n' + str(transmision.real_profit) + '\n'
             + str(transmision.status) + '\n' + str(transmision.volume) + '\n'
             )
            myFile.close()










'''

for i in a:
    total_profit += i.real_profit
    i.show_profit()
    myFile = open('data_1.txt', 'a') 
    free_space = '    '
    myFile.write('\n' + str(i.bought_at)+ free_space + str(i.sold_at) + free_space + str (i.profit) + free_space + str(i.real_profit))
    myFile.close()
    
print(total_profit)
'''


