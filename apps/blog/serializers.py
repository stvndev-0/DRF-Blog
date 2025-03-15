from rest_framework import serializers
from .models import (
    Category, Post, Comment,
    PostLikes)
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PostListSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'cover',
            'description',
            'slug',
            'created_at',
            'user',
            'likes',
            'comments',
            'category'
        ]

    def get_likes(self, obj):
        return obj.likes.filter().count()

    def get_comments(self, obj):
        return obj.comments.filter().count()

class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=155, required=True)
    description = serializers.CharField(max_length=255)
    content = serializers.CharField(required=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=True
    )
    
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user',)

class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'title',
            'slug',
            'cover',
            'description',
            'content',
            'updated_at',
            'user',
            'comments',
        ]

    def get_comments(self, obj):
        """
        Filtrar solo los comentarios principales
        """
        comments = obj.comments.filter(parent__isnull=True)
        return CommentSerializer(comments, many=True).data

class ReplySerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    
    class Meta:
        model = Comment
        fields = ['id', 'text', 'user', 'updated_at']
        read_only_fields = ('replies',)

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    replies = ReplySerializer(many=True, required=False)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'user', 'updated_at', 'replies']
        read_only_fields = ('user', 'post')

class PostLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLikes
        fields = '__all__'
        read_only_fields = ('user', 'post')