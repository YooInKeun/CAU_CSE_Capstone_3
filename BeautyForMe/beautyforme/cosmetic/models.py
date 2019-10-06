from django.db import models

class Cosmetic(models.Model):
    test = models.CharField(max_length=200)
