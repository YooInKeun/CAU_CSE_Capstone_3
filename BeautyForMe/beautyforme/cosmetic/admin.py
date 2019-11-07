from django.contrib import admin
from .models import *

admin.site.register(Brand)
admin.site.register(Big_Category)
admin.site.register(Small_Category)
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(Cosmetic)
admin.site.register(User_Cosmetic)
admin.site.register(User_Interested_Cosmetic)
admin.site.register(Cosmetic_Importance)