from django.urls import path

from . import views


app_name = 'makeup'
urlpatterns = [
    path('recommend/', views.RecommendMakeupTV.as_view(), name='recommend'),
    path('recommend/result/', views.RecommendResultTV.as_view(), name='recommend_result'),
    path('recommend/result/video/', views.VideoTV.as_view(), name='video'),
    path('recommend/result/video/detail/', views.VideoDetailTV.as_view(), name='vidio_detail'),
]