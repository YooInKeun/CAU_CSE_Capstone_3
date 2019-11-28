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

        for i in range(0, len(data), 6):
            for j in range(len(data[i+2])):
                try:
                    if j == 0 and (data[i+2][j] == "" or data[i+2][j] == None or data[i+2][j] == Null):
                        data[i+2][j] = ""
                    elif j != 0 and data[i+2][j] == "":
                        continue
                        
                    Cosmetic.object.get(product = Product.objects.get(brand=Brand.objects.get(brand_name=data[i][0]), product_name=data[i+1][0]),
                                        type_name = data[i+2][j])
                    # print(data[i+1][0])
                    print("이미 존재하는 제품입니다.")
                except:
                    try:
                        # print(data[i][0], data[i+1][0], data[i+2][j])
                        cosmetic = Cosmetic(product = Product.objects.get(brand=Brand.objects.get(brand_name=data[i][0]), product_name=data[i+1][0]),
                                            type_name = data[i+2][j],                       
                                            rgb_value = "None", 
                                            image_link = data[i+4][0])
                        cosmetic.save()
                    except:
                        #print("error")
                        pass