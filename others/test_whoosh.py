# -*- coding: utf-8 -*-
"""
Created on Wed May 19 10:07:18 2021

@author: shangfr
"""

from whoosh.sorting import FieldFacet
from whoosh.index import open_dir
from whoosh.qparser import QueryParser,MultifieldParser
import os
from whoosh.index import create_in
from whoosh.fields import *
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
index = open_dir(indexdir)  # 读取建立好的索引
with index.searcher() as searcher:
    #parser = QueryParser("sub_class", index.schema)
    parser = MultifieldParser(["category","sub_class"], index.schema)
    myquery = parser.parse("广告牌 OR 破损")
    facet = FieldFacet("code", reverse=True)  # 按序排列搜索结果
    # limit为搜索结果的限制，默认为10，详见博客开头的官方文档
    results = searcher.search(myquery, limit=10, sortedby=facet)
    print('一共发现%d份文档。' % len(results))
    for result in results:
        print(result.fields())
        new_list.append(result.fields())
