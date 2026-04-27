"""Database models for AI Code Reviewer."""
from django.db import models
from django.contrib.auth.models import User


class CodeReview(models.Model):
    """Model for storing code reviews."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    code_content = models.TextField()
    language = models.CharField(max_length=50, default='python')
    created_at = models.DateTimeField(auto_now_add=True)
    issues_found = models.JSONField(default=dict)
    score = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='completed')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review by {self.user.username} - {self.language}"


class CodeSnippet(models.Model):
    """Model for storing code snippets."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='snippets')
    title = models.CharField(max_length=200)
    code = models.TextField()
    language = models.CharField(max_length=50, default='python')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class UserProfile(models.Model):
    """Extended user profile."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='default.png', blank=True)
    total_reviews = models.IntegerField(default=0)
    total_issues_fixed = models.IntegerField(default=0)
    average_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"


class ActivityLog(models.Model):
    """Model for tracking user activities."""
    ACTION_CHOICES = [
        ('review', 'Code Review'),
        ('snippet', 'Snippet Created'),
        ('login', 'User Login'),
        ('register', 'User Registration'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.action}"