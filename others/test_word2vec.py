# -*- coding: utf-8 -*-
"""
Created on Wed May 19 14:46:47 2021

@author: shangfr
"""

from paddlehub.reader.tokenization import load_vocab
import paddlehub as hub
from paddlenlp.embeddings import TokenEmbedding

wordemb = TokenEmbedding("w2v.baidu_encyclopedia.target.word-word.dim300")
print(wordemb.cosine_sim("苹果", "手机"))
test_token_embedding = wordemb.search("中国梦")


simnet_model = hub.Module(name="simnet_bow")
results = simnet_model.similarity([['跑步跑步跑步跑步跑步'], ["哎哎哎哎哎哎"]])

vocab = load_vocab(simnet_model.get_vocab_path())
# 这是把 中文词语 转化为 词表 中对应 ID 的函数


def convert_tokens_to_ids(vocab, text):  # 输入为词表，和要转化的 text
    wids = []  # 初始化一个空的集合，用于存放输出
    tokens = text.split(" ")  # 将传入的 text 用 空格 做分割，变成 词语字符串 的列表
    for token in tokens:  # 每次从列表里取出一个 词语
        wid = vocab.get(token, None)
        if not wid:
            wid = vocab["unknown"]
        wids.append(wid)
    return wids


convert_tokens_to_ids(vocab, "苹果")


lda_webpage = hub.Module(name="lda_webpage")
lda_webpage.cal_query_doc_similarity(
    query='电话', document='苹果手机是苹果公司发布搭载iOS操作系统的系列手机。')
lda_webpage.cal_doc_keywords_similarity(
    '包含主题分布下各个主题ID和对应的概率分布。其中，list的基本元素为dict，dict的key为主题ID，value为各个主题ID对应的概率。')
