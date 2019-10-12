from django.conf.urls import url
from rest_framework.authtoken import views as token_views

from api import views

urlpatterns = [
    url(r'^profile/$', views.ProfileInfo.as_view()),
]