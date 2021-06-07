# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 17:03:44 2021

@author: shangfr
"""

from server import create_app
from gevent import pywsgi

app = create_app('dev')


if __name__ == '__main__':
    print('server 已启动')
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
