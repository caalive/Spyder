#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 17/07/19 10:01 PM
# Author : CA

# from bs4 import BeautifulSoup
# import requests
# from requests.exceptions import RequestException
# import re
# from urllib.parse import urlencode
# import json
# from bs4 import BeautifulSoup


import requests
from bs4 import BeautifulSoup

url = 'http://www.win4000.com/wallpaper_detail_132034.html'

response = requests.get(url)

html = BeautifulSoup(response.text, 'lxml')

print(html)
