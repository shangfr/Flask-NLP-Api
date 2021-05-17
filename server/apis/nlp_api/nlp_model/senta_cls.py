# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 10:34:19 2021

@author: shangfr
"""
import paddlehub as hub

class Sentiment(object):
    '情绪识别模型'

    def __init__(self):
        pass
    
    @classmethod
    def load_model(cls):
    
        cls.senta = hub.Module(name="senta_bilstm")
        print('模型加载完成')
        
    @staticmethod 
    def senta_probs(sentence):
        '''
    
        Parameters
        ----------
        sentence : text or text list
            DESCRIPTION.
    
        Returns
        -------
        negative_probs.
    
        '''
        if isinstance(sentence, list):
            pass     
        else:
           sentence = [sentence]
        results = Sentiment.senta.sentiment_classify(texts=sentence)
        return [result['negative_probs'] for result in results]

if __name__ == "__main__":
    
    Sentiment.load_model()
    test_text = "这部电影真他妈的很差劲"
    results = Sentiment.senta_probs(test_text)
    print(results)

