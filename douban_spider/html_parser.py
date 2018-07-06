# coding=utf-8
from bs4 import BeautifulSoup
import re


class HtmlParser(object):

    def _get_new_urls(self, soup):
        new_urls = set()
        url_nodes = soup.find_all('a', href=re.compile(r'https://movie.douban.com/subject/(.+)/?from=subject-page'))
        for url_node in url_nodes:
            url = url_node['href']
            # print url
            pure_url = url.split('?')[0]
            new_urls.add(pure_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        res_data = {}
        # url
        res_data['url'] = page_url

        # <h1><span property="v:itemreviewed">肖申克的救赎 The Shawshank Redemption</span><span class="year">(1994)</span></h1>
        name_node = soup.find(id='content').find('h1')
        res_data['name'] = name_node.get_text()

        # <strong class="ll rating_num" property="v:average">9.6</strong>
        score_node = soup.find('strong', class_="ll rating_num")
        res_data['score'] = score_node.get_text()

        # <a href="collections" class="rating_people"><span property="v:votes">1058964</span>人评价</a>
        population_node = soup.find('a', class_="rating_people").find('span')
        res_data['population'] = population_node.get_text()

        return res_data

    def parse(self, page_url, html_cont):
        if html_cont is None:
            return None
        soup = BeautifulSoup(
            html_cont,
            'html.parser',
            from_encoding='utf8'
        )
        new_urls = self._get_new_urls(soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data
