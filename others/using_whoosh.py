# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 17:03:45 2021

@author: shangfr
"""
import os
from whoosh.index import open_dir, create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser

# 创建schema, stored为True表示该字段内容能够在检索结果中显示


def build_index(file_path, indexdir="words_indexdir"):
    schema = Schema(title=TEXT(stored=True), path=ID(
        stored=True), words=KEYWORD(stored=True))
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
    ix = create_in(indexdir, schema)
    writer = ix.writer()
    with open(file_path, 'r', encoding='utf-8') as filereader:
        num = 1
        for row in filereader:
            title_num = str(num) + " line"
            writer.add_document(title=title_num, path=file_path, words=row)
            num += 1
    writer.commit()
    return "Step One:  索引已经构建完成--------------------- "


def search_word(search, indexdir="words_indexdir"):

    ix = open_dir(indexdir)
    word_list = []
    with ix.searcher() as searcher:
        query = QueryParser("words", ix.schema).parse(search)
        results = searcher.search(query, limit=None)
        print("Step Two: 搜索已经完成--------------------- ")
        print('一共发现%d份文档。' % len(results))
        for result in results:
            print(result.fields())
            word_list.append(result.fields())
    return [word['words'].split() for word in word_list]


def search_all(search):

    word_list = []
    indexdir = ["words_indexdir", "words2_indexdir"]
    for index_dir in indexdir:
        ix = open_dir(index_dir)
        with ix.searcher() as searcher:
            query = QueryParser("words", ix.schema).parse(search)
            results = searcher.search(query, limit=None)
            print("Step Two: 搜索已经完成--------------------- ")
            print('一共发现%d份文档。' % len(results))
            for result in results:
                word_list.append(result.fields())
    return [word['words'].split() for word in word_list]


if __name__ == '__main__':

    file_path = 'chinese_dictionary/AitSimwords.txt'
    build_index(file_path)
    build_index('chinese_dictionary/dict_synonym.txt',
                indexdir="words2_indexdir")
    
    build_index('chinese_dictionary/sim_words.txt',
                indexdir="indexdir/simwords")
    
    search_word("垃圾")
    search_word("垃圾", indexdir="indexdir/simwords")
    search_all("垃圾")





    file_name = raw_input(
        "Please input the path of file you want to build index: ")
    step_result = "Something went wrong......."
    try:
        step_result = build_index(file_name)
    finally:
        print(step_result)
    search = raw_input("Please input the word you want to search: ")
    step_result = "Something went wrong......"
    try:
        step_result = search_word(search)
    finally:
        print(step_result)
