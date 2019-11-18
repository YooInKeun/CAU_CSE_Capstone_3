from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User
import datetime

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
    tag_names = models.ManyToManyField(Tag, blank=True)
    category = models.ForeignKey(Small_Category, on_delete=models.CASCADE)
    image_link = models.CharField(max_length=1000, default="")

    def __str__(self):
        return '[' + str(self.brand) + '] ' + self.product_name

# 화장품
class Cosmetic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
    type_name = models.CharField(max_length=100, default="")
    rgb_value = models.CharField(max_length=100, default="")
    image_link = models.TextField(default="")
    similar_cosmetics = JSONField(default="")

    def __str__(self):
        return '[' + str(self.product.product_name) + '] ' + self.type_name

# 유저 화장품
class User_Cosmetic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cosmetic = models.ForeignKey(Cosmetic, on_delete=models.CASCADE)
    expiration_date = models.DateField(max_length=100, default="")
    alarm_cycle = models.IntegerField(blank=True, null=True, default=0)
    is_consent_alarm = models.BooleanField(default=True)
    selected_similar_cosmetics = JSONField(default="")

    def __str__(self):
        return '(' + str(self.user) + ') ' + str(self.cosmetic)


# 유저 관심 화장품
class User_Interested_Cosmetic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cosmetic = models.ForeignKey(Cosmetic, on_delete=models.CASCADE)
    selected_similar_cosmetics = JSONField(default="")

    def __str__(self):
        return '(' + str(self.user) + ') ' + str(self.cosmetic)

# 화장품별 중요도
class Cosmetic_Importance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    importance = JSONField(default={"스킨":10, "로션":10, "에센스":10, "크림":10, "미스트":10, "메이크업픽서":10, "페이스오일":10, "토너/필링패드":10,
                                    
                                    "메이크업베이스:":10, "톤업크림":10, "베이스프라이머":10, "포인트프라이머":10, "파운데이션":10, "비비크림":10, 
                                    "씨씨크림":10, "쿠션타입":10, "컨실러":10, "팩트":10, "파우더":10, "트윈케익":10,
                                    
                                    "립스틱":10, "립글로스/락커":10, "립틴트":10, "립밤":10, "립라이너":10, "아이라이너":10, "마스카라":10, "픽서/영양제":10,
                                    "아이섀도우":10, "아이브로우":10, "하이라이터":10, "쉐딩":10, "블러셔":10})