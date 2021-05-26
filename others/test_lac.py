# -*- coding: utf-8 -*-
"""
Created on Wed May 19 18:07:27 2021

@author: shangfr
"""

from LAC import LAC

# 装载分词模型
lac = LAC(mode='seg')
# 装载LAC模型
lac = LAC(mode='lac')
# 装载词语重要性模型
lac = LAC(mode='rank')

# 装载干预词典, sep参数表示词典文件采用的分隔符，为None时默认使用空格或制表符'\t'
lac.load_customization('custom.txt', sep=None)

lac.add_word("中国梦/n")
lac.add_word("")
# 单个样本输入，输入为Unicode编码的字符串
text = u"LAC是个优秀的分词工具，中国爆发了新冠病毒"
seg_result = lac.run(text)

# 批量样本输入, 输入为多个句子组成的list，平均速率会更快
texts = [u"LAC是个优秀的分词工具", u"百度是一家高科技公司"]
seg_result = lac.run(texts)


