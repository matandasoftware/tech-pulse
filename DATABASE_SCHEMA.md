# 🗄️ Tech Pulse - Database Schema

Complete database schema design with models, relationships, and data dictionary.

---

## 📊 Entity Relationship Diagram

```
┌─────────────────────┐
│     NewsSource      │
├─────────────────────┤
│ id (PK)             │
│ name                │
│ url                 │
│ source_type         │
│ scraping_config     │
│ is_active           │
│ fetch_interval      │
│ last_fetched_at     │
│ created_at          │
│ updated_at          │
└──────────┬──────────┘
           │
           │ 1:N
           │
           ▼
┌─────────────────────┐         ┌─────────────────────┐
│      Article        │    N:M  │      Category       │
├─────────────────────┤◄────────├─────────────────────┤
│ id (PK)             │         │ id (PK)             │
│ source_id (FK)      │         │ name                │
│ title               │         │ slug                │
│ url                 │         │ description         │
│ content             │         │ icon                │
│ summary             │         │ color               │
│ author              │         │ created_at          │
│ published_date      │         └─────────────────────┘
│ image_url           │
│ fetched_at          │
│ is_published        │
│ view_count          │
│ created_at          │
│ updated_at          │
└──────────┬──────────┘
           │
           │ 1:N
           │
           ▼
┌─────────────────────┐         ┌─────────────────────┐
│  UserInteraction    │    N:1  │        User         │
├─────────────────────┤◄────────├─────────────────────┤
│ id (PK)             │         │ id (PK)             │
│ user_id (FK)        │         │ username            │
│ article_id (FK)     │         │ email               │
│ interaction_type    │         │ first_name          │
│ comment_text        │         │ last_name           │
│ created_at          │         │ date_joined         │
│ updated_at          │         │ last_login          │
└─────────────────────┘         └─────────────────────┘
```

---

## 📋 Model Definitions

### 1. NewsSource Model

**Description**: Stores configuration for each news source

```python
class NewsSource(models.Model):
    """Configuration for a news source."""
    
    SOURCE_TYPES = [
        ('rss', 'RSS Feed'),
        ('scrape', 'Web Scraping'),
        ('api', 'Third-party API'),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    url = models.URLField(unique=True)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    scraping_config = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    fetch_interval = models.IntegerField(default=3600)  # seconds
    last_fetched_at = models.DateTimeField(null=True, blank=True)
    success_count = models.IntegerField(default=0)
    failure_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'news_sources'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['source_type']),
        ]
    
    def __str__(self):
        return self.name
```

**Field Descriptions**:

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `id` | Integer | Primary key | Auto-increment |
| `name` | String(200) | Display name of source | Required |
| `url` | URL | Base URL of news source | Unique, Required |
| `source_type` | String(20) | Type of source (RSS/Scrape/API) | Choices |
| `scraping_config` | JSON | Scraping rules and selectors | Optional |
| `is_active` | Boolean | Whether source is enabled | Default: True |
| `fetch_interval` | Integer | Seconds between fetches | Default: 3600 |
| `last_fetched_at` | DateTime | Last successful fetch | Nullable |
| `success_count` | Integer | Number of successful fetches | Default: 0 |
| `failure_count` | Integer | Number of failed fetches | Default: 0 |
| `created_at` | DateTime | Record creation time | Auto-set |
| `updated_at` | DateTime | Last update time | Auto-update |

**scraping_config JSON Structure**:
```json
{
  "article_list_selector": ".article-list > article",
  "title_selector": "h2.title",
  "content_selector": "div.content",
  "date_selector": "time.published",
  "author_selector": "span.author",
  "image_selector": "img.featured",
  "pagination": {
    "type": "infinite_scroll",
    "trigger": "button.load-more"
  }
}
```

---

### 2. Article Model

**Description**: Stores aggregated news articles

