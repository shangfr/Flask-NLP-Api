# -*- coding: utf-8 -*-
"""
Created on Thu May 13 14:48:16 2021

@author: shangfr
"""
from gevent import pywsgi
from utils.mylog import log
from utils.config import config_by_name
from flask import Flask
from flask import Blueprint
from flask_restx import Api

from dict_api import api as dict_api
from text_api import api as text_api

nlp_v1 = Blueprint('nlp_v1', __name__, url_prefix='/nlp/v1')
api = Api(nlp_v1,
          version='1.0',
          title='nlp api by using flask restx',
          description='使用flask_restx框架开发的nlp模型Api，基于paddlehub模型'
          )
api.add_namespace(dict_api)
api.add_namespace(text_api)


def create_app(config_name):
    # 创建Flask对象
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # 注册蓝图
    log.logger.info('注册蓝图，启动NLP Api ...')
    app.register_blueprint(nlp_v1)
    return app


if __name__ == '__main__':

    app = create_app('dev')
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    print('server 已启动')
    server.serve_forever()
