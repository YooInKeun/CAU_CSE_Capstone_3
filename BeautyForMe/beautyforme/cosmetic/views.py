from django.views.generic import TemplateView
from django.shortcuts import render, redirect

from .models import *

def register_cosmetics(request):
    if request.user.is_authenticated is False:
        return redirect('accounts:login')
    return render(request, 'cosmetic/register.html')

def registered_cosmetics(request):
    if request.user.is_authenticated is False:
        return redirect('accounts:login')
    return render(request, 'cosmetic/registered.html')

# class RegisterCosmeticsTV(TemplateView):
#     template_name = 'cosmetic/register.html'

# class RegisteredCosmeticsTV(TemplateView):
#     template_name = 'cosmetic/registered.html'