```python
class Article(models.Model):
    """Aggregated news article."""
    
    id = models.AutoField(primary_key=True)
    source = models.ForeignKey(
        NewsSource, 
        on_delete=models.CASCADE,
        related_name='articles'
    )
    title = models.CharField(max_length=500)
    url = models.URLField(unique=True, max_length=2000)
    content = models.TextField()
    summary = models.TextField(blank=True)
    author = models.CharField(max_length=200, blank=True)
    published_date = models.DateTimeField()
    image_url = models.URLField(blank=True, max_length=2000)
    is_published = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)
    fetched_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Many-to-Many relationship with Category
    categories = models.ManyToManyField('Category', related_name='articles')
    
    class Meta:
        db_table = 'articles'
        ordering = ['-published_date']
        indexes = [
            models.Index(fields=['published_date']),
            models.Index(fields=['source', 'published_date']),
            models.Index(fields=['is_published']),
        ]
        # Full-text search index (PostgreSQL specific)
        # Can be added via migration:
        # CREATE INDEX article_search_idx ON articles 
        # USING GIN (to_tsvector('english', title || ' ' || content));
    
    def __str__(self):
        return self.title
```

**Field Descriptions**:

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `id` | Integer | Primary key | Auto-increment |
| `source` | ForeignKey | Reference to NewsSource | CASCADE delete |
| `title` | String(500) | Article headline | Required |
| `url` | URL | Original article URL | Unique, Required |
| `content` | Text | Full article content | Required |
| `summary` | Text | Article summary/excerpt | Optional |
| `author` | String(200) | Article author | Optional |
| `published_date` | DateTime | Original publish date | Required |
| `image_url` | URL | Featured image URL | Optional |
| `is_published` | Boolean | Visibility flag | Default: True |
| `view_count` | Integer | Number of views | Default: 0 |
| `fetched_at` | DateTime | When article was fetched | Auto-set |
| `created_at` | DateTime | Record creation time | Auto-set |
| `updated_at` | DateTime | Last update time | Auto-update |
| `categories` | M2M | Related categories | - |

---

### 3. Category Model

**Description**: Article categorization system

```python
class Category(models.Model):
    """Article category/topic."""
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # Icon class or emoji
    color = models.CharField(max_length=7, default='#3B82F6')  # Hex color
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='subcategories'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
```

**Field Descriptions**:

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `id` | Integer | Primary key | Auto-increment |
| `name` | String(100) | Category name | Unique, Required |
| `slug` | SlugField(100) | URL-friendly name | Unique, Required |
| `description` | Text | Category description | Optional |
| `icon` | String(50) | Icon identifier | Optional |
| `color` | String(7) | Hex color code | Default: #3B82F6 |
| `parent` | ForeignKey | Parent category (for hierarchy) | Nullable |
| `is_active` | Boolean | Visibility flag | Default: True |
| `created_at` | DateTime | Record creation time | Auto-set |

**Example Categories**:
```python
# Top-level categories
categories = [
    {'name': 'Artificial Intelligence', 'slug': 'ai', 'icon': '🤖', 'color': '#8B5CF6'},
    {'name': 'Web Development', 'slug': 'web-dev', 'icon': '🌐', 'color': '#3B82F6'},
    {'name': 'Mobile Development', 'slug': 'mobile', 'icon': '📱', 'color': '#10B981'},
    {'name': 'Cloud Computing', 'slug': 'cloud', 'icon': '☁️', 'color': '#06B6D4'},
    {'name': 'DevOps', 'slug': 'devops', 'icon': '⚙️', 'color': '#F59E0B'},
    {'name': 'Cybersecurity', 'slug': 'security', 'icon': '🔒', 'color': '#EF4444'},
    {'name': 'Data Science', 'slug': 'data-science', 'icon': '📊', 'color': '#EC4899'},
    {'name': 'Programming Languages', 'slug': 'languages', 'icon': '💻', 'color': '#6366F1'},
]
```

---

### 4. UserInteraction Model

**Description**: User interactions with articles

```python
class UserInteraction(models.Model):
    """User interaction with articles (bookmark, like, comment)."""
    
    INTERACTION_TYPES = [
        ('bookmark', 'Bookmark'),
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('share', 'Share'),
    ]
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='interactions'
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='interactions'
    )
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    comment_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_interactions'
        ordering = ['-created_at']
        unique_together = [['user', 'article', 'interaction_type']]
        indexes = [
            models.Index(fields=['user', 'interaction_type']),
            models.Index(fields=['article', 'interaction_type']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.interaction_type} - {self.article.title[:50]}"
```

