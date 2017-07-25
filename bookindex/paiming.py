#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 17/06/04 2:25 PM
# Author : CA

import bs4
from bs4 import BeautifulSoup
import lxml
import re
import requests

def getHtmlText(url):
    try:
        r = requests.get(url)
        r.encoding = r.apparent_encoding
        r.raise_for_status()
        return r.text
    except:
        return 'Request Faild....'

def fillUnivList(ulist, html):
    soup = BeautifulSoup(html, 'lxml')
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            ulist.append([tds[0].string, tds[1].string, tds[2].string])

def prinUnivList(ulist, num):
    print('{:^10}\t{:^6}\t{:^10}'.format('排名', '学校名称', '总分'))
    for i in range(num):
        u = ulist[i]
        print('{:^10}\t{:^15}\t{:^6}'.format(u[0], u[1], u[2]))

if __name__ == '__main__':
    url = 'http://www.zuihaodaxue.cn/zuihaodaxuepaiming2017.html'
    uinfo = []
    html = getHtmlText(url)
    fillUnivList(uinfo, html)
    prinUnivList(uinfo, 20)







