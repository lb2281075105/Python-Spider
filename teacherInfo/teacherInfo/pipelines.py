# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
class TeacherinfoPipeline(object):
    def __init__(self):
        self.filename = codecs.open('teacher.json','wb','utf-8')
    def process_item(self, item, spider):
        print(item)
        html = json.dumps(dict(item),ensure_ascii=False)
        self.filename.write(html + '\n')
        return item

    def open_spider(self, spider):
        pass
        # self.filename.close()