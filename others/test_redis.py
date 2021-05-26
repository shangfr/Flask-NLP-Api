# -*- coding: utf-8 -*-
"""
Created on Mon May 24 11:58:21 2021

@author: shangfr
"""

import redis

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
r.set('food', 'mutton', ex=3)    # key是"food" value是"mutton" 将键值对存入redis缓存
print(r.get('food'))  # mutton 取出键food对应的值

r.set("visit:12306:totals", 34634)
print(r.get("visit:12306:totals"))

r.incr("visit:12306:totals")
r.incr("visit:12306:totals")

print(r.get("visit:12306:totals"))
