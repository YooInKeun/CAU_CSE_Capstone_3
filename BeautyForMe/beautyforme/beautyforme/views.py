from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'instagram_home.html'


class PreparationView(TemplateView):
    template_name = 'instagram_preparation.html'
