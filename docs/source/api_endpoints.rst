API Endpoints
=============

Complete API reference for Tech Pulse REST API.

**Author:** Matanda Software

Base URL
--------

All API endpoints are prefixed with ``/api/``

- **Development:** ``http://127.0.0.1:8000/api/``
- **Production:** ``https://yourdomain.com/api/``

Authentication
--------------

**Public Endpoints (No Auth Required):**

- ``GET`` requests to all endpoints
- Read-only access to articles, sources, categories

**Authenticated Endpoints (Login Required):**

- ``POST`` - Create new resources
- ``PUT/PATCH`` - Update existing resources
- ``DELETE`` - Delete resources

**Authentication Methods:**

- **Session Authentication** - Login via Django admin, then use browsable API
- **Token Authentication** - Add DRF TokenAuthentication for API clients

Response Format
---------------

**All list endpoints return paginated responses:**

.. code-block:: json

   {
     "count": 128,
     "next": "http://127.0.0.1:8000/api/articles/?page=2",
     "previous": null,
     "results": [
       { /* article object */ },
       { /* article object */ },
       ...
     ]
   }

**Detail endpoints return single objects:**

.. code-block:: json

   {
     "id": 1,
     "title": "Article Title",
     ...
   }

Articles Endpoint
-----------------

Manage news articles from RSS feeds.

List Articles
~~~~~~~~~~~~~

.. http:get:: /api/articles/

   Retrieve a paginated list of articles.

   **Query Parameters:**

   .. list-table::
      :widths: 20 10 70
      :header-rows: 1

      * - Parameter
        - Type
        - Description
      * - ``page``
        - integer
        - Page number (default: 1)
      * - ``page_size``
        - integer
        - Items per page (default: 20, max: 100)
      * - ``search``
        - string
        - Search in title, content, and author
      * - ``source``
        - integer
        - Filter by source ID
      * - ``category``
        - integer
        - Filter by category ID
      * - ``ordering``
        - string
        - Sort field: ``published_at``, ``-published_at``, ``title``, ``-title``

   **Example Request:**

   .. code-block:: http

      GET /api/articles/?search=AI&source=1&ordering=-published_at HTTP/1.1
      Host: 127.0.0.1:8000
      Accept: application/json

   **Example Response (200 OK):**

   .. code-block:: json

      {
        "count": 128,
        "next": "http://127.0.0.1:8000/api/articles/?page=2&search=AI&source=1",
        "previous": null,
        "results": [
          {
            "id": 45,
            "title": "ChatGPT-5 Released with Advanced Reasoning",
            "slug": "chatgpt-5-released-with-advanced-reasoning",
            "url": "https://techcrunch.com/2026/02/18/chatgpt-5-released",
            "summary": "OpenAI announces ChatGPT-5 with improved reasoning capabilities...",
            "author": "John Doe",
            "source": 1,
            "source_name": "TechCrunch",
            "category": 2,
            "category_name": "Artificial Intelligence",
            "published_at": "2026-02-18T20:00:00Z",
            "fetched_at": "2026-02-19T10:00:00Z",
            "updated_at": "2026-02-19T10:00:00Z"
          },
          {
            "id": 47,
            "title": "Google's Gemini AI Surpasses GPT-4 Benchmarks",
            "slug": "googles-gemini-ai-surpasses-gpt-4-benchmarks",
            "url": "https://techcrunch.com/2026/02/17/gemini-benchmarks",
            "summary": "Google announces Gemini has beaten GPT-4 on key AI benchmarks...",
            "author": "Jane Smith",
            "source": 1,
            "source_name": "TechCrunch",
            "category": 2,
            "category_name": "Artificial Intelligence",
            "published_at": "2026-02-17T15:30:00Z",
            "fetched_at": "2026-02-19T10:00:00Z",
            "updated_at": "2026-02-19T10:00:00Z"
          }
        ]
      }

   **What the response contains:**

   - ``count``: Total number of articles matching filters
   - ``next``: URL to next page (null if last page)
   - ``previous``: URL to previous page (null if first page)
   - ``results``: Array of article objects (20 per page)

   **Status Codes:**

   - ``200 OK`` - Success
   - ``400 Bad Request`` - Invalid query parameters

