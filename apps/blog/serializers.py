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

class PostDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['title', 'slug','description', 'content', 'updated_at', 'user', 'comments']

    def get_comments(self, obj):
        """
        Filtrar solo los comentarios principales
        """
        comments = obj.comments.filter(parent__isnull=True)
        return CommentSerializer(comments, many=True).data

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'user', 'updated_at']
        read_only_fields = ('replies',)

class CommentSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True, required=False)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'user', 'updated_at', 'replies']
        read_only_fields = ('user', 'post')