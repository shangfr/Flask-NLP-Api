# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 11:24:38 2021

@author: shangfr
"""
from flask_restx import Namespace, Resource, fields
from .nlp_model.words_extract import WordExtract

api = Namespace("text", description="text api任务")

Todos = {
    'dict': {'task': '词典管理: get-查询词典；post-word、tag增加新词；delete-word删除新词；'},
    'report': {'task': '我要报: post-sentence,return-关键词、事件类型、地点、所在网格'},
    'text': {'task': '文本分析: post-sentence,return-分词、负向情绪值'}
}

todo = api.model(
    "Todo", {"task": fields.String(
        required=True, description="The task details")}
)

listed_todo = api.model(
    "ListedTodo",
    {
        "id": fields.String(required=True, description="The todo ID"),
        "todo": fields.Nested(todo, description="The Todo"),
    },
)

parser1 = api.parser()
parser1.add_argument('sentence', type=str, required=True)


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in Todos:
        api.abort(404, "Todo {} doesn't exist".format(todo_id))

# Todo
# shows a single todo item and lets you delete a todo item

class TextAnalyse(Resource):
    @api.marshal_with(todo, code=201)
    def get(self):
        """查看事件分词与情绪识别"""
        return {'task': Todos.get('text')}

    @api.expect(parser1)
    def post(self):
        """进行事件分词与情绪识别"""
        args = parser1.parse_args()
        sentence = args['sentence']
        words = WordExtract.seg_depart(sentence)
        return {'task': '事件分词与情绪识别', 'result': words}, 201


api.add_resource(TextAnalyse, '/')
