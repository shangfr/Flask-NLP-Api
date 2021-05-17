# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 11:24:38 2021

@author: shangfr
"""
from flask_restx import Namespace, Resource, fields
from .nlp_model.words_extract import WordDict

api = Namespace("dict", description="dict api任务")

dict_manage = WordDict()

userdict = api.model(
    "userdict",
    {
        "id": fields.String(required=True, description="The words' identifier"),
        "name": fields.String(required=True, description="The word name"),
    },
)

WORDS = [
    {"id": 1, "name": "Felix"},
]

parser = api.parser()
parser.add_argument('word', type=str, required=True)
parser.add_argument('tag')


class DictManage(Resource):
    """Shows a list of all words, and lets you POST to add new word"""

    def get(self):
        """查看自定义词典"""
        result = {}
        result['userdict'] = dict_manage.get_userdict()
        return result

    @api.expect(parser)
    def post(self):
        """增加新词，包含词性"""
        args = parser.parse_args()
        uword = args['word']
        tag = args['tag']
        dict_manage.add_userdict(uword, tag)
        return {'task': '增加新词', 'word': uword}, 201

    @api.doc(responses={204: "Word deleted"})
    @api.expect(parser)
    def delete(self):
        """删除新词"""
        args = parser.parse_args()
        uword = args['word']
        dict_manage.del_userdict(uword)
        return {'task': '删除新词', 'word': uword}, 204


api.add_resource(DictManage, '/')
