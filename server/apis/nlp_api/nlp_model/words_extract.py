# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 10:49:00 2021

@author: shangfr
"""
import jieba
import jieba.analyse
import re
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
jieba.setLogLevel(40)


class WordDict(object):
    '''
    分词字典管理：jieba只支持读取自定义词典txt文件，改成支持读取数据库；
    user_dict：  初始化加载的用户词典 list
    '''
    user_dict = []

    def __init__(self):
        pass

    @classmethod
    def load_userdict(cls, url='sqlite:///nlp.db', table='user_dict'):
        '''
        Parameters
        ----------
        cls : TYPE
            通过类方法，加载数据库，读取user_dict.
        url : TYPE, optional
            DESCRIPTION. The default is 'sqlite:///nlp.db'.
        table : TYPE, optional
            DESCRIPTION. The default is 'user_dict'.

        Returns
        -------
        None.

        '''
        cls.engine = create_engine(url)
        cls.table = table
        user_word = pd.read_sql(cls.table, cls.engine)
        cls.user_dict = user_word.to_dict('records')
        # 载入词典，需要重启
        jieba.initialize()
        for row in cls.user_dict:
            jieba.add_word(word=row['word'], freq=row['freq'], tag=row['tag'])

    @staticmethod
    def show_addwords():
        '''
        Returns
        -------
        user_word_list : TYPE
            用户新增字典.

        '''
        user_word_df = pd.read_sql(WordDict.table, WordDict.engine)
        user_word_list = user_word_df.to_dict('records')
        for word in WordDict.user_dict:
            if word in user_word_list:
                user_word_list.remove(word)
        return user_word_list

    @staticmethod
    def add_userdict(uword):
        if isinstance(uword, list):
            with WordDict.engine.connect() as conn:
                conn.execute(
                    text(
                        "INSERT INTO user_dict (word, freq, tag) VALUES (:word, :freq, :tag)"),
                    uword
                )

            for row in uword:
                jieba.add_word(word=row['word'],
                               freq=row['freq'], tag=row['tag'])

        else:
            pass

    @staticmethod
    def del_userdict(uword):
        if isinstance(uword, list):
            with WordDict.engine.connect() as conn:
                conn.execute(
                    text(
                        "DELETE FROM user_dict WHERE word =:word"),
                    uword
                )
            for row in uword:
                jieba.del_word(word=row['word'])
        else:
            pass

class WordExtract(object):

    '分词、关键词提取'
    stop_word_l = []

    def __init__(self):
        pass

    # 对句子进行中文分词
    @staticmethod
    def seg_depart(sentence):
        '''
        Parameters
        ----------
        sentence : TYPE
            DESCRIPTION.

        Returns
        -------
        dict
            DESCRIPTION.

        '''
        # 对文档中的每一行进行中文分词
        sentence = re.sub(r'[^\u4e00-\u9fa5^a-z^A-Z^0-9]', '', sentence)
        sentence_depart = jieba.lcut(sentence)
        all_words = [
            word for word in sentence_depart if word not in WordExtract.stop_word_l]

        return {'segwords': all_words}

    # 对上报事件进行实体识别、类型判断、已经办事地点匹配。
    @staticmethod
    def key_word(sentence):
        '''

        Parameters
        ----------
        sentence : TYPE
            DESCRIPTION.
        length : TYPE, optional
            DESCRIPTION. The default is 20.

        Returns
        -------
        dict
            DESCRIPTION.

        '''
        sentence = re.sub(r'[^\u4e00-\u9fa5^a-z^A-Z^0-9]', '', sentence)
        all_pos = ['PER', 'LOC', 'ORG', 'TIME',
                   'USER', 'ns', 'n', 'vn', 'v', 'nr']
        keywords = jieba.analyse.extract_tags(
            sentence, topK=5, allowPOS=all_pos, withWeight=False, withFlag=True)

        keywords = dict(keywords)

        return {'keywords': keywords}



if __name__ == "__main__":
    # 加载用户字典
    WordDict.load_userdict()
    WordDict.user_dict
    uword = [{'word': '自治区', 'freq': 5, 'tag': 'n'}]
    WordDict.add_userdict(uword)
    WordDict.show_addwords()
    WordDict.del_userdict(uword)

    
    
