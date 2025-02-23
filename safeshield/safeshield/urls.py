# core/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Include app-specific URLs
    path('', include('safeshieldapp.urls')),  # This includes the safeshieldapp URLs
]
