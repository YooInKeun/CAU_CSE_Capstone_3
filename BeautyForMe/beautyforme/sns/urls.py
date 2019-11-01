from django.urls import path

from . import views
from .views import SnsCreate, SnsDelete, SnsDetail, SnsList, SnsUpdate

app_name = 'sns'
urlpatterns = [
    path('create/', SnsCreate.as_view(), name='create'),
    path('delete/<int:pk>/', SnsDelete.as_view(), name='delete'),
    path('update/<int:pk>/', SnsUpdate.as_view(), name='update'),
    path('detail/<int:pk>/', SnsDetail.as_view(), name='detail'),
    path('index/sns', SnsList.as_view(), name='list'),
    path('index/', views.SnsIndexTV.as_view(), name='index'),
]
