from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from .models import *


class SnsIndexTV(TemplateView):
    template_name = 'sns/index.html'


class SnsList(ListView):
    model = sns
    template_name_suffix = '_list'


class SnsCreate(CreateView):
    model = sns
    fields = ['text', 'image']
    template_name_suffix = '_create'
    success_url = 'sns/'


class SnsUpdate(UpdateView):
    model = sns
    fields = ['text', 'image']
    template_name_suffix = '_update'
    success_url = 'sns/'


class SnsDelete(DeleteView):
    model = sns
    template_name_suffix = '_delete'
    success_url = 'sns/'

class SnsDetail(DetailView):
    model = sns
    template_name_suffix = '_detail'

