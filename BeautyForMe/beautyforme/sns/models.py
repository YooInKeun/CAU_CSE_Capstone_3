from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
# Create your models here.


class Sns(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='timeline_photo/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    like = models.ManyToManyField(User, related_name='like_post', blank=True)
    favorite = models.ManyToManyField(
        User, related_name='favorite_post', blank=True)

    def __str__(self):
        return "text : "+self.text

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse('sns:detail', args=[self.id])

    @property
    def created_korean_time(self):
        korean_timezone = timezone(settings.TIME_ZONE)
        return self.created.astimezone(korean_timezone)
