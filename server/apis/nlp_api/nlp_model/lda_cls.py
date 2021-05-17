# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 10:34:19 2021

@author: shangfr
"""
import paddlehub as hub

class EtypeRec(object):
    '事件类别识别模型'

    def __init__(self):
        pass
    
    @classmethod
    def load_model(cls):
    
        cls.lda_webpage = hub.Module(name="lda_webpage")
        print('模型加载完成')
        
    @staticmethod 
    def etype_sim(sentence):
        '''
    
        Parameters
        ----------
        sentence : text or text list
             事件类型匹配模型是以无监督学习的方式对上报事件的隐含语义结构进行聚类的统计模型，该模型主要采用LDA算法。LDA根据对词的共现信息的分析，拟合出词-事件-类型的分布，从而将词、文本映射到一个语义空间中。通过计算上报文本与事件类型之间的相似度进行智能匹配。
    
        Returns
        -------
        event type.
    
        '''

        sim = 0
        result = 'A-21-01'
        type_list = [{'Name': '矛盾调解', 
                      'typeCode': 'A-21-01', 
                      'Words': ['矛盾调解','矛盾','调解','吵闹','口角','喝多',
                                '堵塞','打架','挑衅','剐','蹭','发生','交通']},
                     {'Name': '邻里纠纷', 
                      'typeCode': 'A-21-02', 
                      'Words': ['邻里纠纷','邻居','邻里','垃圾','垃圾桶','停车',
                                '乱','下水道','太吵','影响','强行','堵塞','堆放',
                                '高空','违章建筑','漏水','装修','电梯','费用',
                                '大型犬','坠物','擅自','楼上楼下','水电费','装修','阻止']},
                     {'Name': '劳资纠纷', 
                      'typeCode': 'A-21-03', 
                      'Words': ['劳资纠纷','合同','拒绝','赔偿','工资','公司','拖欠工资']}
                     ]
        

        for t in type_list:
            r = EtypeRec.lda_webpage.cal_query_doc_similarity(t['Name'],sentence)
            if r > sim:
                sim = r
                result = t['typeCode']
            else:
                pass
        

        '''
        #关键词匹配算法
        sentence = re.sub(r'[^\u4e00-\u9fa5^a-z^A-Z^0-9]', '', sentence)
        content_l = jieba.lcut(sentence)
           
        for ty in type_list:
            ins = [v for v in content_l if v in ty['Words']]
            if len(ins) > sim:
                sim = len(ins)
                result = ty['typeCode']
            else:
                pass
        '''    
        return {'typeCode':result,'value':str(round(sim,3))}

if __name__ == "__main__":
    
    EtypeRec.load_model()
    test_text = '今天上班路过体育南大街的时候发现路灯坏了很长时间了,政府应该早点派人修一下'
    results = EtypeRec.etype_sim(test_text)
    print(results)
