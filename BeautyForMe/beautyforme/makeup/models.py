from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField
import datetime
import json

# 유튜버
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

# 비디오 즐겨찾기
class Video_Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    def __str__(self):
        return '(' + str(self.user) + ') ' + str(self.video)