# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 10:12:08 2021

@author: shangfr
"""

import pymssql
import pandas as pd
from sshtunnel import SSHTunnelForwarder #Run pip install sshtunnel

server = SSHTunnelForwarder(
    ssh_address_or_host='215.13.12.22',
    ssh_port=2210,
    ssh_username="root",
    ssh_password="zddf6",
    local_bind_address=('127.0.0.10'),
    remote_bind_address=('1821.91.216.2')
)

server.start()
conn = pymssql.connect(
    host='127.0.0.10',
    #port=18004,
    user='smartddd',
    password='ddddd',
    charset='utf8',  #字符编码
    database='Eddddcity'
    )

df = pd.read_sql('show tables;', conn)
server.stop()
print('stop')

