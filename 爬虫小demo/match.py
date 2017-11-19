# -*- coding:utf-8 -*-

import re
import urllib2

class Content:

    def __init__(self):
        self.page = 1

    def get_html(self):
        # 获取整个网页的html内容
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Mobile Safari/537.36"}
        url = "http://www.neihan8.com/article/list_5_"+str(self.page)+".html"
        request = urllib2.Request(url=url, headers=headers)
        response = urllib2.urlopen(request)
        html = response.read()
        return html

    def get_content(self):
        pattern = re.compile(r'<div.*?class="f18 mb20">(.*?)</div>', re.S)
        content_list = pattern.findall(self.get_html())
        for content in content_list:
            result_content = content.decode('gbk').replace("<p>", "").replace("</p>", "") \
                .replace("&ldquo;", "").replace("<br />", "") \
                .replace("&rdquo;", "").replace("&hellip", "")

            with open("content.txt", "a") as file:
                file.write(result_content.encode("utf-8"))
                file.close

if __name__ == "__main__":

    content = Content()
    while True:
        content.page+=1
        print content.page
        content.get_content()

"""
r 打开只读文件，该文件必须存在。
r+ 打开可读写的文件，该文件必须存在。
w 打开只写文件，若文件存在则文件长度清为0，即该文件内容会消失。若文件不存在则建立该文件。
w+ 打开可读写文件，若文件存在则文件长度清为零，即该文件内容会消失。若文件不存在则建立该文件。
a 以附加的方式打开只写文件。若文件不存在，则会建立该文件，如果文件存在，写入的数据会被加到文件尾，即文件原先的内容会被保留。
a+ 以附加方式打开可读写的文件。若文件不存在，则会建立该文件，如果文件存在，写入的数据会被加到文件尾后，即文件原先的内容会被保留。
"""