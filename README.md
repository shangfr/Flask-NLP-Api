
# flask_nlp_api
nlp flask restful api for Chinese text
[TOC]

| 算法模型类别	| 模型描述| 
| :----: | :----- |
| 分词模块	| 对中文文本进行中文分词，支持自定义名词的动态调整、支持敏感词过滤；对分词结果进行词频统计。| 
| 关键词提取模块	| 对中文文本进行关键词提取，支持热词（自定义名词）的匹配与权重值设置，输出指定数量的热词词频列表，用于词云展示。| 
| 情感倾向分析模型	| 针对带有主观描述的中文文本，可自动判断该文本的情感极性类别并给出相应的置信度，能够帮助政府分析热点话题和危机舆情监控，为政府提供有利的决策支持。该模型基于一个双向LSTM结构，输出消极情感倾向度的分值：0-10分。| 
| 事件类型匹配模型	| 事件类型匹配模型是以无监督学习的方式对上报事件的隐含语义结构进行聚类的统计模型，该模型主要采用LDA算法。LDA根据对词的共现信息的分析，拟合出词-事件-类型的分布，从而将词、文本映射到一个语义空间中。通过计算上报文本与事件类型之间的相似度进行智能匹配。| 

文件解释
-----------

样例包括:

* README.md - 本文件
* Jenkinsfile - 用以自动构建和测试的脚本
* Dockerfile - 用以自动构建 Docker 镜像的脚本
* requirements.txt - 依赖包文件 pip freeze > requirements_all.txt   pipreqs ./ --encoding=utf-8
* app.py - 主 Flask 服务器端源代码
* api.py - Restful Api
* restx_api.py - RestX Restful Api 带 swagger log

快速开始
---------------

如下这些引导，假定你想在自己的电脑上开发本项目。

1. 安装依赖

        $ pip install -r requirements.txt


2. 启动服务器

        $ python restx_api.py

3. 打开 http://0.0.0.0:5000/ .

Swagger Web
---------------

![avatar](/resources/pic.png)

curl test
---------------

curl http://127.0.0.1:5000/nlp/v1/report

curl http://127.0.0.1:5000/nlp/v1/report -d "sentence=今天上班路过体育南大街的时候发现路灯坏了很长时间了,政.应该早点派人修一下" -X POST


