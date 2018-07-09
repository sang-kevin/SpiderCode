# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 22:25:24 2018

@author: 11152
"""


#网页下载

import requests
from urllib.request import urlopen
    
class HtmlDownloader(object):

    def download(self, url):     #下载的url
        if url is None:
            return None
        print(url)
        #User Agent伪装为浏览器进行爬取
        defined_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
             Chrome/67.0.3396.99 Safari/537.36'
        }
        response = requests.get(url, headers=defined_headers)
        print(response.status_code)
        if response.status_code != 200:      #请求失败！=200
            return None
        else:
            return response.content          #请求成功返回下载内容