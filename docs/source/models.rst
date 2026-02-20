Data Models
===========

Complete database schema documentation for Tech Pulse.

**Author:** Matanda Software

Overview
--------

Tech Pulse uses three core models:

1. **Source** - RSS feed sources
2. **Category** - Article categories
3. **Article** - News articles

**Relationships:**

- Source → Articles (One-to-Many)
- Category → Articles (One-to-Many)

Database Diagram
----------------

.. code-block:: text

    ┌──────────────────────┐
    │       Source         │
    ├──────────────────────┤
    │ id (PK)              │
    │ name                 │
    │ url                  │
    │ source_type          │
    │ website              │
    │ description          │
    │ is_active            │
    │ fetch_interval       │
    │ last_fetched         │
    │ created_at           │
    │ updated_at           │
    └──────────┬───────────┘
               │
               │ 1:N (ForeignKey)
               │
    ┌──────────▼───────────┐       ┌──────────────────────┐
    │      Article         │       │      Category        │
    ├──────────────────────┤       ├──────────────────────┤
    │ id (PK)              │       │ id (PK)              │
    │ title                │       │ name                 │
    │ slug                 │       │ slug                 │
    │ url (UNIQUE)         │       │ description          │
    │ content              │       │ created_at           │
    │ summary              │       └──────────┬───────────┘
    │ author               │                  │
    │ source_id (FK) ──────┘                  │ 1:N (ForeignKey)
    │ category_id (FK) ───────────────────────┘
    │ image_url            │
    │ published_at         │
    │ fetched_at           │
    │ created_at           │
    │ updated_at           │
    └──────────────────────┘

Source Model
------------

Represents an RSS feed source.

**File:** ``articles/models.py``

**Table Name:** ``articles_source``

Field Reference
~~~~~~~~~~~~~~~

.. py:class:: Source

   .. py:attribute:: id
      :type: AutoField (Primary Key)

      Auto-incrementing unique identifier.

   .. py:attribute:: name
      :type: CharField(max_length=200)

      Display name of the source.

      **Example:** ``"TechCrunch"``, ``"The Verge"``

      **Required:** Yes

      **Indexed:** No

   .. py:attribute:: url
      :type: URLField(max_length=500)

      RSS feed URL to fetch from.

      **Example:** ``"https://techcrunch.com/feed/"``

      **Required:** Yes

      **Validation:** Must be valid URL format

      **Note:** Should point to RSS/Atom XML feed, not HTML page

   .. py:attribute:: source_type
      :type: CharField(max_length=20)

      Type of source: ``"RSS"``, ``"API"``, or ``"SCRAPER"``

      **Choices:**
      
      - ``RSS`` - RSS/Atom feed (implemented)
      - ``API`` - REST API endpoint (future)
      - ``SCRAPER`` - Web scraping (future)

      **Default:** ``"RSS"``

      **Required:** Yes

   .. py:attribute:: website
      :type: URLField(max_length=500, blank=True, null=True)

      Main website URL (for attribution).

      **Example:** ``"https://techcrunch.com"``

      **Required:** No

   .. py:attribute:: description
      :type: TextField(blank=True)

      Brief description of the source.

      **Example:** ``"Technology and startup news"``

      **Required:** No

   .. py:attribute:: is_active
      :type: BooleanField(default=True)

      Whether to fetch from this source.

      **True:** Source will be included in ``fetch_articles``

      **False:** Source will be skipped

      **Default:** ``True``

      **Use case:** Temporarily disable problematic sources without deleting

   .. py:attribute:: fetch_interval
      :type: IntegerField(default=60)

      Minutes between fetches (for future scheduling).

      **Example:** ``60`` = fetch every hour

      **Default:** ``60``

      **Note:** Not currently enforced by code; for future scheduler

   .. py:attribute:: last_fetched
      :type: DateTimeField(blank=True, null=True)

      Timestamp of last successful fetch.

      **Updated by:** ``fetch_articles`` command

      **Format:** ISO 8601 datetime with timezone

      **Example:** ``2026-02-20T10:30:00Z``

   .. py:attribute:: created_at
      :type: DateTimeField(auto_now_add=True)

      When source was added to database.

      **Automatically set:** On creation

      **Cannot be modified**

   .. py:attribute:: updated_at
      :type: DateTimeField(auto_now=True)

      Last modification time.

      **Automatically updated:** On every save

