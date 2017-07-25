#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 17/06/03 11:11 AM
# Author : CA

import queue
import threading

urllist = ['http://www.quanshu.net/map/{}.html'.format(n) for n in range(1, 10)]

# 实例化一个先入先出队列qu
qu = queue.Queue()

# # 将任务加入队列
# for n in urllist:
#     qu.put(n)
# print(qu.qsize())
#
# # 从队列中取出任务
# for n in range(qu.qsize()):
#     print(qu.qsize())
#     print(qu.get())

def getTask(taskqu):
    print('%s is running...'% threading.current_thread().name)
    while not taskqu.empty():
        print(taskqu.get())
    print('get done')


def putTask(taskqu, data):
    print('%s is running...' % threading.current_thread().name)
    for n in data:
        taskqu.put(n)
    print('put done')

putTask(qu, urllist)

t1 = threading.Thread(target=getTask, args=(qu, ), name='getTask')
t2 = threading.Thread(target=getTask, args=(qu, ), name='getTask')

t1.start()
t2.start()
