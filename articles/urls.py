"""
URL Configuration for the Articles API.

This module defines API URL patterns using DRF's DefaultRouter:
- /api/sources/ - Source endpoints
- /api/categories/ - Category endpoints
- /api/articles/ - Article endpoints

The router automatically generates URLs for all CRUD operations.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SourceViewSet, CategoryViewSet, ArticleViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'sources', SourceViewSet, basename='source')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'articles', ArticleViewSet, basename='article')

# The API URLs are determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
