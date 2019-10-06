from django.urls import path

from . import views


app_name = 'makeup'
urlpatterns = [
    path('recommend/', views.RecommendMakeupTV.as_view(), name='recommend'),
]