# -*- coding:utf-8 -*-

import urllib2,os
import lxml.etree

class Xunmall():
    def __init__(self):
        self.url = "http://www.xunmall.com"

    def get_html(self,p1 = ""):
        # headers = {
        # "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Mobile Safari/537.36"}
        request = urllib2.Request(self.url + p1)
        response = urllib2.urlopen(request)
        html = response.read()
        return html

    def get_xpath(self):
        xmlcontent = lxml.etree.HTML(self.get_html())
        xmllist = xmlcontent.xpath('//h2[@class="floor_name"]/text()')

        for item in xmllist:
            with open('title.txt','a') as file:
                file.write(item.encode('utf-8') + '\n')
                file.close


    def get_image(self):
        xmlimage = lxml.etree.HTML(self.get_html())
        imagelist = xmlimage.xpath('//div[@class="color_top"]/img/@src')
        if os.path.isdir('./imgs'):
           pass
        else:
            os.mkdir("./imgs")
        for item in imagelist:
            # print self.url + item
            with open('imgs/' + (self.url + item)[-8:],'a+') as file:
                file.write(self.get_html(item))
                file.close

    def get_theme(self):
        xmltheme = lxml.etree.HTML(self.get_html())
        themelist = xmltheme.xpath('//h3[@class="floor_theme"]/text()')

        for item in themelist:
            with open('theme.txt','a') as file:
                file.write(item.encode('utf-8') + '\n')
                file.close

        sloganlist = xmltheme.xpath('//p[@class="slogan"]/text()')
        for item in sloganlist:
            with open('theme.txt','a') as file:
                file.write(item.encode('utf-8') + '\n')
                file.close

        give_outlist = xmltheme.xpath('//p[@class="give_out"]/text()')
        for item in give_outlist:
            with open('theme.txt', 'a') as file:
                file.write(item.encode('utf-8') + '\n')
                file.close

    def get_html1(self,p2):
        request = urllib2.Request(p2)
        response = urllib2.urlopen(request)
        html = response.read()
        return html

    # 食品标题和图片
    def foodImageTitle(self):
        foodImage = lxml.etree.HTML(self.get_html())
        foodImageList = foodImage.xpath('//div[@class="pro_image"]/img/@src')

        if os.path.isdir('./foodimage'):
           pass
        else:
            os.mkdir("./foodimage")
        for item in foodImageList:
            # print item
            with open('foodimage/' + item[-20:],'a+') as file:
                file.write(self.get_html1(item))
                file.close

    # 每个零食的详细信息（标题、图片、副标题）
    def detail(self):
        detailLink = lxml.etree.HTML(self.get_html())
        detailLinkList = detailLink.xpath('//div[@class="nth_floor first_floor"]/div[@class="goods_box"]/ul[@class="item_list"]//a/@href')
        for item in detailLinkList:
            # print item[-18:]
            detailUrl = lxml.etree.HTML(self.get_html("/" + item[-18:]))
            detailImageList = detailUrl.xpath(
                '//div[@class="info-panel panel1"]/img/@src')

            for detailitem in detailImageList:
                # print '正在下载详情图片'

                if os.path.isdir('./' + item[-18:-5]):
                    pass
                else:
                    os.mkdir("./" + item[-18:-5])

                with open(item[-18:-5] + '/' + detailitem[-9:], 'a+') as file:
                    file.write(self.get_html1(detailitem))
                    file.close
            # 商品标题
            detailtitleList = detailUrl.xpath(
                '//div[@class="col-lg-7 item-inner"]//h1[@class="fl"]/text()')

            for title in detailtitleList:
                with open('foodtitle.txt', 'a+') as file:
                    file.write(title.encode('utf-8') + '\n')
                    file.close
            # 商品编号
            goodnumberList = detailUrl.xpath(
                '//div[@class="col-lg-7 item-inner"]//li[@class="col-lg-5 col-md-5"]/text()')
            for number in goodnumberList:
                # print number
                if os.path.isdir('./qrcoder'):
                    pass
                else:
                    os.mkdir("./qrcoder")

                with open('qrcoder', 'a+') as file:
                    file.write(number.encode('utf-8') + '\n')
                    file.close


            # 商品二维码:data_code
            coderImageList = detailUrl.xpath('//div[@class="clearfixed"]//div[@class="barcode fr"]/img/@data_code')

            for item in coderImageList:
                # print item
                with open('goodnumber.txt', 'a+') as file:
                    file.write(item + '\n')
                    file.close




if __name__ == "__main__":
    # 获取分类标题
    xunmall = Xunmall()
    # xunmall.get_xpath()
    # 获取图片
    # xunmall.get_image()
    # 图片上面的标题
    # xunmall.get_theme()
    # 休闲食品标题和图片
    # xunmall.foodImageTitle()
    xunmall.detail()