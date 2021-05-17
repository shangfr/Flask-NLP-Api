# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 10:49:00 2021

@author: shangfr
"""
import jieba
import jieba.analyse
import re
from .senta_cls import Sentiment
from .lda_cls import EtypeRec


# 载入词典

user_word_l = ['']
stop_word_l = ['']

jieba.setLogLevel(40)

# Sentiment.load_model()
# EtypeRec.load_model()
# jieba.initialize()


class WordDict(object):
    '''
    分词字典管理：
    user_word_l：  初始化用户词典 list
    get_userdict: 增加新词 fun
    del_userdict: 删除新词 fun
    '''
    word_l = user_word_l

    def __init__(self):
        '''

        Parameters
        ----------
        word_l : list
            初始化用户词典.

        Returns
        -------
        None.

        '''
        # self.init_model()
        self.add_userdict(self.word_l)

    def get_userdict(self):
        return self.word_l

    def add_userdict(self, uword, tag='USER'):
        if isinstance(uword, list):
            for w in uword:
                jieba.add_word(w, tag=tag)
        else:
            jieba.add_word(uword, tag=tag)
            self.word_l.append(uword)

    def del_userdict(self, uword):
        if isinstance(uword, list):
            for w in uword:
                jieba.del_word(w)
        else:
            jieba.del_word(uword)
            self.word_l.remove(uword)


class WordExtract(object):

    '分词、关键词提取、情绪倾向识别'

    def __init__(self):
        pass

    # 对句子进行中文分词
    @staticmethod
    def seg_depart(sentence, senta=True):
        '''
        Parameters
        ----------
        sentence : TYPE
            DESCRIPTION.
        senta : TYPE, optional
            DESCRIPTION. The default is True.
        keywords : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        dict
            DESCRIPTION.

        '''
        # 对文档中的每一行进行中文分词
        sentence = re.sub(r'[^\u4e00-\u9fa5^a-z^A-Z^0-9]', '', sentence)
        sentence_depart = jieba.lcut(sentence)
        all_words = [
            word for word in sentence_depart if word not in stop_word_l]
        if senta:
            senta_values = Sentiment.senta_probs(sentence)
        else:
            senta_values = [0]

        return {'segwords': all_words, 'sentavalue': round(10*senta_values[0], 2)}

    # 对上报事件进行实体识别、类型判断。
    @staticmethod
    def key_word(sentence, etype_rec=True):
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

        if etype_rec:
            etype = EtypeRec.etype_sim(sentence)
        else:
            etype = ''

        return {'keywords': dict(keywords), 'etype': etype}


if __name__ == "__main__":
    #dict_manage = WordDict()
    test_text = "今天上班路过体育南大街的时候发现路灯坏了很长时间了,政府应该早点派人修一下。"
    result = WordExtract.seg_depart(test_text, senta=False)
    print(result)

    WordDict().add_userdict('体育南大街', tag='LOC')
    result = WordExtract.key_word(test_text, etype_rec=False)
    print(result)
