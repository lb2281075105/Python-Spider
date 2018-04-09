#coding=utf-8

import itchat
# import全部消息类型
from itchat.content import *
# 处理个人分享消息
# 包括文本、位置、名片、通知、分享(49重点)
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
  # 微信里，每个用户和群聊，都使用很长的ID来区分
  if msg["MsgType"] == 49:
      print "个人分享文章地址链接Url:" + "---------------------------"
      print msg["Url"]
      print "个人分享文章类型编号MsgType:" + "---------------------------"
      print msg["MsgType"]
      print "个人分享Content:" + "---------------------------"
      print msg["Content"]
  else:
      print "不是个人分享的文章"
  # return msg['Text']
  itchat.send('%s: %s : %s' % (msg['Type'], msg['Text'],msg['Url']), msg['FromUserName'])

# 处理群聊消息
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=True)
def text_reply(msg):
    if msg["MsgType"] == 49:
        print "群聊分享文章地址链接Url:" + "---------------------------"
        print msg["Url"]
        print "群聊分享分享文章类型编号MsgType:" + "---------------------------"
        print msg["MsgType"]
        print "群聊分享Content:" + "---------------------------"
        print msg["Content"]
    else:
        print "不是群聊分享的文章"
        # return msg['Text']
    itchat.send('%s: %s : %s' % (msg['Type'], msg['Text'], msg['Url']), msg['FromUserName'])

itchat.auto_login()
# 绑定消息响应事件后，让itchat运行起来，监听消息
itchat.run()