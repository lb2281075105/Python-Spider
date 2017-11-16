# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouyuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # 房间名
    vertical = scrapy.Field()
    # 昵称
    name = scrapy.Field()
    # 房间照片
    room_src = scrapy.Field()
    # 地区
    anchor_city = scrapy.Field()
    imagesPath = scrapy.Field()


