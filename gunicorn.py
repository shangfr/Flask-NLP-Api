# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 16:10:50 2021

@author: shangfr
"""

workers = 4    # 定义同时开启的处理请求的进程数量，根据网站流量适当调整
worker_class = "gevent"   # 采用gevent库，支持异步处理请求，提高吞吐量
bind = "0.0.0.0:5000"
backlog = 2048
pidfile = "logs/gunicorn.pid"
accesslog = "logs/access.log"
errorlog = "logs/debug.log"
timeout = 600
debug = False
capture_output = True

# gunicorn --config gunicorn.py api:app
# pstree -ap|grep gunicorn 

# ENTRYPOINT ["gunicorn", "--config", "gunicorn.py", "api:app"]