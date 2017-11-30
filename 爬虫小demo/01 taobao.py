from urllib import request, parse, error
import json
import os
import pymysql
import ssl
# 请求链接需要设置ssl认证
ssl._create_default_https_context = ssl._create_unverified_context


class TaoBao():

    def __init__(self):
        # 设置头部
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        # 设置get参数
        self.params = {'_input_charset': 'utf-8',
                  'q': '',
                  'viewFlag': 'A',
                  'sortType': 'default',
                  'searchStyle': '',
                  'searchRegion': 'city',
                  'searchFansNum': '',
                  'currentPage': '',
                  'pageSize': '20'
                  }
        self.url = 'https://mm.taobao.com/tstar/search/tstar_model.do'


    def get_connect(self):

        self.tablename = 'taobao'
        self.db = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='test', charset='utf8')
        self.cur = self.db.cursor()
        self.cur.execute('USE test')
        try:
            # 创建表
            self.cur.execute('CREATE TABLE '+self.tablename+' (id BIGINT(7) NOT NULL AUTO_INCREMENT, name VARCHAR(100), city VARCHAR(20), height VARCHAR(10), weight VARCHAR(10), homepage VARCHAR(100), profile VARCHAR(100), pic VARCHAR(100), created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(id))')
        except pymysql.err.InternalError as e:
            print(e)
        # 修改表字段
        self.cur.execute('ALTER DATABASE test CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci')
        self.cur.execute('ALTER TABLE '+self.tablename+' CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        self.cur.execute('ALTER TABLE '+self.tablename+' CHANGE name name VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        self.cur.execute('ALTER TABLE '+self.tablename+' CHANGE city city VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        self.cur.execute('ALTER TABLE '+self.tablename+' CHANGE height height VARCHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        self.cur.execute('ALTER TABLE '+self.tablename+' CHANGE weight weight VARCHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        self.cur.execute('ALTER TABLE '+self.tablename+' CHANGE homepage homepage VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        self.cur.execute('ALTER TABLE '+self.tablename+' CHANGE profile profile VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        self.cur.execute('ALTER TABLE '+self.tablename+' CHANGE pic pic VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')

    def insert_table(self,name, city, height, weight, hompage, profile, pic):
        self.cur.execute('INSERT INTO '+self.tablename+' (name, city, height, weight, homepage, profile, pic) VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")', (name, city, height, weight, hompage, profile, pic))
        self.cur.connection.commit()


    def get_html(self,page):
        self.params['currentPage'] = str(page)
        # urlencode可以把字典=键值对编码成url地址中get参数
        self.param = parse.urlencode(self.params).encode('utf-8')
        # data=self.param 上传参数
        req = request.Request(self.url, data=self.param, headers=self.headers)
        content = request.urlopen(req)
        content = json.loads(content.read().decode('gbk'))
        if content['status'] == -1:
            return -1

        return content

    def parser_json(self,content, page):
        meinvist = []
        # 解析json数据
        data = content['data']['searchDOList']
        for list in data:
            temp = {}
            temp['id'] = str(list['userId'])
            temp['name'] = list['realName']
            temp['city'] = list['city']
            temp['height'] = str(list['height'])
            temp['weight'] = str(list['weight'])
            temp['favornum'] = str(list['totalFavorNum'])
            temp['profile'] = 'http:'+list['avatarUrl']
            temp['pic'] = 'http:'+list['cardUrl']

            # meinvist.append(temp)
            self.mkdir(temp['name'])
            print('%s正在抓取%s'%(page, temp['name']))
            self.get_img(temp['profile'], temp['name'], 'profile')
            self.get_img(temp['pic'], temp['name'], 'pic')
            if not os.path.exists('./'+temp['name']+'/info.txt'):
                with open('./'+temp['name']+'/info.txt', 'w') as f:
                    f.write(temp['name']+'\n')
                    f.write(temp['city']+'\n')
                    f.write(temp['height']+'\n')
                    f.write(temp['weight']+'\n')
            # 插入数据库
            self.insert_table(temp['name'], temp['city'], temp['height'], temp['weight'], 'https://mm.taobao.com/self/aiShow.htm?userId='+temp['id'], temp['profile'], temp['pic'])
        # return meinvist

    # 判断文件夹是否存在
    def mkdir(self,path):
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            print('目录已存在！')

    # 判断文件是否存在
    def get_img(self,url, path, name):
        if os.path.exists('./' + path + '/' + name + '.jpg'):
            print('文件已存在！')
            return 0
        try:
            req = request.Request(url, headers=self.headers)
            reponse = request.urlopen(req)
            get_img = reponse.read()
            with open('./' + path + '/' + name + '.jpg', 'wb') as fp:
                fp.write(get_img)
            # 也可以用一下代码实现图片的下载
            # request.urlretrieve(img, './' + path + '/' + name + '.jpg')
        except error.URLError as e:
            print(e.reason)



if __name__ == '__main__':
    page = 1
    taobao = TaoBao()
    taobao.get_connect()
    while True:
        content = taobao.get_html(page)
        if content == -1:
            print('抓取完毕！')
            exit()
        # 解析json
        taobao.parser_json(content, page)
        page += 1
