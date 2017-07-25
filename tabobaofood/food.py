#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 17/07/24 9:06 PM
# Author : CA


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
from pyquery import PyQuery as pq
from config import *
import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

# browser = webdriver.Chrome() #调用Chrome浏览器,显示
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS) #不显示浏览器,后台调用
wait = WebDriverWait(browser, 10)
browser.set_window_size(1440, 900)

def search():
    print('正在搜索....')
    try:
        browser.get('http://www.taobao.com')  #查询入口
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))  #文本输入框id
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button'))  #搜索按钮css
        )
        # print(type(input))
        input.send_keys(KEY_WORD)
        # print(type(submit))
        submit.click()
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')) #总页数css
        )
        #解析页面获取商品信息
        get_products()
        return total.text
    except TimeoutException:
        return search()


def next_page(page_number):
    print('正在跳转到第%s页....'%page_number)
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input')) #商品信息css
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')) #输入页数确定css
        )

        input.clear()
        input.send_keys(page_number)
        submit.click()
        #比较当前页数字是否和传入数据相等
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number))) #页数输入框css
        #解析页面获取商品信息

        get_products()
    except TimeoutException:  #超时重新执行调用next_page函数
        next_page(page_number)


def get_products():
    print('正在解析....')
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product =  {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        # print(product)
    print('解析成功...')
        # save_to_mongo(product)
    # print(product)

#存储到数据库
def save_to_mongo(result):
    print(result)
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到数据库成功!', result)
    except Exception:
        print('存储到数据库失败!', result)

def main():
    try:
        total = search()
        total = int(re.split(' ', total)[1])
        #print(total)
        for i in range(2, total + 1):
            next_page(i)
    except Exception:
        print('抓取出错了!!!!')
    finally:
        browser.close()

if __name__ == '__main__':
    main()
