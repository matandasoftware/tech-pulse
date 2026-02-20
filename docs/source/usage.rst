Usage Guide
===========

Practical guide for using Tech Pulse API in real-world scenarios.

**Author:** Matanda Software

Getting Started
---------------

This guide assumes you have already:

- ✅ Installed Tech Pulse (:doc:`installation`)
- ✅ Created a superuser account
- ✅ Added RSS sources in admin panel
- ✅ Fetched initial articles

Starting the Server
-------------------

**Every time you work on the project:**

.. code-block:: bash

   # Navigate to project directory
   cd C:\Users\pfare\Projects\tech-pulse

   # Activate virtual environment
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux

   # Start development server
   python manage.py runserver

**Server runs at:** http://127.0.0.1:8000/

**Stop server:** Press ``Ctrl+C``

Admin Panel Usage
-----------------

The admin panel is your control center for managing content.

Accessing Admin
~~~~~~~~~~~~~~~

1. Start server
2. Navigate to: http://127.0.0.1:8000/admin/
3. Login with superuser credentials

**What you can do:**

- ✅ Add/edit/delete RSS sources
- ✅ Create/manage categories
- ✅ View/edit/delete articles
- ✅ Manage user permissions
- ✅ View database statistics

Managing RSS Sources
~~~~~~~~~~~~~~~~~~~~

**Add New Source:**

1. Go to **Sources** → **Add Source**
2. Fill in the form:

.. code-block:: text

   Name: The Verge
   URL: https://www.theverge.com/rss/index.xml
   Source Type: RSS
   Website: https://www.theverge.com
   Description: Technology news and media network
   Is Active: ✓ Checked
   Fetch Interval: 60 (minutes)

3. Click **Save**

**What each field means:**

- **Name:** Display name for the source (shown in API)
- **URL:** RSS feed URL (must be valid XML feed)
- **Source Type:** RSS, API, or SCRAPER (only RSS implemented currently)
- **Website:** Main website URL (for attribution/linking)
- **Description:** Brief description of the source
- **Is Active:** Uncheck to stop fetching from this source
- **Fetch Interval:** How often to fetch (in minutes) - used for future scheduling

**Edit Existing Source:**

1. Go to **Sources**
2. Click on source name
3. Edit fields
4. Click **Save**

**Deactivate Source:**

1. Find the source
2. Uncheck **Is Active**
3. Click **Save**

**Effect:** ``fetch_articles`` command will skip this source.

**Delete Source:**

⚠️ **Warning:** Deleting a source will also delete all articles from that source (CASCADE delete).

1. Go to source detail page
2. Click **Delete** button
3. Confirm deletion

Managing Categories
~~~~~~~~~~~~~~~~~~~

**Add Category:**

1. Go to **Categories** → **Add Category**
2. Fill in:

.. code-block:: text

   Name: Artificial Intelligence
   Description: AI, machine learning, and neural networks

3. Click **Save**

**What happens:**

- **Slug** is auto-generated: ``artificial-intelligence``
- **Article count** shows 0 initially
- **Created timestamp** is recorded

**Assign Articles to Categories:**

1. Go to **Articles**
2. Click on an article
3. Select **Category** from dropdown
4. Click **Save**

**Bulk assign categories:**

1. Go to **Articles** list
2. Select multiple articles (checkboxes)
3. Choose action: "Assign category"
4. Select category
5. Click **Go**

*(Note: Bulk actions require custom admin actions - not implemented by default)*

Managing Articles
~~~~~~~~~~~~~~~~~

**View Articles:**

1. Go to **Articles**
2. Browse paginated list
3. Use filters (right sidebar):

   - By source
   - By category
   - By publication date

**Edit Article:**

1. Click on article title
2. Modify fields
3. Click **Save**

**Common edits:**

- Fix title capitalization
- Assign to category
- Update author name
- Change published date

**Delete Articles:**

1. Click on article
2. Click **Delete** button
3. Or select multiple articles → Actions → Delete selected

**Search Articles:**

Use search box at top:

- Searches in: title, content, author
- Example: "ChatGPT" finds all articles mentioning ChatGPT

