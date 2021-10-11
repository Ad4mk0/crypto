from binance.client import Client
from w import akey, skey
api_key = akey               
api_secret = skey
import math


client = Client(api_key, api_secret)



'''
def floatPrecision(f, n):
	n = int(math.log10(1 / float(n)))
	f = math.floor(float(f) * 10 ** n) / 10 ** n
	f = "{:0.0{}f}".format(float(f), n)
	return str(int(f)) if int(n) == 0 else f

symbol_info = client.get_symbol_info('BTCUSDT')

tick_size = float(list(filter(lambda f: f['filterType'] == 'PRICE_FILTER', symbol_info['filters']))[0]['tickSize'])
step_size = float(list(filter(lambda f: f['filterType'] == 'LOT_SIZE', symbol_info['filters']))[0]['stepSize'])
price = float(list(filter(lambda x: x['symbol'] == 'BTCUSDT', client.get_all_tickers()))[0]['price'])

price = floatPrecision(price, tick_size)
usdt_balance = float(client.get_asset_balance(asset='USDT')['free'])
quantity = floatPrecision(usdt_balance / float(price), step_size)

buy = client.order_limit_buy(symbol='BTCUSDT',quantity=quantity,price=price)'''



lol = client.get_asset_balance(asset='BTC')
juj = (float(lol.get('free'))*0.995)

juj = round(juj,6)
print(juj)

sorder = client.create_order(
    symbol='BTCUSDT',
    side=Client.SIDE_SELL,   
    type=Client.ORDER_TYPE_MARKET,
    quantity = juj
    )


#https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#new-order--trade
#https://python-binance.readthedocs.io/en/latest/account.html#id2
#https://github.com/yasinkuyu/binance-trader/blob/master/app/Orders.py