# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 14:34:19 2021

@author: shangfr
"""

from flask import Flask
from gevent import pywsgi
from flask_restful import reqparse, Api, Resource
from model.words_extract import WordDict, WordExtract
from mylog import MyLogger

dict_log = MyLogger('logs/api_dict.log',level='debug')

#from flask_cors import CORS
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["RESTFUL_JSON"] = {'ensure_ascii': False}
#cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)


dict_manage = WordDict()
dict_manage.add_userdict('体育南大街',tag='LOC')
dict_manage.add_userdict('东王新村',tag='LOC')
#text_analyse = WordExtract()

Todos = {
    'dict': {'词典管理':'get-查询词典；post-word、tag增加新词；delete-word删除新词；'},
    'report': {'我要报':'post-sentence,return-关键词、事件类型、地点、所在网格'},
    'text': {'文本分析':'post-sentence,return-分词、负向情绪值'}
}

parser = reqparse.RequestParser()
parser.add_argument('word')
parser.add_argument('tag')
parser.add_argument('sentence',location="json")

# Todo
# shows a single todo item and lets you delete a todo item
class TodoList(Resource):
    def get(self):
        print('获取api server 列表。')
        return Todos

class DictManage(Resource):
    def get(self):
        result = {'task':Todos.get('dict')}
        result['userdict'] = dict_manage.get_userdict()
        return result

    def post(self):
        args = parser.parse_args()
        uword = args['word']
        tag = args['tag']
        dict_manage.add_userdict(uword,tag)
        dict_log.logger.info("增加新词: %s %s"%(uword,tag))
        return {'task': '增加新词', 'word':uword}, 201

    def delete(self):
        args = parser.parse_args()
        uword = args['word']
        dict_manage.del_userdict(uword)
        return {'task': '删除新词', 'word':uword}, 204

class TextAnalyse(Resource):
    def get(self):
        return {'task':Todos.get('text')}

    def post(self):
        args = parser.parse_args()
        sentence = args['sentence']
        words = WordExtract.seg_depart(sentence)
        return {'task': '事件分词与情绪识别', 'result':words}, 201

class EventReport(Resource):
    def get(self):
        return {'task':Todos.get('report')}

    def post(self):
        args = parser.parse_args()
        r_sen = args['sentence']
        words = WordExtract.key_word(r_sen)
        return {'task': '我要报', 'result':words}, 201
    
##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/nlp/v1/task')
api.add_resource(DictManage, '/nlp/v1/dict')
api.add_resource(EventReport, '/nlp/v1/report')
api.add_resource(TextAnalyse, '/nlp/v1/text')


if __name__ == '__main__':
    #app.run(debug=True)
    print('server 已启动')
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)   
    server.serve_forever()
    