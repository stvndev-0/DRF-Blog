from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import Category, Post
from .serializers import CategorySerializer, PostListSerializer

# Category
class CategoryListView(generics.ListAPIView):
    """
    Obtiene todas las categorias.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PostByCategoryView(generics.ListAPIView):
    """
    Obtiene los posts de una categoria.
    """
    serializer_class = PostListSerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug', None)
        category = get_object_or_404(Category, slug=slug)
        return Post.objects.filter(category=category, status='Public')