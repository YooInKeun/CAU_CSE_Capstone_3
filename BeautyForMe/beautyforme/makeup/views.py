from django.views.generic import TemplateView

from .models import *

class RecommendMakeupTV(TemplateView):
    template_name = 'makeup/recommend.html'