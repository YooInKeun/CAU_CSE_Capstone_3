from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from .views import CommentCreateAjaxView, CommentUpdateView, CommentDeleteView

app_name = 'comment'
urlpatterns = [
    # path('create/<int:feed_pk>/',
    #      CommentCreateAjaxView.as_view(), name='comment-create'),
    path('create/<int:feed_pk>/',
         CommentCreateAjaxView.as_view(), name='comment-create'),
    path('update/<int:pk>/', CommentUpdateView.as_view(), name='comment-update'),
    path('delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
]
