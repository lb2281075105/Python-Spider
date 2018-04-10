#coding=utf8
import os
import pickle
from email.header import Header
from email.utils import parseaddr, formataddr

import wechatsogou

# 添加一个文件，将已经发送成功的文章标题序列化到文件，防止多次运行导致重复发送邮件
file_path = 'sent_articles_file'

# 一些敏感词，简单过滤一下
sensitive_words = ['鄙视链', '中奖名单', '成功说一口流利英语', '婚姻', '恋爱']

ws_api = wechatsogou.WechatSogouAPI()

# 获取公众号文章信息
def get_article(gzh):
    articles = ws_api.get_gzh_article_by_history(gzh)
    print(len(articles['article']))
    return articles['article']

# 设置下编码
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


")

if '__main__' == __name__:
    
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