Fetching Articles
-----------------

The core functionality - fetching news from RSS feeds.

Manual Fetch (All Sources)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python manage.py fetch_articles

**What happens:**

1. Queries database for active RSS sources
2. Fetches each feed's XML
3. Parses entries
4. Extracts: title, URL, content, summary, author, date, image
5. Saves to database (``update_or_create`` prevents duplicates)
6. Updates source ``last_fetched`` timestamp
7. Prints summary statistics

**Expected output:**

.. code-block:: text

   Starting RSS feed fetch...

   Fetching from: TechCrunch
     URL: https://techcrunch.com/feed/
     Found 20 entries
     ✓ Created: Threads posts can now be shared directly to your Instagram...
     ✓ Created: Toy Story 5 takes aim at creepy AI toys...
     ↻ Updated: Meta's metaverse leaves virtual reality...
     Summary: 18 created, 2 updated, 0 skipped

   Fetching from: The Verge
     URL: https://www.theverge.com/rss/index.xml
     Found 18 entries
     ✓ Created: Apple announces new iPad Pro...
     Summary: 18 created, 0 updated, 0 skipped

   ======================================================================
   Fetch complete!
     Total entries processed: 38
     ✓ New articles created: 36
     ↻ Existing articles updated: 2
   ======================================================================

**Symbols explained:**

- ✓ **Created:** New article added to database
- ↻ **Updated:** Existing article refreshed (same URL)
- ✗ **Error:** Problem processing entry (skipped)

**How long it takes:**

- ~2-5 seconds per source (with 20 articles)
- 6 sources: ~15-30 seconds total

Fetch Specific Source
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python manage.py fetch_articles --source 1

**Use case:** Only fetch from one source (testing, or if one source has issues).

**How to find source ID:**

1. Admin panel → Sources
2. Click on source
3. Look at URL: ``/admin/articles/source/1/change/`` (ID is 1)

Re-running Fetch
~~~~~~~~~~~~~~~~

**Safe to run multiple times!**

.. code-block:: bash

   python manage.py fetch_articles

**What happens:**

- Existing articles are **updated** (not duplicated)
- New articles are **created**
- Duplicate detection uses **URL as unique key**

**Example:**

.. code-block:: text

   First run:  20 created, 0 updated
   Second run: 0 created, 20 updated (all exist already)
   Third run:  5 created, 15 updated (5 new articles published)

Scheduled Fetching (Future)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For automatic fetching every hour, see :doc:`management_commands` for scheduling options:

- **Cron** (Linux/macOS)
- **Task Scheduler** (Windows)
- **Celery Beat** (Production)

Using the API
-------------

Exploring the Browsable API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Django REST Framework provides a **browsable HTML interface**:

1. Start server
2. Navigate to: http://127.0.0.1:8000/api/
3. Click on endpoints to explore

**Features:**

- ✅ View JSON responses
- ✅ Interactive forms for POST/PUT
- ✅ Filter options on the right
- ✅ Pagination controls at bottom
- ✅ Login/logout in top-right corner

**Try it:**

1. Go to: http://127.0.0.1:8000/api/articles/
2. See list of articles
3. Use filters on right:
   - Search: "AI"
   - Source: Select "TechCrunch"
   - Ordering: "-published_at"
4. Click **Filter**
5. See filtered results!

Basic Queries
~~~~~~~~~~~~~

**Get all articles:**

.. code-block:: bash

   curl http://127.0.0.1:8000/api/articles/

**Get specific article:**

.. code-block:: bash

   curl http://127.0.0.1:8000/api/articles/1/

**Get all sources:**

.. code-block:: bash

   curl http://127.0.0.1:8000/api/sources/

**Get all categories:**

.. code-block:: bash

   curl http://127.0.0.1:8000/api/categories/

Filtering Articles
~~~~~~~~~~~~~~~~~~

**By Source (TechCrunch):**

.. code-block:: bash

   curl "http://127.0.0.1:8000/api/articles/?source=1"

**By Category (AI):**

.. code-block:: bash

   curl "http://127.0.0.1:8000/api/articles/?category=2"

**By Search Term:**

