#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 17/06/02 11:27 AM
# Author : CA

# 导入所需的库文件及函数
import queue
import re
import threading

import requests

from bookindex.csvwrite import creatListCSV

# 爬取全书网小数
# 构建所有小说分类列表url
# http://www.quanshu.net/map/1.html 分类起始地址
urllist = ['http://www.quanshu.net/map/{}.html'.format(n) for n in range(1, 4)]

url = 'http://www.quanshu.net/map/1.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
}

urlhead = 'http://www.quanshu.net/'

# 获取函数执行时间
# def getExec(func,k):
#     begin = datetime.datetime.now()
#     func(k)
#     end = datetime.datetime.now()
#     return end - begin

kk = '<a href="1.html" class="hottext">玄幻魔法</a>'

# 书名链接和对应的书名正则表达式
linkAndTitle = re.compile('<a href="(/book.*?)".*?>(.*?)</a>', re.S)
# 获取分类名
# bookCategory = re.compile('<a.*?class="hottext">(.*?)</', re.S)

# kk = '<div class="c_head"><a href="1.html" class="hottext">玄幻魔法</a>'

# bookname = re.findall(bookCategory, kk)
# print(bookname)
# 获取分类名
res = requests.get(url, headers=headers)
if res.status_code == 200:
    res = res.content.decode('gbk')
    bookname = re.findall('<div class="c_head".*?</div>', res)
    bookname = re.findall('<a.*?>(.*?)<', bookname[0])
    print('分类列表如下：%s' % bookname)

# 获取书名链接和书名
def getLinkAndName(str):
    link = re.findall(linkAndTitle, str)
    return link

# 获取每个分类列表的url
def getUrl(urllist):
    for n in urllist:
        yield n

# 获取每个分类下的书名和书名链接
# def getUrlInfo(genfunc):
#     count = 0
#     for url in genfunc:
#         print('正在请求########%s#############分类下的所有书名列表。。。。' % bookname[count])
#         res = requests.get(url, headers=headers)
#         time.sleep(2)
#         if res.status_code == 200:
#             print('正在转换.....')
#             res = res.content.decode('gbk')
#             print('正在解析.....')
#             data = getLinkAndName(res)
#             print('准备写入文件....')
#             # 将获取的链接和书名写入文件
#             creatListCSV(bookname[count] + '.csv', ['BookLink', 'bookName'], data)
#             print('%s分类下的所有书名列表写入文件完毕。' % bookname[count])

#             count += 1
#
# getUrlInfo(urllist)

qtask = queue.Queue()
for n in urllist:
    qtask.put(n)

lock = threading.Lock()

def getUrlInfo(genfunc):
    while not genfunc.empty():
        lock.acquire()
        print('%s is get lock.......' % threading.current_thread().name)
        url = genfunc.get()
        print(url)
        res = requests.get(url, headers=headers)
        print(res.status_code)
        if res.status_code == 200:
            print('%s 正在转换.....' % threading.current_thread().name)
            res = res.content.decode('gbk')
            print('%s 正在解析.....' % threading.current_thread().name)
            data = getLinkAndName(res)
            print('%s 准备写入文件....' % threading.current_thread().name)
            # 将获取的链接和书名写入文件
            creatListCSV(bookname[len(urllist) - 1 - genfunc.qsize()] + '.csv', ['BookLink', 'bookName'], data)
            lock.release()
            print('%s release....' % threading.current_thread().name)
        else:
            lock.release()
            print('%s release....' % threading.current_thread().name)
    else:

        lock.release()
        print('all done!!!!')
        return


t1 = threading.Thread(target=getUrlInfo, args=(qtask, ), name='t1')
t2 = threading.Thread(target=getUrlInfo, args=(qtask, ), name='t2')
t3 = threading.Thread(target=getUrlInfo, args=(qtask, ), name='t3')

t1.start()
t2.start()
t3.start()














