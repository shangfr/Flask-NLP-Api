# -*- coding: utf-8 -*-
"""
Created on Fri May 14 11:03:02 2021

@author: shangfr
"""
from words_extract import WordDict

# 加载用户字典
WordDict.load_userdict()
# 查看用户字典
WordDict.user_dict

# 添加、删除新词
uword = [{'word': '自治区', 'freq': 5, 'tag': 'n'}]
WordDict.add_userdict(uword)
WordDict.show_addwords()
WordDict.del_userdict(uword)