.. code-block:: bash

   curl "http://127.0.0.1:8000/api/articles/?search=ChatGPT"

**Search matches:**

- Article title
- Article content
- Author name

**Search is case-insensitive:** "chatgpt" = "ChatGPT" = "CHATGPT"

Sorting Results
~~~~~~~~~~~~~~~

**Newest first (default):**

.. code-block:: bash

   curl "http://127.0.0.1:8000/api/articles/?ordering=-published_at"

**Oldest first:**

.. code-block:: bash

   curl "http://127.0.0.1:8000/api/articles/?ordering=published_at"

**Alphabetical (A-Z):**

.. code-block:: bash

   curl "http://127.0.0.1:8000/api/articles/?ordering=title"

**Reverse alphabetical (Z-A):**

.. code-block:: bash

   curl "http://127.0.0.1:8000/api/articles/?ordering=-title"

**Combining filters:**

.. code-block:: bash

   curl "http://127.0.0.1:8000/api/articles/?source=1&search=AI&ordering=-published_at"

Pagination
~~~~~~~~~~

**Page 1 (default):**

.. code-block:: bash

   curl "http://127.0.0.1:8000/api/articles/"

**Page 2:**

.. code-block:: bash

   curl "http://127.0.0.1:8000/api/articles/?page=2"

**Custom page size:**

.. code-block:: bash

   curl "http://127.0.0.1:8000/api/articles/?page_size=50"

**Response structure:**

.. code-block:: json

   {
     "count": 128,
     "next": "http://127.0.0.1:8000/api/articles/?page=3",
     "previous": "http://127.0.0.1:8000/api/articles/?page=1",
     "results": [ /* 20 articles */ ]
   }

**Iterating through all pages:**

.. code-block:: python

   import requests

   url = 'http://127.0.0.1:8000/api/articles/'
   all_articles = []

   while url:
       response = requests.get(url)
       data = response.json()
       all_articles.extend(data['results'])
       url = data['next']  # Next page URL (None when done)

   print(f"Fetched {len(all_articles)} articles")

Real-World Examples
-------------------

Example 1: Display Latest Tech News
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Show 10 most recent articles on a website.

**API Call:**

.. code-block:: bash

   curl "http://127.0.0.1:8000/api/articles/?ordering=-published_at&page_size=10"

**Python Implementation:**

.. code-block:: python

   import requests

   response = requests.get('http://127.0.0.1:8000/api/articles/', params={
       'ordering': '-published_at',
       'page_size': 10
   })

   articles = response.json()['results']

   for article in articles:
       print(f"📰 {article['title']}")
       print(f"   By {article['author']} | {article['source_name']}")
       print(f"   {article['summary']}")
       print(f"   🔗 {article['url']}\n")

**Output:**

.. code-block:: text

   📰 ChatGPT-5 Released with Advanced Reasoning
      By John Doe | TechCrunch
      OpenAI announces ChatGPT-5 with improved reasoning...
      🔗 https://techcrunch.com/2026/02/18/chatgpt-5-released

   📰 Google's Gemini AI Surpasses GPT-4 Benchmarks
      By Jane Smith | TechCrunch
      Google announces Gemini has beaten GPT-4...
      🔗 https://techcrunch.com/2026/02/17/gemini-benchmarks

Example 2: Search for Specific Topic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Find all articles about "artificial intelligence" from last week.

**API Call:**

.. code-block:: bash

   curl "http://127.0.0.1:8000/api/articles/?search=artificial+intelligence&ordering=-published_at"

**JavaScript (Frontend):**

.. code-block:: javascript

   async function searchArticles(query) {
       const params = new URLSearchParams({
           search: query,
           ordering: '-published_at'
       });

       const response = await fetch(`http://127.0.0.1:8000/api/articles/?${params}`);
       const data = await response.json();

       displayResults(data.results);
   }

   function displayResults(articles) {
       const container = document.getElementById('articles');
       container.innerHTML = '';

       articles.forEach(article => {
           const div = document.createElement('div');
           div.className = 'article-card';
           div.innerHTML = `
               <h3>${article.title}</h3>
               <p class="meta">
                   ${article.author} | ${article.source_name} | 
                   ${new Date(article.published_at).toLocaleDateString()}
               </p>
               <p>${article.summary}</p>
               <a href="${article.url}" target="_blank">Read More →</a>
           `;
           container.appendChild(div);
       });
   }

   // Usage
   searchArticles('artificial intelligence');

