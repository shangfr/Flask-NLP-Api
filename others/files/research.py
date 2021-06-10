# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 17:09:54 2021

@author: shangfr
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

personinfo = pd.read_csv('red_tables/personinfo.csv')

personinfo['createTime'] = pd.to_datetime(personinfo['createTime'], format='%Y-%m-%d')

df = personinfo['createTime'].dt.date.value_counts()
df.index = pd.to_datetime(df.index)
df.sum()

df.plot(title='红管家用户数统计（日）-（总数%s）'%df.sum(), label='用户数', fontsize=20,lw=2.0,figsize=(16, 9))
df.resample('m').sum().plot(kind='bar',lw=2.0,figsize=(16, 9))

df.resample('m').sum().to_period('m').plot(kind='pie',autopct='%.1f%%', title='红管家每月新增用户数占比',figsize=(9, 9))


begin_date = personinfo['date'].min()
end_date = personinfo['date'].max()
t_range = pd.date_range(begin_date.date(), end_date.date())
#data = pd.Series(np.arange(4), index=t_range)


reportinfo = pd.read_csv('red_tables/reportinfo.csv',parse_dates=['eventTime','backTime'])
#reportinfo1 = pd.read_csv('red_tables/reportinfo1.csv')


df = reportinfo['eventTime'].dt.date.value_counts()
df.index = pd.to_datetime(df.index)
df.sum()

df.plot(title='红管家报事统计（日）-（总数%s）'%df.sum(),  fontsize=20,lw=2.0,figsize=(16, 9))



reportinfo['Feedback'] = pd.Series((reportinfo['backTime'] - reportinfo['eventTime']).values/np.timedelta64(1, 'h'))
reportinfo = reportinfo.loc[reportinfo['Feedback']>=0]
reportinfo['createName'].value_counts().head()
reportinfo['backPerson'].value_counts().head()

ad_counts = reportinfo[['backPerson','Feedback']].groupby('backPerson')['Feedback'].agg(['mean','count']) # 列表可以同时使用多个函数

df_t = pd.Series((reportinfo['backTime'] - reportinfo['eventTime']).values/np.timedelta64(1, 'h'))
df_t = df_t[df_t >= 0]

df_t.describe()

import jieba
import jieba.analyse
info_l = []
for info in reportinfo['content']:
    info_l=info_l+jieba.analyse.textrank(info, topK=3, withWeight=False)

info_dict = {}
for key in info_l:
    info_dict[key] = info_dict.get(key, 0) + 1
  
  
from pyecharts.charts import WordCloud

data = list(info_dict.items())
 
mywordcloud = WordCloud()
mywordcloud.add('',data, shape='circle')
### 渲染图片
mywordcloud.render()




import time

time_1 = 1598239265
time_tuple_1 = time.localtime(time_1)
bj_time = time.strftime("%Y/%m/%d %H:%M:%S", time_tuple_1)
print("北京时间：", bj_time)

import datetime
def getInformation(idnum):
    
    if idnum is np.nan:
        infos = np.nan
    elif len(idnum)<18:
        infos = np.nan
    else:
        birth_year = int(idnum[6:10])
        birth_month = int(idnum[10:12])
        birth_day = int(idnum[12:14])
        birthday = "{0}-{1}-{2}".format(birth_year, birth_month, birth_day)
        
        sexnum = int(idnum[16:17])
        if sexnum % 2 == 0:
            sex = 0
        else:
            sex = 1
        now = (datetime.datetime.now() + datetime.timedelta(days=1))
        year = now.year
        month = now.month
        day = now.day
        if year == birth_year:
            age = 0
        else:
            if birth_month > month or (birth_month == month and birth_day > day):
                age = year - birth_year - 1
            else:
                age = year - birth_year
        #infos = [birthday,age,sex]
        infos = age
    return infos

personinfo['cardinfo'] = personinfo['cardNum'].apply(getInformation)





df = pd.read_csv('data/问题分类清单.csv')

import jieba

df['关键词'] = df['基本分类'].apply(lambda x: jieba.lcut_for_search(x))


def eventEncoder(array,bit):
    '''
    Parameters
    ----------
    arrary : df array
        DESCRIPTION.
    bit : int
        编码位数.

    Returns
    -------
    字符串编码

    '''
    from sklearn import preprocessing
    le = preprocessing.LabelEncoder()
    
    arrayEncoder = map(lambda x: str(x).rjust(bit,'0'), le.fit_transform(array)) 
    return list(arrayEncoder)



df['eventID'] = df['办理等级'] + eventEncoder(df['办理部门'],3)
df['eventID'] = df['eventID'] + eventEncoder(df['类别'],3)
df['eventID'] = df['eventID'] + eventEncoder(df['基本分类'],3)






%timeit 