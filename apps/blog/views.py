from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer

# Category
class CategoryListView(generics.ListAPIView):
    """
    Obtiene todas las categorias.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