Example 3: Filter by Source and Category
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Show only TechCrunch articles in "AI" category.

**API Call:**

.. code-block:: bash

   curl "http://127.0.0.1:8000/api/articles/?source=1&category=2"

**Python with Pandas (Data Analysis):**

.. code-block:: python

   import requests
   import pandas as pd

   # Fetch articles
   response = requests.get('http://127.0.0.1:8000/api/articles/', params={
       'source': 1,
       'category': 2,
       'page_size': 100
   })

   articles = response.json()['results']

   # Convert to DataFrame
   df = pd.DataFrame(articles)

   # Analysis
   print(f"Total articles: {len(df)}")
   print(f"\nMost prolific authors:")
   print(df['author'].value_counts().head(5))

   print(f"\nArticles per day:")
   df['date'] = pd.to_datetime(df['published_at']).dt.date
   print(df['date'].value_counts().sort_index())

Example 4: Build RSS Feed Reader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Create a simple command-line RSS reader.

.. code-block:: python

   #!/usr/bin/env python3
   """Simple CLI RSS reader for Tech Pulse API"""

   import requests
   from datetime import datetime

   API_BASE = 'http://127.0.0.1:8000/api'

   def list_sources():
       """Show available sources"""
       response = requests.get(f'{API_BASE}/sources/')
       sources = response.json()
       
       print("\n📰 Available Sources:\n")
       for source in sources:
           print(f"  {source['id']}. {source['name']} ({source['article_count']} articles)")

   def read_articles(source_id=None, search=None):
       """Read articles with optional filters"""
       params = {'page_size': 20, 'ordering': '-published_at'}
       
       if source_id:
           params['source'] = source_id
       if search:
           params['search'] = search
       
       response = requests.get(f'{API_BASE}/articles/', params=params)
       data = response.json()
       
       print(f"\n📚 Found {data['count']} articles\n")
       
       for i, article in enumerate(data['results'], 1):
           pub_date = datetime.fromisoformat(article['published_at'].replace('Z', '+00:00'))
           print(f"{i}. {article['title']}")
           print(f"   {article['source_name']} | {article['author']} | {pub_date.strftime('%Y-%m-%d %H:%M')}")
           print(f"   {article['summary'][:100]}...")
           print(f"   🔗 {article['url']}\n")

   def main():
       import sys
       
       if len(sys.argv) == 1:
           list_sources()
           print("\nUsage:")
           print("  python reader.py <source_id>")
           print("  python reader.py search <query>")
       
       elif sys.argv[1] == 'search':
           query = ' '.join(sys.argv[2:])
           read_articles(search=query)
       
       else:
           source_id = int(sys.argv[1])
           read_articles(source_id=source_id)

   if __name__ == '__main__':
       main()

**Usage:**

.. code-block:: bash

   # List sources
   python reader.py

   # Read from TechCrunch
   python reader.py 1

   # Search for AI articles
   python reader.py search "artificial intelligence"

Example 5: Email Daily Digest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Send email with today's top articles.

