import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
#import yahoofinancials 
import time

plt.rcParams['timezone'] = 'UTC'  #nastavenie time-zony grafu

class transmision():
    def __init__(self, bought_at, value, sold_at, sell_prize, status, volume, stock, profit):
        self.bought_at = bought_at
        self.value = value
        self.sold_at = sold_at
        self.sell_prize = sell_prize
        self.status = status
        self.volume = volume
        self.stock = stock
        self.profit = profit

    def show(self):
        print(self.bought_at) 
        print(self.value) 
        print(self.sold_at) 
        print(self.status) 
        print(self.volume) 
        print(self.stock) 
        print(self.profit) 

    def show_profit(self):
        real_profit = (self.sell_prize - self.value)*self.volume
        print(self.bought_at, self.sold_at, self.profit) 
        print(real_profit)

    def real_profit(self):
        real_profit = (self.sell_prize - self.value)*self.volume
        return(real_profit)
    

   




stock_name = "RLC-USD"
stock = yf.Ticker(stock_name)
date_start = '2020-05-13'
date_end = '2020-05-14'
date_interval = '1m'

#data =(stock.history(period = '1d', interval = date_interval))
data =(stock.history(start = date_start, end = date_end, interval = date_interval))
#data =(stock.history(period='1d',interval='1m'))

closeprices = data.get('Close', None)
closeprices.drop(closeprices.tail(1).index,inplace=True) #odjebanie timestampy od yFinance

sma50 = closeprices.rolling(window=50).mean()
sma20 = closeprices.rolling(window=20).mean()

idx = np.argwhere(np.diff(np.sign(sma50 - sma20))).flatten()
idx = idx[49:len(idx):1]



transmisions = []

max_spending = 20
points = []
points_time = []

total_investments = 0
for i in idx:
    if sma20[i+1] > sma50[i+1]:
        points.append(i)
        points_time.append(closeprices.index[i])
        bought_at = closeprices.index[i+1]
        buy_prize = closeprices[i+1]
        volume = max_spending / buy_prize
        total_investments += volume * buy_prize
        trans = transmision(bought_at, buy_prize, bought_at, buy_prize, 'done', volume, stock_name, 0)
        a = 0
        while (a > -0.02 and a < 0.03) and i < len(closeprices) - 2 :
            i += 1
            trans.sold_at = closeprices.index[i]
            trans.sell_prize = closeprices[i]
            a = -((trans.value - trans.sell_prize) / trans.value)
            trans.profit = a
        print(trans)
        transmisions.append(trans)
        trans.show_profit()

total_profit = 0
myFile = open('data_1.txt', 'a') 
myFile.write('\n' + str(points))
myFile.write('\n' + str(points_time))


for i in transmisions:
    total_profit += i.real_profit()
    i.show_profit()
    myFile = open('data_1.txt', 'a') 
    qwe = i.real_profit()
    free_space = '    '
    myFile.write('\n' + str(i.bought_at)+ free_space + str(i.sold_at) + free_space + str (i.profit) + free_space + str(i.real_profit()))
    myFile.close()
    
print('')
print(total_profit)
print(total_investments)

File = open('raw_data_1.txt', 'a') 
File.write('\n' + str(len(closeprices)))
File.close()

for index, value in closeprices.items():
    File = open('raw_data_1.txt', 'a') 
    File.write('\n' + str(index) + '  ' + str(value))
    File.close()



plt.figure(figsize = (12,6))
plt.plot(closeprices, label='SPY Adj Close', linewidth = 2)
plt.plot(sma50, label='50 day rolling SMA', linewidth = 1.5)
plt.plot(sma20, label='20 day rolling SMA', linewidth = 1.5)
plt.show()
