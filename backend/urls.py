"""
URL configuration for backend project.

Main URL routing for Tech Pulse:
- /admin/ - Django admin panel
- /api/ - REST API endpoints (articles app)
- /api-auth/ - DRF login/logout views
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin panel
    path('admin/', admin.site.urls),
    
    # REST API endpoints
    path('api/', include('articles.urls')),
    
    # DRF browsable API authentication
    path('api-auth/', include('rest_framework.urls')),
]