from django.urls import path

from . import views


app_name = 'cosmetic'
urlpatterns = [
    path('register/', views.register_cosmetics, name='register'),
    path('registered/', views.registered_cosmetics, name='registered'),
]