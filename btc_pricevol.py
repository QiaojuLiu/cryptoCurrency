import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

import numpy as np
import pandas as pd
import tushare as ts

#获取数据
pro = ts.pro_api()
df = pro.btc_pricevol(start_date ='20100101',end_date = '20190516')
df = df[::-1]
df.to_csv('picture/btc.csv')
btc_data = pd.read_csv('picture/btc.csv',index_col = 'date',parse_dates = True)

#价格最低的时候
date_min = btc_data[btc_data.price == btc_data.price.min()]
#价格最高的时候
date_max = btc_data[btc_data.price == btc_data.price.max()]

#如果在最高价的时候入手，每个时间段的浮亏的情况
btc_loss = btc_data[btc_data.index>date_max.index[0]]
btc_loss['percent%'] = (1-btc_loss.price/date_max.price[0])*100

#如果在最地点的时候入手，每个时间段的浮赢的情况

btc_gain = btc_data[btc_data.index>date_min.index[0]]
btc_gain['percent%'] = (btc_gain.price/date_min.price[0])*100

#计算log return值
def log_return(data):
    data['shift_price'] = btc_data['price'].shift(1)
    data.columns = ['xuhao','price','volume','shift_price']
    data = btc_data.dropna()
    data['log_return'] = np.log(data.price/data.shift_price)
    return data
  
"""btc_data_shift = btc_data['price'].shift(1)
btc_data['shift'] = btc_data_shift
btc_data.columns = ['xuhao','price','volume','shift_price']
btc_data = btc_data.dropna()"""


btc_data = log_return(btc_data)
#按季度,月，周预处理

btc_data_quarter = btc_data.resample('Q').mean()
btc_data_month = btc_data.resample('M').mean()
btc_data_week = btc_data.resample('W').mean()
#计算价格上涨的次数和下降的次数
btc_data_above_0 = pd.Series(list(filter(lambda x:x > 0,btc_data.log_return)),name = 'above_0')
btc_data_below_0 = pd.Series(list(filter(lambda x:x <= 0,btc_data.log_return)),name = 'below_0')

btc_data_above_0_desc = btc_data_above_0.describe()
btc_data_below_0_desc = btc_data_below_0.describe()

#可视化
def picture(data,col_name1,col_name2,name,title):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(data[col_name1],'r',label = col_name1)
    ax1.legend(loc='upper left')
    ax1.set_ylabel('Price/$')
    ax2 = ax1.twinx()
    ax2.plot(data[col_name2],'k',label = col_name2)
    ax2.set_ylabel('volume')
    ax2.legend(loc='upper right')
    plt.title(title)
    plt.tight_layout()
    plt.savefig('picture/{}.png'.format(name))
    
    
if __name__ == '__main__':
    picture(btc_data,'price','volume','btc_pv','Price and Volume of BTC')
    picture(btc_data,'log_return','volume','log_return','Log_return and Volume')
    
    






