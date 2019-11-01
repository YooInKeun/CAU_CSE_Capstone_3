import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beautyforme.settings")
import django
django.setup()
from cosmetic.models import *
import csv

if __name__=='__main__':
    with open('Sample Data/(전체) 기초.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        data=list(csv.reader(csvDataFile))
        # Product.objects.all().delete()
        # print(Product.objects.get(product_name="asdd").tag_names.all())
        try:
            Product.objects.get(product_name=data[1][0])
            # print("이미 존재하는 제품입니다.")
        except:
            product = Product(brand=Brand.objects.get(brand_name=data[0][0]),
                      product_name=data[1][0],
                      # tag_names=Tag.objects.get(tag_name="보습"),
                      category=Small_Category.objects.get(small_category="크림"))
            product.save()
            product.tag_names.add(Tag.objects.get(tag_name="보습"))

        for i in range(3, len(data), 6):
            try:
                Product.objects.get(product_name=data[i+4][0])
                print("이미 존재하는 제품입니다.")
            except:
                product = Product(brand=Brand.objects.get(brand_name=data[i+3][0]),
                        product_name=data[i+4][0],
                        # tag_names=Tag.objects.get(tag_name=data[i]),
                        category=Small_Category.objects.get(small_category=data[i+2][0]))
                product.save()

                for j in range(len(data[i])):
                    product.tag_names.add(Tag.objects.get(tag_name=data[i][j]))