from django.conf.urls import url
from rest_framework.authtoken import views as token_views

from api import views

urlpatterns = [
    url(r'^user/$', views.UserInfo.as_view()),
    url(r'^user/(?P<pk>[\w:|-]+)/$', views.UserInfo.as_view()),
    url(r'^profile/$', views.ProfileInfo.as_view()),
    url(r'^profile/(?P<pk>[\w:|-]+)/$', views.ProfileInfo.as_view()),
]