Retrieve Single Article
~~~~~~~~~~~~~~~~~~~~~~~~

.. http:get:: /api/articles/(int:id)/

   Get detailed information about a specific article.

   **Path Parameters:**

   - ``id`` (integer) - Article ID

   **Example Request:**

   .. code-block:: http

      GET /api/articles/45/ HTTP/1.1
      Host: 127.0.0.1:8000
      Accept: application/json

   **Example Response (200 OK):**

   .. code-block:: json

      {
        "id": 45,
        "title": "ChatGPT-5 Released with Advanced Reasoning",
        "slug": "chatgpt-5-released-with-advanced-reasoning",
        "url": "https://techcrunch.com/2026/02/18/chatgpt-5-released",
        "content": "OpenAI today announced the release of ChatGPT-5, the latest iteration of their flagship AI model. The new version features significantly improved reasoning capabilities, better context understanding, and enhanced multi-modal processing...",
        "summary": "OpenAI announces ChatGPT-5 with improved reasoning capabilities and multi-modal processing.",
        "author": "John Doe",
        "source": 1,
        "source_name": "TechCrunch",
        "category": 2,
        "category_name": "Artificial Intelligence",
        "image_url": "https://techcrunch.com/wp-content/uploads/2026/02/chatgpt5.jpg",
        "published_at": "2026-02-18T20:00:00Z",
        "fetched_at": "2026-02-19T10:00:00Z",
        "created_at": "2026-02-19T10:00:00Z",
        "updated_at": "2026-02-19T10:00:00Z"
      }

   **Note:** Detail view includes full ``content`` field (not in list view for performance).

   **Status Codes:**

   - ``200 OK`` - Success
   - ``404 Not Found`` - Article doesn't exist

Create Article
~~~~~~~~~~~~~~

.. http:post:: /api/articles/

   Create a new article (requires authentication).

   **Request Headers:**

   - ``Content-Type: application/json``
   - ``Authorization: Token your-auth-token`` (if using token auth)

   **Request Body:**

   .. code-block:: json

      {
        "title": "New Article Title",
        "url": "https://example.com/new-article",
        "content": "Full article content goes here...",
        "summary": "Brief summary of the article...",
        "author": "Jane Smith",
        "source": 1,
        "category": 2,
        "published_at": "2026-02-20T12:00:00Z",
        "image_url": "https://example.com/image.jpg"
      }

   **Required Fields:**

   - ``title`` (string, max 500 chars)
   - ``url`` (string, must be unique)
   - ``source`` (integer, source ID)
   - ``published_at`` (ISO 8601 datetime string)

   **Optional Fields:**

   - ``content`` (string)
   - ``summary`` (string, max 1000 chars)
   - ``author`` (string, max 200 chars, default: "Unknown")
   - ``category`` (integer, category ID)
   - ``image_url`` (string)

   **Example Response (201 Created):**

   .. code-block:: json

      {
        "id": 150,
        "title": "New Article Title",
        "slug": "new-article-title",
        "url": "https://example.com/new-article",
        "content": "Full article content goes here...",
        "summary": "Brief summary of the article...",
        "author": "Jane Smith",
        "source": 1,
        "source_name": "TechCrunch",
        "category": 2,
        "category_name": "Artificial Intelligence",
        "image_url": "https://example.com/image.jpg",
        "published_at": "2026-02-20T12:00:00Z",
        "fetched_at": "2026-02-20T14:30:00Z",
        "created_at": "2026-02-20T14:30:00Z",
        "updated_at": "2026-02-20T14:30:00Z"
      }

   **Validation Errors (400 Bad Request):**

   .. code-block:: json

      {
        "url": ["article with this url already exists."],
        "title": ["This field may not be blank."],
        "source": ["This field is required."]
      }

   **Status Codes:**

   - ``201 Created`` - Article created successfully
   - ``400 Bad Request`` - Validation errors
   - ``401 Unauthorized`` - Authentication required

