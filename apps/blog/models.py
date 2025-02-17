from django.db import models
from django.conf import settings
from django.utils.text import slugify

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug or self.name != self.slug:
            self.slug = slugify(self.name)
        self.clean()
        super().save(*args, **kwargs)


class Post(models.Model):
    class StatusChoices(models.TextChoices):
        PRIVATE = 'Private'
        PUBLIC = 'Public'
    
    title = models.CharField(max_length=155)
    slug = models.CharField(max_length=155, blank=True, null=True, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PRIVATE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug or self.title != self.slug:
            self.slug = slugify(self.title)
        self.clean()
        super().save(*args, **kwargs)

class Comment(models.Model):
    text = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)

    def __str__(self):
        return self.text