# coding=utf-8
import xlwt


class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_excel(self):
        wbook = xlwt.Workbook()
        wsheet = wbook.add_sheet(u'豆瓣高分电影')
        wsheet.write(0, 0, u'URL')
        wsheet.write(0, 1, u'电影名')
        wsheet.write(0, 2, u'评分')
        wsheet.write(0, 3, u'评价人数')
        i = 1
        for data in self.datas:
            wsheet.write(i, 0, data['url'])
            wsheet.write(i, 1, data['name'])
            wsheet.write(i, 2, data['score'])
            wsheet.write(i, 3, data['population'])
            i += 1
        wbook.save(u'豆瓣爬虫.xls')