.. code-block:: python

   import requests
   from datetime import datetime, timedelta
   from email.mime.text import MIMEText
   from email.mime.multipart import MIMEMultipart
   import smtplib

   def fetch_today_articles():
       """Get articles from last 24 hours"""
       yesterday = (datetime.now() - timedelta(days=1)).isoformat()
       
       response = requests.get('http://127.0.0.1:8000/api/articles/', params={
           'ordering': '-published_at',
           'page_size': 20
       })
       
       articles = response.json()['results']
       
       # Filter to last 24 hours (could also use API date filter)
       recent = []
       for article in articles:
           pub_date = datetime.fromisoformat(article['published_at'].replace('Z', '+00:00'))
           if pub_date > datetime.now() - timedelta(days=1):
               recent.append(article)
       
       return recent

   def create_email_html(articles):
       """Generate HTML email content"""
       html = """
       <html>
       <head>
           <style>
               body { font-family: Arial, sans-serif; }
               .article { margin-bottom: 20px; padding: 15px; border-left: 3px solid #007bff; }
               .title { font-size: 18px; font-weight: bold; color: #333; }
               .meta { color: #666; font-size: 14px; }
               .summary { margin-top: 10px; }
           </style>
       </head>
       <body>
           <h1>🗞️ Tech Pulse Daily Digest</h1>
           <p>Here are today's top tech stories:</p>
       """
       
       for article in articles:
           html += f"""
           <div class="article">
               <div class="title"><a href="{article['url']}">{article['title']}</a></div>
               <div class="meta">{article['source_name']} | {article['author']}</div>
               <div class="summary">{article['summary']}</div>
           </div>
           """
       
       html += """
       </body>
       </html>
       """
       
       return html

   def send_digest():
       """Send email digest"""
       articles = fetch_today_articles()
       
       if not articles:
           print("No new articles today")
           return
       
       # Create email
       msg = MIMEMultipart('alternative')
       msg['Subject'] = f"Tech Pulse Daily Digest - {len(articles)} articles"
       msg['From'] = 'digest@techpulse.com'
       msg['To'] = 'subscriber@example.com'
       
       html_content = create_email_html(articles)
       msg.attach(MIMEText(html_content, 'html'))
       
       # Send (configure SMTP settings)
       # with smtplib.SMTP('smtp.gmail.com', 587) as server:
       #     server.starttls()
       #     server.login('your-email@gmail.com', 'your-password')
       #     server.send_message(msg)
       
       print(f"Digest prepared with {len(articles)} articles")

   if __name__ == '__main__':
       send_digest()

Common Workflows
----------------

Daily Routine
~~~~~~~~~~~~~

1. **Morning:** Run ``fetch_articles`` to get overnight news
2. **Review:** Check admin panel for new articles
3. **Categorize:** Assign categories to interesting articles
4. **Share:** Use API to display on website/app

Weekly Maintenance
~~~~~~~~~~~~~~~~~~

1. **Check Sources:** Visit each source's website to verify RSS feeds still work
2. **Review Errors:** Check console output for fetch failures
3. **Clean Data:** Delete duplicate/spam articles if any
4. **Add Sources:** Find and add new quality tech news sources

Content Curation
~~~~~~~~~~~~~~~~

1. **Fetch Articles:** ``python manage.py fetch_articles``
2. **Browse:** Use browsable API to find interesting articles
3. **Filter:** Use search/filters to find specific topics
4. **Export:** Use API to export selected articles
5. **Publish:** Share via your platform

Troubleshooting
---------------

No Articles Appearing
~~~~~~~~~~~~~~~~~~~~~

**Check:**

1. Are sources active? (Admin → Sources → Is Active checkbox)
2. Have you run fetch command? ``python manage.py fetch_articles``
3. Check console output for errors
4. Test RSS URL in browser (should show XML)

API Returns Empty Results
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Check:**

1. Articles exist: http://127.0.0.1:8000/admin/articles/article/
2. Remove filters: Try ``/api/articles/`` without query params
3. Check pagination: Try ``?page=1``

Search Not Working
~~~~~~~~~~~~~~~~~~

**Remember:**

- Search is case-insensitive
- Searches in: title, content, author
- Try broader terms: "AI" instead of "Artificial Intelligence GPT-5"
- Check spelling

Fetch Command Fails
~~~~~~~~~~~~~~~~~~~

**Common causes:**

1. **No internet:** Check connection
2. **Invalid URL:** Test in browser
3. **Timeout:** Some feeds are slow, command has 30s timeout
4. **Server down:** Source's server might be offline temporarily

**Solution:** Check error message, fix URL or deactivate source

Next Steps
----------

Now that you know how to use Tech Pulse:

- **Explore Models:** :doc:`models` - Understand data structure
- **Automation:** :doc:`management_commands` - Set up scheduling
- **Extend:** Add custom filters, views, or integrations

Happy news aggregating! 📰

*Created by Matanda Software*