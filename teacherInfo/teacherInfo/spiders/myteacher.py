# -*- coding: utf-8 -*-
import scrapy
from teacherInfo.items import TeacherinfoItem

class MyteacherSpider(scrapy.Spider):
    name = 'myteacher'
    allowed_domains = ['itcast.cn']
    # start_urls = ("http://www.itcast.cn/channel/teacher.shtml",) 元组也可以
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml#ac',
                  'http://www.itcast.cn/channel/teacher.shtml#acloud',
                  'http://www.itcast.cn/channel/teacher.shtml#adesign',
                  'http://www.itcast.cn/channel/teacher.shtml#ads',
                  'http://www.itcast.cn/channel/teacher.shtml#ajavaee',
                  'http://www.itcast.cn/channel/teacher.shtml#anetmarket',
                  'http://www.itcast.cn/channel/teacher.shtml#aphp',
                  'http://www.itcast.cn/channel/teacher.shtml#apm',
                  'http://www.itcast.cn/channel/teacher.shtml#apython',
                  'http://www.itcast.cn/channel/teacher.shtml#astack',
                  'http://www.itcast.cn/channel/teacher.shtml#atest',
                  'http://www.itcast.cn/channel/teacher.shtml#aui',
                  'http://www.itcast.cn/channel/teacher.shtml#auijp',
                  'http://www.itcast.cn/channel/teacher.shtml#aweb']
    # 爬虫的约束区域
    def parse(self, response):
        # 存放老师信息的集合
        items = []
        print(response.body)
        for each in response.xpath("//div[@class='li_txt']"):
            # 将我们得到的数据封装到一个 `ItcastItem` 对象
            item = TeacherinfoItem()
            # extract()方法返回的都是unicode字符串
            name = each.xpath("h3/text()").extract()
            position = each.xpath("h4/text()").extract()
            info = each.xpath("p/text()").extract()

            # xpath返回的是包含一个元素的列表
            item['name'] = name[0]
            item['position'] = position[0]
            item['info'] = info[0]

            items.append(item)
            yield item
        # 直接返回最后数据
        # return items
