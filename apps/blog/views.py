from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from core.permissions import IsOwnerOrReadOnly
from .models import Category, Post, Comment
from .serializers import (
    CategorySerializer, PostListSerializer,
    PostSerializer, PostDetailSerializer,
    CommentSerializer)

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

class PostDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Actualiza o elimina un post mediante su slug.
    """
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'slug'

class CommentCreateView(generics.CreateAPIView):
    """
    Crea un comentario mediante el slug del post.
    Crea una respuesta mediante el comment_id del comentario padre.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, slug=self.kwargs.get('slug'))
        comment_id = self.request.data.get('comment_id', None)
        parent = None

        if comment_id:
            parent = get_object_or_404(Comment, id=comment_id)
            if parent.parent:
                raise ValidationError({'detail': 'Nested replies are not allowed'})
            
        serializer.save(user=self.request.user, post=post, parent=parent)

class CommentUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Actualiza o elimina un comment mediante su pk.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]