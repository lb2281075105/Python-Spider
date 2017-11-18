# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
from HongNiangNet.items import HongniangnetItem
# 分布式
from scrapy.spider import Rule
from scrapy_redis.spiders import RedisCrawlSpider

# class HongniangSpider(CrawlSpider):
class HongniangSpider(RedisCrawlSpider):

    name = 'hongniang'
    allowed_domains = ['hongniang.com']
    # start_urls = ['http://www.hongniang.com/match?&page=1']
    redis_key = "hongniangSpider:start_urls"

    # 动态域范围获取
    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(HongniangSpider, self).__init__(*args, **kwargs)

    # 每一页匹配规则
    page_links = LinkExtractor(allow=(r"hongniang.com/match?&page=\d+"))
    # 每个人个人主页匹配规则
    profile_links = LinkExtractor(allow=(r"hongniang.com/user/member/id/\d+"))
    rules = (
        # 没有回调函数，说明follow是True
        Rule(page_links),
        # 有回调函数，说明follow是False
        Rule(profile_links, callback='parse_item',follow=True),
    )

    def parse_item(self, response):

        item = HongniangnetItem()
        # 注意：xpath获取位置时，不从0开始
        # 用户名
        item["username"] = self.get_username(response)
        # 年龄
        item["age"] = self.get_age(response)
        # 头像图片链接
        item["header_link"] = self.get_header_link(response)
        # 相册图片链接
        item["images_url"] = self.get_images_url(response)
        # 内心独白
        item["content"] = self.get_content(response)
        # 籍贯
        item["place_from"] = self.get_place_from(response)
        # 学历
        item["education"] = self.get_education(response)
        # 爱好
        item["hobby"] = self.get_hobby(response)
        # 个人主页链接
        item["source_url"] = response.url
        # 数据来源网站
        item["source"] = "hongniang"

        yield item

    def get_username(self,response):
        username = response.xpath("//div[@class='name nickname']/text()").extract()
        if len(username):
            username = username[0]
        else:
            username = "NULL"
        return username.strip()

    def get_age(self,response):
        age = response.xpath("//div[@class='mem_main']/div[@class='sub1']/div[@class='right']/div[@class='info2']/div[1]/ul[1]/li[1]/text()").extract()
        if len(age):
            age = age[0]
            print(age)
        else:
            age = "NULL"
        return age.strip()

    def get_header_link(self,response):
        header_link = response.xpath("//div[@class='mem_main']/div[@class='sub1']/div[@class='left']/div[@id='tFocus']/div[@id='tFocusBtn']/div[@id='tFocus-btn']/ul//img[1]/@src").extract()
        if len(header_link):
            header_link = header_link[0]
        else:
            header_link = "NULL"
        return header_link.strip()

    def get_images_url(self,response):
        images_url = response.xpath("//div[@class='mem_main']/div[@class='sub1']/div[@class='left']/div[@id='tFocus']/div[@id='tFocusBtn']/div[@id='tFocus-btn']/ul//img/@src").extract()
        if len(images_url):
            images_url = images_url
        else:
            images_url = "NULL"
        return images_url

    def get_content(self,response):
        ontent = response.xpath("//div[@class='mem_main']/div[@class='sub1']/div[@class='right']/div[@class='info5']/div[@class='text']/text()").extract()
        if len(ontent):
            ontent = ontent[0]
        else:
            ontent = "NULL"
        return ontent.strip()

    def get_place_from(self,response):
        place_from = response.xpath("//div[@class='mem_main']/div[@class='sub2']/div[@class='info1'][1]/div[@class='right']/ul[2]/li[1]/text()").extract()
        if len(place_from):
            place_from = place_from[0]
        else:
            place_from = "NULL"
        return place_from.strip()

    def get_education(self,response):
        education = response.xpath("//div[@class='mem_main']/div[@class='sub1']/div[@class='right']/div[@class='info2']/div/ul[2]/li[2]/text()").extract()
        if len(education):
            education = education[0]
        else:
            education = "NULL"
        return education.strip()
    def get_hobby(self,response):
        hobby = response.xpath("//div[@class='mem_main']//div[@class='sub2']/div[@class='info1'][2]/div[@class='right'][1]/ul[1]/li[4]/text()").extract()
        if len(hobby):
            hobby = hobby[0]
        else:
            hobby = "NULL"
        return hobby.strip()

