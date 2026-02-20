Management Commands
===================

Custom Django management commands for automation and maintenance.

**Author:** Matanda Software

Overview
--------

Tech Pulse includes custom management commands that extend Django's built-in ``manage.py`` functionality.

**Available Commands:**

- ``fetch_articles`` - Fetch articles from RSS feeds

**Location:** ``articles/management/commands/``

fetch_articles Command
----------------------

Fetches articles from all active RSS sources and saves them to the database.

**File:** ``articles/management/commands/fetch_articles.py``

**Author:** Matanda Software

**Purpose:** Automate article collection from RSS feeds without manual intervention.

Synopsis
~~~~~~~~

.. code-block:: bash

   python manage.py fetch_articles [OPTIONS]

**Options:**

.. option:: --source <ID>

   Fetch from a specific source ID only. If not provided, fetches from all active RSS sources.

   **Type:** Integer

   **Example:** ``--source 1``

Description
~~~~~~~~~~~

The ``fetch_articles`` command automates the process of collecting news articles from RSS feeds. It:

1. **Queries Database:** Finds all active RSS sources (or specific source if ``--source`` provided)
2. **Fetches Feeds:** Makes HTTP request to each RSS feed URL
3. **Parses XML:** Uses ``feedparser`` library to parse RSS/Atom XML
4. **Extracts Data:** Pulls title, URL, content, author, date, image from each entry
5. **Prevents Duplicates:** Uses ``update_or_create`` with URL as unique key
6. **Saves to Database:** Creates new articles or updates existing ones
7. **Updates Timestamp:** Records when source was last fetched
8. **Reports Results:** Prints detailed summary to console

**Key Features:**

- ✅ **Robust Error Handling:** Continues processing even if one source fails
- ✅ **Encoding Support:** Handles UTF-8, ASCII, and other encodings automatically
- ✅ **Timeout Protection:** 30-second timeout prevents hanging on slow feeds
- ✅ **Custom User-Agent:** Identifies as TechPulse for better server compatibility
- ✅ **Detailed Logging:** Console output shows progress and errors
- ✅ **Idempotent:** Safe to run multiple times (no duplicates created)

Usage Examples
~~~~~~~~~~~~~~

**Fetch from all active sources:**

.. code-block:: bash

   python manage.py fetch_articles

**Output:**

.. code-block:: text

   Starting RSS feed fetch...

   Fetching from: TechCrunch
     URL: https://techcrunch.com/feed/
     Found 20 entries
     ✓ Created: Threads posts can now be shared directly to your Instagram...
     ✓ Created: Toy Story 5 takes aim at creepy AI toys...
     ✓ Created: Meta's metaverse leaves virtual reality...
     Summary: 20 created, 0 updated, 0 skipped

   Fetching from: The Verge
     URL: https://www.theverge.com/rss/index.xml
     Found 18 entries
     ✓ Created: Apple announces new iPad Pro...
     Summary: 18 created, 0 updated, 0 skipped

   ======================================================================
   Fetch complete!
     Total entries processed: 38
     ✓ New articles created: 38
     ↻ Existing articles updated: 0
   ======================================================================

**Fetch from specific source:**

.. code-block:: bash

   python manage.py fetch_articles --source 1

**Output:**

.. code-block:: text

   Starting RSS feed fetch...

   Fetching from: TechCrunch
     URL: https://techcrunch.com/feed/
     Found 20 entries
     ✓ Created: New article 1...
     ✓ Created: New article 2...
     Summary: 20 created, 0 updated, 0 skipped

   ======================================================================
   Fetch complete!
     Total entries processed: 20
     ✓ New articles created: 20
   ======================================================================

**Re-running (updates existing articles):**

.. code-block:: bash

   python manage.py fetch_articles

**Output:**

.. code-block:: text

   Starting RSS feed fetch...

   Fetching from: TechCrunch
     URL: https://techcrunch.com/feed/
     Found 20 entries
     ↻ Updated: Threads posts can now be shared...
     ↻ Updated: Toy Story 5 takes aim at creepy AI toys...
     ✓ Created: Brand new article published just now...
     Summary: 1 created, 19 updated, 0 skipped

   ======================================================================
   Fetch complete!
     Total entries processed: 20
     ✓ New articles created: 1
     ↻ Existing articles updated: 19
   ======================================================================

