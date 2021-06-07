# -*- coding: utf-8 -*-
"""
Created on Thu May 13 14:48:16 2021

@author: shangfr
"""
from flask import Blueprint
from flask_restx import Api

from .dict_api import api as dict_api
from .text_api import api as text_api

nlp_v1 = Blueprint('nlp_v1', __name__, url_prefix='/nlp/v1')
api = Api(nlp_v1,
          version='1.0',
          title='nlp api by using flask restx',
          description='使用flask_restx框架开发的nlp模型Api，基于paddlehub模型'
          )
api.add_namespace(dict_api)
api.add_namespace(text_api)
