# -*- coding: utf-8 -*-
"""
Created on Wed May 19 10:07:18 2021

@author: shangfr
"""

from functools import reduce
import operator
from whoosh import scoring
import jieba
from whoosh.sorting import FieldFacet
from whoosh.index import open_dir
from whoosh.qparser import QueryParser, MultifieldParser
import os
from whoosh.index import create_in
from whoosh.fields import ID, TEXT, Schema
from jieba.analyse import ChineseAnalyzer
import json

# 解析test.csv文件
with open('others/test.csv', 'r', encoding='utf-8') as f:
    texts = [_.strip().split(',')
             for _ in f.readlines() if len(_.strip().split(',')) == 5]


# 创建schema, stored为True表示能够被检索
schema = Schema(code=ID(stored=True),
                category=TEXT(stored=True, analyzer=ChineseAnalyzer()),
                sub_class=TEXT(stored=True, analyzer=ChineseAnalyzer()),
                level=ID(stored=True),
                department=ID(stored=True)
                )

# 存储schema信息至indexdir目录
indexdir = 'others/indexdir/'
if not os.path.exists(indexdir):
    os.mkdir(indexdir)
ix = create_in(indexdir, schema)

# 按照schema定义信息，增加需要建立索引的文档，将texts内容写入
writer = ix.writer()
for i in range(1, len(texts)):
    code, category, sub_class, level, department = texts[i]
    writer.add_document(code=code, category=category, sub_class=sub_class,
                        level=level, department=department)
writer.commit()


# 创建一个检索器
searcher = ix.searcher()

# 检索content中出现'明月'的文档
results = searcher.find("category", "城市")
print('一共发现%d份文档。' % len(results))
for i in range(min(10, len(results))):
    print(json.dumps(results[i].fields(), ensure_ascii=False))


# 以上为建立索引的过程
new_list = []
index = open_dir('indexdir/')  # 读取建立好的索引
inputstring = "中国and(国际or物流)and开幕"
inputstring = "中国and(国际or物流)and开幕"

seg_list = jieba.cut_for_search("路过体育南大街发现很多建筑垃圾，满大街都是")  # 搜索引擎模式
inputstring = (" OR ".join(seg_list))
with index.searcher(weighting=scoring.TF_IDF()) as searcher:
    parser = QueryParser("sub_class", index.schema)
    #parser = MultifieldParser(["category", "sub_class"], index.schema)
    #myquery = parser.parse("广告牌 OR 破损")
    myquery = parser.parse(inputstring)
    # facet = FieldFacet("code", reverse=True)  # 按序排列搜索结果
    # limit为搜索结果的限制，默认为10，详见博客开头的官方文档
    #results = searcher.search(myquery, limit=5, sortedby=facet)
    results = searcher.search(myquery, limit=5, scored=True)
    print('一共发现%d份文档。' % len(results))
    for result in results:
        print(result.fields(), result.score)
        new_list.append(result.fields())


with open('chinese_dictionary/AitSimwords.txt', 'r', encoding='utf-8') as f:
    sim_words_01 = f.readlines()

with open('chinese_dictionary/dict_synonym.txt', 'r', encoding='utf-8') as f:
    sim_words_02 = f.readlines()
 
sim_words_01_t = [words.split() for words in sim_words_01]
sim_words_02_t = [words.split() for words in sim_words_02]

for words_l in sim_words_02_t:
    del(words_l[0])

sim_words_01_t = [' '.join(words) for words in sim_words_01_t]
sim_words_02_t = [' '.join(words) for words in sim_words_02_t]

with open('chinese_dictionary/sim_words2.txt', 'w', encoding='utf-8') as f:
    for line in sim_words_01_t+sim_words_02_t:
        f.write(line+'\n')


    

'''
t = len(sim_words_01_t)
for a in sim_words_01_t:
    for b in sim_words_02_t:
        intersection = [v for v in a if v in b]
        if len(intersection) > 0:
            b.extend([v for v in a])
    t = t-1
    if t % 1000 == 0:
        print(t)
'''

sim_words = reduce(operator.add, sim_words_01_t)




import json


json_file_path = 'chinese_dictionary/sim_words.json'
json_file = open(json_file_path, mode='w', encoding='utf-8')
 
save_json_content = []
for words_l in sim_words_01_t:
    result_json = {
        "words": words_l,
        "source": 1}
    save_json_content.append(result_json)

for words_l in sim_words_02_t:
    result_json = {
        "words": words_l,
        "source": 2}
    save_json_content.append(result_json)
# json.dump(save_json_content, json_file, indent=4)  
json.dump({'data':save_json_content}, json_file, ensure_ascii=False, indent=4) # 保存中文


with open(json_file_path, 'r', encoding='UTF-8') as load_f:
    sim_words_dict = json.load(load_f)







# 存储schema信息至indexdir目录
indexdir = 'others/indexdir/'
if not os.path.exists(indexdir):
    os.mkdir(indexdir)
ix = create_in(indexdir, schema)

# 按照schema定义信息，增加需要建立索引的文档，将texts内容写入
writer = ix.writer()
for i in range(1, len(texts)):
    code, category, sub_class, level, department = texts[i]
    writer.add_document(code=code, category=category, sub_class=sub_class,
                        level=level, department=department)
writer.commit()






