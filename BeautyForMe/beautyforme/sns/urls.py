from django.urls import path

from . import views


app_name = 'sns'
urlpatterns = [
    path('index/', views.SnsIndexTV.as_view(), name='index'),
]