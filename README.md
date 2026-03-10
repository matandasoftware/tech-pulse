# Tech Pulse v1.0 🚀

**A Django-powered RSS news aggregation platform that automatically fetches, organizes, and serves tech news articles through a REST API.**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16.1-orange.svg)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Automation](#automation)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## 🎯 Overview

**Tech Pulse v1.0** is a news aggregation platform built with Django and Django REST Framework. It automatically fetches articles from RSS feeds, categorizes them, and provides a clean REST API for accessing aggregated content.

Perfect for:
- Building custom news readers
- Aggregating industry-specific content
- Learning Django REST Framework
- Automated content curation

---

## ✨ Features

### Core Functionality
- ✅ **Automated RSS Fetching** - Scheduled article retrieval from multiple sources
- ✅ **RESTful API** - Full CRUD operations for sources, categories, and articles
- ✅ **Content Management** - Django admin interface with custom filters
- ✅ **Duplicate Prevention** - URL-based article deduplication
- ✅ **Search & Filter** - Advanced filtering by source, category, date, and keywords
- ✅ **Pagination** - Built-in API pagination for large datasets
- ✅ **Windows Scheduler Ready** - Automated fetch script included

### Technical Features
- 🔧 Clean architecture with separation of concerns
- 📚 Comprehensive inline documentation
- 🛡️ Error handling for network failures and parsing issues
- 🎨 Custom Django admin interface
- 📊 Source activity tracking (last fetched, article counts)
- 🔐 Authentication-ready API (IsAuthenticatedOrReadOnly)

---

## 🛠️ Tech Stack

### Backend
- **Python 3.11+**
- **Django 6.0.2** - Web framework
- **Django REST Framework 3.16.1** - API toolkit
- **django-filter 25.2** - Advanced filtering

### Data & Processing
- **SQLite** - Development database
- **feedparser 6.0.12** - RSS feed parsing
- **requests 2.32.5** - HTTP library

### Documentation
- **Sphinx 9.1.0** - Documentation generator
- **sphinx_rtd_theme 3.1.0** - Read the Docs theme

### Additional Tools
- **colorama 0.4.6** - Terminal colors
- **Jinja2 3.1.6** - Templating
- **Pygments 2.19.2** - Syntax highlighting

---

## 📂 Project Structure

```
tech-pulse/
├── backend/                    # Django project settings
│   ├── settings.py            # Main configuration
│   ├── urls.py                # URL routing
│   ├── wsgi.py                # WSGI entry point
│   └── asgi.py                # ASGI entry point
│
├── articles/                   # Main Django app
│   ├── models.py              # Source, Category, Article models
│   ├── views.py               # API ViewSets
│   ├── serializers.py         # DRF serializers
│   ├── admin.py               # Admin interface customization
│   ├── urls.py                # API URL patterns
│   └── management/
│       └── commands/
│           └── fetch_articles.py  # RSS fetching command
│
├── docs/                       # Sphinx documentation
│   ├── source/                # Documentation source files
│   ├── Makefile              # Unix build script
│   └── make.bat              # Windows build script
│
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── fetch_articles.bat         # Windows scheduler script
└── README.md                  # This file
```

---

## 🚀 Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- virtualenv (recommended)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/matandasoftware/tech-pulse.git
cd tech-pulse
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### Step 6: Run Development Server

```bash
python manage.py runserver
```

Access the application:
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **API Root:** http://127.0.0.1:8000/api/
- **Browsable API:** http://127.0.0.1:8000/api-auth/

---

## 💻 Usage

### Adding RSS Sources

1. Log in to the admin panel: http://127.0.0.1:8000/admin/
2. Navigate to **Sources** → **Add Source**
3. Fill in:
   - **Name:** Source identifier (e.g., "TechCrunch")
   - **URL:** RSS feed URL
   - **Source Type:** Select "RSS Feed"
   - **Is Active:** Check to enable fetching
   - **Fetch Interval:** Minutes between fetches (default: 60)
4. Save

### Creating Categories

1. Navigate to **Categories** → **Add Category**
2. Enter category name (e.g., "Technology", "Business")
3. Slug will auto-generate
4. Save

### Fetching Articles

**Manual Fetch (All Sources):**
```bash
python manage.py fetch_articles
```

**Fetch from Specific Source:**
```bash
python manage.py fetch_articles --source 1
```

**Output Example:**
```
Starting RSS feed fetch...

Fetching from: TechCrunch
  URL: https://techcrunch.com/feed/
  ✓ Fetched 25 entries
  ✓ Created: 15 | Updated: 5 | Skipped: 5

SUMMARY:
  Total Fetched: 25
  Total Created: 15
  Total Updated: 5
  Total Skipped: 5
```

---

## 🌐 API Endpoints

### Base URL
```
http://127.0.0.1:8000/api/
```

### Sources API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/sources/` | List all sources |
| GET | `/api/sources/{id}/` | Retrieve single source |
| POST | `/api/sources/` | Create source (admin) |
| PUT | `/api/sources/{id}/` | Update source (admin) |
| DELETE | `/api/sources/{id}/` | Delete source (admin) |

**Query Parameters:**
- `search` - Search by name or URL
- `ordering` - Order by name, created_at

**Example Response:**
```json
{
  "id": 1,
  "name": "TechCrunch",
  "url": "https://techcrunch.com/feed/",
  "source_type": "RSS",
  "is_active": true,
  "fetch_interval": 60,
  "last_fetched": "2026-02-26T10:30:00Z",
  "article_count": 142,
  "created_at": "2026-02-20T08:00:00Z",
  "updated_at": "2026-02-26T10:30:00Z"
}
```

### Categories API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories/` | List all categories |
| GET | `/api/categories/{id}/` | Retrieve single category |
| POST | `/api/categories/` | Create category (admin) |
| PUT | `/api/categories/{id}/` | Update category (admin) |
| DELETE | `/api/categories/{id}/` | Delete category (admin) |

**Example Response:**
```json
{
  "id": 1,
  "name": "Technology",
  "slug": "technology",
  "description": "Tech news and innovations",
  "article_count": 89,
  "created_at": "2026-02-20T08:00:00Z"
}
```

### Articles API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/articles/` | List all articles |
| GET | `/api/articles/{id}/` | Retrieve single article |
| POST | `/api/articles/` | Create article (admin) |
| PUT | `/api/articles/{id}/` | Update article (admin) |
| DELETE | `/api/articles/{id}/` | Delete article (admin) |

**Query Parameters:**
- `source` - Filter by source ID
- `category` - Filter by category ID
- `published_at` - Filter by publish date
- `search` - Search title, content, author
- `ordering` - Order by published_at, fetched_at, title

**Example Response:**
```json
{
  "id": 1,
  "title": "Breaking: New AI Model Released",
  "slug": "breaking-new-ai-model-released",
  "url": "https://example.com/article",
  "content": "Full article content...",
  "summary": "Brief summary...",
  "image_url": "https://example.com/image.jpg",
  "author": "John Doe",
  "source": 1,
  "source_name": "TechCrunch",
  "category": 1,
  "category_name": "Technology",
  "published_at": "2026-02-26T09:00:00Z",
  "fetched_at": "2026-02-26T10:30:00Z",
  "updated_at": "2026-02-26T10:30:00Z"
}
```

---

## ⏰ Automation

### Windows Task Scheduler (Recommended for Windows)

The project includes `fetch_articles.bat` for automated fetching.

**Setup:**

1. **Edit the batch file** - Update paths in `fetch_articles.bat`:
   ```batch
   SET PROJECT_DIR=C:\path\to\your\tech-pulse
   ```

2. **Open Task Scheduler** - Windows → Search "Task Scheduler"

3. **Create Basic Task:**
   - Name: "Tech Pulse Article Fetch"
   - Trigger: Daily at preferred time (e.g., every 6 hours)
   - Action: Start a Program
   - Program/script: Browse to `fetch_articles.bat`

4. **Save and Test**

**Logs:** Check `logs/fetch_articles.log` for execution history.

### Linux/macOS Cron Job

Add to crontab (`crontab -e`):

```bash
# Fetch articles every 6 hours
0 */6 * * * cd /path/to/tech-pulse && /path/to/venv/bin/python manage.py fetch_articles >> logs/fetch.log 2>&1
```

### Celery (Advanced - Production)

For production deployments, consider integrating Celery for async task processing.

---

## ⚙️ Configuration

### Database

**Development (SQLite - Default):**
```python
# backend/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Production (PostgreSQL - Recommended):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'techpulse',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Timezone

Update timezone in `backend/settings.py`:
```python
TIME_ZONE = 'UTC'  # Change to your timezone (e.g., 'America/New_York')
```

### Pagination

Adjust API pagination in `backend/settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20  # Change default page size
}
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes:**
   ```bash
   git commit -m "Add amazing feature"
   ```
