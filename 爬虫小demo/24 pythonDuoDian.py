# 优鲜蔬菜
# 1、共页爬取所有商品
# 2、通过商品skuId获取商品详情页面
# 3、用到动态获取商品信息selenium，自动化

# 商品列表原链接：https://gatewx.dmall.com/customersite/searchWareByCategory?param=%7B%22pageNum%22%3A1%2C%22pageSize%22%3A30%2C%22venderId%22%3A%221%22%2C%22storeId%22%3A%22108%22%2C%22sort%22%3A%221%22%2C%22categoryId%22%3A11346%2C%22categoryLevel%22%3A3%2C%22cateSource%22%3A1%2C%22bizType%22%3A%221%22%7D&token=&source=2&tempid=C7C148906AA000022AB812DF113D9500&pubParam=%7B%22utmSource%22%3A%22wxmp%22%7D&_=1512218030903
# 商品列表url解码后连接：https://gatewx.dmall.com/customersite/searchWareByCategory?param={"pageNum":1,"pageSize":30,"venderId":"1","storeId":"108","sort":"1","categoryId":11346,"categoryLevel":3,"cateSource":1,"bizType":"1"}&token=&source=2&tempid=C7C148906AA000022AB812DF113D9500&pubParam={"utmSource":"wxmp"}&_=1512218030903

# https://i.dmall.com/?source_id=wxmp#item/view/item/item:id=1-108-11348
# 商品详情有 --- 轮播图、猜你喜欢图片、商品宣传图
from  urllib import request
import os
import json
import jsonpath
import time
import ssl
from selenium import webdriver
import pymysql
from lxml import etree
ssl._create_default_https_context = ssl._create_unverified_context

