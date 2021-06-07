
# flask_nlp_api
nlp flask restful api for Chinese text

> 通过jieba进行分词、关键词提取的RestX API框架，支持数据库自定义字典，支持动态调整user dict

> 通过paddlehub的开源模型simnet，对事件文本进行分类。

| 算法模型类别	| 模型描述| 
| :----: | :----- |
| 分词模块	| 对中文文本进行中文分词，支持自定义名词的动态调整、支持敏感词过滤；对分词结果进行词频统计。| 
| 关键词提取模块	| 对中文文本进行关键词提取，支持热词（自定义名词）的匹配与权重值、词性设置，输出指定数量的热词词频列表，用于词云展示。| 
| 事件类型匹配模型	| 事件类型匹配模型是以无监督学习的方式对上报事件的隐含语义结构进行聚类的统计模型，该模型主要采用LDA算法。LDA根据对词的共现信息的分析，拟合出词-事件-类型的分布，从而将词、文本映射到一个语义空间中。通过计算上报文本与事件类型之间的相似度进行智能匹配。| 

文件解释
-----------

样例包括:

* README.md - 本文件
* Jenkinsfile - 用以自动构建和测试的脚本
* Dockerfile - 用以自动构建 Docker 镜像的脚本
* requirements.txt - 依赖包文件 pip freeze > requirements_all.txt   pipreqs ./ --encoding=utf-8
* manage.py - 主 Flask 服务器端源代码
* nlp.db - [数据库文件](server/apis/nlp_api/nlp_model/README.md)
* server - RestX Restful Api 带 swagger log


        +--server
        | +--api.py
        | +--apis
        | | +--nlp_api
        | | | +--dict_api.py
        | | | +--nlp_model
        | | | | +--data
        | | | | | +--event_category.json
        | | | | +--extra_dict
        | | | | | +--stop_words.txt
        | | | | +--lda_cls.py
        | | | | +--README.md
        | | | | +--simnet_cls.py
        | | | | +--test_model.py
        | | | | +--words_extract.py
        | | | | +--__init__.py
        | | | +--text_api.py
        | | | +--__init__.py
        | +--config.py
        | +--mylog.py
        | +--static
        | +--templates
        | +--__init__.py
        +--utils
        | +--db.py
        | +--nlp_db.py


快速开始
---------------

如下这些引导，假定你想在自己的电脑上开发本项目。

1. 安装依赖

        $ pip install -r requirements.txt


2. 启动服务器

        $ python manage.py run

'''
gunicorn -k gevent -c gun.conf 项目文件:项目名
'''

3. 打开 http://127.0.0.1:5000/nlp/v1/

Swagger Web
---------------

post /text
segword-分词；keyword-关键词提取；cls-事件分类；

![avatar](/resources/swagger_ui.png)


curl test
---------------

curl http://127.0.0.1:5000/nlp/v1/text

curl http://127.0.0.1:5000/nlp/v1/text -d "sentence=今天上班路过体育南大街的时候发现路灯坏了很长时间了,应该早点派人修一下" -X POST


