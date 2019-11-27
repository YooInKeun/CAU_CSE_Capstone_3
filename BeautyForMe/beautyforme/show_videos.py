import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beautyforme.settings")
import django
django.setup()
from cosmetic.models import *
from makeup.models import *
import csv

youtuber = "Risabae"
file_name = "risabae_matched_001"

if __name__=='__main__':
    videos = Video.objects.all()

    for video in videos:
        cosmetics = video.cosmetics.replace(" ", "").replace("'", "").replace("{", "").replace("}", "").split(",")

        for cosmetic in cosmetics:
            cosmetic_number = int(cosmetic.split(":")[0])

        if cosmetic_number >= 5:
            print(f'{cosmetic_number}개 : {video.title}')
               