Command Structure
~~~~~~~~~~~~~~~~~

**Class-Based Command:**

.. code-block:: python

   from django.core.management.base import BaseCommand

   class Command(BaseCommand):
       """
       Fetch articles from RSS feeds and save to database.
       """
       help = 'Fetch articles from active RSS feed sources'

       def add_arguments(self, parser):
           """Define command-line arguments"""
           parser.add_argument(
               '--source',
               type=int,
               help='Fetch from specific source ID only',
           )

       def handle(self, *args, **options):
           """Main command logic"""
           # Fetch and process articles

       def extract_article_data(self, entry, source):
           """Extract data from RSS entry"""
           # Parse RSS entry into Article fields

**Key Components:**

1. **help** - Short description (shown in ``python manage.py help``)
2. **add_arguments()** - Define command-line arguments
3. **handle()** - Main execution logic
4. **extract_article_data()** - Helper method for data extraction

How It Works
~~~~~~~~~~~~

**Step 1: Query Sources**

.. code-block:: python

   if options['source']:
       sources = Source.objects.filter(id=options['source'], is_active=True, source_type='RSS')
   else:
       sources = Source.objects.filter(is_active=True, source_type='RSS')

**Filters:**

- ``is_active=True`` - Only active sources
- ``source_type='RSS'`` - Only RSS sources (not API/SCRAPER)
- Optional: ``id=X`` - Specific source if ``--source`` provided

**Step 2: Fetch RSS Feed**

.. code-block:: python

   response = requests.get(
       source.url,
       timeout=30,
       headers={
           'User-Agent': 'TechPulse/1.0 (RSS Reader; +https://github.com/matandasoftware/tech-pulse)'
       }
   )
   response.raise_for_status()
   feed = feedparser.parse(response.content)

**Why requests + feedparser:**

- ``requests`` handles HTTP, encoding, timeouts
- ``feedparser`` handles RSS/Atom XML parsing
- Together: Robust against encoding issues

**Step 3: Parse Entries**

.. code-block:: python

   for entry in feed.entries:
       article_data = self.extract_article_data(entry, source)
       article, created = Article.objects.update_or_create(
           url=article_data['url'],
           defaults=article_data
       )

**update_or_create logic:**

1. Look for existing article with same URL
2. If found: **Update** with new data
3. If not found: **Create** new article

**Prevents duplicates!** ✅

**Step 4: Extract Data**

.. code-block:: python

   def extract_article_data(self, entry, source):
       # Get title
       title = entry.get('title', 'No Title').strip()
       
       # Get URL (required)
       url = entry.get('link', '').strip()
       
       # Get content (try multiple sources)
       content = ''
       if hasattr(entry, 'content'):
           content = entry.content[0].get('value', '')
       elif hasattr(entry, 'description'):
           content = entry.description
       
       # Get summary
       summary = entry.get('summary', '')
       if not summary and content:
           summary = content[:200] + '...'
       
       # Get author
       author = entry.get('author', 'Unknown').strip()
       
       # Get published date
       published_at = None
       if hasattr(entry, 'published_parsed') and entry.published_parsed:
           published_at = timezone.datetime(*entry.published_parsed[:6])
           if timezone.is_naive(published_at):
               published_at = timezone.make_aware(published_at)
       else:
           published_at = timezone.now()
       
       # Get image URL
       image_url = None
       if hasattr(entry, 'media_content') and entry.media_content:
           image_url = entry.media_content[0].get('url')
       elif hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
           image_url = entry.media_thumbnail[0].get('url')
       
       return {
           'title': title[:500],
           'url': url[:500],
           'content': content,
           'summary': summary[:1000] if summary else '',
           'author': author[:200],
           'source': source,
           'category': None,  # Can be assigned later
           'published_at': published_at,
           'image_url': image_url[:500] if image_url else None,
           'fetched_at': timezone.now(),
       }

**Data Sources (RSS fields):**

