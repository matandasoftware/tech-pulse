"""
Django Admin Configuration for the Tech Pulse Articles Application.

This module customizes the Django admin interface:
- SourceAdmin: Manages news sources with fetch tracking
- CategoryAdmin: Manages article categories
- ArticleAdmin: Manages aggregated articles with filters

Includes custom filters, search fields, and list displays.
Applies the duplicate button fix pattern.
"""
from django.contrib import admin
from .models import Source, Category, Article


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    """
    Admin interface for Source model.
    Shows source details, fetch status, and activity.
    """
    list_display = [
        'name',
        'source_type',
        'is_active',
        'last_fetched',
        'get_article_count',
        'created_at'
    ]
    list_filter = ['source_type', 'is_active', 'created_at']
    search_fields = ['name', 'url']
    readonly_fields = ['created_at', 'updated_at', 'last_fetched']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'url', 'source_type')
        }),
        ('Fetch Settings', {
            'fields': ('is_active', 'fetch_interval', 'last_fetched')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def changelist_view(self, request, extra_context=None):
        """Remove the duplicate ADD SOURCE + button from the changelist page"""
        extra_context = extra_context or {}
        extra_context['has_add_permission'] = False
        return super().changelist_view(request, extra_context)
    
    def get_article_count(self, obj):
        """Return count of articles from this source"""
        return obj.articles.count()
    get_article_count.short_description = 'Articles'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for Category model.
    Shows category details and article counts.
    """
    list_display = ['name', 'slug', 'get_article_count', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    
    def changelist_view(self, request, extra_context=None):
        """Remove the duplicate ADD CATEGORY + button from the changelist page"""
        extra_context = extra_context or {}
        extra_context['has_add_permission'] = False
        return super().changelist_view(request, extra_context)
    
    def get_article_count(self, obj):
        """Return count of articles in this category"""
        return obj.articles.count()
    get_article_count.short_description = 'Articles'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Admin interface for Article model.
    Shows article details with source and category filters.
    """
    list_display = [
        'title',
        'source',
        'category',
        'author',
        'published_at',
        'fetched_at'
    ]
    list_filter = ['source', 'category', 'published_at', 'fetched_at']
    search_fields = ['title', 'content', 'summary', 'author']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['fetched_at', 'updated_at']
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Article Information', {
            'fields': ('title', 'slug', 'url', 'author')
        }),
        ('Content', {
            'fields': ('summary', 'content', 'image_url')
        }),
        ('Classification', {
            'fields': ('source', 'category')
        }),
        ('Timestamps', {
            'fields': ('published_at', 'fetched_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def changelist_view(self, request, extra_context=None):
        """Remove the duplicate ADD ARTICLE + button from the changelist page"""
        extra_context = extra_context or {}
        extra_context['has_add_permission'] = False
        return super().changelist_view(request, extra_context)