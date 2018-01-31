# -*- coding:utf-8 -*-

import urllib2
import lxml.etree
class Login():
    def __init__(self):
        self.url = "https://www.zhihu.com/#signin"

    def get_html(self):
        # headers = {
        # "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Mobile Safari/537.36"}
        request = urllib2.Request(self.url)
        response = urllib2.urlopen(request)
        html = response.read()
        return html

    def get_xpath(self):
        # print self.get_html()
        xmlcontent = lxml.etree.HTML(self.get_html())
        xmllist = xmlcontent.xpath('//div[@class="view view-signin"]/form/input/@value')

        for item in xmllist:
            print item
            with open('title.txt','a') as file:
                file.write(item.encode('utf-8') + '\n')
                file.close


if __name__ == "__main__":
    login = Login()
    login.get_xpath()