#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 17/06/02 11:30 PM
# Author : CA

# 导入csv模块
import csv

def creatListCSV(fileName='', listHead=[], listData=[]):
    print(fileName)
    csvfile = open(fileName, 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerow(listHead)
    writer.writerows(listData)
    csvfile.close()



