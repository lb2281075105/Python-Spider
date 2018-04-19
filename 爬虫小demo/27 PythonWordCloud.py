# encoding: utf-8
import os
from pyecharts import WordCloud
# 词云
def pythonWordCloud(x,y,label):
    wordcloud = WordCloud(width=1300, height=620)
    wordcloud.add("", x, y, word_size_range=[20, 100],shape="triangle-forward")
    wordcloud.render()
    os.system(r"render.html")
x = [
     'PythonCoder', '爬虫', '人工智能', '大数据', 'Django',
     'Flask', '机器学习', '数据分析', '深度学习', '运维测试', 'TensorFlow',
     '真实面试经历', '真实面试题', '自然语言处理', 'NLP',"数据处理",
     '500GB资料免费送', '开放源码', '免费学习群', '面试简历', 'JCSON']
y = [
     10000, 6181, 4386, 4055, 2467, 2244, 1898, 1484, 1112,
     965, 847, 582, 555, 550, 462, 366, 360, 282, 273, 265,5000]

pythonWordCloud(x,y,"词云")