4. **Push to the branch:**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide
- Write descriptive commit messages
- Add docstrings to new functions/classes
- Update documentation for new features
- Test thoroughly before submitting PR

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Pfarelo Channel Mudau**  
*Matanda Software*

- **GitHub:** [@matandasoftware](https://github.com/matandasoftware)
- **Email:** pfarelochannel@gmail.com
- **Portfolio:** [HyperionDev Portfolio](https://www.hyperiondev.com/portfolio/PC25060018465/)
- **LinkedIn:** [Pfarelo Mudau](https://linkedin.com/in/pfarelo-mudau-37882a3a9)

### About the Developer

Software Engineer | Physics Graduate | Bomb Technician (SAPS)

Ranked **2nd out of 115 students** (98% average) in HyperionDev's Software Engineering Bootcamp. Passionate about building scalable systems that bridge the gap between human needs and technological solutions.

---

## 🙏 Acknowledgments

- **Django Community** - For the excellent framework and documentation
- **Django REST Framework** - For making API development enjoyable
- **HyperionDev** - For comprehensive software engineering education
- **RSS Feed Providers** - For making content accessible

---

## 📚 Documentation

Full project documentation (built with Sphinx):

```bash
cd docs
make html  # Linux/macOS
# OR
make.bat html  # Windows
```

View docs: `docs/build/html/index.html`

---

## 🔮 Future Enhancements

- [ ] Frontend React/Vue.js interface
- [ ] Docker containerization
- [ ] PostgreSQL migration
- [ ] Celery integration for async tasks
- [ ] Email notifications for new articles
- [ ] AI-powered article categorization
- [ ] User authentication and personalized feeds
- [ ] Article sentiment analysis
- [ ] GraphQL API endpoint

---

## 📸 Screenshots

*Coming soon - Admin interface and API browsable views*

---

## 🐛 Known Issues

- RSS feeds with malformed XML may fail silently
- Some sources may require custom User-Agent headers
- Timezone handling for article publish dates varies by source

**Report issues:** [GitHub Issues](https://github.com/matandasoftware/tech-pulse/issues)

---

## 📞 Support

Need help? Have questions?

- **Issues:** [GitHub Issues](https://github.com/matandasoftware/tech-pulse/issues)
- **Email:** pfarelochannel@gmail.com
- **Discussions:** [GitHub Discussions](https://github.com/matandasoftware/tech-pulse/discussions)

---

**Built with ❤️ using Django & DRF**

*Tech Pulse v1.0 - Aggregating the future, one article at a time.*