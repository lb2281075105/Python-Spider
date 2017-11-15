# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json

class DoubanmoviePipeline(object):
    def process_item(self, item, spider):
        
        self.filename = codecs.open('movie.json','a',encoding='utf-8')
        html = json.dumps(dict(item),ensure_ascii=False)
        self.filename.write(html + '\n')
        self.filename.close()
        
        return item


# host = settings["MONGODB_HOST"]
#         port = settings["MONGODB_PORT"]
#         dbname = settings["MONGODB_DBNAME"]
#         sheetname= settings["MONGODB_SHEETNAME"]
#
#         # 创建MONGODB数据库链接
#         client = pymongo.MongoClient(host = host, port = port)
#         # 指定数据库
#         mydb = client[dbname]
#         # 存放数据的数据库表名
#         self.sheet = mydb[sheetname]
#
#     def process_item(self, item, spider):
#         data = dict(item)
#         self.sheet.insert(data)
#         return item