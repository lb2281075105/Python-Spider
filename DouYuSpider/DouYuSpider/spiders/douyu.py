# -*- coding: utf-8 -*-
import scrapy
import json

from DouYuSpider.items import DouyuspiderItem
class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    # 不可设置为allowed_domains = ['http://capi.douyucdn.cn']
    allowed_domains = ['capi.douyucdn.cn']

    offset = 0
    url = "http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset="

    start_urls = [url + str(offset)]

    def parse(self, response):
        data = json.loads(response.text)['data']

        for each in data:
            item = DouyuspiderItem()

            item["vertical"] = each["vertical_src"].encode("utf-8")
            item["name"] = each["nickname"].encode("utf-8")
            item["room_src"] = each["room_src"].encode("utf-8")
            item["anchor_city"] = each["anchor_city"].encode("utf-8")

            yield item

        self.offset += 20
        yield scrapy.Request(self.url + str(self.offset),callback = self.parse)

