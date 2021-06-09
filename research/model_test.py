# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 17:25:03 2021

@author: shangfr
"""

from whoosh.qparser import QueryParser
from whoosh.fields import *
from whoosh.index import open_dir, create_in
import os
import pandas as pd
import jieba
import cnsyn

event_df = pd.read_excel('resources/report_event.xlsx', index_col=0)
event_df.reset_index(inplace=True, drop=True)

event_df['keywords'] = event_df['基本分类'].apply(jieba.lcut_for_search)

from functools import reduce
import operator
sim_words = reduce(operator.add, event_df['keywords'])

df = pd.Series(sim_words).value_counts()

def stop_words(lst):
    WORDS = ['或', '和', '及', '类', '管理', '相关','人员','其它',
             '与','而','W','已','，',
             '问题', '（', '的', '等', '）', '、', '“', '”', '《', '》']
    return [x for x in lst if x not in WORDS]


event_df['keywords'] = event_df['keywords'].apply(stop_words)


def sim_words(lst):
    import operator
    from functools import reduce

    lm = reduce(operator.add, map(cnsyn.search, lst))
    
    if len(lm) == 0 or len(lm) > 38:
        lm = lst
    return lm


event_df['simwords'] = event_df['keywords'].apply(sim_words)

#event_df['allwords'] = event_df['keywords']+event_df['simwords']
#event_df['allwords'] = event_df['allwords'].apply(set)

event_df.to_csv('resources/report_event.csv', encoding="utf_8_sig")
# 创建schema, stored为True表示该字段内容能够在检索结果中显示

event_df = pd.read_csv('resources/report_event.csv',index_col=0)

event_df['keywords'] = event_df['keywords'].apply(eval)
event_df['simwords'] = event_df['simwords'].apply(eval)

#event_df[ '基本分类'].value_counts()  #drop_duplicates()

#df = event_df.describe()

def build_index(data, indexdir="query"):
    schema = Schema(wid=ID(stored=True),  
                    category=TEXT(stored=True),classes=TEXT(stored=True),
                    level=ID(stored=True), department=ID(stored=False), 
                    keywords=KEYWORD(stored=False),
                    simwords=KEYWORD(stored=False))
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
    ix = create_in(indexdir, schema)
    writer = ix.writer()

    for i, row in data.iterrows():
        writer.add_document(
            wid=str(i), category=row[0],classes=row[1], 
            level=row[2],department=row[3],
            keywords=row[4],simwords=row[5])
    writer.commit()
    return "Step One:  索引已经构建完成--------------------- "


build_index(event_df)

def search_word(word, indexdir="query"):

    ix = open_dir(indexdir)

    with ix.searcher() as searcher:
        query = QueryParser("keywords", ix.schema).parse(word)
        results = searcher.search(query, limit=None)
        print("Step Two: 搜索已经完成--------------------- ")
        print('一共发现%d份文档。' % len(results))

        for result in results:
            print(result.fields())
            
search_word('金融')

seg_list = jieba.cut_for_search("最近发现这个小区有传销人员，请注意调查")  # 搜索引擎模式
inputstring = (" OR ".join(seg_list))

search_word(inputstring)

jieba.add_word("师风")
jieba.lcut("私搭乱建")
jieba.lcut_for_search("私搭乱建")