Methods
~~~~~~~

.. py:method:: article_count()

   Returns the number of articles from this source.

   **Returns:** Integer

   **Example:**

   .. code-block:: python

      source = Source.objects.get(name="TechCrunch")
      count = source.article_count()
      print(f"TechCrunch has {count} articles")

   **Implementation:**

   .. code-block:: python

      def article_count(self):
          return self.articles.count()

.. py:method:: __str__()

   String representation (used in admin and shell).

   **Returns:** Source name

   **Example:** ``"TechCrunch"``

Usage Examples
~~~~~~~~~~~~~~

**Create new source:**

.. code-block:: python

   from articles.models import Source

   source = Source.objects.create(
       name="TechCrunch",
       url="https://techcrunch.com/feed/",
       source_type="RSS",
       website="https://techcrunch.com",
       description="Technology and startup news",
       is_active=True,
       fetch_interval=60
   )

   print(f"Created source: {source.name}")

**Query sources:**

.. code-block:: python

   # Get all active RSS sources
   active_sources = Source.objects.filter(is_active=True, source_type='RSS')

   # Get specific source
   tc = Source.objects.get(name="TechCrunch")

   # Get sources never fetched
   unfetched = Source.objects.filter(last_fetched__isnull=True)

**Update source:**

.. code-block:: python

   source = Source.objects.get(name="TechCrunch")
   source.is_active = False
   source.save()

**Delete source (CASCADE deletes articles):**

.. code-block:: python

   source = Source.objects.get(name="TechCrunch")
   article_count = source.articles.count()
   source.delete()
   print(f"Deleted source and {article_count} articles")

Category Model
--------------

Represents an article category for organization.

**File:** ``articles/models.py``

**Table Name:** ``articles_category``

Field Reference
~~~~~~~~~~~~~~~

.. py:class:: Category

   .. py:attribute:: id
      :type: AutoField (Primary Key)

      Auto-incrementing unique identifier.

   .. py:attribute:: name
      :type: CharField(max_length=100, unique=True)

      Category name.

      **Example:** ``"Technology"``, ``"Artificial Intelligence"``

      **Required:** Yes

      **Unique:** Yes (no duplicate category names)

   .. py:attribute:: slug
      :type: SlugField(max_length=120, unique=True, blank=True)

      URL-friendly version of name.

      **Example:** ``"artificial-intelligence"``

      **Auto-generated:** From ``name`` on save

      **Unique:** Yes

      **Format:** Lowercase, hyphens instead of spaces

   .. py:attribute:: description
      :type: TextField(blank=True)

      Category description.

      **Example:** ``"AI, machine learning, and neural networks"``

      **Required:** No

   .. py:attribute:: created_at
      :type: DateTimeField(auto_now_add=True)

      When category was created.

      **Automatically set:** On creation

Methods
~~~~~~~

.. py:method:: article_count()

   Returns the number of articles in this category.

   **Returns:** Integer

.. py:method:: save(*args, **kwargs)

   Overridden to auto-generate slug from name.

   **Logic:**

   .. code-block:: python

      def save(self, *args, **kwargs):
          if not self.slug:
              self.slug = slugify(self.name)
          super().save(*args, **kwargs)

.. py:method:: __str__()

   String representation.

   **Returns:** Category name

Usage Examples
~~~~~~~~~~~~~~

**Create category:**

.. code-block:: python

   from articles.models import Category

   category = Category.objects.create(
       name="Artificial Intelligence",
       description="AI, machine learning, and neural networks"
   )

   print(f"Slug: {category.slug}")  # "artificial-intelligence"

**Query categories:**

