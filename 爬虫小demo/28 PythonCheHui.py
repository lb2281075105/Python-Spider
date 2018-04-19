#coding=utf-8

# 微信，找回好友、群聊用户撤回的消息
# 说明：可以撤回的有文本文字、语音、视频、图片、位置、名片、分享、附件

import itchat
from itchat.content import *
import sys
import time
import re
import os

reload(sys)
sys.setdefaultencoding('utf8')

msg_information = {}
# 针对表情包的内容
face_bug = None

@itchat.msg_register([TEXT,PICTURE,FRIENDS,CARD,MAP,SHARING,RECORDING,ATTACHMENT,VIDEO],isFriendChat=True,isGroupChat=True)
def receive_msg(msg):
    global face_bug
    # 接收消息的时间
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if msg.has_key('ActualNickName'):
        # 群消息的发送者,用户的唯一标识
        from_user = msg['ActualUserName']
        # 发送者群内的昵称
        msg_from = msg['ActualNickName']
        # 获取所有好友
        friends = itchat.get_friends(update=True)
        for f in friends:
            # 如果群消息是好友发的
            if from_user == f['UserName']:
                # 优先使用好友的备注名称，没有则使用昵称
                if f['RemarkName']:
                    msg_from = f['RemarkName']
                else:
                    msg_from = f['NickName']
                break
        # 获取所有的群
        groups = itchat.get_chatrooms(update=True)
        for g in groups:
            # 根据群消息的FromUserName匹配是哪个群
            if msg['FromUserName'] == g['UserName']:
                group_name = g['NickName']
                group_menbers = g['MemberCount']
                break
        group_name = group_name + "(" + str(group_menbers) +")"
    else:
        # 优先使用备注名称
        if itchat.search_friends(userName=msg['FromUserName'])['RemarkName']:
            msg_from = itchat.search_friends(userName=msg['FromUserName'])['RemarkName']
        else:
            # 在好友列表中查询发送信息的好友昵称
            msg_from = itchat.search_friends(userName=msg['FromUserName'])['NickName']
        group_name = ""
    # 信息发送的时间
    msg_time = msg['CreateTime']
    # 每条信息的id
    msg_id = msg['MsgId']
    # 储存信息的内容
    msg_content = None
    # 储存分享的链接，比如分享的文章和音乐
    msg_share_url = None
    # 如果发送的消息是文本或者好友推荐
    if msg['Type'] == 'Text' or msg['Type'] == 'Friends':
        msg_content = msg['Text']

    # 如果发送的消息是附件、视频、图片、语音
    elif msg['Type'] == "Attachment" or msg['Type'] == "Video" \
        or msg['Type'] == 'Picture' \
        or msg['Type'] == 'Recording':
        # 内容就是他们的文件名
        msg_content = msg['FileName']
        # 下载文件
        msg['Text'](str(msg_content))
    # 如果消息为分享的位置信息
    elif msg['Type'] == 'Map':
        x, y, location = re.search(
                                   "<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1, 2, 3)
                                   if location is None:
                                       # 内容为详细的地址
                                       msg_content = r"纬度->" + x.__str__() + " 经度->" + y.__str__()
                                   else:
                                       msg_content = r"" + location
# 如果消息为分享的音乐或者文章，详细的内容为文章的标题或者是分享的名字
elif msg['Type'] == 'Sharing':
    msg_content = msg['Text']
    # 记录分享的url
        msg_share_url = msg['Url']
    face_bug = msg_content
    # 将信息存储在字典中，每一个msg_id对应一条信息
    msg_information.update(
                           {
                           msg_id: {
                           "msg_from": msg_from,
                           "msg_time": msg_time,
                           "msg_time_rec": msg_time_rec,
                           "msg_type": msg["Type"],
                           "msg_content": msg_content,
                           "msg_share_url": msg_share_url,
                           "group_name":group_name
                           }
                           }
                           )

# 监听是否有消息撤回
# 使用下面的装饰器监听，会发送4条消息
# @itchat.msg_register(NOTE,isFriendChat=True,isGroupChat=True,isMpChat=True)

# 监听是否有消息撤回
# 使用下面的装饰器监听，会发送1条消息
@itchat.msg_register(NOTE)
def information(msg):
    # 这里如果这里的msg['Content']中包含消息撤回和id，就执行下面的语句
    if '撤回了一条消息' in msg['Content']:
        # 在返回的content查找撤回的消息的id
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
        # 获取到消息原文
        old_msg = msg_information.get(old_msg_id)
        # 如果发送的是表情包
        if len(old_msg_id)<11:
            # 发送撤回的提示给文件助手
            itchat.send_file(face_bug,toUserName='filehelper')
        # 把暂时存储的信息可以删除掉,也可以选择不删除
        # os.remove(face_bug)
        else:
            msg_body = old_msg.get('group_name') + old_msg.get('msg_from') +"\n" + old_msg.get('msg_time_rec') \
                + "撤回了:" + "\n" + r"" + old_msg.get('msg_content')
            
            # 如果是分享的文件被撤回了，那么就将分享的url加在msg_body中发送给文件助手
            if old_msg['msg_type'] == "Sharing":
                msg_body += "\n链接是:" + old_msg.get('msg_share_url')
            print msg_body
            # 将撤回消息发给文件助手
            itchat.send_msg(msg_body, toUserName='filehelper')
            
            # 有文件的话也要将文件发送回去
            if old_msg["msg_type"] == "Picture" \
                or old_msg["msg_type"] == "Recording" \
                or old_msg["msg_type"] == "Video" \
                or old_msg["msg_type"] == "Attachment":
                file = '@fil@%s' % (old_msg['msg_content'])
                itchat.send(msg=file, toUserName='filehelper')
                # 把暂时存储的信息可以删除掉,也可以选择不删除
                os.remove(old_msg['msg_content'])
            # 删除字典旧消息
    msg_information.pop(old_msg_id)

itchat.auto_login(hotReload=True)
itchat.run()
