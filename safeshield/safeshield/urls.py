# core/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Include app-specific URLs
    path('', include('safeshieldapp.urls')),  # This includes the safeshieldapp URLs
]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('safeshieldapp.urls')),  # Include safeshieldapp routes
]
from django.contrib import admin
from django.urls import path, include

  # Include safeshieldapp routes


