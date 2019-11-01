import requests
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beautyforme.settings")
import django
django.setup()
from cosmetic.models import *

if __name__=='__main__':
    Big_Category(big_category="기초").save()
    Big_Category(big_category="베이스").save()
    Big_Category(big_category="색조").save()