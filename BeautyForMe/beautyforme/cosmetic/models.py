from django.db import models
from jsonfield import JSONField

class Cosmetic(models.Model):
    big_category = models.CharField(max_length=100, default="")
    small_category = models.CharField(max_length=100, default="")
    cosmetic_name = models.CharField(max_length=30, default="")
    brand_name = models.CharField(max_length=30, default="")
    image_link = models.CharField(max_length=100, default="")
    option_names = JSONField(default="")
    tag_names = JSONField(default="")

    def __str__(self):
        full_name = '[' + self.brand_name + '] '+ self.cosmetic_name
        return full_name