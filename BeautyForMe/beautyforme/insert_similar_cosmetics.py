from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beautyforme.settings")
import django
django.setup()
from cosmetic.models import *

if __name__=='__main__':

    # print(Cosmetic.objects.get(id=448).similar_cosmetics)
    # test = {}
    # for i in range(3):
    #     test[i] = "테스트"
    # print(test)

    # for cosmetic in Cosmetic.objects.all():
    #     cosmetic.similar_cosmetics = {}
    #     cosmetic.save()

    # for cosmetic in Cosmetic.objects.all():
    #     print(cosmetic.similar_cosmetics)

    for cosmetic in Cosmetic.objects.all():
        # print(cosmetic.similar_cosmetics)

        # print(cosmetic.product.category)
        i=0
        tmp = {}
        print(str(cosmetic.id) + ' 시작!')
        compared_cosmetics = Cosmetic.objects.filter(product__category=cosmetic.product.category)
        for compared_cosmetic in compared_cosmetics:
            if cosmetic.rgb_value != "None":
                if cosmetic.rgb_value == compared_cosmetic.rgb_value and cosmetic.product.category == compared_cosmetic.product.category and cosmetic != compared_cosmetic:
                    tmp[i] = compared_cosmetic.id
                    print(str(cosmetic) + ', id값: ' + str(cosmetic.id) + ', rgb: ' + str(cosmetic.rgb_value) + '// 유사화장품: ' + str(compared_cosmetic) + ', id값: ' + str(compared_cosmetic.id) + ', rgb:' + str(compared_cosmetic.rgb_value))
                    i += 1
        cosmetic.similar_cosmetics = tmp
        cosmetic.save()