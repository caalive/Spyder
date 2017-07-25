#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 17/07/22 10:05 PM
# Author : CA

import os
import re
from config import *

# def create_url(offset = 1):
#     for idnex in range(offset):
#         yield 'http://www.win4000.com/wallpaper_208_0_0_{}.html'.format(offset)
#
#
# for i in create_url():
#     print(i)

# def create_path(offset, flodername):
#     temp = '\\'.join(('\\' + offset, flodername))
#     path = os.getcwd() + '/images'    #在当前目录的images目录下新建多级子目录
#     if not os.path.exists(path + temp):  #不存在则创建子目录
#         os.makedirs(path + temp)
#     os.chdir(path + temp)          #返回子目录的路径
#     return os.getcwd()
#
#
# print(create_path('1', 'ccc'))


# print('\\'.join(('1', 'ccc')))

# url = 'http://www.win4000.com/wallpaper_208_0_0_1.html'
# print(url[::-1])
# partten = re.compile('.*?\.(\d)')
# offset = re.match(partten, url[::-1])
# print(ss.group(1))

# groups = [offset for offset in range(START_GROUP, END_GROUP)]


#temp = [1, [1, [1]]]

L = [1,2,3,4]
for i in L:
    print(i+1)
# temp=[[1,2],[3,4],[5,6,[3,7,9]]]
#
# def di(data):
#     for i in data:
#         if isinstance(i, list):
#             di(i)
#         else:
#             L.append(i)
#     return L
#
# def mmp(data):
#     for item in data:
#         print(data[0], item)
#
#
# # di(temp)
# ss  = di(temp)
# mmp(ss)