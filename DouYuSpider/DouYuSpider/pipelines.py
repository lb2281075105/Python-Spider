# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import codecs
import json

class DouyuspiderPipeline(object):
    def __init__(self):
        # 创建一个只写文件，指定文本编码格式为utf-8
        self.filename = codecs.open('douyu.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):

        html = json.dumps(dict(item),ensure_ascii='utf-8')
        self.filename.write(html + '\n')
        return item

    # def spider_closed(self, spider):
    #     self.file.close()