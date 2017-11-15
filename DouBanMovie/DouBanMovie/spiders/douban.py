# -*- coding: utf-8 -*-
import scrapy
from DouBanMovie.items import DoubanmovieItem

class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    offset = 0
    url = 'https://movie.douban.com/top250?start='
    start_urls = (
        url + str(offset),
    )

    def parse(self, response):
        item = DoubanmovieItem()
        # 电影全部信息
        movies = response.xpath("//div[@class='info']")
        for eachmovie in movies:
            
            titlelist = eachmovie.xpath("./div[@class='hd']/a/span[@class='title'][1]/text()")
            if len(titlelist) == 0:
                item['title'] = ''
            else:
                item['title'] = titlelist.extract()[0]
            info = eachmovie.xpath("./div[@class='bd']/p/text()").extract()[0]
            item['info'] = info.replace('\n','').strip()
            item['star'] = eachmovie.xpath("./div[@class='bd']/div[@class='star']/span[@class='rating_num']/text()").extract()[0]
            quotelist = eachmovie.xpath("./div[@class='bd']/p[@class='quote']/span[@class='inq']/text()")
            if len(quotelist) == 0:
                item['quote'] = ''
            else:
                item['quote'] = quotelist.extract()[0]
            yield item


        if self.offset < 225:
            self.offset += 25
            yield scrapy.Request(self.url + str(self.offset),callback = self.parse)

