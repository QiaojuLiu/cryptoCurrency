import tushare as ts
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
fontproperties=FontProperties(fname='/System/Library/Fonts/PingFang.ttc')

pro = ts.pro_api()
exchange = ['huobi','okex','biance','bitfinex']
asset_type = ['coin','future']
data_coin = []
data_future = []
for e in exchange:
    df_coin = pro.coinfees(exchange = e,asset_type = asset_type[0])
    df_future = pro.coinfees(exchange = e,asset_type = asset_type[1])
    data_coin.append(df_coin)
    data_future.append(df_future)
    
    
coin_fee = pd.concat(data_coin)
future_fee = pd.concat(data_future)

coin_min = coin_fee.min()
coin_max = coin_fee.max()

future_min = future_fee.min()
future_max = future_fee.max()

#可视化
f_maker_fee = [float(fee)*2000000 for fee in future_fee.maker_fee]
f_taker_fee = [float(fee)*2000000 for fee in future_fee.taker_fee]
x1 = np.ones(8)
y = np.arange(8)
x2 = x1+1
for i in range(8):
	plt.scatter(x1[i],y[i],s=f_taker_fee[i])
for i in range(8):
	if f_maker_fee[i] > 0:
		plt.scatter(x2[i],y[i],s=f_maker_fee[i])
	elif f_maker_fee[i] < 0:
		maker_fee[i] = abs(maker_fee[i])
		plt.scatter(x2[i],y[i],color='green',s=f_maker_fee[i])

                            
                                 
