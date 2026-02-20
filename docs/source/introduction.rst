Introduction
============

Overview
--------

Tech Pulse is a news aggregation REST API built with Django and Django REST Framework. It automatically fetches articles from multiple RSS feeds, stores them in a database, and provides a powerful API for querying and filtering articles.

**Created by:** Matanda Software

Key Features
------------

📰 **RSS Feed Aggregation**
   Automatically fetch articles from multiple tech news sources including TechCrunch, The Verge, Ars Technica, Wired, and Hacker News.

🔍 **Advanced Search**
   Full-text search across article titles, content, and authors using Django's search functionality.

🎯 **Smart Filtering**
   Filter articles by source, category, publication date, and more. Combine multiple filters for precise results.

📊 **Pagination**
   Efficiently handle large datasets with built-in pagination (20 articles per page by default).

🔒 **Flexible Permissions**
   Public read access for browsing, authenticated access for creating/updating content.

⚡ **Performance Optimized**
   Database queries optimized with select_related and prefetch_related for fast response times.

🤖 **Automation Ready**
   Built-in management command for scheduled RSS feed fetching (cron/celery compatible).

📚 **Comprehensive API**
   RESTful API with filtering, search, ordering, and pagination built-in.

Tech Stack
----------

**Backend Framework:**

- Python 3.12
- Django 6.0.2
- Django REST Framework 3.15

**Key Libraries:**

- django-filter 24.3 - Advanced filtering
- feedparser - RSS/Atom feed parsing
- requests - HTTP library for fetching feeds

**Database:**

- SQLite (development)
- PostgreSQL-ready (production)

**Documentation:**

- Sphinx with Read the Docs theme

**Version Control:**

- Git & GitHub

Project Structure
-----------------

.. code-block:: text

    tech-pulse/
    ├── articles/                      # Main Django app
    │   ├── management/
    │   │   └── commands/
    │   │       └── fetch_articles.py  # RSS fetcher command
    │   ├── migrations/                # Database migrations
    │   ├── admin.py                   # Admin configuration
    │   ├── models.py                  # Data models
    │   ├── serializers.py             # DRF serializers
    │   ├── urls.py                    # API routing
    │   └── views.py                   # API views
    ├── backend/                       # Django settings
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── docs/                          # Sphinx documentation
    │   ├── source/
    │   └── build/
    ├── venv/                          # Virtual environment
    ├── manage.py
    └── requirements.txt

Use Cases
---------

**News Aggregation Platforms**
   Build a centralized dashboard for tech news from multiple sources.

**Content Curation**
   Automatically collect and categorize articles for content marketing.

**Research & Analysis**
   Gather tech news data for trend analysis and market research.

**Personal News Feed**
   Create a customized tech news feed with your favorite sources.

**API Backend**
   Provide article data to mobile apps, websites, or other services.

Architecture
------------

**Data Flow:**

1. RSS feeds are configured in the admin panel
2. Management command fetches articles from active sources
3. Articles are parsed and stored in database (duplicates prevented)
4. REST API exposes articles with filtering/search/pagination
5. Clients consume API to display articles

**Key Design Decisions:**

- **URL-based deduplication:** Articles are unique by URL to prevent duplicates
- **Source tracking:** Every article links to its source for attribution
- **Timezone-aware:** All timestamps use Django's timezone utilities
- **Slug generation:** Automatic URL-friendly slugs for SEO
- **Read-only by default:** Public API is read-only for security

Why Tech Pulse?
---------------

✅ **Production-Ready Code**
   Robust error handling, validation, and security best practices.

✅ **Scalable Architecture**
   Designed to handle thousands of articles efficiently.

✅ **Developer-Friendly**
   Clean code, comprehensive documentation, easy to extend.

✅ **Portfolio Quality**
   Demonstrates full-stack API development skills.

✅ **Real-World Functionality**
   Solves actual problems (news aggregation, content curation).

Author
------

**Matanda Software**

- GitHub: https://github.com/matandasoftware
- Repository: https://github.com/matandasoftware/tech-pulse

License
-------

This project is available for portfolio and educational purposes.

Next Steps
----------

- **Installation:** See :doc:`installation` to get started
- **API Reference:** See :doc:`api_endpoints` for endpoint documentation
- **Usage Guide:** See :doc:`usage` for examples