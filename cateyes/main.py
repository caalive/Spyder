#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 17/07/18 10:18 PM
# Author : CA
import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool


def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    #print(html)
    pars_one_page(html)
    for item in pars_one_page(html):
        #print(item)
        write_file(item)


def pars_one_page(html):
    partten = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)"'
                         + '.*?alt="(.*?)".*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>', re.S)

    items = re.findall(partten, html)
    print(items)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5]+item[6]
        }

def write_file(data):
    with open('result.txt', 'a', encoding='utf8') as f:
        f.write(json.dumps(data, ensure_ascii=False)+'\n')
        f.close()

if __name__ == "__main__":
    # for i in range(10):
    #     main(i * 10)
    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])

