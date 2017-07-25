#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 17/07/22 10:44 AM
# Author : CA

import requests
from bs4 import BeautifulSoup
import re
import xlsxwriter
from requests.exceptions import RequestException

def get_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            #print(response.text[:1000])
            return response.content.decode('gbk')
        else:
            return None
    except RequestException:
        return None

def parse_page(html):
    if html:
        soup = BeautifulSoup(html, 'lxml')
        sh, sz = soup.select('div.sltit')[0].get_text(),soup.select('div.sltit')[1].get_text()
        stockinfo = soup.select('#quotesearch ul li a')  #标签递归选择
        for item in stockinfo:
            namecode = re.match("(.*)\((.*)\).*", item.string)
            name = namecode.group(1)
            code = namecode.group(2)
            href = item['href']
            yield name, code, href


def main():
    worksheet, workbook = create_excel('沪深股票代码.xlsx')
    url = 'http://quote.eastmoney.com/stocklist.html'
    html = get_page(url)
    parse_page(html)
    index = 1
    print('开始写入EXCEL文件')
    for item in parse_page(html):
        write_to_excel(worksheet, item, index)
        index += 1
    print('写入完毕!')
    workbook.close()


def create_excel(filename, sheetname = '沪深股票代码'):
    workbook = xlsxwriter.Workbook(filename)
    bold = workbook.add_format({'bold':True})
    worksheet = workbook.add_worksheet(sheetname)
    worksheet.write('A1', 'StockName', bold)
    worksheet.write('B1', 'StockCode', bold)
    worksheet.write('C1', 'StockLink', bold)
    return worksheet, workbook


def write_to_excel(worksheet, data, rowindex):  #写入一行数据
    row = rowindex
    col = len(data)
    for index in range(col):
        worksheet.write(row, index, data[index])

if __name__ == '__main__':
    main()
