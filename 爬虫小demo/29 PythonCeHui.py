import sys
import os, re, shutil, time, collections, json

from html.parser import HTMLParser
from xml.etree import ElementTree as ETree

import itchat
from itchat.content import *

msg_store = collections.OrderedDict()
timeout = 600
sending_type = {'Picture': 'img', 'Video': 'vid'}
data_path = 'data'
nickname = ''
bot = None

if __name__ == '__main__':
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    # if the QR code doesn't show correctly, you can try to change the value
    # of enableCdmQR to 1 or -1 or -2. It nothing works, you can change it to
    # enableCmdQR=True and a picture will show up.
    bot = itchat.new_instance()
    bot.auto_login(hotReload=True, enableCmdQR=2)
    nickname = bot.loginInfo['User']['NickName']

def clear_timeouted_message():
    now = time.time()
    count = 0
    for k, v in list(msg_store.items()):
        if now - v['ReceivedTime'] > timeout:
            count += 1
        else:
            break
    for i in range(count):
        item = msg_store.popitem(last=False)

def get_sender_receiver(msg):
    sender = nickname
    receiver = nickname
    if msg['FromUserName'][0:2] == '@@': # group chat
        sender = msg['ActualNickName']
        m = bot.search_chatrooms(userName=msg['FromUserName'])
        if m is not None:
            receiver = m['NickName']
    elif msg['ToUserName'][0:2] == '@@': # group chat by myself
        if 'ActualNickName' in msg:
            sender = msg['ActualNickName']
        else:
            m = bot.search_friends(userName=msg['FromUserName'])
            if m is not None:
                sender = m['NickName']
        m = bot.search_chatrooms(userName=msg['ToUserName'])
        if m is not None:
            receiver = m['NickName']
    else: # personal chat
        m = bot.search_friends(userName=msg['FromUserName'])
        if m is not None:
            sender = m['NickName']
        m = bot.search_friends(userName=msg['ToUserName'])
        if m is not None:
            receiver = m['NickName']
    return HTMLParser().unescape(sender), HTMLParser().unescape(receiver)

def print_msg(msg):
    msg_str = ' '.join(msg)
    print(msg_str)
    return msg_str

def get_whole_msg(msg, download=False):
    sender, receiver = get_sender_receiver(msg)
    if len(msg['FileName']) > 0 and len(msg['Url']) == 0:
        if download: # download the file into data_path directory
            fn = os.path.join(data_path, msg['FileName'])
            msg['Text'](fn)
            if os.path.getsize(fn) == 0:
                return []
            c = '@%s@%s' % (sending_type.get(msg['Type'], 'fil'), fn)
        else:
            c = '@%s@%s' % (sending_type.get(msg['Type'], 'fil'), msg['FileName'])
        return ['[%s]->[%s]:' % (sender, receiver), c]
    c = msg['Text']
    if len(msg['Url']) > 0:
        try: # handle map label
            content_tree = ETree.fromstring(msg['OriContent'])
            if content_tree is not None:
                map_label = content_tree.find('location')
                if map_label is not None:
                    c += ' ' + map_label.attrib['poiname']
                    c += ' ' + map_label.attrib['label']
        except:
            pass
        url = HTMLParser().unescape(msg['Url'])
        c += ' ' + url
    return ['[%s]->[%s]: %s' % (sender, receiver, c)]

@bot.msg_register([TEXT, PICTURE, MAP, CARD, SHARING, RECORDING,
    ATTACHMENT, VIDEO, FRIENDS], isFriendChat=True, isGroupChat=True)
def normal_msg(msg):
    print_msg(get_whole_msg(msg))
    now = time.time()
    msg['ReceivedTime'] = now
    msg_id = msg['MsgId']
    msg_store[msg_id] = msg
    clear_timeouted_message()

@bot.msg_register([NOTE], isFriendChat=True, isGroupChat=True)
def note_msg(msg):
    print_msg(get_whole_msg(msg))
    content = HTMLParser().unescape(msg['Content'])
    try:
        content_tree = ETree.fromstring(content)
    except Exception:
        # invent/remove to chatroom
        return
    if content_tree is None:
        return
    revoked = content_tree.find('revokemsg')
    if revoked is None:
        return
    old_msg_id = revoked.find('msgid').text
    old_msg = msg_store.get(old_msg_id)
    if old_msg is None:
        return
    msg_send = get_whole_msg(old_msg, download=True)
    for m in msg_send:
        bot.send(m, toUserName='filehelper')
    clear_timeouted_message()

if __name__ == '__main__':
    bot.run()