# -*- coding:utf-8 -*-
from django.db import models

class AiDuoDian(models.Model):

    image = models.CharField(max_length=1000)
    goodName = models.CharField(max_length=200)
    price = models.CharField(max_length=40)