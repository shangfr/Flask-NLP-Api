# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 10:34:19 2021

@author: shangfr
"""
import json
import pandas as pd
import paddlehub as hub

with open("server/nlp_model/data/event_category.json", 'r', encoding='UTF-8') as load_f:
    event_type_dict = json.load(load_f)

TagList = event_type_dict['data']

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
        df = df.loc[df['similarity'] > 0.5,['category','similarity']]

        return df.to_dict(orient='records')


if __name__ == "__main__":

    EventCls.load_model()
    test_text = '某小区，张某不顾周围居民的劝阻，把车停在消防通道上，影响居民的生命财产安全，并威胁周围人少管闲事，希望派出所民警能够介入处理。'
    results = EventCls.event_sim(test_text)
    print(results)
    df = pd.DataFrame(results)
