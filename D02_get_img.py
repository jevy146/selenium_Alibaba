# -*- coding: utf-8 -*-
# @Time    : 2020/6/17 14:41
# @Author  : 结尾！！
# @FileName: D02_get_img.py
# @Software: PyCharm


import requests

def open_requests(img, img_name):
    img_url ='https:'+ img
    res=requests.get(img_url)
    with open(f"./downloads_picture/{img_name}",'wb') as fn:
        fn.write(res.content)

import pandas as pd
df1=pd.read_csv('./alibaba_com_img.csv',)
for img in df1["img"]:
    if pd.isnull(img):
        pass
    else:
        if '@sc01' in img:
            img_name=img[24:]
            print(img,img_name)
            open_requests(img, img_name)