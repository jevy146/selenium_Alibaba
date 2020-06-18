# -*- coding: utf-8 -*-
# @Time    : 2020/6/17 14:09
# @Author  : 结尾！！
# @FileName: D01_spider_alibaba_com.py
# @Software: PyCharm


from selenium.webdriver import ChromeOptions
import time
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

#第一步实现对淘宝的登陆
class Chrome_drive():
    def __init__(self):
        ua = UserAgent()

        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)

        NoImage = {"profile.managed_default_content_settings.images": 2}  # 控制 没有图片
        option.add_experimental_option("prefs", NoImage)

        # option.add_argument(f'user-agent={ua.chrome}')  # 增加浏览器头部

        # chrome_options.add_argument(f"--proxy-server=http://{self.ip}")  # 增加IP地址。。

        option.add_argument('--headless')  #无头模式 不弹出浏览器

        self.browser = webdriver.Chrome(options=option)
        self.browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'
        })  #去掉selenium的驱动设置

        self.browser.set_window_size(1200,768)
        self.wait = WebDriverWait(self.browser, 12)

    def get_login(self):
        url='https://www.alibaba.com/'

        self.browser.get(url)
        #self.browser.maximize_window()  # 在这里登陆的中国大陆的邮编
        #这里进行人工登陆。
        time.sleep(2)
        self.browser.refresh()  # 刷新方法 refres
        return


    #获取判断网页文本的内容：
    def index_page(self,page,wd):
        """
        抓取索引页
        :param page: 页码
        """
        print('正在爬取第', page, '页')


        words=wd.replace(' ','_')

        url = f'https://www.alibaba.com/products/{words}.html?IndexArea=product_en&page={page}'
        js1 = f" window.open('{url}')"  # 执行打开新的标签页
        print(url)
        self.browser.execute_script(js1)  # 打开新的网页标签
            # 执行打开新一个标签页。
        self.browser.switch_to.window(self.browser.window_handles[-1])  # 此行代码用来定位当前页面窗口
        self.buffer()  # 网页滑动  成功切换
            #等待元素加载出来
        time.sleep(3)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#root > div > div.seb-pagination > div > div.seb-pagination__pages > a:nth-child(10)')))
            #获取网页的源代码
        html =  self.browser.page_source

        get_products(wd,html)

        self.close_window()


    def buffer(self): #滑动网页的
        for i in range(20):
            time.sleep(0.8)
            self.browser.execute_script('window.scrollBy(0,380)', '')  # 向下滑行300像素。

    def close_window(self):
        length=self.browser.window_handles
        print('length',length) #判断当前网页窗口的数量
        if  len(length) > 3:
            self.browser.switch_to.window(self.browser.window_handles[1])
            self.browser.close()
            time.sleep(1)
            self.browser.switch_to.window(self.browser.window_handles[-1])


import csv
def save_csv(lise_line):
    file = csv.writer(open("./alibaba_com_img.csv",'a',newline="",encoding="utf-8"))
    file.writerow(lise_line)

#解析网页，
from scrapy.selector import Selector
def get_products(wd,html_text):
    """
    提取商品数据
    """
    select=Selector(text=html_text)
    # 大概有47个
    items = select.xpath('//*[@id="root"]/div/div[3]/div[2]/div/div/div/*').extract()
    print('产品数 ',len(items))
    for i in range(1, 49):
        title = select.xpath(
            f'//*[@id="root"]/div/div[3]/div[2]/div/div/div/div[{i}]/div/div[2]/h4/a/@title').extract()  # 产品的标题
        title_href = select.xpath(
            f'//*[@id="root"]/div/div[3]/div[2]/div/div/div/div[{i}]/div/div[2]/h4/a/@href').extract()  # 产品的详情页
        start_num = select.xpath(
            f'//*[@id="root"]/div/div[3]/div[2]/div/div/div/div[{i}]/div/div[2]/div[1]/div/p[2]/span/text()').extract()  # 起订量
        price = select.xpath(
            f'//*[@id="root"]/div/div[3]/div[2]/div/div/div/div[{i}]/div/div[2]/div[1]/div/p[1]/@title').extract()  # 产品的价格
        adress_href = select.xpath(
            f'//*[@id="root"]/div/div[3]/div[2]/div/div/div/div[{i}]/div/div[3]/a/@href').extract()  # 商家链接
        adress = select.xpath(
            f'//*[@id="root"]/div/div[3]/div[2]/div/div/div/div[{i}]/div/div[3]/a/@title').extract()  # 商家地址
        Response_Rate = select.xpath(
            f'//*[@id="root"]/div/div[3]/div[2]/div/div/div/div[{i}]/div/div[3]/div[2]/div[1]/span/span/text()').extract()  # 复购率
        Transaction = select.xpath(
            f'//*[@id="root"]/div/div[3]/div[2]/div/div/div/div[{i}]/div/div[3]/div[2]/div[2]/span//text()').extract()  # 交易量
        img = select.xpath(
            f'//*[@id="root"]/div/div[3]/div[2]/div/div/div/div[{i}]/div/div[1]/a/div[2]/div[1]/img/@src').extract()  # 图片
        all_down =[wd]+ title +img+ title_href + start_num + price + adress + adress_href + Response_Rate + Transaction
        save_csv(all_down)
        print(title, img,title_href, start_num, price, adress, adress_href, Response_Rate, Transaction)




def main():
    """
    遍历每一页
    """
    run=Chrome_drive()
    run.get_login() #先扫码登录

    wd=['turkey fryer','towel warmer']
    for w in wd:

        for i in range(1, 6):
            run.index_page(i,w)


if __name__ == '__main__':
    csv_title = 'word,title,img,title_href,start_num,price,adress,adress_href,Response_Rate,Transaction,Transactioning'.split(
        ',')
    save_csv(csv_title)
    main()