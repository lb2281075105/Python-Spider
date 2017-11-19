#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib2
import re

class Spider:
    def __init__(self):
        # 初始化起始页位置
        self.page = 1
        # 爬取开关，如果为True继续爬取
        self.switch = True

    def loadPage(self):
        """
            作用：下载页面
        """
        print "正在下载数据...."
        url = "http://www.neihan8.com/article/list_5_" + str(self.page) + ".html"
        headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        request = urllib2.Request(url, headers = headers)
        response = urllib2.urlopen(request)

        # 获取每页的HTML源码字符串
        html = response.read()
        #print html

        # 创建正则表达式规则对象，匹配每页里的段子内容，re.S 表示匹配全部字符串内容
        pattern = re.compile('<div\sclass="f18 mb20">(.*?)</div>', re.S)

        # 将正则匹配对象应用到html源码字符串里，返回这个页面里的所有段子的列表
        content_list = pattern.findall(html)

        # 调用dealPage() 处理段子里的杂七杂八
        self.dealPage(content_list)

    def dealPage(self, content_list):
        """
            处理每页的段子
            content_list : 每页的段子列表集合
        """
        for item in content_list:
            # 将集合里的每个段子按个处理，替换掉无用数据
            item = item.replace("<p>","").replace("</p>", "").replace("<br>", "")
            #print item.decode("gbk")
            # 处理完后调用writePage() 将每个段子写入文件内
            self.writePage(item)

    def writePage(self, item):
        """
            把每条段子逐个写入文件里
            item: 处理后的每条段子
        """
        # 写入文件内
        print "正在写入数据...."
        with open("duanzi.txt", "a") as f:
            f.write(item)

    def startWork(self):
        """
            控制爬虫运行
        """
        # 循环执行，直到 self.switch == False
        while self.switch:
            # 用户确定爬取的次数
            self.loadPage()
            command = raw_input("如果继续爬取，请按回车（退出输入quit)")
            if command == "quit":
                # 如果停止爬取，则输入 quit
                self.switch = False
            # 每次循环，page页码自增1
            self.page += 1
        print "谢谢使用！"


if __name__ == "__main__":
    duanziSpider = Spider()
#    duanziSpider.loadPage()
    duanziSpider.startWork()

