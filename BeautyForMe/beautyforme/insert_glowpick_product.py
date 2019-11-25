import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beautyforme.settings")
import django
django.setup()
from cosmetic.models import *
import csv

if __name__=='__main__':
    with open('db_insert_data/All Data/final_cosmetics.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        data=list(csv.reader(csvDataFile))
        # Product.objects.all().delete()
        # print(Product.objects.get(product_name="asdd").tag_names.all())
        # try:
        #     Product.objects.get(product_name=data[1][0])
        #     # print("이미 존재하는 제품입니다.")
        # except:
        #     product = Product(brand=Brand.objects.get(brand_name=data[0][0]),
        #               product_name=data[1][0],
        #               # tag_names=Tag.objects.get(tag_name="보습"),
        #               category=Small_Category.objects.get(small_category="크림"))
        #     product.save()
        #     product.tag_names.add(Tag.objects.get(tag_name="보습"))

        for i in range(0, len(data), 6):
            try:
                Product.objects.get(brand=Brand.objects.get(brand_name=data[i][0]), product_name=data[i+1][0])
                print("이미 존재하는 제품입니다.")
            except:
                product = Product(brand=Brand.objects.get(brand_name=data[i][0]),
                        product_name=data[i+1][0],
                        # tag_names=Tag.objects.get(tag_name=data[i]),
                        image_link=data[i+4][0],
                        category=Small_Category.objects.get(small_category=data[i+5][0]))
                product.save()

                try:
                    for j in range(len(data[i+3])):
                        product.tag_names.add(Tag.objects.get(tag_name=data[i+3][j]))
                except:
                    print("tag pass")

        # for i in range(0, len(data), 6):
        #     try:
        #         product = Product.objects.get(product_name=data[i+1][0])
        #         # product.save()
        #         for j in range(len(data[i])):
        #              #stripped_tag_name = data[i+3][j].strip()
        #             product.tag_names.add(Tag.objects.get(tag_name=stripped_tag_name))
        #             # print(product.product_name)
        #         # print(product.tag_names.all())print(product.tag_names.all())
        #             # print('\n')
        #     except:
        #         print("tag insert error")