from django.urls import path
from .views import *


urlpatterns = [
    path('accounts', AuthorCreate.as_view(), name='user-create'),
    path('accounts/login', AuthorLogin.as_view(), name='user-login'),
    path('accounts/put-delete', AuthorUpdateDeleteAPI.as_view(), name='user-update-delete'),
    path('me', AuthorDetail.as_view(), name='user-detail'),
    path('blog', BlogCreateFetchAll.as_view(), name='blog-create-getall'),
    path('blog/<int:pk>', BlogGetPutDeleteCustomURL.as_view(), name='blog-get-put-delete'),
    path('like/<int:post_id>', LikeUnlikePost.as_view(), name='like-unlike-blog'),
]
