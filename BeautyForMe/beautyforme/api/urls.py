from django.conf.urls import url
from rest_framework.authtoken import views as token_views

from api import views

urlpatterns = [
    url(r'^user/cosmetic/interested/$', views.UserInterestedCosmeticInfo.as_view()),
    url(r'^user/cosmetic/interested/(?P<pk>[\w:|-]+)/$', views.UserInterestedCosmeticInfo.as_view()),
    url(r'^user/cosmetic/$', views.UserCosmeticInfo.as_view()),
    url(r'^user/cosmetic/(?P<pk>[\w:|-]+)/$', views.UserCosmeticInfo.as_view()),
    url(r'^user/$', views.UserInfo.as_view()),
    url(r'^user/(?P<pk>[\w:|-]+)/$', views.UserInfo.as_view()),
    url(r'^profile/$', views.ProfileInfo.as_view()),
    url(r'^profile/(?P<pk>[\w:|-]+)/$', views.ProfileInfo.as_view()),
    url(r'^cosmetic/$', views.CosmeticInfo.as_view()),
    url(r'^cosmetic/(?P<pk>[\w:|-]+)/$', views.CosmeticInfo.as_view()),
]