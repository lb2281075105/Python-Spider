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

# 爬取微信群或者是好友分享的文章
# 监听微信公众号分享的文章
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
                        source = xmlcontent.xpath('//span[@class="rich_media_meta rich_media_meta_text rich_media_meta_nickname"]/text()')
                        time = xmlcontent.xpath('//em[@class="rich_media_meta rich_media_meta_text"]/text()')
                        print "来源"
                            print source, time
                                # 下载图片
                                print "下载图片"
                                    # print imgArray
                                    # print title[0]
                                    get_image(title, imgArray, source, time,msg["Url"])
                                
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

                                                            # return msg['Text']
                                                            # itchat.send('%s: %s : %s' % (msg['Type'], msg['Text'],msg['Url']), msg['FromUserName'])
                                                            print "lalallala"
                                                                # 获取到的信息是某某人和登录者之间的通讯，如果不是和登录这通讯就获取不到
                                                                print itchat.search_friends(userName=msg['FromUserName'])['NickName']
                                                                print itchat.search_friends(userName=msg['ToUserName'])['NickName']
                                                                    
                                                                    else:
                                                                        print "不是个人分享的文章"


# 处理群聊消息
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=True)
def text_reply(msg):
    print msg
    if msg["MsgType"] == 49:
        print "群聊分享文章地址链接Url:" + "---------------------------"
        print msg["Url"]
        
        xmlcontent = lxml.etree.HTML(get_html(msg["Url"]))
        title = xmlcontent.xpath('//h2[@class="rich_media_title"]/text()')
        imgArray = xmlcontent.xpath('//img[@data-type="png"]/@data-src')
        # 来源
        source = xmlcontent.xpath('//span[@class="rich_media_meta rich_media_meta_text rich_media_meta_nickname"]/text()')
        time = xmlcontent.xpath('//em[@class="rich_media_meta rich_media_meta_text"]/text()')
        print "来源"
        print source,time
        # 下载图片
        print "下载图片"
        # print imgArray
        # print title[0]
        get_image(title,imgArray,source,time,msg["Url"])
        
        print "群聊分享文章类型编号MsgType:" + "---------------------------"
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
        print "lalallala群"
        # itchat.send('%s: %s : %s' % (msg['Type'], msg['Text'], msg['Url']), msg['FromUserName'])
        
        print msg['FromUserName']
        print msg['ToUserName']
        
        receiver = "@123c6bbefef9d63462d989f117152dd0d05e0fe94c82a273ea4238a170eb0862"
        # "@@df97b8b54074a1c5af029d9f637f2bbc58eb796126285a0c22cb450ac912ff7f"
        if msg['FromUserName'] == receiver:
            print "----------- 自己在群里发的文章 ------------"
            # 自己在群里发的文章
            print "昵称:"
            print msg['ActualNickName']
            print " ----------- "
            print "群名称:"
            print itchat.search_chatrooms(userName=msg['ToUserName'])['NickName']
            chatRoomName = "呵呵各地"
            if itchat.search_chatrooms(userName=msg['ToUserName'])['NickName'] == chatRoomName:
                pass
            else:
                pass
    
        else:
            # 群友发的文章
            print "----------- 群友发的文章 -----------"
            print "昵称:"
            print msg['ActualNickName']
            print " ----------- "
            print "群名称:"
            print itchat.search_chatrooms(userName=msg['FromUserName'])['NickName']
            chatRoomName = "呵呵各地"
            if itchat.search_chatrooms(userName=msg['FromUserName'])['NickName'] == chatRoomName:
                pass
            else:
                pass
else:
    print "不是群聊分享的文章"
# return msg['Text']


# 处理微信公众号消息
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isMpChat=True)
def text_reply(msg):
    print msg
    print itchat.search_mps(name='PythonCoder')
    if msg["MsgType"] == 49:
        print "监听到制定微信公众号分享的文章链接："
        print msg["Url"]
    else:
        print "微信公众号分享的不是文章"

# 获取网页内容
def get_html(url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    html = response.read()
    return html

# 下载图片
def get_image(title,imgArray,source,time,linkurl):
    print "标题"
    result = cur.execute("select url from pythonitchat WHERE url='"+ linkurl + "'")
    print(str(result) + '------------url-----------')
    
    if result:
        print("数据库里面存在此数据")
    else:
        if os.path.isdir('./imgs'):
            pass
        else:
            os.mkdir("./imgs")
        for item in imgArray:
            with open('imgs/' + (item)[-30:].replace('/','-') + ".png", 'a+') as file:
                file.write(get_html(item))
                file.close

cur.execute(
            'INSERT INTO ' + tablename + ' (title,url, img,source,time) VALUES (%s, %s,%s,%s, %s)',
            (title[0].strip().replace("\n", ""),linkurl, json.dumps(imgArray, ensure_ascii=False),source[0].strip().replace("\n", ""),time[0].strip().replace("\n", "")))
    cur.connection.commit()
    print title[0]
    print("------------------------  插入成功  ----------------------------------")

# 连接数据库
def get_connect():
    
    try:
        # 创建表
        cur.execute(
                    'CREATE TABLE ' + tablename + ' (id BIGINT(7) NOT NULL AUTO_INCREMENT, title VARCHAR(1000),url VARCHAR(10000), img VARCHAR(1000), source VARCHAR(1000), time VARCHAR(1000), created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(id))')
    except pymysql.err.InternalError as e:
        print(e)
    # 修改表字段
    cur.execute('ALTER DATABASE itchat CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci')
    cur.execute(
                'ALTER TABLE ' + tablename + ' CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
cur.execute(
            'ALTER TABLE ' + tablename + ' CHANGE title title VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
    cur.execute(
                'ALTER TABLE ' + tablename + ' CHANGE url url VARCHAR(10000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
                cur.execute(
                            'ALTER TABLE ' + tablename + ' CHANGE img img VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
                cur.execute(
                            'ALTER TABLE ' + tablename + ' CHANGE source source VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
                cur.execute(
                            'ALTER TABLE ' + tablename + ' CHANGE time time VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')


# 热登录(在一段时间内不用扫码登录还能保持登录状态)
get_connect()
print "哈哈"
itchat.auto_login(hotReload=True)
# 绑定消息响应事件后，让itchat运行起来，监听消息
itchat.run()
