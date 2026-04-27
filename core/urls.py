"""URL configuration for core app."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('review/', views.review, name='review'),
    path('review-history/', views.review_history, name='review_history'),
    path('snippets/', views.snippets, name='snippets'),
    path('snippets/delete/<int:snippet_id>/', views.delete_snippet, name='delete_snippet'),
    path('api/review/', views.api_review, name='api_review'),
    path('about/', views.about, name='about'),
    path('features/', views.features, name='features'),
]