Update Article
~~~~~~~~~~~~~~

.. http:put:: /api/articles/(int:id)/

   Update an existing article (requires authentication).

   **Full update** - All fields required.

   **Request Body:** Same as Create Article

   **Status Codes:**

   - ``200 OK`` - Article updated
   - ``400 Bad Request`` - Validation errors
   - ``401 Unauthorized`` - Authentication required
   - ``404 Not Found`` - Article doesn't exist

.. http:patch:: /api/articles/(int:id)/

   Partial update - Only send fields you want to change.

   **Example Request:**

   .. code-block:: json

      {
        "title": "Updated Title",
        "category": 3
      }

   **Status Codes:** Same as PUT

Delete Article
~~~~~~~~~~~~~~

.. http:delete:: /api/articles/(int:id)/

   Delete an article (requires authentication).

   **Example Request:**

   .. code-block:: http

      DELETE /api/articles/45/ HTTP/1.1
      Host: 127.0.0.1:8000

   **Response (204 No Content):**

   Empty response body.

   **Status Codes:**

   - ``204 No Content`` - Article deleted successfully
   - ``401 Unauthorized`` - Authentication required
   - ``404 Not Found`` - Article doesn't exist

Sources Endpoint
----------------

Manage RSS feed sources.

List Sources
~~~~~~~~~~~~

.. http:get:: /api/sources/

   Get a list of all RSS sources.

   **Example Response (200 OK):**

   .. code-block:: json

      [
        {
          "id": 1,
          "name": "TechCrunch",
          "url": "https://techcrunch.com/feed/",
          "source_type": "RSS",
          "website": "https://techcrunch.com",
          "description": "Technology and startup news",
          "is_active": true,
          "fetch_interval": 60,
          "last_fetched": "2026-02-20T10:00:00Z",
          "article_count": 45,
          "created_at": "2026-02-18T12:00:00Z",
          "updated_at": "2026-02-20T10:00:00Z"
        },
        {
          "id": 2,
          "name": "The Verge",
          "url": "https://www.theverge.com/rss/index.xml",
          "source_type": "RSS",
          "website": "https://www.theverge.com",
          "description": "Technology news and media network",
          "is_active": true,
          "fetch_interval": 60,
          "last_fetched": "2026-02-20T10:00:00Z",
          "article_count": 38,
          "created_at": "2026-02-18T13:00:00Z",
          "updated_at": "2026-02-20T10:00:00Z"
        }
      ]

   **Note:** ``article_count`` is computed on-the-fly (counts related articles).

Retrieve Single Source
~~~~~~~~~~~~~~~~~~~~~~~

.. http:get:: /api/sources/(int:id)/

   Get details of a specific source.

   **Status Codes:**

   - ``200 OK`` - Success
   - ``404 Not Found`` - Source doesn't exist

Create/Update/Delete Source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Similar to Articles endpoint. Requires authentication.

**Required fields for creation:**

- ``name`` (string, max 200 chars)
- ``url`` (string, valid URL)
- ``source_type`` (string: "RSS", "API", or "SCRAPER")

Categories Endpoint
-------------------

Manage article categories.

List Categories
~~~~~~~~~~~~~~~

.. http:get:: /api/categories/

   Get a list of all categories.

   **Example Response (200 OK):**

   .. code-block:: json

      [
        {
          "id": 1,
          "name": "Technology",
          "slug": "technology",
          "description": "General technology news",
          "article_count": 67,
          "created_at": "2026-02-18T12:00:00Z"
        },
        {
          "id": 2,
          "name": "Artificial Intelligence",
          "slug": "artificial-intelligence",
          "description": "AI, ML, and neural networks",
          "article_count": 34,
          "created_at": "2026-02-18T12:00:00Z"
        }
      ]

Retrieve Single Category
~~~~~~~~~~~~~~~~~~~~~~~~~

.. http:get:: /api/categories/(int:id)/

   Get details of a specific category.

