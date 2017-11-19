# -*- coding:utf-8 -*-

import urllib2
import lxml.etree

class GetImage():

    def __init__(self):
        self.tieba = "https://tieba.baidu.com"
        self.count = 50

    def get_html(self,url):
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        html = response.read()
        return html

    def get_xpath(self):
        # 起始页
        baginPage = int(raw_input("请输入起始页："))
        # 结束页
        endPage = int(raw_input("请输入结束页："))
        for pagecount in  range(baginPage,endPage + 1):
            pn = (pagecount - 1) * self.count
            urllink = self.tieba + "/f?kw=%E7%BE%8E%E5%A5%B3&ie=utf-8&pn=" + str(pn)
            xmlcontent = lxml.etree.HTML(self.get_html(urllink))
            # content = xmlcontent.xpath('//div[@class="t_con cleafix"]/div/div/div/a/@href')
            # content = xmlcontent.xpath('//div[@class="threadlist_title pull_left j_th_tit "]//a[@class="j_th_tit "]/@href')
            content = xmlcontent.xpath('//a[@class="j_th_tit "]/@href')

            for item in content:
                itemcontent = lxml.etree.HTML(self.get_html(self.tieba + item))
                print self.tieba + item
                itemlist = itemcontent.xpath('//img[@class="BDE_Image"]//@src')
                for imageitem in itemlist:
                    get_image = self.get_html(imageitem)
                    with open("images/" + imageitem[-10:],'a') as file:
                        file.write(get_image)
                        file.close

if __name__ == "__main__":
    getImages = GetImage()
    getImages.get_xpath()