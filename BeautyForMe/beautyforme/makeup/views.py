from django.views.generic import TemplateView
from django.shortcuts import render

from .models import *
import json

class RecommendMakeupTV(TemplateView):
    template_name = 'makeup/recommend.html'

def recommend_result(request):
    raws = json.loads(request.POST.get('selected_cosmetics'))
    cosmetics = {}
    cosmetics['cosmetics'] = raws
    
    cosmetic_ids = []
    for raw in raws:
        cosmetic_ids.append(raw['id'])
    
    print(cosmetics)
    print(cosmetic_ids)
    return render(request, 'makeup/recommend_result.html')

# class RecommendResultTV(TemplateView):
#     template_name = 'makeup/recommend_result.html'

class VideoTV(TemplateView):
    template_name = 'makeup/video_list.html'

class VideoDetailTV(TemplateView):
    template_name = 'makeup/video_detail.html'