"""Admin configuration for core app."""
from django.contrib import admin
from .models import CodeReview, CodeSnippet, UserProfile, ActivityLog


@admin.register(CodeReview)
class CodeReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'language', 'score', 'created_at']
    list_filter = ['language', 'created_at']
    search_fields = ['user__username', 'code_content']


@admin.register(CodeSnippet)
class CodeSnippetAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'language', 'created_at']
    list_filter = ['language', 'created_at']
    search_fields = ['title', 'user__username']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_reviews', 'average_score', 'created_at']
    search_fields = ['user__username']


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'description', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['user__username', 'description']