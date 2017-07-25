#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 17/07/22 9:38 PM
# Author : CA

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import os
from hashlib import md5
from config import *
import re
from multiprocessing import Pool

from sqlalchemy import create_engine    #导入mysql数据库创建引擎
from sqlalchemy.ext.declarative import declarative_base     #创建数据库表,声明映像
from sqlalchemy import Column, String, Integer  #导入表头属性值
from sqlalchemy.orm import sessionmaker     #创建数据库会话连接

engine = create_engine(DB_URL)  #创建引擎
Base = declarative_base(engine) #创建数据库表,声明映像

#创建数据库表对应的类
class WallPaper(Base):
    __tablename__ = 'wallPaperDetail'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(100), nullable=False)
    detail_href = Column(String(100), nullable=False)

    def __repr__(self):
        return 'wallPaperDetail(id={}, title={}, detail_href={})'.format(self.id, self.title, self.detail_href)

#将对应的类映射到数据库表中
Base.metadata.create_all()

#创建数据库会话连接

Session = sessionmaker(engine)
session = Session()

#添加数据
' [title, [images_url]]'
def write_data_to_dababase(data):  #将数据插入数据库
   for item in data:
       for href in item[1]:
            print('正在插入数据...')
            page_info = WallPaper(title=item[0], detail_href=href)
            session.add(page_info)
            session.commit()
            print('插入数据成功..', item[0], href)

def get_one_page(url):  #获取组图页面的信息
    try:
        response = requests.get(url)
        #print(response)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html, page_index):  #解析单个页面详细信息
    soup = BeautifulSoup(html, 'lxml')
    page_info = soup.select('ul.main-img.clearfix p a') #组图链接的提取规则
    for item in page_info:  #item为组图链接
        title = item.string
        #print(title)
        title_href = item['href']
        #print(title_href)
        partten = re.compile('.*?\.(\d)') #获取当前页的索引,后面创建文件夹使用
        page_number = re.match(partten, page_index[::-1]).group(1)
        #print(title_href)
        #print(page_index)
        detail_page = get_one_page(title_href)
        if detail_page:  #单个图片的详细信息
            soup = BeautifulSoup(detail_page, 'lxml')
            page_info = soup.select('ul.ulBigPic img') #单幅图链接提取规则
            images_url = [i['src'] for i in page_info]  # images_url 为单幅图链接组成的列表
            if images_url:
                print('正在下载第' + page_number + '页图片....')
                for image in images_url:
                    download_image(image, page_number, title)   #下载组图
                print('第' + page_number + '页图片下载完毕!')
                yield [title, images_url]  # 返回值为组图的title和组图内每幅图片的链接
                #image为单幅图片链接,[i['src'] for i in page_info]循环取每一幅图片的链接
def get_page_detail(): #获取单个URL的页面详细信息
    url = 'http://www.win4000.com/?c=index&a=record'
    try:
        response = requests.post(url)
        print(response)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def download_image(url, index, title):  #下载图片
    #print('正在下载第' + index + '页图片', title, url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content, index, title)
        return None
    except RequestException:
        print('请求图片出错', url)
        return None


def save_image(content, offset, title):  #保存图片文件
    file_path = create_path(offset, title) #创建文件保存路径
    file_path = '{0}/{1}.{2}'.format(file_path, md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()
    else:
        print('图片已存在,略过下载')


def create_path(offset, flodername):  #根据索引页和文件名创建文件夹
    temp_path = '\\'.join(('\\' + str(offset), flodername))
    path = os.getcwd() + '\images'  # 在当前目录的images目录下新建多级子目录
    if not os.path.exists(path + temp_path):  # 不存在则创建子目录
        os.makedirs(path + temp_path)
    os.chdir(path + temp_path)  # 返回子目录的路径
    picpath = os.getcwd()
    os.chdir('../../../')
    return picpath


# def flat_list(data, container):#递归解包list
#     for li in data:
#         if isinstance(li, list):
#             flat_list(li, container)
#         else:
#             container.append(li)
#     return container


# def gen_data(data):  #返回解析的扁平数据
#     #print(data)
#     for item in data:
#         if item != data[0]:
#             yield data[0], item

def main(offset):   #主函数
   for url_index_page in create_url(offset):
       html = get_one_page(url_index_page)  #获取索引页信息
       image_data = parse_one_page(html, url_index_page) #解析索引页信息,返回当前页每组图片的详细信息,为嵌套的数据结构
       write_data_to_dababase(image_data)  # 数据写入数据库


def create_url(offset):  #生成索引页链接
    for index in range(offset):
        yield 'http://www.win4000.com/wallpaper_208_0_0_{}.html'.format(offset)


if __name__ == '__main__':
    pool = Pool()
    groups = [offset for offset in range(START_GROUP, END_GROUP + 1)]
    pool.map(main, groups)
    #main(1)