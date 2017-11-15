# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanmovieItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 信息
    info = scrapy.Field()
    # 评分
    star = scrapy.Field()
    # 简介
    quote = scrapy.Field()
    
    
