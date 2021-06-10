# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 14:23:29 2021

@author: shangfr
"""

import sys, fitz
import os
import datetime
 
def pyMuPDF_fitz(pdfPath, imagePath):
    startTime_pdf2img = datetime.datetime.now()#开始时间
    
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=72
        zoom_x = 2 #(1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 2
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        
        if not os.path.exists(imagePath):#判断存放图片的文件夹是否存在
            os.makedirs(imagePath) # 若图片文件夹不存在就创建
        
        pix.writePNG(imagePath+'/'+'images_%s.jpg' % pg)#将图片写入指定的文件夹内
        try:
            pic2word(imagePath+'/'+'images_%s.jpg' % pg)
        except:
            pass
    endTime_pdf2img = datetime.datetime.now()#结束时间
    print('pdf2img时间=',(endTime_pdf2img - startTime_pdf2img).seconds)
 
def pyMuPDF2_fitz(pdfPath, imagePath):
    pdfDoc = fitz.open(pdfPath) # open document
    for pg in range(pdfDoc.pageCount): # iterate through the pages
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像
        # 此处若是不做设置，默认图片大小为：792X612, dpi=72
        zoom_x = 1.33333333 #(1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 1.33333333
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate) # 缩放系数1.3在每个维度  .preRotate(rotate)是执行一个旋转
        rect = page.rect                         # 页面大小
        mp = rect.tl + (rect.bl - (0,75/zoom_x)) # 矩形区域    56=75/1.3333
        clip = fitz.Rect(mp, rect.br)            # 想要截取的区域
        pix = page.getPixmap(matrix=mat, alpha=False, clip=clip) # 将页面转换为图像
        if not os.path.exists(imagePath):
            os.makedirs(imagePath)
        pix.writePNG(imagePath+'/'+'psReport_%s.jpg' % pg+2)# store image as a PNG
 
if __name__ == "__main__":
    pdfPath = 'XX区问题投诉案（事）件分级（ABCD）分类清单汇总.pdf'
    imagePath = 'image'
    pyMuPDF_fitz(pdfPath, imagePath)#只是转换图片
    #pyMuPDF2_fitz(pdfPath, imagePath)#指定想要的区域转换成图片


import paddlehub as hub
import cv2

ocr = hub.Module(name="chinese_ocr_db_crnn_mobile")
text_detector = hub.Module(name="chinese_text_detection_db_server")
result = ocr.recognize_text(images=[cv2.imread('image/images_3.jpg')],visualization=True)
result = text_detector.detect_text(images=[cv2.imread('image/images_3.jpg')],visualization=True)

ocr = hub.Module(name="chinese_ocr_db_crnn_server")
result = text_detector.detect_text(images=[cv2.imread('image/images_3.jpg')],visualization=True)

result = ocr.recognize_text(images=[cv2.imread('image/images_3.jpg')],visualization=True)

import pandas as pd
df = pd.DataFrame(result[0]['data'])



# encoding:utf-8

import requests
import base64
import sys
import json
import pandas as pd

'''
通用文字识别（高精度版）
'''
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus
# 防止https证书校验不正确
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = '0PlMroCqwXTgOPAtQPu0iph1'

SECRET_KEY = 'XT1hzB9TRmoT2UAEcW7mIuUC9jNoiwhL'

"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'


"""
    获取token
"""
IS_PY3 = True
def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    if (IS_PY3):
        result_str = result_str.decode()


    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print ('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print ('please overwrite the correct API_KEY and SECRET_KEY')
        exit()

# 获取access token
token = fetch_token()
request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate"
request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
#request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/form"
# 二进制方式打开图片文件

def pic2word(img_path):
    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())
    
    params = {"image":img}
    access_token = token
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate"
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print (response.json())
    
    df = response.json()['words_result']
    
    df = pd.DataFrame(df)
    df_location = pd.DataFrame(df.location.tolist())
    df_location['words'] = df['words']
    df_location.sort_values(by=['top', 'left'], inplace=True)
    df_location['top_v'] = df_location["top"].shift(-1) - df_location["top"]
    h = df_location.shape[0] 
    with open('text.txt', mode='a', encoding="utf-8") as filename:
        
        for i in range(h):
            j = df_location.iloc[i,5]
            word = df_location.iloc[i,4]
            filename.write(word)
            filename.write('       ') # 换行
            if j > 3:
                filename.write('\n') # 换行
for pg in range(2,35):            
    pic2word('image'+'/'+'images_%s.jpg' % pg)     
            
            
            

            