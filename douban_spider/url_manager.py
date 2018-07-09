# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 11:44:46 2018

@author: 11152
"""


#管理链接

class UrlManager(object):
        def __init__(self):
                self.new_urls=set()    #存放爬取的新的链接
                self.old_urls=set()    #存放旧的链接
                
                
        def has_new_url(self):                       #判断管理器中是否 新的url
                return len(self.new_urls)!=0     #self.new_urls不为0时，说明有待爬取url
                

        def add_new_url(self,url):              #向管理器中加入新的url
                if url is None:          #如果链接不存在就返回
                        return
                #如果链接既不在新链接偶不在老链接就将其添加进新链接中，避免重复添加
                if url not in self.new_urls and url not in self.old_urls:     
                        self.new_urls.add(url)
 
               
        def add_new_urls(self,urls):            #向管理器中添加批量url
                if urls is None or len(urls)==0:     #如果链接不存在或者长度为0，返回
                        return
                else:
                        for url in urls:              #否则，对在urls中的链接，就添加进新的url中
                                self.add_new_url(url)
                                
               
        def get_new_url(self):            #获取新的url
                new_url = self.new_urls.pop()      #从获取新的url，并移除这个url
                self.old_urls.add(new_url)               
                return new_url
                
       
                