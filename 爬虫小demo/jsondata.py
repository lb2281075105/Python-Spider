# -*- coding:utf-8 -*-

import json
import jsonpath
import urllib2

class Json():
    def __init__(self):
        self.url = "http://www.lagou.com/lbs/getAllCitySearchLabels.json"

    def get_json(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0)'}
        request = urllib2.Request(self.url,headers=headers)
        response = urllib2.urlopen(request)
        html = response.read()
        jsonobj = json.loads(html)
        # 获取城市名称
        namelist = jsonpath.jsonpath(jsonobj,'$..name')
        for name in namelist:
            print(name)

        # 把列表存储为字符串
        nametext = json.dumps(namelist,ensure_ascii=False)
        with open('name.txt','a') as file:
            file.write(nametext.encode("utf-8"))
            file.close


if __name__ == "__main__":
    jsono = Json()
    jsono.get_json()
