# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 11:44:19 2018

@author: 11152
"""

#网页解析

from bs4 import BeautifulSoup
import re

class HtmlParser(object):
        
        def _get_new_urls(self,page_url,soup):
                new_urls = set()    #将得到的属性存储到new_urls
                links=soup.find_all('a', href=re.compile(r'https://movie.douban.com/subject/(.+)/?from=subject-page'))
                for link in links:
                        new_url=link['href']
                        pure_url = new_url.split('?')[0]     #切片href中?之前的链接
                        new_urls.add(pure_url)      #添加new_urls
                return new_urls
        
        
        def _get_new_data(self, page_url, soup):
                res_data = {}   #空字典
                
                #电影链接，存放入res_data中，列名
                res_data['url'] = page_url
                
                #获取电影名，存放入res_data
                # <h1><span property="v:itemreviewed">肖申克的救赎 The Shawshank Redemption</span><span class="year">(1994)</span></h1>
                name_node = soup.find(id='content').find('h1')
                res_data['name'] = name_node.get_text()
                print(res_data['name'])
                #获取电影类型 
                ##<span property="v:genre">犯罪</span>
                style_node=soup.find_all('span', property="v:genre")
                texts = []
                for node in style_node:
                        text = node.get_text()
                        texts.append(text)
                
                style = "/".join(texts)
                print(style)
                res_data['style'] = style
                
                #获取电影评分
                # <strong class="ll rating_num" property="v:average">9.6</strong>
                score_node = soup.find('strong', class_="ll rating_num")
                res_data['score'] = score_node.get_text()
                
                #电影评价人数
                # <a href="collections" class="rating_people"><span property="v:votes">1058964</span>人评价</a>
                population_node = soup.find('a', class_="rating_people").find('span')
                res_data['population'] = population_node.get_text()
                if int(res_data['population']) >= 200000:
                        return res_data
                else:
                        return {}    
        

        def parse(self, page_url,html_cont):
                if page_url is None or html_cont is None:
                        return
                soup = BeautifulSoup(html_cont , 'html.parser',from_encoding='utf-8')     #解析
                new_urls = self._get_new_urls(page_url, soup)    #新的网页
                new_data = self._get_new_data(page_url, soup)    #新的数据
                return new_urls, new_data
                
                
                