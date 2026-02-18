"""
Django models for the Tech Pulse Articles Application.

This module defines the core data models for news aggregation:
- Source: News sources (RSS feeds, APIs, websites)
- Category: Article categorization (Tech, Business, Science, etc.)
- Article: Aggregated news articles from external sources

Each model includes validation, custom methods, and relationships
to support automated news aggregation and display.
"""
from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class Source(models.Model):
    """
    Represents a news source (RSS feed, API, website).
    Sources are automatically fetched and parsed for articles.
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text='Source name (e.g., TechCrunch, The Verge)'
    )
    
    url = models.URLField(
        unique=True,
        help_text='Source URL or RSS feed URL'
    )
    
    source_type = models.CharField(
        max_length=20,
        choices=[
            ('RSS', 'RSS Feed'),
            ('API', 'API Integration'),
            ('SCRAPER', 'Web Scraper'),
        ],
        default='RSS',
        help_text='How we fetch articles from this source'
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this source is actively being fetched'
    )
    
    fetch_interval = models.IntegerField(
        default=60,
        help_text='How often to fetch (in minutes)'
    )
    
    last_fetched = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When we last fetched articles from this source'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Source'
        verbose_name_plural = 'Sources'
        ordering = ['name']


class Category(models.Model):
    """
    Represents an article category.
    Used to organize articles by topic (Tech, Business, Science, etc.).
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='Category name (e.g., Technology, Business)'
    )
    
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        help_text='URL-friendly version of category name'
    )
    
    description = models.TextField(
        blank=True,
        help_text='Category description'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        """
        Auto-generate slug from name if not provided.
        Ensures slug is unique.
        """
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure slug is unique
            original_slug = self.slug
            counter = 1
            while Category.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']


class Article(models.Model):
    """
    Represents a news article aggregated from external sources.
    Articles are automatically fetched, parsed, and stored.
    """
    title = models.CharField(
        max_length=500,
        help_text='Article headline'
    )
    
    slug = models.SlugField(
        max_length=550,
        unique=True,
        blank=True,
        help_text='URL-friendly version of title'
    )
    
    url = models.URLField(
        unique=True,
        help_text='Original article URL'
    )
    
    content = models.TextField(
        blank=True,
        help_text='Full article content (if fetched)'
    )
    
    summary = models.TextField(
        blank=True,
        help_text='Article summary or excerpt'
    )
    
    image_url = models.URLField(
        blank=True,
        null=True,
        help_text='Article featured image URL'
    )
    
    author = models.CharField(
        max_length=200,
        blank=True,
        help_text='Article author name'
    )
    
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        related_name='articles',
        help_text='Source this article came from'
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
        help_text='Article category'
    )
    
    published_at = models.DateTimeField(
        help_text='When the article was originally published'
    )
    
    fetched_at = models.DateTimeField(
        auto_now_add=True,
        help_text='When we fetched this article'
    )
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        """
        Auto-generate slug from title if not provided.
        Ensures slug is unique.
        """
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure slug is unique
            original_slug = self.slug
            counter = 1
            while Article.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} - {self.source.name}"
    
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-published_at']
        # Prevent duplicate articles from same source
        constraints = [
            models.UniqueConstraint(
                fields=['source', 'url'],
                name='unique_source_url'
            )
        ]