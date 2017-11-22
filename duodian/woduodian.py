#encoding=utf-8

import MySQLdb
import json
import jsonpath
import urllib2
import os
class DuoDian():
    def __init__(self):
        self.url = 'https://gatewx.dmall.com/customersite/searchWareByCategory?param={"pageNum":1,"pageSize":30,"venderId":"1","storeId":"108","sort":"1","categoryId":11347,"categoryLevel":3,"cateSource":1,"bizType":"1"}&token=&source=2&tempid=C7B357489E400002B1514BD01B00E270&pubParam={"utmSource":"wxmp"}&_=1511256196255'
        # 建立和数据库的连接
        self.db = MySQLdb.connect(host='127.0.0.1', user="root", passwd="", db="test")
        # 获取操作游标
        self.cursor = self.db.cursor()

    def get_html(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0)'}
        request = urllib2.Request(self.url,headers=headers)
        response = urllib2.urlopen(request)
        html = response.read()
        return html

    def get_html1(self,url):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0)'}
        request = urllib2.Request(url,headers=headers)
        response = urllib2.urlopen(request)
        html = response.read()
        return html

    def get_content(self):
        jsonobj = json.loads(self.get_html())
        # 商品名称
        namelist = jsonpath.jsonpath(jsonobj, '$..title')
        # 商品价格
        pricelist = jsonpath.jsonpath(jsonobj, '$..promotionPrice')
        # 商品图片
        imglist = jsonpath.jsonpath(jsonobj, '$..img')
        listdata = zip(imglist,namelist,pricelist)



        for item in listdata:
            # print(item[1])
            try:
                result = self.cursor.execute(
                    "insert into myduodian_aiduodian (image,goodName,price) VALUES (%s,%s,%s)",[item[0],item[1],item[2]])
                self.db.commit()
                print(result)
            except Exception as e:
                self.db.rollback()
                print('失败')

        # 关闭连接，释放资源
        self.db.close()


if __name__ == "__main__":
    duodian = DuoDian()
    duodian.get_content()