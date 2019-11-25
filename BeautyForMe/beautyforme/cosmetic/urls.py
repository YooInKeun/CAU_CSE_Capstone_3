from django.urls import path

from . import views


app_name = 'cosmetic'
urlpatterns = [
    path('register/', views.RegisterCosmeticsTV.as_view(), name='register'),
    path('registered/', views.RegisteredCosmeticsTV.as_view(), name='registered'),
]