- ``title`` ← ``<title>``
- ``url`` ← ``<link>``
- ``content`` ← ``<content:encoded>`` or ``<description>``
- ``summary`` ← ``<summary>`` or first 200 chars of content
- ``author`` ← ``<author>`` or ``<dc:creator>``
- ``published_at`` ← ``<published>`` or ``<pubDate>``
- ``image_url`` ← ``<media:content>``, ``<media:thumbnail>``, or ``<enclosure>``

**Step 5: Update Timestamp**

.. code-block:: python

   source.last_fetched = timezone.now()
   source.save()

**Tracks when source was last fetched** (visible in admin panel).

Error Handling
~~~~~~~~~~~~~~

The command handles multiple error types gracefully:

**Timeout Errors:**

.. code-block:: text

   Fetching from: SlowSource
     URL: https://slowfeed.com/rss
     ✗ Timeout: Feed took too long to respond

**Connection Errors:**

.. code-block:: text

   Fetching from: DownSource
     URL: https://downsite.com/feed
     ✗ Connection Error: Could not reach feed

**HTTP Errors:**

.. code-block:: text

   Fetching from: BrokenSource
     URL: https://example.com/404feed
     ✗ HTTP Error: 404

**Parse Errors:**

.. code-block:: text

   Fetching from: BadFeed
     URL: https://badfeed.com/rss
     ✗ Parse Error: document declared as us-ascii, but parsed as utf-8

**Invalid Entry Errors:**

.. code-block:: text

   Fetching from: TechCrunch
     Found 20 entries
     ✓ Created: Article 1...
     ✗ Error processing entry: Missing required field 'url'
     ✓ Created: Article 2...
     Summary: 19 created, 0 updated, 1 skipped

**Key Behavior:**

- ✅ Errors don't stop entire fetch
- ✅ Other sources continue processing
- ✅ Detailed error messages in output
- ✅ Summary shows skipped entries

Output Format
~~~~~~~~~~~~~

**Console Output Symbols:**

.. code-block:: text

   ✓ Created:   New article added to database
   ↻ Updated:   Existing article refreshed
   ✗ Error:     Problem occurred (entry skipped)
   ⚠ Warning:   Non-critical issue

**Color Coding:**

- **Green** (✓ Created): ``self.style.SUCCESS``
- **Yellow** (↻ Updated): ``self.style.WARNING``
- **Red** (✗ Error): ``self.style.ERROR``

**Summary Statistics:**

.. code-block:: text

   ======================================================================
   Fetch complete!
     Total entries processed: 128
     ✓ New articles created: 85
     ↻ Existing articles updated: 40
     ✗ Entries skipped: 3
   ======================================================================

Performance
~~~~~~~~~~~

**Typical Performance:**

- **Single source:** 2-5 seconds (20 articles)
- **6 sources:** 15-30 seconds (120 articles)
- **Network dependent:** Slow feeds increase time

**Timeout:** 30 seconds per feed

**Database Operations:**

- ``update_or_create`` - O(1) lookup by URL (indexed)
- Bulk operations not used (incremental processing for error isolation)

**Memory Usage:** Minimal (processes entries one at a time)

Scheduling
----------

Running Automatically
~~~~~~~~~~~~~~~~~~~~~

For production use, schedule the command to run automatically:

Cron (Linux/macOS)
^^^^^^^^^^^^^^^^^^

**Edit crontab:**

.. code-block:: bash

   crontab -e

**Add entry:**

.. code-block:: bash

   # Run every hour at minute 0
   0 * * * * cd /path/to/tech-pulse && /path/to/venv/bin/python manage.py fetch_articles >> /var/log/tech-pulse-fetch.log 2>&1

   # Run every 30 minutes
   */30 * * * * cd /path/to/tech-pulse && /path/to/venv/bin/python manage.py fetch_articles

   # Run daily at 6 AM
   0 6 * * * cd /path/to/tech-pulse && /path/to/venv/bin/python manage.py fetch_articles

**Cron syntax:**

.. code-block:: text

   * * * * * command
   │ │ │ │ │
   │ │ │ │ └─── Day of week (0-7, Sunday=0 or 7)
   │ │ │ └───── Month (1-12)
   │ │ └─────── Day of month (1-31)
   │ └───────── Hour (0-23)
   └─────────── Minute (0-59)

**Examples:**