**Field Descriptions**:

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `id` | Integer | Primary key | Auto-increment |
| `user` | ForeignKey | Reference to User | CASCADE delete |
| `article` | ForeignKey | Reference to Article | CASCADE delete |
| `interaction_type` | String(20) | Type of interaction | Choices |
| `comment_text` | Text | Comment content (if applicable) | Optional |
| `created_at` | DateTime | Interaction timestamp | Auto-set |
| `updated_at` | DateTime | Last update time | Auto-update |

---

### 5. User Model (Django Built-in)

**Description**: Extended Django User model

```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom user model (extends Django's AbstractUser)."""
    
    # Additional fields beyond Django's default
    bio = models.TextField(max_length=500, blank=True)
    avatar_url = models.URLField(blank=True)
    preferred_categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name='subscribers'
    )
    email_notifications = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'users'
```

**Default Django User Fields**:
- `username`, `email`, `password`
- `first_name`, `last_name`
- `is_staff`, `is_active`, `is_superuser`
- `date_joined`, `last_login`

---

## 🔗 Relationships

### One-to-Many Relationships

1. **NewsSource → Article** (1:N)
   - One source has many articles
   - Cascade delete: Deleting a source removes its articles

2. **Article → UserInteraction** (1:N)
   - One article has many interactions
   - Cascade delete: Deleting an article removes its interactions

3. **User → UserInteraction** (1:N)
   - One user has many interactions
   - Cascade delete: Deleting a user removes their interactions

4. **Category → Category** (Self-referential)
   - Categories can have parent categories
   - SET NULL on delete: Deleting parent doesn't delete children

### Many-to-Many Relationships

1. **Article ↔ Category** (N:M)
   - One article can belong to multiple categories
   - One category contains multiple articles
   - Junction table: `article_categories`

2. **User ↔ Category** (N:M via preferred_categories)
   - Users can subscribe to multiple categories
   - Categories can have multiple subscribers

---

## 📊 Database Indexes

### Performance-Critical Indexes

```sql
-- Articles table
CREATE INDEX idx_articles_published_date ON articles(published_date DESC);
CREATE INDEX idx_articles_source_published ON articles(source_id, published_date DESC);
CREATE INDEX idx_articles_is_published ON articles(is_published) WHERE is_published = TRUE;
CREATE INDEX idx_articles_url_hash ON articles USING HASH(url);  -- For uniqueness checks

-- Full-text search (PostgreSQL)
CREATE INDEX idx_articles_search ON articles 
USING GIN(to_tsvector('english', title || ' ' || content));

-- News sources table
CREATE INDEX idx_sources_active ON news_sources(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_sources_type ON news_sources(source_type);

-- User interactions table
CREATE INDEX idx_interactions_user_type ON user_interactions(user_id, interaction_type);
CREATE INDEX idx_interactions_article ON user_interactions(article_id);

-- Categories table
CREATE INDEX idx_categories_slug ON categories(slug);
CREATE INDEX idx_categories_parent ON categories(parent_id);
```

---

## 🔍 Common Queries

### Query Examples

```python
# 1. Get latest articles from active sources
Article.objects.filter(
    source__is_active=True,
    is_published=True
).select_related('source').prefetch_related('categories').order_by('-published_date')[:20]

# 2. Get articles by category
Article.objects.filter(
    categories__slug='ai',
    is_published=True
).order_by('-published_date')

# 3. Get user's bookmarked articles
Article.objects.filter(
    interactions__user=user,
    interactions__interaction_type='bookmark'
).order_by('-interactions__created_at')

# 4. Get trending articles (most interactions in last 7 days)
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

week_ago = timezone.now() - timedelta(days=7)
Article.objects.filter(
    published_date__gte=week_ago
).annotate(
    interaction_count=Count('interactions')
).order_by('-interaction_count')[:10]

# 5. Search articles (PostgreSQL full-text search)
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

search_vector = SearchVector('title', weight='A') + SearchVector('content', weight='B')
search_query = SearchQuery('machine learning')

Article.objects.annotate(
    rank=SearchRank(search_vector, search_query)
).filter(rank__gte=0.3).order_by('-rank')

# 6. Get source statistics
NewsSource.objects.annotate(
    article_count=Count('articles'),
    avg_view_count=Avg('articles__view_count')
).order_by('-article_count')
```

