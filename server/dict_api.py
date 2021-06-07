# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 11:24:38 2021

@author: shangfr
"""
from flask_restx import Namespace, Resource, fields
from .nlp_model.words_extract import WordDict

api = Namespace("dict", description="dict api任务")

# 加载用户字典
WordDict.load_userdict()

userdict = api.model(
    "userdict",
    {
        "id": fields.String(required=False, description="The word's identifier"),
        "word": fields.String(required=True, description="The word's name"),
        "freq": fields.Integer(required=False, description="The word's freq"),
        "tag": fields.String(required=False, description="The word's tag"),
    },
)

WORDS = [{'word': '自治区', 'freq': 5, 'tag': 'n'}]

parser = api.parser()
parser.add_argument('word', type=str, required=True)
parser.add_argument('freq', type=int)
parser.add_argument('tag')


class DictManage(Resource):
    """Shows a list of all words, and lets you POST to add new word"""

    def get(self):
        """查看自定义词典"""
        result = {}
        result['success'] = True
        result['msg'] = "查看自定义词典"
        result['data'] = WordDict.user_dict
        result['add_word'] = WordDict.show_addwords()
        return result

    @api.expect(parser)
    def post(self):
        """增加新词，包含词性"""
        args = parser.parse_args()
        # 添加、删除新词
        if args['freq'] == None:
            freq = 10
        else:
            freq = args['freq']
        uword = [{'word': args['word'], 'freq': freq, 'tag': args['tag']}]
        WordDict.add_userdict(uword)
        return {'task': '增加新词', 'data': uword}, 201

    @api.doc(responses={204: "Word deleted"})
    @api.expect(parser)
    def delete(self):
        """删除新词"""
        args = parser.parse_args()
        uword = [{'word': args['word']}]
        WordDict.del_userdict(uword)
        return {'task': '删除新词', 'data': uword}, 204


api.add_resource(DictManage, '')
