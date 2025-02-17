from rest_framework import serializers
from .models import Category, Post, Comment

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

class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=155, required=True)
    description = serializers.CharField(max_length=255)
    content = serializers.CharField(required=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=True)
    
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user',)