from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
import json

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
    importance = JSONField(default=json.dumps(
        
                            {
                                "기초": {
                                    "스킨":5, "로션":5, "에센스":5, "크림":5, "미스트":5, 
                                    "메이크업픽서":5, "페이스오일":5, "토너/필링패드":5
                                    },
                                    
                                "베이스": {
                                    "메이크업베이스":5, "톤업크림":5, "베이스프라이머":5, "포인트프라이머":5, 
                                    "파운데이션":5, "비비크림":5, "씨씨크림":5, "쿠션타입":5, "컨실러":5, "팩트":5,
                                    "파우더":5, "트윈케익":5
                                    },
                                            
                                "색조": {
                                    "립스틱":5, "립글로스/락커":5, "립틴트":5, "립밤":5, "립라이너":5,
                                    "아이라이너":5, "마스카라":5, "픽서/영양제":5, "아이섀도우":5, "아이브로우":5,
                                    "하이라이터":5, "쉐딩":5, "블러셔":5
                                    }
                            }, ensure_ascii=False))
    def __str__(self):
        return '(' + str(self.user) + ') ' + str(self.importance)

@receiver(post_save, sender=User)
def create_user_cosmetic_importance(sender, instance, created, **kwargs):
    if created:
        Cosmetic_Importance.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_cosmetic_importance(sender, instance, **kwargs):
    instance.cosmetic_importance.save()