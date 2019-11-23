from django.db import models
from jsonfield import JSONField
import datetime
import json
# Create your models here.
class Youtuber(models.Model):
    name = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.name

# 화장품
class Video(models.Model):
    title = models.CharField(max_length=200, default="")
    thumbnail = models.TextField(default="")
    link = models.TextField(default="")
    upload_date = models.DateField(max_length=100, default="")
    hits = models.IntegerField(default=0)
    youtuber = models.ForeignKey(Youtuber, on_delete=models.CASCADE)
    cosmetics = JSONField(default="")

    def __str__(self):
        return '[' + str(self.youtuber.name) + '] ' + self.title