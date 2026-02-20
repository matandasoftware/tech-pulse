Installation
============

This guide walks you through setting up Tech Pulse on your local machine.

**Author:** Matanda Software

Prerequisites
-------------

Before installing Tech Pulse, ensure you have:

- **Python 3.12 or higher** - `Download from python.org <https://www.python.org/downloads/>`_
- **pip** - Python package manager (included with Python)
- **Git** - Version control system
- **Virtual environment** - Recommended for isolation

**Check your Python version:**

.. code-block:: bash

   python --version
   # Should show: Python 3.12.x

Quick Start
-----------

Follow these steps to get Tech Pulse running in under 5 minutes:

Step 1: Clone the Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/matandasoftware/tech-pulse.git
   cd tech-pulse

**What this does:** Downloads the project code to your computer.

Step 2: Create Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Windows:**

.. code-block:: bash

   python -m venv venv
   venv\Scripts\activate

**macOS/Linux:**

.. code-block:: bash

   python3 -m venv venv
   source venv/bin/activate

**What this does:** 
- Creates isolated Python environment in ``venv/`` folder
- Activates it (you'll see ``(venv)`` in terminal)
- Keeps project dependencies separate from system Python

**Why it matters:** Prevents conflicts between project dependencies and other Python projects.

Step 3: Install Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install -r requirements.txt

**What this does:** Installs all required Python packages:

- Django 6.0.2
- Django REST Framework 3.15
- django-filter 24.3
- feedparser (RSS parsing)
- requests (HTTP library)
- And their dependencies (~30 packages total)

**Expected output:**

.. code-block:: text

   Collecting Django==6.0.2
   Collecting djangorestframework==3.15
   ...
   Successfully installed Django-6.0.2 djangorestframework-3.15 ...

**This takes 1-2 minutes.**

Step 4: Run Database Migrations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python manage.py migrate

**What this does:** 
- Creates SQLite database file (``db.sqlite3``)
- Creates database tables for:
  - Django built-in tables (users, sessions, permissions)
  - Tech Pulse tables (sources, categories, articles)

**Expected output:**

.. code-block:: text

   Operations to perform:
     Apply all migrations: admin, auth, contenttypes, sessions, articles
   Running migrations:
     Applying contenttypes.0001_initial... OK
     Applying auth.0001_initial... OK
     Applying admin.0001_initial... OK
     Applying articles.0001_initial... OK
     ...

**What's happening behind the scenes:**

.. code-block:: sql

   -- Django creates tables like:
   CREATE TABLE articles_source (
       id INTEGER PRIMARY KEY,
       name VARCHAR(200),
       url VARCHAR(200),
       ...
   );

   CREATE TABLE articles_article (
       id INTEGER PRIMARY KEY,
       title VARCHAR(500),
       url VARCHAR(500) UNIQUE,
       source_id INTEGER REFERENCES articles_source(id),
       ...
   );

Step 5: Create Superuser
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python manage.py createsuperuser

**Prompts you'll see:**

.. code-block:: text

   Username: admin
   Email address: admin@example.com
   Password: ********
   Password (again): ********
   Superuser created successfully.

**What this does:** Creates admin account for accessing Django admin panel at ``/admin/``.

**Security tip:** Use a strong password, especially for production deployments.

Step 6: Run Development Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python manage.py runserver

**Expected output:**

.. code-block:: text

   Watching for file changes with StatReloader
   Performing system checks...

   System check identified no issues (0 silenced).
   February 20, 2026 - 15:30:00
   Django version 6.0.2, using settings 'backend.settings'
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CTRL-BREAK.

**What this does:** Starts Django development server on port 8000.

Step 7: Access the Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Open your browser and visit:

- **API Root:** http://127.0.0.1:8000/api/
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **Articles List:** http://127.0.0.1:8000/api/articles/
- **Sources List:** http://127.0.0.1:8000/api/sources/
- **Categories List:** http://127.0.0.1:8000/api/categories/

**What you'll see:**

- API Root: List of available endpoints in Django REST Framework's browsable API
- Admin Panel: Django admin interface (login with superuser credentials)
- Articles: Empty list (we'll add articles next)

Detailed Setup
--------------

Environment Variables (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For production deployments, use environment variables:

**Create:** ``.env`` file in project root:

.. code-block:: bash

   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   DATABASE_URL=postgres://user:password@host:port/dbname

**Install python-decouple:**

.. code-block:: bash

   pip install python-decouple

**Update settings.py:**

.. code-block:: python

   from decouple import config

   SECRET_KEY = config('SECRET_KEY', default='django-insecure-...')
   DEBUG = config('DEBUG', default=True, cast=bool)
   ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

Database Options
~~~~~~~~~~~~~~~~

**SQLite (Default - Development):**

Already configured. Database file: ``db.sqlite3``

**Advantages:**
- Zero configuration
- File-based (easy backup)
- Perfect for development

**Disadvantages:**
- Not suitable for production with multiple users
- No concurrent write support

**PostgreSQL (Recommended - Production):**

1. Install PostgreSQL on your system
2. Create database:

   .. code-block:: sql

      CREATE DATABASE tech_pulse;
      CREATE USER tech_pulse_user WITH PASSWORD 'your_password';
      GRANT ALL PRIVILEGES ON DATABASE tech_pulse TO tech_pulse_user;

3. Install psycopg2:

   .. code-block:: bash

      pip install psycopg2-binary

4. Update ``backend/settings.py``:

   .. code-block:: python

      DATABASES = {
          'default': {
              'ENGINE': 'django.db.backends.postgresql',
              'NAME': 'tech_pulse',
              'USER': 'tech_pulse_user',
              'PASSWORD': 'your_password',
              'HOST': 'localhost',
              'PORT': '5432',
          }
      }

5. Run migrations:

   .. code-block:: bash

      python manage.py migrate

**MySQL (Alternative):**

Similar to PostgreSQL, but use ``django.db.backends.mysql`` engine and install ``mysqlclient``.

Initial Data Setup
------------------

The database is now empty. Let's add content!

Add RSS Sources via Admin
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Start server: ``python manage.py runserver``
2. Go to: http://127.0.0.1:8000/admin/
3. Login with superuser credentials
4. Click **Sources** → **Add Source**
5. Fill in the form:

**Example: TechCrunch**

- **Name:** TechCrunch
- **URL:** ``https://techcrunch.com/feed/``
- **Source Type:** RSS
- **Website:** ``https://techcrunch.com``
- **Description:** Technology and startup news
- **Is Active:** ✓ Checked
- **Fetch Interval:** 60

6. Click **Save and add another**
7. Repeat for other sources

**Recommended Sources:**

.. code-block:: text

   TechCrunch:     https://techcrunch.com/feed/
   The Verge:      https://www.theverge.com/rss/index.xml
   Ars Technica:   https://feeds.arstechnica.com/arstechnica/index
   Wired:          https://www.wired.com/feed/rss
   Hacker News:    https://hnrss.org/frontpage

Fetch Articles
~~~~~~~~~~~~~~

Stop the server (``Ctrl+C``) and run:

.. code-block:: bash

   python manage.py fetch_articles

**Expected output:**

.. code-block:: text

   Starting RSS feed fetch...

   Fetching from: TechCrunch
     URL: https://techcrunch.com/feed/
     Found 20 entries
     ✓ Created: Article title 1...
     ✓ Created: Article title 2...
     ...

   ======================================================================
   Fetch complete!
     Total entries processed: 100
     ✓ New articles created: 100
   ======================================================================

**What this does:**
- Connects to each active RSS source
- Parses XML feed
- Extracts article data (title, URL, content, author, date, image)
- Saves to database (prevents duplicates by URL)
- Updates source ``last_fetched`` timestamp

**Now restart server and visit:** http://127.0.0.1:8000/api/articles/

**You'll see 100+ real tech articles!** 🎉

Add Categories (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Go to admin: http://127.0.0.1:8000/admin/
2. Click **Categories** → **Add Category**
3. Add categories:

   - Technology
   - Business
   - Science
   - AI & Machine Learning
   - Startups
   - Mobile
   - Security

4. Assign articles to categories manually or via API

Troubleshooting
---------------

"Command not found: python"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**macOS/Linux:** Use ``python3`` instead of ``python``

.. code-block:: bash

   python3 --version
   python3 manage.py runserver

"No module named 'articles'"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solution:** Make sure you're in the project root directory:

.. code-block:: bash

   cd tech-pulse
   ls  # Should see: manage.py, articles/, backend/, etc.

"Port already in use"
~~~~~~~~~~~~~~~~~~~~~

**Solution:** Another process is using port 8000. Use different port:

.. code-block:: bash

   python manage.py runserver 8080

Or find and kill the process:

.. code-block:: bash

   # Windows
   netstat -ano | findstr :8000
   taskkill /PID <pid> /F

   # macOS/Linux
   lsof -i :8000
   kill -9 <pid>

Migration Errors
~~~~~~~~~~~~~~~~

**Solution:** Delete database and recreate:

.. code-block:: bash

   # Stop server
   # Delete db.sqlite3 file
   del db.sqlite3  # Windows
   rm db.sqlite3   # macOS/Linux

   # Recreate
   python manage.py migrate
   python manage.py createsuperuser

"Permission denied" on Linux/macOS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solution:** Check file permissions:

.. code-block:: bash

   chmod +x manage.py
   python3 manage.py runserver

Virtual Environment Not Activating
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Windows PowerShell Execution Policy:**

.. code-block:: powershell

   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   venv\Scripts\activate

RSS Fetch Fails
~~~~~~~~~~~~~~~

**Check:**

1. Internet connection is active
2. RSS feed URL is correct (test in browser)
3. Source is marked as "Active" in admin
4. Check error messages in console output

Next Steps
----------

Now that Tech Pulse is installed:

1. **Explore the API:** :doc:`api_endpoints`
2. **Learn usage patterns:** :doc:`usage`
3. **Understand the data models:** :doc:`models`
4. **Set up automation:** :doc:`management_commands`

Production Deployment
---------------------

For production deployment, see these guides:

**Deployment Checklist:**

- [ ] Use PostgreSQL instead of SQLite
- [ ] Set ``DEBUG = False`` in settings
- [ ] Configure ``ALLOWED_HOSTS``
- [ ] Use environment variables for secrets
- [ ] Set up HTTPS/SSL
- [ ] Configure static files (``collectstatic``)
- [ ] Set up process manager (Gunicorn/uWSGI)
- [ ] Configure web server (Nginx/Apache)
- [ ] Set up scheduled tasks (cron/Celery)
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Enable database backups

**Deployment Platforms:**

- **Heroku:** Easy deployment with PostgreSQL addon
- **DigitalOcean:** App Platform or Droplet
- **AWS:** Elastic Beanstalk or EC2
- **PythonAnywhere:** Simple Python hosting
- **Railway:** Modern deployment platform

**Resources:**

- Django Deployment Checklist: https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/
- Django REST Framework Deployment: https://www.django-rest-framework.org/topics/deployment/