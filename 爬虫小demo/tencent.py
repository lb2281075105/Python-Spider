# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import urllib2

class Tencent():
    def __init__(self):
        self.url = 'http://hr.tencent.com/position.php?&start=10#a'

    def get_html(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0)'}
        request = urllib2.Request(self.url,headers=headers)
        html = urllib2.urlopen(request)
        return html

    def get_content(self):
        techlist = []
        soup = BeautifulSoup(self.get_html(),'lxml')
        positionlist = soup.select('.l > a')
        even = soup.select('.even')
        odd = soup.select('.odd')
        even + odd

        for position in positionlist:
            with open("position.txt",'a') as file:
                file.write(position.string.encode("utf-8") + "\n")
                file.close

        for technology in even:
            with open("technology.txt",'a') as file:
                file.write("" + technology.select('td')[1].string.encode("utf-8"))
                file.write("   人数：" + technology.select('td')[2].string.encode("utf-8"))
                file.write("   地点：" + technology.select('td')[3].string.encode("utf-8"))
                file.write("   时间：" + technology.select('td')[4].string.encode("utf-8") + "\n")
                file.close

        for technology in odd:
            with open("technology.txt",'a') as file:
                file.write("" + technology.select('td')[1].string.encode("utf-8"))
                file.write("   人数：" + technology.select('td')[2].string.encode("utf-8"))
                file.write("   地点：" + technology.select('td')[3].string.encode("utf-8"))
                file.write("   时间：" + technology.select('td')[4].string.encode("utf-8") + "\n")
                file.close

        # items = {} 也可以这么存储数据到文件
        # items["name"] = name
        # str = json.dumps(items, ensure_ascii=False)
        # output.write(line.encode('utf-8'))
        # output.close()
if __name__ == "__main__":
    tencent = Tencent()
    tencent.get_content()