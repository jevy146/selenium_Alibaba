# -*- coding: utf-8 -*-
# @Time    : 2020/1/19 10:17
# @Author  : 结尾！！
# @FileName: 4将图片插入到excel中.py
# @Software: PyCharm



from PIL import Image
import os
import xlwings as xw
path='./alibaba_com.xlsx'
app = xw.App(visible=True, add_book=False)
wb = app.books.open(path)

sht = wb.sheets['alibaba_com_img']
img_list=sht.range("D2").expand('down').value
print(len(img_list))


def write_pic(cell,img_name):
    path=f'./downloads_picture/{img_name}'
    print(path)
    fileName = os.path.join(os.getcwd(), path)
    img = Image.open(path).convert("RGB")
    print(img.size)
    w, h = img.size
    x_s = 70  # 设置宽 excel中，我设置了200x200的格式
    y_s = h * x_s / w  #  等比例设置高
    sht.pictures.add(fileName, left=sht.range(cell).left, top=sht.range(cell).top, width=x_s, height=y_s)


if __name__ == '__main__':

    for index,img in enumerate(img_list):
        cell="B"+str(index+2)
        if '@sc01' in img:
            img_name = img[24:]
            try:
                write_pic(cell,img_name)

                print(cell,img_name)
            except:
                print("没有找到这个img_name的图片",img_name)

    wb.save()
    wb.close()
    app.quit()

