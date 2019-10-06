from django.views.generic import TemplateView

from .models import *

class SnsIndexTV(TemplateView):
    template_name = 'sns/index.html'