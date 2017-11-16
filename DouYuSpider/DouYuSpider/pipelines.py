# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
# import codecs
# import json
import os
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings

# class DouyuspiderPipeline(object):
#     def __init__(self):
#         # 创建一个只写文件，指定文本编码格式为utf-8
#         self.filename = codecs.open('douyu.json', 'w', encoding='utf-8')
#     def process_item(self, item, spider):
#
#         html = json.dumps(dict(item),ensure_ascii='utf-8')
#         self.filename.write(html + '\n')
#         return item
#
#     # def spider_closed(self, spider):
#     #     self.file.close()

# scrapy下载图片需要安装pip install image/Pillow
class DouYuImagesPipelines(ImagesPipeline):
    IMAGES_STORE = get_project_settings().get("IMAGES_STORE")

    def get_media_requests(self, item, info):
        image_url = item["vertical"]
        yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        # 固定写法，获取图片路径，同时判断这个路径是否正确，如果正确，就放到 image_path里，ImagesPipeline源码剖析可见
        image_path = [x["path"] for ok, x in results if ok]

        os.rename(self.IMAGES_STORE + "/" + image_path[0], self.IMAGES_STORE + "/" + item["name"] + ".jpg")
        item["imagesPath"] = self.IMAGES_STORE + "/" + item["name"]

        return item