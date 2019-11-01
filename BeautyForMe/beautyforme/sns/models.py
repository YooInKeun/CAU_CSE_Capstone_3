from django.db import models
from django.contrib.auth.models import User


class sns(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='timeline_photo/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)
    update = models.created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "text :" + self.text

    class Meta:
        ordering = ['-created']
