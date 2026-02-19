"""
REST API Serializers for the Tech Pulse Articles Application.

This module contains Django REST Framework serializers that convert
model instances to JSON for API responses:
- SourceSerializer: Serializes Source objects with article counts
- CategorySerializer: Serializes Category objects with article counts
- ArticleSerializer: Serializes Article objects with related data

Serializers handle data validation and nested relationships.
"""
from rest_framework import serializers
from .models import Source, Category, Article


class SourceSerializer(serializers.ModelSerializer):
    """
    Serializer for Source model.
    Includes computed field for article count.
    """
    article_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Source
        fields = [
            'id',
            'name',
            'url',
            'source_type',
            'is_active',
            'fetch_interval',
            'last_fetched',
            'article_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'last_fetched']
    
    def get_article_count(self, obj):
        """Return count of articles from this source"""
        return obj.articles.count()


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    Includes computed field for article count.
    """
    article_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'article_count',
            'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_article_count(self, obj):
        """Return count of articles in this category"""
        return obj.articles.count()


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for Article model.
    Includes related source and category names.
    """
    source_name = serializers.ReadOnlyField(source='source.name')
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'slug',
            'url',
            'content',
            'summary',
            'image_url',
            'author',
            'source',
            'source_name',
            'category',
            'category_name',
            'published_at',
            'fetched_at',
            'updated_at'
        ]
        read_only_fields = ['slug', 'fetched_at', 'updated_at']