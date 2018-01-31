
# -*- coding:utf-8 -*-
import pytesseract
from PIL import Image

# PIL读取与存储图像

# 1、PIL识别图片上面文字
images = Image.open('test.png')
text = pytesseract.image_to_string(images)
print text

# 2、PIL保存成灰色图片
# -*- coding: utf-8 -*-
from PIL import Image

# 打开图像得到一个PIL图像对象
img = Image.open("test.png")
# 将其转为一张灰度图
img = img.convert('L')
# 存储该张图片
try:
  img.save("test.png")
except IOError:
  print "cannot convert"


# 3、PIL生成缩略图
# -*- coding: utf-8 -*-
from PIL import Image

# 打开图像得到一个PIL图像对象
img = Image.open("test.png")
# 创建最长边为128的缩略图
img.thumbnail((128,128))
# 存储该张图片
try:
  img.save("test.png")
except IOError:
  print "cannot convert"


# 4、PIL调整尺寸与旋转
# -*- coding: utf-8 -*-
from PIL import Image

# 打开图像得到一个PIL图像对象
img = Image.open("test.png")
# 修改图片大小，参数为一元组
img = img.resize((100,200))
# 使图片逆时针选择45度
img = img.rotate(45)
# 存储该张图片
try:
  img.save("test.png")
except IOError:
  print "cannot convert"


