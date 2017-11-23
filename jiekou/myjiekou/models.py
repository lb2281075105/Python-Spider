# encoding=utf-8
from django.db import models

# Create your models here.

class MyModel(models.Model):
    # 姓名
    name = models.CharField(max_length=20)
    # 年龄
    age = models.CharField(max_length=100)
    # 爱好
    hobby = models.CharField(max_length=300)


