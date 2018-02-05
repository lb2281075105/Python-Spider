from urllib import request
import re, os, datetime
from selenium import webdriver
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class TaoBaoInfo:
    def __init__(self):
        self.dirName = 'MyTaoBaoInfo'
        self.driver = webdriver.PhantomJS(executable_path='./phantomjs-2.1.1-macosx/bin/phantomjs')
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0)'}

    # 获取页面内容提取
    def getPageContent(self, page):

        url = "https://mm.taobao.com/json/request_top_list.htm?page=" + str(page)
        response = request.Request(url, headers = self.headers)
        response = request.urlopen(response)

        # 正则获取
        pattern_link = re.compile(r'<div.*?class="pic-word">.*?<img src="(.*?)".*?'
                                  r'<a.*?class="lady-name".*?href="(.*?)".*?>(.*?)</a>.*?'
                                  r'<em>.*?<strong>(.*?)</strong>.*?'
                                  r'<span>(.*?)</span>'
                                  , re.S)
        items = re.findall(pattern_link, response.read().decode('gbk'))

        for item in items:
            # 详情页面：头像，个人详情，名字，年龄，地区

            detailPage = item[1]
            name = item[2]
            self.getDetailPage(detailPage, name)

    def getDetailPage(self, url, name):
        url = 'http:' + url
        self.driver.get(url)
        base_msg = self.driver.find_elements_by_xpath('//div[@class="mm-p-info mm-p-base-info"]/ul/li')
        brief = ''
        for item in base_msg:
            print(item.text)
            brief += item.text + '\n'

        icon_url = self.driver.find_element_by_xpath('//div[@class="mm-p-model-info-left-top"]//img')
        icon_url = icon_url.get_attribute('src')
        dir = self.dirName + '/' + name
        self.mkdir(dir)
        # 保存头像
        try:
            self.saveIcon(icon_url, dir, name)
        except Exception as e:
            print(u'保存头像失败 %s' % (e))

        # 开始跳转相册列表
        images_url = self.driver.find_element_by_xpath('//ul[@class="mm-p-menu"]//a')
        images_url = images_url.get_attribute('href')
        try:
            self.getAllImage(images_url, name)
        except Exception as e:
            print(u'获取所有相册异常 %s' % e)

        try:
            self.saveBrief(brief,dir, name)

        except Exception as e:
            print(u'保存个人信息失败 %s' % e)

    # 保存个人信息
    def saveBrief(self, content,dir, name):
        fileName = dir + '/' + name + '.txt'
        with open(fileName,'w+') as file:
            file.write(content)
        print(u'下载完成' + '\n' + '\n')
    # 获取所有图片
    def getAllImage(self, images_url, name):
        self.driver.get(images_url)
        # 只获取第一个相册
        photos = self.driver.find_element_by_xpath('//div[@class="mm-photo-cell-middle"]//h4/a')
        photos_url = photos.get_attribute('href')
        # 进入相册页面获取相册内容
        self.driver.get(photos_url)
        images_all = self.driver.find_elements_by_xpath('//div[@id="mm-photoimg-area"]/a/img')

        self.saveImgs(images_all, name)

    def saveImgs(self, images, name):
        index = 1

        for imageUrl in images:
            splitPath = imageUrl.get_attribute('src').split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = "jpg"
            fileName = self.dirName + '/' + name + '/' + name + str(index) + "." + fTail
            self.saveImg(imageUrl.get_attribute('src'), fileName)
            index += 1

    def saveIcon(self, url, dir, name):
        splitPath = url.split('.')
        fTail = splitPath.pop()
        fileName = dir + '/' + name + '.' + fTail
        print(fileName)
        self.saveImg(url, fileName)

    # 写入图片
    def saveImg(self, imageUrl, fileName):
        print(imageUrl)
        u = request.urlopen(imageUrl)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        f.close()


    # 创建目录
    def mkdir(self, path):
        path = path.strip()
        print(u'正在下载 %s 个人信息' % path)
        if os.path.exists(path):
            return False
        else:
            os.makedirs(path)
            return True

if __name__ == "__main__":
    taoBaoInfo = TaoBaoInfo()
    # 输入需要下载的页数
    page = input("请输入要下载的页数：")
    for index in range(1, int(page) + 1):
        taoBaoInfo.getPageContent(index)
