# -*- coding: utf-8 -*-
"""
Created on Thu May 13 14:38:50 2021

@author: shangfr
"""

from flask import Flask
from .config import config_by_name


def create_app(config_name):
    # 创建Flask对象
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # 注册蓝图
    from server.api import nlp_v1
    app.register_blueprint(nlp_v1)
    return app



