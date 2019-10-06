from django.views.generic import TemplateView

from .models import *

class RegisterCosmeticsTV(TemplateView):
    template_name = 'cosmetic/register.html'

class RegisteredCosmeticsTV(TemplateView):
    template_name = 'cosmetic/registered.html'