.. code-block:: python

   # Get all categories
   categories = Category.objects.all()

   # Get by slug
   ai_category = Category.objects.get(slug="artificial-intelligence")

   # Get categories with articles
   active_categories = Category.objects.filter(articles__isnull=False).distinct()

**Count articles:**

.. code-block:: python

   category = Category.objects.get(name="Technology")
   count = category.article_count()
   print(f"{category.name} has {count} articles")

Article Model
-------------

Represents a news article fetched from RSS feeds.

**File:** ``articles/models.py``

**Table Name:** ``articles_article``

Field Reference
~~~~~~~~~~~~~~~

.. py:class:: Article

   .. py:attribute:: id
      :type: AutoField (Primary Key)

      Auto-incrementing unique identifier.

   .. py:attribute:: title
      :type: CharField(max_length=500)

      Article title.

      **Example:** ``"ChatGPT-5 Released with Advanced Reasoning"``

      **Required:** Yes

      **Max Length:** 500 characters

      **Indexed:** No (but searchable)

   .. py:attribute:: slug
      :type: SlugField(max_length=550, unique=True, blank=True)

      URL-friendly version of title.

      **Example:** ``"chatgpt-5-released-with-advanced-reasoning"``

      **Auto-generated:** From ``title`` on save

      **Unique:** Yes

      **Use case:** SEO-friendly URLs, human-readable identifiers

   .. py:attribute:: url
      :type: URLField(max_length=500, unique=True)

      Original article URL.

      **Example:** ``"https://techcrunch.com/2026/02/18/chatgpt-5-released"``

      **Required:** Yes

      **Unique:** Yes (prevents duplicate articles)

      **Note:** Used as primary duplicate detection key in ``fetch_articles``

   .. py:attribute:: content
      :type: TextField(blank=True)

      Full article content.

      **Source:** Extracted from RSS ``<content>`` or ``<description>`` tags

      **Required:** No

      **Length:** Unlimited

      **Note:** May contain HTML tags

   .. py:attribute:: summary
      :type: TextField(blank=True)

      Short article summary.

      **Source:** RSS ``<summary>`` tag or first 200 chars of content

      **Required:** No

      **Typical Length:** 100-200 characters

      **Use case:** Preview text, meta descriptions

   .. py:attribute:: author
      :type: CharField(max_length=200, blank=True, default="Unknown")

      Article author name.

      **Example:** ``"John Doe"``, ``"Jane Smith"``

      **Source:** RSS ``<author>`` tag

      **Default:** ``"Unknown"`` if not provided

      **Required:** No

   .. py:attribute:: source
      :type: ForeignKey(Source, on_delete=CASCADE, related_name='articles')

      Which source this article came from.

      **Relationship:** Many articles to one source

      **On Delete:** CASCADE (delete articles when source is deleted)

      **Required:** Yes

      **Reverse Relationship:** ``source.articles.all()``

   .. py:attribute:: category
      :type: ForeignKey(Category, on_delete=SET_NULL, related_name='articles', blank=True, null=True)

      Article category.

      **Relationship:** Many articles to one category

      **On Delete:** SET_NULL (keep articles, clear category)

      **Required:** No

      **Reverse Relationship:** ``category.articles.all()``

   .. py:attribute:: image_url
      :type: URLField(max_length=500, blank=True, null=True)

      Featured image URL.

      **Source:** RSS ``<media:content>``, ``<media:thumbnail>``, or ``<enclosure>`` tags

      **Required:** No

      **Note:** External URL (not hosted locally)

   .. py:attribute:: published_at
      :type: DateTimeField()

      When article was originally published.

      **Source:** RSS ``<published>`` or ``<pubDate>`` tag

      **Format:** Timezone-aware datetime

      **Default:** Current time if not provided

      **Required:** Yes (but auto-set)

   .. py:attribute:: fetched_at
      :type: DateTimeField(auto_now_add=True)

      When we fetched this article.

      **Automatically set:** On creation

      **Cannot be modified**

      **Use case:** Track how fresh our data is

   .. py:attribute:: created_at
      :type: DateTimeField(auto_now_add=True)

      When record was created in our database.

      **Automatically set:** On creation

   .. py:attribute:: updated_at
      :type: DateTimeField(auto_now=True)

      Last modification time.

      **Automatically updated:** On every save

      **Use case:** Track when articles were re-fetched/updated

