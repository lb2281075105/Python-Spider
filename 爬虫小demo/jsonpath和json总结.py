# -*- coding:utf-8 -*-


import json
import jsonpath
import time

# 1、第一种存储字典和数组

listDict = [{"city": "北京"},{"name": "小明"}]
strlist = json.dumps(listDict,  ensure_ascii=False)
print type(strlist) # <type 'str'>
# 写数据
with open("listDict.json",'w') as file:
    file.write(strlist)

# 2、第二种存储字典和数组
listStr = [{"city": "北京"}, {"name": "大刘"}]
json.dump(listStr, open("listStr.json","w"), ensure_ascii=False)

dictStr = {"city": "北京", "name": "大刘"}
json.dump(dictStr, open("dictStr.json","w"), ensure_ascii=False)
time.sleep(1)

# ------------ 从文件里面取数据 ---------

dictList = json.load(open("listDict.json",'r'))
# 输出北京
print dictList[0]["city"]
# ------------ 读出字典loads ----------
strDict = '{"city": "北京", "name": "大猫"}'
# <type 'dict'>
print type(json.loads(strDict))

jsonobj = json.loads(strDict)

# 从根节点开始，匹配name节点
citylist = jsonpath.jsonpath(jsonobj,'$..name')

print citylist[0].encode('utf-8')