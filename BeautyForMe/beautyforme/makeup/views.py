from django.views.generic import TemplateView

from .models import *

class RecommendMakeupTV(TemplateView):
    template_name = 'makeup/recommend.html'

class RecommendResultTV(TemplateView):
    template_name = 'makeup/recommend_result.html'

class VideoTV(TemplateView):
    template_name = 'makeup/video_list.html'

class VideoDetailTV(TemplateView):
    template_name = 'makeup/video_detail.html'