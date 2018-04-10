#coding=utf8
import os
import pickle
from email.header import Header
from email.utils import parseaddr, formataddr

import wechatsogou
import urllib2
import lxml.etree
import os
import pymysql
import json

# 添加一个文件，将已经发送成功的文章标题序列化到文件，防止多次运行导致重复发送邮件
file_path = 'sent_articles_file'

# 一些敏感词，简单过滤一下
sensitive_words = ['鄙视链', '中奖名单', '成功说一口流利英语', '婚姻', '恋爱']

ws_api = wechatsogou.WechatSogouAPI()

# 连接数据库
tablename = 'pythonwechat'
db = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='itchat', charset='utf8')
cur = db.cursor()
cur.execute('USE itchat')

# 获取公众号文章信息
def get_article(gzh):
    articles = ws_api.get_gzh_article_by_history(gzh)
    print(len(articles['article']))
    return articles['article']

# 设置下编码
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


# 获取网页内容
def get_html(url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    html = response.read()
    return html

# 下载图片
def get_image(title,imgArray,source,time):
    if os.path.isdir('./imgs'):
        pass
    else:
        os.mkdir("./imgs")
    for item in imgArray:
        with open('imgs/' + (item)[-30:].replace('/','-') + ".png", 'a+') as file:
            file.write(get_html(item))
            file.close

cur.execute(
            'INSERT INTO ' + tablename + ' (title, img,source,time) VALUES (%s, %s,%s, %s)',
            (title[0].strip().replace("\n", ""), json.dumps(imgArray, ensure_ascii=False),source[0].strip().replace("\n", ""),time[0].strip().replace("\n", "")))
cur.connection.commit()
print title[0]
print("------------------------  插入成功  ----------------------------------")

# 连接数据库
def get_connect():
    
    try:
        # 创建表
        cur.execute(
                    'CREATE TABLE ' + tablename + ' (id BIGINT(7) NOT NULL AUTO_INCREMENT, title VARCHAR(1000), img VARCHAR(1000), source VARCHAR(1000), time VARCHAR(1000), created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(id))')
    except pymysql.err.InternalError as e:
        print(e)
    # 修改表字段
    cur.execute('ALTER DATABASE itchat CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci')
    cur.execute(
                'ALTER TABLE ' + tablename + ' CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
cur.execute(
            'ALTER TABLE ' + tablename + ' CHANGE title title VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
    cur.execute(
                'ALTER TABLE ' + tablename + ' CHANGE img img VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
                cur.execute(
                            'ALTER TABLE ' + tablename + ' CHANGE source source VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
                cur.execute(
                            'ALTER TABLE ' + tablename + ' CHANGE time time VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')


if '__main__' == __name__:
    # 热登录(在一段时间内不用扫码登录还能保持登录状态)
    get_connect()
    print "哈哈"
    
    # 定义一个公众号列表
    gzh_list = ['技术最前线', 'python', '全民独立经纪人', '程序视界', '非著名程序员']
    
    # 指定邮箱列表，这里有个建议，请邮件列表中将发件人添加到白名单，降低发送的失败率
    mail_list = ['2281075105@qq.com','lb2281075105@126.com']
    for gzh in gzh_list:
        # 查找公众号之前，先从文件中反序列化出已经成功发送的文章列表
        if os.path.exists(file_path):
            f = open(file_path, 'rb')
            sent_list = pickle.load(f)
            f.close()
        articles = get_article(gzh)
        for article in articles:
            print(article['title'],'\n\t' ,article['content_url'])
            
            xmlcontent = lxml.etree.HTML(get_html(article['content_url']))
            title = xmlcontent.xpath('//h2[@class="rich_media_title"]/text()')
            imgArray = xmlcontent.xpath('//img[@data-type="png"]/@data-src')
            # 来源
            source = xmlcontent.xpath(
                                      '//span[@class="rich_media_meta rich_media_meta_text rich_media_meta_nickname"]/text()')
                                      time = xmlcontent.xpath('//em[@class="rich_media_meta rich_media_meta_text"]/text()')
                                      print "来源"
                                      print source, time
                                      # 下载图片
                                      print "下载图片"
                                      # print imgArray
                                      # print title[0]
            get_image(title, imgArray, source, time)

