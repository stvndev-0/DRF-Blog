from django.urls import path
from .views import (
    CategoryListView, PostByCategoryView,
    PostCreateView)

urlpatterns = [
    path('category', CategoryListView.as_view(), name='categories'),
    path('category/<slug:slug>', PostByCategoryView.as_view(), name='posts-by-category'),
    path('posts', PostCreateView.as_view(), name='posts-create'),
]