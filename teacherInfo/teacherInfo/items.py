# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# Item 定义结构化数据字段,用来保存爬取到的数据
class TeacherinfoItem(scrapy.Item):

    # 获取名字
    name = scrapy.Field()
    # 职称
    position = scrapy.Field()
    # 个人信息
    info = scrapy.Field()


