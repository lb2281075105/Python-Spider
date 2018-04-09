#coding=utf-8
'''
itchat:获取分享给群或者个人的技术文章
(0) 熟悉itchat,(https://www.cnblogs.com/Chenjiabing/p/6907397.html)
(1) itchat 扫码次数太多会被限制扫码登录微信。
(2) itchat:获取分享给群或者个人的技术文章,提取出文章链接、文章标题、文章首页图片、文章内容
(3) 通过获取到的文章链接，爬虫文章内容。
(4) 判断是接收方(ToUserName)是谁、发送方(FromUserName)是谁就是通过唯一的ID来判别的。
(5) python itchat 热登陆(itchat.auto_login(hotReload=True))
(6) xpath模块爬取文章标题、文章内图片
(7) 搭建web服务器环境(Mac使用XAMPP)
(8) pymysql模块自动创建数据库、创建字段、保存内容到字段
(9) navicat 的使用
(10) python 相关模块的使用
'''


import itchat
# import全部消息类型
from itchat.content import *
import urllib2
import lxml.etree
import os
import pymysql
import json

# 连接数据库
tablename = 'pythonitchat'
db = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='itchat', charset='utf8')
cur = db.cursor()
cur.execute('USE itchat')

# 处理个人分享消息
# 包括文本、位置、名片、通知、分享(49重点)
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print msg
        # 微信里，每个用户和群聊，都使用很长的ID来区分
        if msg["MsgType"] == 49:
            print "个人分享文章地址链接Url:" + "---------------------------"
                
                xmlcontent = lxml.etree.HTML(get_html(msg["Url"]))
                print xmlcontent
                    title = xmlcontent.xpath('//h2[@class="rich_media_title"]/text()')

                    imgArray = xmlcontent.xpath('//img[@data-type="png"]/@data-src')
                        # 下载图片
                        print "下载图片"
                            # print imgArray
                            # print title[0]
                            get_image(title,imgArray)

                            print msg["Url"]
                                print "个人分享文章类型编号MsgType:" + "---------------------------"
                                    print msg["MsgType"]
                                    print "个人分享Content:" + "---------------------------"
                                        print msg["Content"]
                                        print "个人分享FromUserName:" + "---------------------------"
                                            print msg["FromUserName"]
                                            print "个人分享ToUserName:" + "---------------------------"
                                                print msg["ToUserName"]
                                                print "个人分享链接标题FileName:" + "---------------------------"
                                                    print msg["FileName"]
                                                        else:
                                                            print "不是个人分享的文章"
                                                                # return msg['Text']
                                                                itchat.send('%s: %s : %s' % (msg['Type'], msg['Text'],msg['Url']), msg['FromUserName'])

# 处理群聊消息
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=True)
def text_reply(msg):
    print msg
    if msg["MsgType"] == 49:
        print "群聊分享文章地址链接Url:" + "---------------------------"
        print msg["Url"]
        
        xmlcontent = lxml.etree.HTML(get_html(msg["Url"]))
        print xmlcontent
        title = xmlcontent.xpath('//h2[@class="rich_media_title"]/text()')
        
        imgArray = xmlcontent.xpath('//img[@data-type="png"]/@data-src')
        # 下载图片
        print "下载图片"
        # print imgArray
        # print title[0]
        get_image(title,imgArray)
        
        print "群聊分享分享文章类型编号MsgType:" + "---------------------------"
        print msg["MsgType"]
        print "群聊分享Content:" + "---------------------------"
        print msg["Content"]
        print "群聊分享FromUserName:" + "---------------------------"
        print msg["FromUserName"]
        print "群聊分享ToUserName:" + "---------------------------"
        print msg["ToUserName"]
        print "群聊分享链接标题FileName:" + "---------------------------"
        print msg["FileName"]
    # print "分享者昵称ActualNickName:" + "---------------------------"
    # print msg["ActualNickName"]
    else:
        print "不是群聊分享的文章"
    # return msg['Text']
    itchat.send('%s: %s : %s' % (msg['Type'], msg['Text'], msg['Url']), msg['FromUserName'])

# 获取网页内容
def get_html(url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    html = response.read()
    return html

# 下载图片
def get_image(title,imgArray):
    if os.path.isdir('./imgs'):
        pass
    else:
        os.mkdir("./imgs")
    for item in imgArray:
        with open('imgs/' + (item)[-30:].replace('/','-') + ".png", 'a+') as file:
            file.write(get_html(item))
            file.close

cur.execute(
            'INSERT INTO ' + tablename + ' (title, img) VALUES (%s, %s)',
            (title[0].strip().replace("\n", ""), json.dumps(imgArray, ensure_ascii=False)))
cur.connection.commit()
print title[0]
print("------------------------  插入成功  ----------------------------------")

# 连接数据库
def get_connect():
    
    try:
        # 创建表
        cur.execute(
                    'CREATE TABLE ' + tablename + ' (id BIGINT(7) NOT NULL AUTO_INCREMENT, title VARCHAR(1000), img VARCHAR(1000), created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(id))')
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

# 热登录(在一段时间内不用扫码登录还能保持登录状态)
get_connect()
print "哈哈"
itchat.auto_login(hotReload=True)
# 绑定消息响应事件后，让itchat运行起来，监听消息
itchat.run()