---

## 🗃️ Sample Data

### Initial Data Seeds

```python
# seeds.py - Sample data for development

from sources.models import NewsSource, Article, Category
from django.utils import timezone

# Categories
categories_data = [
    {'name': 'AI & Machine Learning', 'slug': 'ai', 'icon': '🤖'},
    {'name': 'Web Development', 'slug': 'web', 'icon': '🌐'},
    {'name': 'Mobile', 'slug': 'mobile', 'icon': '📱'},
    {'name': 'Cloud & DevOps', 'slug': 'cloud', 'icon': '☁️'},
    {'name': 'Security', 'slug': 'security', 'icon': '🔒'},
]

for cat_data in categories_data:
    Category.objects.get_or_create(**cat_data)

# News Sources
sources_data = [
    {
        'name': 'TechCrunch',
        'url': 'https://techcrunch.com/feed/',
        'source_type': 'rss',
    },
    {
        'name': 'Hacker News',
        'url': 'https://news.ycombinator.com/rss',
        'source_type': 'rss',
    },
    {
        'name': 'Dev.to',
        'url': 'https://dev.to/feed',
        'source_type': 'rss',
    },
]

for source_data in sources_data:
    NewsSource.objects.get_or_create(
        url=source_data['url'],
        defaults=source_data
    )
```

---

## 📈 Database Size Estimates

### Storage Planning

| Table | Avg Row Size | Rows/Year | Annual Storage |
|-------|--------------|-----------|----------------|
| Articles | 10 KB | 50,000 | ~500 MB |
| NewsSource | 1 KB | 100 | ~100 KB |
| Category | 0.5 KB | 50 | ~25 KB |
| UserInteraction | 1 KB | 100,000 | ~100 MB |
| Users | 2 KB | 1,000 | ~2 MB |
| **Total** | - | - | **~600 MB/year** |

**3-Year Projection**: ~1.8 GB (manageable for small VPS)

---

## 🛠️ Database Maintenance

### Regular Tasks

```python
# management/commands/db_maintenance.py

# 1. Clean up old articles (older than 1 year)
from datetime import timedelta
from django.utils import timezone

one_year_ago = timezone.now() - timedelta(days=365)
Article.objects.filter(published_date__lt=one_year_ago).delete()

# 2. Update article statistics
Article.objects.update(view_count=F('view_count'))  # Recalculate

# 3. Vacuum database (PostgreSQL)
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("VACUUM ANALYZE articles;")

# 4. Rebuild indexes
cursor.execute("REINDEX TABLE articles;")
```

---

## 🔐 Data Privacy & Compliance

### PII (Personally Identifiable Information)

**Stored PII**:
- User email (encrypted at rest)
- Username
- User interactions

**GDPR Compliance**:
```python
# User data export
def export_user_data(user):
    return {
        'profile': UserSerializer(user).data,
        'interactions': UserInteractionSerializer(
            user.interactions.all(), many=True
        ).data,
        'bookmarks': user.interactions.filter(
            interaction_type='bookmark'
        ).values('article__title', 'created_at')
    }

# User data deletion (GDPR Right to be Forgotten)
def delete_user_data(user):
    user.interactions.all().delete()
    user.delete()
```

---

## 📝 Migration Strategy

### Initial Migration

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load seed data
python manage.py loaddata categories
```

### Schema Changes

Follow these principles:
1. **Backward compatible changes** (add columns, not remove)
2. **Zero-downtime migrations** (multi-step process)
3. **Data migrations separate from schema** migrations

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-18  
**Author**: @matandasoftware