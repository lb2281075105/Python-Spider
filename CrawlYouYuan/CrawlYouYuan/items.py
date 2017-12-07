# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CrawlyouyuanItem(scrapy.Item):
    # 用户名
    username = scrapy.Field()
    # 年龄
    age = scrapy.Field()
    # 头像图片的链接
    header_url = scrapy.Field()
    # 相册图片的链接
    images_url = scrapy.Field()
    # 内心独白
    content = scrapy.Field()
    # 籍贯
    place_from = scrapy.Field()
    # 学历
    education = scrapy.Field()
    # 兴趣爱好
    hobby = scrapy.Field()
    # 个人主页
    source_url = scrapy.Field()
    # 数据来源网站
    sourec = scrapy.Field()
    # utc 时间
    time = scrapy.Field()
    # 爬虫名
    spidername = scrapy.Field()
