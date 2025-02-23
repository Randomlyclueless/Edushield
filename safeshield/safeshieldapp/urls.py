from django.urls import path
from .views import upload_file, success

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('success/', success, name='success'),
]