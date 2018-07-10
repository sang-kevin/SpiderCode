# -*- coding: utf-8 -*-
import xlwt


class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    # 收集数据
    def collect_data(self, data):
        if not data:
            return None
        else:
            self.datas.append(data)
            if len(self.datas) == 5:
                return "finished"

    # 数据输出
    def output_excel(self):
        style_heading = xlwt.easyxf("""
                                        font:
                                            name Cambria,
                                            colour_index black,
                                            bold on,
                                            height 0xD0;
                                        align:
                                            wrap off,
                                            vert center;
                                        pattern:
                                            pattern solid,
                                            fore-colour 0x16;
                                        borders:
                                            left THIN,
                                            right THIN,
                                            top THIN,
                                            bottom THIN;
                                        """
                                    )
        wbook = xlwt.Workbook()
        wsheet = wbook.add_sheet(u'豆瓣高分电影')
        wsheet.write(0, 0, u'豆瓣链接', style_heading)
        wsheet.col(0).width = 200 * 50
        wsheet.write(0, 1, u'电影名', style_heading)
        wsheet.col(1).width = 200 * 50
        wsheet.write(0, 2, u'电影类型', style_heading)
        wsheet.col(2).width = 100 * 50
        wsheet.write(0, 3, u'豆瓣评分', style_heading)
        wsheet.col(3).width = 50 * 50
        wsheet.write(0, 4, u'评价人数', style_heading)
        wsheet.col(4).width = 50 * 50

        i = 1
        for data in self.datas:
            wsheet.write(i, 0, data['url'])
            wsheet.write(i, 1, data['name'])
            wsheet.write(i, 2, data['style'])
            wsheet.write(i, 3, float(data['score']))
            wsheet.write(i, 4, float(data['population']))
            i += 1
        wbook = wbook.sort(wbook['score'])
        wbook.save(u'豆瓣爬虫.xls')