Methods
~~~~~~~

.. py:method:: save(*args, **kwargs)

   Overridden to auto-generate slug from title.

   **Logic:**

   .. code-block:: python

      def save(self, *args, **kwargs):
          if not self.slug:
              base_slug = slugify(self.title)
              unique_slug = base_slug
              num = 1
              while Article.objects.filter(slug=unique_slug).exists():
                  unique_slug = f"{base_slug}-{num}"
                  num += 1
              self.slug = unique_slug
          super().save(*args, **kwargs)

   **Handles duplicates:** Appends ``-1``, ``-2``, etc. if slug exists

.. py:method:: __str__()

   String representation.

   **Returns:** Article title (truncated to 50 chars)

   **Example:** ``"ChatGPT-5 Released with Advanced Reasoning"``

Usage Examples
~~~~~~~~~~~~~~

**Create article:**

.. code-block:: python

   from articles.models import Article, Source, Category
   from django.utils import timezone

   source = Source.objects.get(name="TechCrunch")
   category = Category.objects.get(name="Artificial Intelligence")

   article = Article.objects.create(
       title="ChatGPT-5 Released",
       url="https://techcrunch.com/chatgpt-5",
       content="Full article content...",
       summary="OpenAI announces ChatGPT-5...",
       author="John Doe",
       source=source,
       category=category,
       published_at=timezone.now(),
       image_url="https://example.com/image.jpg"
   )

**Query articles:**

.. code-block:: python

   # Latest 10 articles
   latest = Article.objects.order_by('-published_at')[:10]

   # TechCrunch articles only
   tc_articles = Article.objects.filter(source__name="TechCrunch")

   # AI category articles
   ai_articles = Article.objects.filter(category__name="Artificial Intelligence")

   # Search by keyword
   ai_search = Article.objects.filter(title__icontains="AI")

   # Articles from last 24 hours
   from datetime import timedelta
   recent = Article.objects.filter(
       published_at__gte=timezone.now() - timedelta(days=1)
   )

**Optimized queries (avoid N+1):**

.. code-block:: python

   # Without optimization (N+1 queries)
   articles = Article.objects.all()
   for article in articles:
       print(article.source.name)  # Separate query for each!

   # With optimization (2 queries total)
   articles = Article.objects.select_related('source', 'category').all()
   for article in articles:
       print(article.source.name)  # No extra query!

**Update article:**

.. code-block:: python

   article = Article.objects.get(id=1)
   article.category = Category.objects.get(name="Technology")
   article.save()

**Delete article:**

.. code-block:: python

   article = Article.objects.get(id=1)
   article.delete()

**Bulk operations:**

.. code-block:: python

   # Delete old articles
   Article.objects.filter(
       published_at__lt=timezone.now() - timedelta(days=365)
   ).delete()

   # Bulk update category
   Article.objects.filter(title__icontains="AI").update(
       category=Category.objects.get(name="Artificial Intelligence")
   )

Model Relationships
-------------------

Accessing Related Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~

**From Source to Articles:**

.. code-block:: python

   source = Source.objects.get(name="TechCrunch")
   
   # Get all articles
   articles = source.articles.all()
   
   # Count articles
   count = source.articles.count()
   
   # Filter related articles
   recent = source.articles.filter(
       published_at__gte=timezone.now() - timedelta(days=7)
   )

**From Category to Articles:**

.. code-block:: python

   category = Category.objects.get(name="Technology")
   
   # Get all articles
   articles = category.articles.all()
   
   # Latest 5
   latest = category.articles.order_by('-published_at')[:5]

**From Article to Source/Category:**

.. code-block:: python

   article = Article.objects.get(id=1)
   
   # Access source
   print(f"Source: {article.source.name}")
   print(f"Source URL: {article.source.url}")
   
   # Access category (may be None)
   if article.category:
       print(f"Category: {article.category.name}")

