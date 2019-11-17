import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beautyforme.settings")
import django
django.setup()
from cosmetic.models import *
import csv

if __name__=='__main__':
    with open('db_insert_data/All Data/색조.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        data=list(csv.reader(csvDataFile))

        for i in range(0, len(data), 6):
            try:
                Brand.objects.get(brand_name=data[i][0])
                print("이미 존재하는 브랜드명입니다.")
            except:
                Brand(brand_name=data[i][0]).save()
                print(data[i][0])