# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 10:34:19 2021

@author: shangfr
"""
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
import json
import jieba
import pandas as pd
import paddlehub as hub

with open("model/data/event_category.json", 'r', encoding='UTF-8') as load_f:
    event_type_dict = json.load(load_f)

TagList = event_type_dict['data']


def search_word(word, indexdir="query"):

    ix = open_dir(indexdir)
    new_list = []

    with ix.searcher() as searcher:
        query = QueryParser("keywords", ix.schema).parse(word)
        results = searcher.search(query, limit=None)
        for result in results:
            new_list.append(result.fields())
        

    if len(new_list) == 0:
        with ix.searcher() as searcher:
            query = QueryParser("simwords", ix.schema).parse(word)
            results = searcher.search(query, limit=None)
            for result in results:
                new_list.append(result.fields())


                
    print('一共匹配到%d个事件类型。' % len(new_list))
    return new_list


class EventCls(object):
    '事件分类模型'

    def __init__(self):
        pass

    @classmethod
    def load_model(cls):

        cls.simnet_model = hub.Module(name="simnet_bow")
        print('模型加载完成')

    @staticmethod
    def event_sim(sentence):
        '''

        Parameters
        ----------
        sentence : text or text list
            DESCRIPTION.

        Returns
        -------
        event list.

        '''
        test_text_2 = [''.join(t['words']) for t in TagList]
        test_text_1 = [sentence]*len(TagList)
        test_text = [test_text_1, test_text_2]
        results = EventCls.simnet_model.similarity(texts=test_text)
        df = pd.DataFrame(results)
        df['category'] = [t['category'] for t in TagList]
        df.sort_values(by='similarity', ascending=False, inplace=True)
        df = df.loc[df['similarity'] > 0.5, ['category', 'similarity']]

        return df.to_dict(orient='records')

    @staticmethod
    def event_search(sentence):
        '''

        Parameters
        ----------
        sentence : text or text list
            DESCRIPTION.

        Returns
        -------
        event list.

        '''
        seg_list = jieba.cut_for_search(sentence)  # 搜索引擎模式
        inputstring = (" OR ".join(seg_list))

        result = search_word(inputstring)

        return result


if __name__ == "__main__":

    EventCls.load_model()
    test_text = '路过体育南大街发现满大街都是建筑垃圾，希望相关部门处理一下。'
    results = EventCls.event_sim(test_text)
    print(results)
    df = pd.DataFrame(results)
    
    results2 = EventCls.event_search(test_text)
    df2 = pd.DataFrame(results2)
