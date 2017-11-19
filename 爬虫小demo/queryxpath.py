# -*- coding:utf-8 -*-

import urllib2
import json
import lxml.etree
# xpath 模糊查询

class XpathQuery():
    def __init__(self):
        self.url = "https://www.qiushibaike.com/"


    def get_html(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0)'}
        request = urllib2.Request(self.url,headers=headers)
        response = urllib2.urlopen(request)
        html = response.read()
        return html

    def get_xpath(self):
        xmlcontent =  lxml.etree.HTML(self.get_html())
        xmllist = xmlcontent.xpath('//div[contains(@id,"qiushi_tag_")]')
        print len(xmllist)
        # 分享的地方
        sharelist = xmlcontent.xpath('//div[@class="article block untagged mb15 typs_recent"]//div[@class="single-share"]/a/@title')
        for item in range(0,4):
            print sharelist[item]

        for item in xmllist:
            # 用户名
            username = item.xpath('.//div[@class="author clearfix"]/a/h2/text()')
            # 标题
            title = item.xpath('.//a/div[@class="content"]/span/text()')[0]

            with open('title.txt','a') as file:
                file.write(title.encode("utf-8"))
                file.close
            with open('username.txt','a') as file:
                if len(username) == 0:
                    file.write("匿名用户")
                else:
                    file.write(username[0].encode("utf-8"))

            # 好笑数
            votecount = item.xpath('.//span[@class="stats-vote"]/i[@class="number"]/text()')[0]
            print "好笑数：" + votecount
            # 评论数
            commentcount = item.xpath('.//span[@class="stats-comments"]//i[@class="number"]/text()')[0]
            print "评论数：" + commentcount
            # 放在一个字典里进行存储
            dic = {
                "username":username,
                "votecount":votecount,
                "commentcount":commentcount,
                "title": title,
            }
            with open('qiushi.json','a') as file:
                file.write(json.dumps(dic,ensure_ascii=False).encode("utf-8") + '\n')
                file.close


if __name__ == "__main__":
    xpathq = XpathQuery()
    xpathq.get_xpath()