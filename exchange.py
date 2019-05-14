import tushare as ts
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
fontproperties=FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
picture = ['exchange','pair','mount']

kw = {'user-agent':'Mozilla/5.0'}
url = 'https://tushare.pro/document/41?doc_id=66'
r = requests.get(url,headers = kw)
soup = BeautifulSoup(r.text,'html.parser')

#获得国家名和简称
name_list = {}
trs = soup.find_all('tr')
for tr in trs:
    tds = tr.find_all('td')
    if len(tds) == 2:
        short_name = ''.join(tds[0].contents)
        name = ''.join(tds[1].contents)
        name_list[short_name] = name

data = []
pro = ts.pro_api()
for country in name_list:
    df = pro.coinexchanges(area_code = country)
    data.append(df)
  
total_data = pd.concat(data)

#交易对最多的交易所
max_pair = total_data[total_data.pairs == total_data.pairs.max()]
max_name = max_pair['name']
max_name.to_csv('picture/max_pairs.csv')
#交易对最少的交易所
min_pair = total_data[total_data.pairs == total_data.pairs.min()]
min_name = min_pair['name']
min_name.to_csv('picture/min_pairs.csv')

#有期货交易的交易所个数
fut_yes = total_data[total_data['fut_trade'] =='Y' ]
fut_num = len(fut_yes)
fut_ex_name = fut_yes['name']
fut_ex_name.to_csv('picture/fut_ex_name.csv')

#提供场外交易的交易所个数
oct_yes = total_data[total_data['oct_trade'] =='Y' ]
oct_num = len(oct_yes)
oct_ex_name = oct_yes['name']
oct_ex_name.to_csv('picture/oct_ex_name.csv')

#可视化
group_area = total_data.groupby('area_code').count()
group_area = group_area.sort_values(by = 'exchange',ascending = False)


for i in range(20):
    num = group_area['exchange'][i]
    country_name = group_area.index[i]
    plt.bar(name_list[country_name],num,label = num)
plt.legend(loc = 'upper right')
plt.xticks(fontproperties = fontproperties)
plt.title('交易所数全球前20的国家(地区)',fontproperties = fontproperties,
          fontsize='large',fontweight='bold')
plt.ylabel('交易所个数',fontproperties = fontproperties,labelpad = 20)
plt.xlabel('国家(地区)',fontproperties = fontproperties,labelpad = 12)
"""ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')"""
plt.savefig('picture/{}.jpeg'.format(picture[0]),dpi=300, bbox_inches = 'tight')
#plt.show()


    


                                
                                 