.. code-block:: bash

   0 * * * *      # Every hour
   */15 * * * *   # Every 15 minutes
   0 0 * * *      # Daily at midnight
   0 9 * * 1      # Every Monday at 9 AM

Task Scheduler (Windows)
^^^^^^^^^^^^^^^^^^^^^^^^^

**GUI Method:**

1. Open Task Scheduler (``taskschd.msc``)
2. Create Basic Task
3. **Name:** Tech Pulse RSS Fetch
4. **Trigger:** Daily
5. **Repeat task every:** 1 hour
6. **Action:** Start a program
7. **Program:** ``C:\Users\pfare\Projects\tech-pulse\venv\Scripts\python.exe``
8. **Arguments:** ``manage.py fetch_articles``
9. **Start in:** ``C:\Users\pfare\Projects\tech-pulse``
10. Save

**PowerShell Method:**

.. code-block:: powershell

   $action = New-ScheduledTaskAction -Execute "C:\Users\pfare\Projects\tech-pulse\venv\Scripts\python.exe" `
       -Argument "manage.py fetch_articles" `
       -WorkingDirectory "C:\Users\pfare\Projects\tech-pulse"

   $trigger = New-ScheduledTaskTrigger -Daily -At 9am -RepetitionInterval (New-TimeSpan -Hours 1)

   Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "TechPulseFetch" -Description "Fetch Tech Pulse articles"

APScheduler (Python)
^^^^^^^^^^^^^^^^^^^^

**For Django apps that stay running:**

**Install:**

.. code-block:: bash

   pip install apscheduler

**Create:** ``articles/scheduler.py``

.. code-block:: python

   from apscheduler.schedulers.background import BackgroundScheduler
   from django.core.management import call_command

   def start():
       scheduler = BackgroundScheduler()
       
       # Run every hour
       scheduler.add_job(
           fetch_articles_job,
           'interval',
           hours=1,
           id='fetch_articles',
           replace_existing=True
       )
       
       scheduler.start()

   def fetch_articles_job():
       """Wrapper to call management command"""
       call_command('fetch_articles')

**In apps.py:**

.. code-block:: python

   from django.apps import AppConfig

   class ArticlesConfig(AppConfig):
       default_auto_field = 'django.db.models.BigAutoField'
       name = 'articles'

       def ready(self):
           from . import scheduler
           scheduler.start()

Celery Beat (Production)
^^^^^^^^^^^^^^^^^^^^^^^^^

**For scalable production deployments:**

**Install:**

.. code-block:: bash

   pip install celery redis

**Create:** ``articles/tasks.py``

.. code-block:: python

   from celery import shared_task
   from django.core.management import call_command

   @shared_task
   def fetch_articles_task():
       """Celery task to fetch articles"""
       call_command('fetch_articles')

**Configure in settings.py:**

.. code-block:: python

   # Celery Configuration
   CELERY_BROKER_URL = 'redis://localhost:6379/0'
   CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

   CELERY_BEAT_SCHEDULE = {
       'fetch-articles-every-hour': {
           'task': 'articles.tasks.fetch_articles_task',
           'schedule': 3600.0,  # Every hour (in seconds)
       },
   }

**Run workers:**

.. code-block:: bash

   # Worker process
   celery -A backend worker -l info

   # Beat scheduler
   celery -A backend beat -l info

Best Practices
--------------

Recommended Frequency
~~~~~~~~~~~~~~~~~~~~~

**How often to fetch:**

- **News sites:** Every 30-60 minutes
- **Blogs:** Every 2-4 hours
- **Low-traffic sites:** Daily

**Considerations:**

- ⚠️ Don't fetch too frequently (respect source servers)
- ⚠️ Some feeds rate-limit aggressive scrapers
- ✅ Check source's ``fetch_interval`` field for guidance

Monitoring
~~~~~~~~~~

**Track fetch success:**

1. Check ``last_fetched`` timestamp in admin
2. Monitor console output for errors
3. Set up logging to file

**Logging to file:**

.. code-block:: bash

   python manage.py fetch_articles >> /var/log/fetch.log 2>&1

**Parse logs for errors:**

.. code-block:: bash

   grep "Error" /var/log/fetch.log

Error Recovery
~~~~~~~~~~~~~~

**If a source consistently fails:**

