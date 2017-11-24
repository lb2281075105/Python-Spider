# -*- coding:utf-8 -*-
import csv

# 1、txt文件
file = open('file.txt','r')
# 获取所有的信息
print file.read()
file.write("你好")
# 获取所有并且在所有行存在一个数组
print file.readlines()
# 获取第一行
print file.readline()

# 2、读取csv文件

writer = csv.writer(open('test.csv','wb'))
writer.writerow(['col1','col2','col3'])
data = [range(3) for i in range(3)]
for item in data:
    writer.writerow(item)

filelist = csv.reader(open('./test.csv','r'))
for item in filelist:
    print item


# 3、读取xml文件

from xml.dom import minidom
# parse打开xml文件
dom = minidom.parse("info.xml")
# 获取根节点
root = dom.documentElement
print root.nodeName
print root.nodeValue
print root.nodeType
print root.ELEMENT_NODE
print "--" * 8
province = root.getElementsByTagName("province")
print province[0].tagName
print province[0].getAttribute("username")
print province[0].firstChild.data






