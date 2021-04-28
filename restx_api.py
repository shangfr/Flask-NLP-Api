# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 11:24:38 2021

@author: shangfr
"""

from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
from gevent import pywsgi
from model.words_extract import WordDict, WordExtract
from mylog import MyLogger
dict_log = MyLogger('logs/api_dict.log',level='debug',print_screen = False)
#from flask_cors import CORS
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["RESTFUL_JSON"] = {'ensure_ascii': False}
#cors = CORS(app, resources={r"*": {"origins": "*"}})

app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version="1.0", title="NLP API", description="上报事件分析 API",)

ns_task = api.namespace("nlp/v1/task", description="task api任务")
ns_dict = api.namespace("nlp/v1/dict", description="dict api任务")
ns_report = api.namespace("nlp/v1/report", description="report api任务")
ns_text = api.namespace("nlp/v1/text", description="text api任务")

dict_manage = WordDict()
dict_manage.add_userdict('体育南大街',tag='LOC')
dict_manage.add_userdict('东王新村',tag='LOC')
#text_analyse = WordExtract()

Todos = {
    'dict': {'task':'词典管理: get-查询词典；post-word、tag增加新词；delete-word删除新词；'},
    'report': {'task':'我要报: post-sentence,return-关键词、事件类型、地点、所在网格'},
    'text': {'task':'文本分析: post-sentence,return-分词、负向情绪值'}
}

todo = api.model(
    "Todo", {"task": fields.String(required=True, description="The task details")}
)

listed_todo = api.model(
    "ListedTodo",
    {
        "id": fields.String(required=True, description="The todo ID"),
        "todo": fields.Nested(todo, description="The Todo"),
    },
)

parser = api.parser()
parser.add_argument('word', type=str, required=True)
parser.add_argument('tag')

parser1 = api.parser()
parser1.add_argument('sentence', type=str, required=True)

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in Todos:
        api.abort(404, "Todo {} doesn't exist".format(todo_id))

# Todo
# shows a single todo item and lets you delete a todo item
class TodoList(Resource):
    """Shows a list of all todos, and lets you POST to add new tasks"""

    @api.marshal_list_with(listed_todo)
    def get(self):
        """查看所有接口"""
        return [{"id": id, "todo": todo} for id, todo in Todos.items()]

class DictManage(Resource):
    """Shows a list of all words, and lets you POST to add new word"""
    def get(self):
        """查看自定义词典"""
        result = {'task':Todos.get('dict')}
        result['userdict'] = dict_manage.get_userdict()
        return result

    @api.expect(parser)
    def post(self):
        """增加新词，包含词性"""
        args = parser.parse_args()
        uword = args['word']
        tag = args['tag']
        dict_manage.add_userdict(uword,tag)
        dict_log.logger.info("增加新词: %s %s"%(uword,tag))
        return {'task': '增加新词', 'word':uword}, 201

    @api.doc(responses={204: "Word deleted"})
    @api.expect(parser)
    def delete(self):
        """删除新词"""
        args = parser.parse_args()
        uword = args['word']
        dict_manage.del_userdict(uword)
        return {'task': '删除新词', 'word':uword}, 204

class TextAnalyse(Resource):
    @api.marshal_with(todo, code=201)
    def get(self):
        """查看事件分词与情绪识别"""
        return {'task':Todos.get('text')}

    @api.expect(parser1)
    def post(self):
        """进行事件分词与情绪识别"""
        args = parser1.parse_args()
        sentence = args['sentence']
        words = WordExtract.seg_depart(sentence)
        return {'task': '事件分词与情绪识别', 'result':words}, 201

@api.doc(responses={404: "Todo not found"})
class EventReport(Resource):
    """我要报: post-sentence,return-关键词、事件类型、地点、所在网格"""
    @api.marshal_with(todo, code=201)
    def get(self):
        """查看我要报任务"""
        return {'task':Todos.get('report')}
    
    @api.expect(parser1)
    def post(self):
        """提交我要报内容文本"""
        args = parser1.parse_args()
        r_sen = args['sentence']
        words = WordExtract.key_word(r_sen)
        return {'task': '我要报', 'result':words}, 201
    
##
## Actually setup the Api resource routing here
##
ns_task.add_resource(TodoList, '/')
ns_dict.add_resource(DictManage, '/')
ns_report.add_resource(EventReport, '/')
ns_text.add_resource(TextAnalyse, '/')

if __name__ == "__main__":
    #app.run(debug=True)
    print('server 已启动')
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)   
    server.serve_forever()