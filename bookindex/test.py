#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 17/06/03 11:43 AM
# Author : CA

# import queue
# import threading
#
# urllist = ['http://www.quanshu.net/map/{}.html'.format(n) for n in range(1, 10)]
#
#
# # 实例化一个先入先出队列qu
# qu = queue.Queue()
#
# # # 将任务加入队列
# # for n in urllist:
# #     qu.put(n)
# # print(qu.qsize())
# #
# # # 从队列中取出任务
# # for n in range(qu.qsize()):
# #     print(qu.qsize())
# #     print(qu.get())
#
#
# def getTask(taskqu):
#     print('%s is running...'% threading.current_thread().name)
#     while not taskqu.empty():
#         print(taskqu.get())
#     print('get done')
#
#
# def putTask(taskqu, data):
#     print('%s is running...' % threading.current_thread().name)
#     for n in data:
#         taskqu.put(n)
#     print('put done')
#
#
# t1 = threading.Thread(target=putTask, args=(qu, urllist), name='putTask')
# t2 = threading.Thread(target=getTask, args=(qu, ), name='getTask')
#
# t1.start()
# t2.start()


import threading
import time
import inspect
import ctypes

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thread(thread):
    _async_raise(thread.idente, SystemExit)

class TestThread(threading.Thread):
    def run(self):
        print ("begin")
        while True:
            time.sleep(0.1)
        print ("end")

if __name__ == "__main__":
    t = TestThread()
    t.start()
    time.sleep(1)
    stop_thread(t)
    print ("stoped")

