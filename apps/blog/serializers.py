from rest_framework import serializers
from .models import Category, Post

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'description',
            'slug',
            'updated_at',
            'user',
        ] 