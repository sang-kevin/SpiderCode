# -*- coding: utf-8 -*-
import time  # 随机延时
import random
import url_manager, html_downloader, html_parser, html_outputer


# 初始化
class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()  # urls作为url管理器
        self.downloader = html_downloader.HtmlDownloader()  # 下载器
        self.parser = html_parser.HtmlParser()  # 解析器
        self.outputer = html_outputer.HtmlOutputer()  # 输出

    def craw(self, root_url):
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():  # 如果存在新的url
            try:
                new_url = self.urls.get_new_url()  # 获取待爬取的url
                print('爬取 {}'.format(new_url))  # 显示爬取的url
                html_cont = self.downloader.download(new_url)  # 启动下载器下载页面
                print(len(html_cont))
                new_urls, new_data = self.parser.parse(new_url, html_cont)  # 调解析器解析页面，获取数据
                self.urls.add_new_urls(new_urls)  # 新的url添加进url管理器
                result = self.outputer.collect_data(new_data)  # 收集数据
                if result == "finished":
                    break
                time.sleep(random.random() + 1)
            except:
                print('爬取失败')

        self.outputer.output_excel()


# python
if __name__ == '__main__':
    root_url = 'https://movie.douban.com/subject/1292052/'  # 入口链接
    obj_spider = SpiderMain()
    #        print(type(obj_spider.downloader))
    obj_spider.craw(root_url)  # 启动爬虫
