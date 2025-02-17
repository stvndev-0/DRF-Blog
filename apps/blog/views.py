from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from core.permissions import IsOwnerOrReadOnly
from .models import Category, Post
from .serializers import (
    CategorySerializer, PostListSerializer,
    PostSerializer)

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
    
# Posts
class PostCreateView(generics.CreateAPIView):
    """
    Crea un post.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)