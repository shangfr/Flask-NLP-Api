# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 16:31:09 2021

@author: shangfr
"""

import pymysql
import pandas as pd
from sshtunnel import SSHTunnelForwarder #Run pip install sshtunnel

server = SSHTunnelForwarder(
    ssh_address_or_host='222.12.11.228',
    ssh_port=2210,
    ssh_username="root",
    ssh_password="z216",
    local_bind_address=('127.0.0.1', 3306),
    remote_bind_address=('122.168.57.216', 3306)
)

server.start()
conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='qwluqi',
    password='qw#2021',
    db='cms'
)

df = pd.read_sql('select * from zmhd', conn)
server.stop()
print('stop')

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


df.guesttype.value_counts().plot(kind='pie')



df['ctime'] = pd.to_datetime(df['ctime'], format='%Y-%m-%d')

df_c = df['ctime'].dt.date.value_counts()
df_c.index = pd.to_datetime(df_c.index)
df_c.sum()

df_c.plot(title='政民互动事件统计（日）-（总数%s）'%df_c.sum(), label='事件数', fontsize=20,lw=2.0,figsize=(20, 9))



df_c.resample('m').sum().to_period('m').plot(lw=2.0,figsize=(16, 9))


df_cm = df_c.resample('m').sum().to_period('m')