class FreshVegetable():
    def __init__(self,page):
        # 爬取分类修改修改：商品列表地址、商品详情地址、存储的商品分类id=11347
        self.url =  'https://gatewx.dmall.com/customersite/searchWareByCategory?param={"pageNum":' + str(page) + ',"pageSize":64,"venderId":"1","storeId":"108","sort":"1","categoryId":11346,"categoryLevel":3,"cateSource":1,"bizType":"1"}&token=&source=2&tempid=C7C148906AA000022AB812DF113D9500&pubParam={"utmSource":"wxmp"}&_=1512218030903'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0)'}
        self.detailurl = 'https://i.dmall.com/?source_id=wxmp#item/view/item/item:id=1-108-'
        if page == 1:
            self.get_connect()

    def get_connect(self):

        self.tablename = 'duodian'
        self.db = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='sys', charset='utf8')
        self.cur = self.db.cursor()
        self.cur.execute('USE sys')
        try:
            # 创建表
            self.cur.execute(
                'CREATE TABLE ' + self.tablename + ' (id BIGINT(7) NOT NULL AUTO_INCREMENT, title VARCHAR(1000), img VARCHAR(1000), lunfanimg VARCHAR(1000), spec VARCHAR(1000), xcimg VARCHAR(1000), skuid VARCHAR(1000),pimg VARCHAR(1000), plunfanimg VARCHAR(1000),pxcimg VARCHAR(1000) ,categoryid VARCHAR(1000),price VARCHAR(1000),brandname VARCHAR(1000),categoryname VARCHAR(1000),created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(id))')
        except pymysql.err.InternalError as e:
            print(e)
        # 修改表字段
        self.cur.execute('ALTER DATABASE sys CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci')
        self.cur.execute(
            'ALTER TABLE ' + self.tablename + ' CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        self.cur.execute(
            'ALTER TABLE ' + self.tablename + ' CHANGE title title VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        self.cur.execute(
            'ALTER TABLE ' + self.tablename + ' CHANGE img img VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        self.cur.execute(
            'ALTER TABLE ' + self.tablename + ' CHANGE lunfanimg lunfanimg VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        self.cur.execute(
            'ALTER TABLE ' + self.tablename + ' CHANGE spec spec VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        self.cur.execute(
            'ALTER TABLE ' + self.tablename + ' CHANGE xcimg xcimg VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        self.cur.execute(
            'ALTER TABLE ' + self.tablename + ' CHANGE skuid skuid VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        # 存储本地
        self.cur.execute(
            'ALTER TABLE ' + self.tablename + ' CHANGE pimg pimg VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        self.cur.execute(
            'ALTER TABLE ' + self.tablename + ' CHANGE plunfanimg plunfanimg VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        self.cur.execute(
            'ALTER TABLE ' + self.tablename + ' CHANGE pxcimg pxcimg VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        self.cur.execute(
            'ALTER TABLE ' + self.tablename + ' CHANGE categoryid categoryid VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        self.cur.execute(
            'ALTER TABLE ' + self.tablename + ' CHANGE price price VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        self.cur.execute(
            'ALTER TABLE ' + self.tablename + ' CHANGE brandname brandname VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        self.cur.execute(
            'ALTER TABLE ' + self.tablename + ' CHANGE categoryname categoryname VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')

    def get_html(self):
        req = request.Request(self.url,headers=self.headers)
        response = request.urlopen(req)
        html = response.read()
        return html

    def get_mkdir(self):
        jsonobj = json.loads(self.get_html().decode('utf-8'))
        # 列表页 - 图片
        imgList = jsonpath.jsonpath(jsonobj, '$..img')
        # 列表页 - 价格
        pricelist = jsonpath.jsonpath(jsonobj, '$..price')
        # 列表页 - 商品名
        titleList = jsonpath.jsonpath(jsonobj, '$..title')
        # 列表页 - 商品id -- skuId
        skuIdList = jsonpath.jsonpath(jsonobj, '$..promotionInfo.skuId')
        # 商品价格
        priceList = jsonpath.jsonpath(jsonobj, '$..price')
        # 商品品牌
        brandList = jsonpath.jsonpath(jsonobj, '$..brandName')
        # 商品分类
        categoryList = jsonpath.jsonpath(jsonobj, '$..thirdCatName')
        listdata = zip(titleList, imgList, pricelist,skuIdList,priceList,brandList,categoryList)

        for item in listdata:

            print(item)

            # 替换'/'
            import re
            strinfo = re.compile('/')
            itemdir = strinfo.sub('-', item[0])
            print(itemdir)
            time.sleep(1)
            # 商品名称目录
            if not os.path.exists(itemdir):
                os.makedirs(itemdir)
            else:
                print(itemdir + ' -- 目录已存在！')
            self.dataurl = ''
            # 存储本地主页图片链接地址
            self.pimg = ''
            # 列表页 - 图片

            # 文件夹和文件命名不能出现这9个字符：/ \ : * " < > | ？

            if os.path.exists( itemdir + '/' + item[1][-20:].replace('/','-').replace('\\','-').replace(':','-').replace('*','-').replace('"','-').replace('<','-').replace('>','-').replace('|','-').replace('?','-') + '.webp'):
                print('文件已存在！')
                # return 0
            else:

                if item[1].startswith('//'):
                    self.dataurl = "http:" + item[1]
                else:
                    self.dataurl = item[1]
                try:
                    req = request.Request(self.dataurl, headers=self.headers)
                    reponse = request.urlopen(req)
                    get_img = reponse.read()
                    self.pimg = '/pimgs/' + itemdir + '/' + self.dataurl[-20:].replace('/','-').replace('\\','-').replace(':','-').replace('*','-').replace('"','-').replace('<','-').replace('>','-').replace('|','-').replace('?','-') + '.webp'
                    with open( itemdir + '/' + self.dataurl[-20:].replace('/','-').replace('\\','-').replace(':','-').replace('*','-').replace('"','-').replace('<','-').replace('>','-').replace('|','-').replace('?','-') + '.webp', 'wb') as fp:
                        fp.write(get_img)
                except Exception as e:
                    print(e)
            # 详情目录
            if not os.path.exists(itemdir  + '/详情'):
                os.makedirs(itemdir  + '/详情')
            else:
                print('详情' + ' -- 目录已存在！')
            driver = webdriver.PhantomJS(executable_path='./phantomjs-2.1.1-macosx/bin/phantomjs')
            time.sleep(5)
            driver.get(self.detailurl + str(item[3]))
            time.sleep(5)
            driver.find_element_by_class_name('tipinfo').click()
            time.sleep(5)
            html = etree.HTML(driver.page_source)
            imglist = html.xpath('//img/@src')
            print(self.detailurl + str(item[3]))
            # 轮番图
            lunfantu = html.xpath('//img[@class="detail-img"]/@src')
            # 猜你喜欢
            # like = html.xpath('//img[@class="J_ItemImage recommend-img"]/@src')
            # 商品宣传图
            xuanchuan = html.xpath('//div[@class="J_descriptionDetail parameter"]//img/@src')
            # 规格
               # 左边的参数名
            leftspec = html.xpath('//div[@class="left attr_key border-1px border-r border-b"]/text()')
               # 右边的参数值
            rightspec = html.xpath('//div[@class="left attr_value border-1px border-b"]/span/text()')
            spec = zip(leftspec,rightspec)
            # time.sleep(5)
            # print(driver.page_source)
            print(str(item[3]))
            print("-------------------------- 轮播图 --------------------------------")
            print(lunfantu)
            print("--------------------------- 规格 ---------------------------------")
            print(spec)
            print("-------------------------- 介绍图 ---------------------------------")
            print(xuanchuan)
            print("-------------------------- 主页图 ---------------------------------")
            print(self.dataurl)

            for simple in imglist:
                if not os.path.exists( itemdir + '/详情/' + simple[-20:].replace('/','-').replace('\\','-').replace(':','-').replace('*','-').replace('"','-').replace('<','-').replace('>','-').replace('|','-').replace('?','-') + '.webp'):
                    request.urlretrieve(simple, itemdir +  '/详情' + '/' + simple[-20:].replace('/','-').replace('\\','-').replace(':','-').replace('*','-').replace('"','-').replace('<','-').replace('>','-').replace('|','-').replace('?','-') + ".webp")
                    print("正在下载......")
                else:
                    print('文件已存在！')

                #     NOT
                #     NULL
                #     AUTO_INCREMENT, title
                #     VARCHAR(1000), img
                #     VARCHAR(1000), lunfanimg
                #     VARCHAR(1000), spec
                #     VARCHAR(1000), xcimg
                #     VARCHAR(1000),
            # 插入数据库l
           # 判断数据库是否有skuId，有就不插入，无则插入

            result = self.cur.execute("select skuid from duodian WHERE skuid=" + str(item[3]))
            print(str(result) + '-----------------------')


            if result:
                print("数据库里面存在此数据")
            else:
                # 不存在，存数据
                lunfantu1 = {}
                specpagram ={}
                xuanchuan1 = {}
                # 轮番图
                for index1, item1 in enumerate(lunfantu):
                    lunfantu1[index1] = item1
                # 规格
                speckey = 0
                for itemspec in spec:
                    specvalue = str(itemspec[0]) + '-' + str(itemspec[1])
                    specpagram[str(speckey)] = specvalue
                    speckey += 1
                # 介绍图
                for index3, item3 in enumerate(xuanchuan):
                    xuanchuan1[index3] = item3
                # 存储本地图片链接地址
                plunfantu = {}
                pxuanchuan = {}
                for pindex1, pitem1 in enumerate(lunfantu):
                    plunfantu[pindex1] = '/pimgs/' + itemdir + '/详情/' + pitem1[-20:].replace('/','-').replace('\\','-').replace(':','-').replace('*','-').replace('"','-').replace('<','-').replace('>','-').replace('|','-').replace('?','-') + '.webp'
                for pindex2, pitem2 in enumerate(xuanchuan):
                    pxuanchuan[pindex2] = '/pimgs/' + itemdir + '/详情/' + pitem2[-20:].replace('/','-').replace('\\','-').replace(':','-').replace('*','-').replace('"','-').replace('<','-').replace('>','-').replace('|','-').replace('?','-') + '.webp'
                self.cur.execute(
                'INSERT INTO ' + self.tablename + ' (title, img, lunfanimg, spec, xcimg,skuid,pimg, plunfanimg, pxcimg,categoryid,price,brandname,categoryname) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s,%s)',
                (itemdir, self.dataurl, json.dumps(lunfantu1,ensure_ascii=False), json.dumps(specpagram,ensure_ascii=False), json.dumps(xuanchuan1,ensure_ascii=False),str(item[3]),self.pimg,json.dumps(plunfantu,ensure_ascii=False),json.dumps(pxuanchuan,ensure_ascii=False),'11346','%.2f'%(item[4]/100),str(item[5]),str(item[6])))
                self.cur.connection.commit()
                print("------------------------  插入成功  ----------------------------------")

if __name__ == "__main__":

    for page in range(1,3):
        freshVegetable = FreshVegetable(page)
        freshVegetable.get_mkdir()
        print(" -- 爬取完毕 -- ")

