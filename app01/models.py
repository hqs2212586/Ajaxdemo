from django.db import models

# Create your models here.


# 创建一个user表来进行校验
class User(models.Model):
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