1. Check if RSS URL changed (visit website)
2. Test URL in browser (should show XML)
3. Check if site is blocking your User-Agent
4. Temporarily deactivate source (``is_active=False``)
5. Contact site owner if needed

**Re-enable when fixed:**

.. code-block:: python

   source = Source.objects.get(name="ProblematicSource")
   source.is_active = True
   source.save()

Data Cleanup
~~~~~~~~~~~~

**Periodically remove old articles:**

.. code-block:: bash

   # Django shell
   python manage.py shell

.. code-block:: python

   from articles.models import Article
   from django.utils import timezone
   from datetime import timedelta

   # Delete articles older than 1 year
   old_date = timezone.now() - timedelta(days=365)
   deleted_count = Article.objects.filter(published_at__lt=old_date).delete()
   print(f"Deleted {deleted_count[0]} old articles")

Extending the Command
---------------------

Add Email Notifications
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from django.core.mail import send_mail

   # In handle() method, after fetch completes:
   if total_created > 0:
       send_mail(
           subject=f'Tech Pulse: {total_created} new articles',
           message=f'Fetch complete!\n\nNew: {total_created}\nUpdated: {total_updated}',
           from_email='noreply@techpulse.com',
           recipient_list=['admin@example.com'],
       )

Add Slack Notifications
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import requests

   # After fetch completes:
   slack_webhook = 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
   
   requests.post(slack_webhook, json={
       'text': f'📰 Tech Pulse Fetch Complete!\n✓ {total_created} new\n↻ {total_updated} updated'
   })

Add Category Auto-Assignment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def auto_assign_category(self, article):
       """Assign category based on keywords in title"""
       title_lower = article.title.lower()
       
       if any(word in title_lower for word in ['ai', 'artificial intelligence', 'machine learning']):
           article.category = Category.objects.get(name='Artificial Intelligence')
       elif any(word in title_lower for word in ['startup', 'funding', 'investment']):
           article.category = Category.objects.get(name='Startups')
       # ... more rules
       
       article.save()

   # Call in handle():
   if created:
       self.auto_assign_category(article)

Add Retry Logic
~~~~~~~~~~~~~~~

.. code-block:: python

   import time

   def fetch_with_retry(self, source, max_retries=3):
       """Fetch with exponential backoff retry"""
       for attempt in range(max_retries):
           try:
               response = requests.get(source.url, timeout=30)
               response.raise_for_status()
               return feedparser.parse(response.content)
           except requests.exceptions.RequestException as e:
               if attempt < max_retries - 1:
                   wait_time = 2 ** attempt  # Exponential backoff
                   self.stdout.write(f'  Retry in {wait_time}s...')
                   time.sleep(wait_time)
               else:
                   raise

Troubleshooting
---------------

Command Not Found
~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: text

   Unknown command: 'fetch_articles'

**Solution:**

Check folder structure:

.. code-block:: text

   articles/
   ├── management/
   │   ├── __init__.py          ← Must exist (empty)
   │   └── commands/
   │       ├── __init__.py      ← Must exist (empty)
   │       └── fetch_articles.py

Verify ``__init__.py`` files exist and command file is named correctly.

No Active Sources
~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: text

   No active RSS sources found.

**Solution:**

1. Check admin: http://127.0.0.1:8000/admin/articles/source/
2. Ensure sources have ``is_active=True`` checkbox checked
3. Ensure ``source_type`` is "RSS"

ImportError
~~~~~~~~~~~

**Error:**

.. code-block:: text

   ModuleNotFoundError: No module named 'feedparser'
   ModuleNotFoundError: No module named 'requests'

**Solution:**

.. code-block:: bash

   pip install feedparser requests
   pip freeze > requirements.txt

Summary
-------

The ``fetch_articles`` command is the heart of Tech Pulse's automation:

**Key Features:**

- ✅ Fetches from multiple RSS sources
- ✅ Prevents duplicates via URL
- ✅ Robust error handling
- ✅ Detailed console output
- ✅ Scheduling-ready
- ✅ Extensible design

**Usage:**

.. code-block:: bash

   # All sources
   python manage.py fetch_articles

   # Specific source
   python manage.py fetch_articles --source 1

**Schedule it and forget it!** ⏰

*Created by Matanda Software*