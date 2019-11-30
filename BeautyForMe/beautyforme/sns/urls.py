from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from .views import SnsCreate, SnsDelete, SnsDetail, SnsUpdate, SnsList, SnsFavorite, SnsLike, SnsFavoriteList, SnsLikeList, SnsMyList, ranking, upload_file

app_name = 'sns'
urlpatterns = [
    path('mylist/', SnsMyList.as_view(), name='mylist'),
    path('create/', SnsCreate.as_view(), name='create'),
    path('like/<int:sns_id>/', SnsLike.as_view(), name='like'),
    path('favorite/<int:sns_id>/', SnsFavorite.as_view(), name='favorite'),
    path('delete/<int:pk>/', SnsDelete.as_view(), name='delete'),
    path('update/<int:pk>/', SnsUpdate.as_view(), name='update'),
    path('detail/<int:pk>/', SnsDetail.as_view(), name='detail'),
    path('like/', SnsLikeList.as_view(), name='like_list'),
    path('rankinglike/', views.ranking, name='ranking'),
    path('favorite/', SnsFavoriteList.as_view(), name='favorite_list'),
    path('', SnsList.as_view(), name='index'),
    path('image/', views.upload_file, name='imageindex'),
    #path('comment/<int:feed_pk>/', CommentCreateView.as_view(), name='comment')
]