Query Examples
--------------

Common API Usage Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Search for "AI" articles:**

.. code-block:: bash

   curl "http://127.0.0.1:8000/api/articles/?search=AI"

**Get TechCrunch articles only:**

.. code-block:: bash

   curl "http://127.0.0.1:8000/api/articles/?source=1"

**Get AI category articles:**

.. code-block:: bash

   curl "http://127.0.0.1:8000/api/articles/?category=2"

**Get latest 10 articles:**

.. code-block:: bash

   curl "http://127.0.0.1:8000/api/articles/?ordering=-published_at&page_size=10"

**Combine multiple filters:**

.. code-block:: bash

   curl "http://127.0.0.1:8000/api/articles/?search=AI&source=1&category=2&ordering=-published_at"

**Python requests example:**

.. code-block:: python

   import requests

   # Get articles
   response = requests.get('http://127.0.0.1:8000/api/articles/', params={
       'search': 'AI',
       'source': 1,
       'ordering': '-published_at',
       'page': 1
   })

   data = response.json()
   print(f"Found {data['count']} articles")

   for article in data['results']:
       print(f"- {article['title']} ({article['published_at']})")

**JavaScript fetch example:**

.. code-block:: javascript

   const params = new URLSearchParams({
       search: 'AI',
       source: 1,
       ordering: '-published_at',
       page: 1
   });

   fetch(`http://127.0.0.1:8000/api/articles/?${params}`)
       .then(response => response.json())
       .then(data => {
           console.log(`Found ${data.count} articles`);
           data.results.forEach(article => {
               console.log(`- ${article.title}`);
           });
       });

Error Responses
---------------

400 Bad Request
~~~~~~~~~~~~~~~

**Validation errors:**

.. code-block:: json

   {
     "title": ["This field is required."],
     "url": ["Enter a valid URL."]
   }

401 Unauthorized
~~~~~~~~~~~~~~~~

**Authentication required:**

.. code-block:: json

   {
     "detail": "Authentication credentials were not provided."
   }

404 Not Found
~~~~~~~~~~~~~

**Resource doesn't exist:**

.. code-block:: json

   {
     "detail": "Not found."
   }

500 Internal Server Error
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Server error:**

.. code-block:: json

   {
     "detail": "Internal server error. Please try again later."
   }

Rate Limiting
-------------

Currently no rate limiting is implemented. For production:

- Consider Django REST Framework's throttling
- Recommended: 100 requests per minute for anonymous users
- Recommended: 1000 requests per minute for authenticated users

Pagination Details
------------------

**Default page size:** 20 items

**Maximum page size:** 100 items

**Change page size:**

.. code-block:: bash

   curl "http://127.0.0.1:8000/api/articles/?page_size=50"

**Navigate pages:**

.. code-block:: bash

   curl "http://127.0.0.1:8000/api/articles/?page=1"
   curl "http://127.0.0.1:8000/api/articles/?page=2"

**Pagination metadata:**

- ``count`` - Total items across all pages
- ``next`` - Full URL to next page (null if last page)
- ``previous`` - Full URL to previous page (null if first page)

CORS Configuration
------------------

For cross-origin requests (e.g., from frontend on different domain):

**Install django-cors-headers:**

.. code-block:: bash

   pip install django-cors-headers

**Update settings.py:**

.. code-block:: python

   INSTALLED_APPS = [
       ...
       'corsheaders',
   ]

   MIDDLEWARE = [
       'corsheaders.middleware.CorsMiddleware',
       ...
   ]

   CORS_ALLOWED_ORIGINS = [
       "http://localhost:3000",
       "https://yourfrontend.com",
   ]

Versioning
----------

Current API version: **v1.0.0**

Future versions will use URL versioning:

- ``/api/v1/articles/``
- ``/api/v2/articles/``

API Changelog
-------------

**v1.0.0 (2026-02-20)**

- Initial release
- Articles, Sources, Categories endpoints
- Filtering, search, ordering, pagination
- Session authentication