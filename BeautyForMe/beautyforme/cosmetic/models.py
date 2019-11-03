from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User

# 브랜드
class Brand(models.Model):
    brand_name = models.CharField(max_length=100, default="")
    
    def __str__(self):
        return self.brand_name

# 대분류
class Big_Category(models.Model):
    big_category = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.big_category

# 소분류
class Small_Category(models.Model):
    big_category = models.ForeignKey(Big_Category, on_delete=models.CASCADE)
    small_category = models.CharField(max_length=100, default="")

    def __str__(self):
        return '[' + str(self.big_category) + '] ' + self.small_category

# 태그
class Tag(models.Model):
    tag_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.tag_name

# 제품
class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100, default="")
    tag_names = models.ManyToManyField(Tag)
    category = models.ForeignKey(Small_Category, on_delete=models.CASCADE)
    image_link = models.CharField(max_length=100, default="")

    def __str__(self):
        return '[' + str(self.brand) + '] ' + self.product_name

# 화장품
class Cosmetic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
    type_name = models.CharField(max_length=100, default="")
    rgb_value = models.CharField(max_length=100, default="")
    image_link = models.CharField(max_length=100, default="")
    similar_cosmetics = JSONField(default="")

# 유저 화장품
class User_Cosmetic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cosmetic = models.ForeignKey(Cosmetic, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField(max_length=100, default="")
    is_consent_alarm = models.BooleanField(default=True)
    selected_similar_cosmetics = JSONField(default="")

# 유저 관심 화장품
class User_Interested_Cosmetic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cosmetic = models.ForeignKey(Cosmetic, on_delete=models.CASCADE)
    selected_similar_cosmetics = JSONField(default="")

# 화장품별 중요도
class Cosmetic_Importance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Small_Category, on_delete=models.CASCADE)
    importance = JSONField(default="")