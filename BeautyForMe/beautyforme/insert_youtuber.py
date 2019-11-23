import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beautyforme.settings")
import django
django.setup()
from makeup.models import *

if __name__=='__main__':
    Youtuber(name="Pony").save()
    Youtuber(name="Ssin").save()
    Youtuber(name="Risabae").save()
    Youtuber(name="Lamuque").save()
    Youtuber(name="Sunny").save()
    Youtuber(name="Haneul").save()