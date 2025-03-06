from django.urls import path
from .views import (
    CategoryListView, PostByCategoryView,
    PostCreateView, PostDetailUpdateDestroyView,
    CommentCreateView, CommentUpdateDestroyView,
    PostLikesCreateView, PostLikesDestroyView)

urlpatterns = [
    path('category', CategoryListView.as_view(), name='categories'),
    path('category/<slug:slug>', PostByCategoryView.as_view(), name='posts-by-category'),
    path('posts', PostCreateView.as_view(), name='posts-create'),
    path('posts/<slug:slug>', PostDetailUpdateDestroyView.as_view(), name='posts-detail-update-delete'),
    path('posts/<slug:slug>/comments', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>', CommentUpdateDestroyView.as_view(), name='comment-update-delete'),
    path('posts/<slug:slug>/likes', PostLikesCreateView.as_view(), name='post-likes'),
    path('likes/<int:pk>', PostLikesDestroyView.as_view(), name='likes-delete'),
]