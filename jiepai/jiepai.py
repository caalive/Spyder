#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 17/07/19 7:52 PM
# Author : CA

import requests
from requests.exceptions import RequestException
import re
from urllib.parse import urlencode
import json
from bs4 import BeautifulSoup
import pymongo
from config import *
import os
from hashlib import md5
from multiprocessing import Pool


client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def get_page_index(offset, keyword):    #构造索引页GET AJAX 请求参数
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 1
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)  #索引页请求地址
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text                        #返回索引页详细信息
        return None
    except RequestException:
        #print('请求索引失败')
        return None

def parse_index(html):                              #解析索引页内包含的URL
    data = json.loads(html)
    if data and 'data' in data.keys():              #获取JSON字段data并判断是否含有data
        for item in data.get('data'):
            if 'sslocal' not in item.get('url'):
                yield item.get('url')               #返回索引页内的所有URL


def parse_page_datail(html, url):                   #解析单个标题的URL
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    if '- 今日头条' in title:
        title = title.split('- 今日头条')[0]
    image_partten = re.compile('var gallery = (.*?);', re.S)
    result = re.search(image_partten, html)
    if result:
        data = json.loads(result.group(1))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images : down_load_image(image)
            temp = {
                'title': title,
                'images_url': images,
                'title_url': url
            }
            return temp
    else:
        image_url = soup.select('.article-content img')
        if image_url:
            for image in [i['src'] for i in image_url]: down_load_image(image)
            # 使用标签中括号方式获取一个标签的属性值i['src']
            temp = {
                'title': title,
                'images_url': [i['src'] for i in image_url],
                'title_url': url
            }
            return temp

def get_page_detail(url):
    try:
        response = requests.get(url)
        #print(response.status_code)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        #print('请求详情页失败', url)
        return None


def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到MongoDB成功', result)
        return True
    return False

def down_load_image(url):
    print('正在下载', url)
    try:
        response = requests.get(url)
        #print(response.status_code)
        if response.status_code == 200:
            save_image(response.content, FLODER)
        return None
    except RequestException:
        print('请求图片出错', url)
        return None

def save_image(content, flodername):
        file_path = '{0}/{1}.{2}'.format(os.path.abspath(flodername), md5(content).hexdigest(), 'jpg')
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as f:
                f.write(content)
                f.close()

def main(offset):
    html = get_page_index(offset, KEYWORD)
    #print(html)
    for url in parse_index(html):
        #print(url)
        html = get_page_detail(url)
        if html:
            result = parse_page_datail(html, url)
            # if result:
            #     save_to_mongo(result)

if __name__=='__main__':
    groups = [x * 20 for x in range(GROUP_START, GROUP_END + 1)]
    pool = Pool()
    pool.map(main, groups)