Database Indexes
----------------

**Current indexes:**

- Primary keys (``id`` fields) - automatic
- ``Article.url`` - unique constraint creates index
- ``Article.slug`` - unique constraint creates index
- ``Category.name`` - unique constraint creates index
- ``Category.slug`` - unique constraint creates index

**Consider adding for performance:**

.. code-block:: python

   class Article(models.Model):
       # ... fields ...
       
       class Meta:
           indexes = [
               models.Index(fields=['-published_at']),  # For sorting by date
               models.Index(fields=['source', '-published_at']),  # For source+date queries
           ]

Data Validation
---------------

**Model-level validation:**

- ``url`` - Must be valid URL format
- ``unique`` constraints prevent duplicates
- ``max_length`` prevents excessively long data
- ``ForeignKey`` constraints ensure referential integrity

**Example validation in action:**

.. code-block:: python

   # This will raise ValidationError
   article = Article(
       title="",  # Empty title - ValidationError
       url="not-a-url",  # Invalid URL - ValidationError
       source=999,  # Non-existent source - IntegrityError
   )
   article.full_clean()  # Trigger validation

Migrations
----------

**Initial migration:** ``articles/migrations/0001_initial.py``

**Created tables:**

- ``articles_source``
- ``articles_category``
- ``articles_article``

**To create new migration after model changes:**

.. code-block:: bash

   python manage.py makemigrations

**To apply migrations:**

.. code-block:: bash

   python manage.py migrate

Database Schema SQL
-------------------

**Actual SQL (SQLite):**

.. code-block:: sql

   CREATE TABLE "articles_source" (
       "id" INTEGER PRIMARY KEY AUTOINCREMENT,
       "name" VARCHAR(200) NOT NULL,
       "url" VARCHAR(500) NOT NULL,
       "source_type" VARCHAR(20) NOT NULL,
       "website" VARCHAR(500),
       "description" TEXT,
       "is_active" BOOLEAN NOT NULL,
       "fetch_interval" INTEGER NOT NULL,
       "last_fetched" DATETIME,
       "created_at" DATETIME NOT NULL,
       "updated_at" DATETIME NOT NULL
   );

   CREATE TABLE "articles_category" (
       "id" INTEGER PRIMARY KEY AUTOINCREMENT,
       "name" VARCHAR(100) UNIQUE NOT NULL,
       "slug" VARCHAR(120) UNIQUE NOT NULL,
       "description" TEXT,
       "created_at" DATETIME NOT NULL
   );

   CREATE TABLE "articles_article" (
       "id" INTEGER PRIMARY KEY AUTOINCREMENT,
       "title" VARCHAR(500) NOT NULL,
       "slug" VARCHAR(550) UNIQUE NOT NULL,
       "url" VARCHAR(500) UNIQUE NOT NULL,
       "content" TEXT,
       "summary" TEXT,
       "author" VARCHAR(200),
       "image_url" VARCHAR(500),
       "published_at" DATETIME NOT NULL,
       "fetched_at" DATETIME NOT NULL,
       "created_at" DATETIME NOT NULL,
       "updated_at" DATETIME NOT NULL,
       "source_id" INTEGER NOT NULL REFERENCES "articles_source"("id"),
       "category_id" INTEGER REFERENCES "articles_category"("id")
   );

   CREATE INDEX "articles_article_source_id" ON "articles_article"("source_id");
   CREATE INDEX "articles_article_category_id" ON "articles_article"("category_id");

Summary
-------

**3 Models:**

- **Source:** RSS feed sources (6 in database)
- **Category:** Article categories (7 in database)
- **Article:** News articles (100+ in database)

**Key Features:**

- ✅ Auto-generated slugs for SEO
- ✅ Duplicate prevention (unique URLs)
- ✅ Cascade delete (source → articles)
- ✅ Timezone-aware timestamps
- ✅ Optimized relationships (select_related)

*Created by Matanda Software*