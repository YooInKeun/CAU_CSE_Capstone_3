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

        for i in range(3, len(data), 6):
            for j in range(0, len(data[i])):
                try:
                    Tag.objects.get(tag_name=data[i][j])
                    # print("이미 존재하는 태그명입니다.")
                except:
                    # print(data[i][j])
                    Tag(tag_name=data[i][j]).save()