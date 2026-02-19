"""
REST API Views for the Tech Pulse Articles Application.

This module contains API viewsets for external access:
- SourceViewSet: CRUD operations for news sources
- CategoryViewSet: CRUD operations for categories
- ArticleViewSet: CRUD operations for articles with filtering

All viewsets use Django REST Framework's ModelViewSet for
automatic CRUD endpoint generation.
"""
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Source, Category, Article
from .serializers import SourceSerializer, CategorySerializer, ArticleSerializer


class SourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing news sources.
    
    Provides:
    - GET /api/sources/ - List all sources
    - GET /api/sources/{id}/ - Retrieve single source
    - POST /api/sources/ - Create source (admin only)
    - PUT /api/sources/{id}/ - Update source (admin only)
    - DELETE /api/sources/{id}/ - Delete source (admin only)
    """
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'url']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing article categories.
    
    Provides:
    - GET /api/categories/ - List all categories
    - GET /api/categories/{id}/ - Retrieve single category
    - POST /api/categories/ - Create category (admin only)
    - PUT /api/categories/{id}/ - Update category (admin only)
    - DELETE /api/categories/{id}/ - Delete category (admin only)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing articles.
    
    Provides:
    - GET /api/articles/ - List all articles
    - GET /api/articles/{id}/ - Retrieve single article
    - POST /api/articles/ - Create article (admin only)
    - PUT /api/articles/{id}/ - Update article (admin only)
    - DELETE /api/articles/{id}/ - Delete article (admin only)
    
    Supports filtering by source, category, and date.
    Supports searching by title, content, and author.
    """
    queryset = Article.objects.select_related('source', 'category').all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['source', 'category', 'published_at']
    search_fields = ['title', 'content', 'summary', 'author']
    ordering_fields = ['published_at', 'fetched_at', 'title']
    ordering = ['-published_at']