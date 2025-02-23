# safeshieldapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_file, name='upload_file'),
    path('success/', views.success, name='success'),
    path('login/', views.login_view, name='login'),  
    path('signup/', views.signup, name='signup'),
    path('landing/', views.landing, name='landing'),
    path('contactus/', views.contactus, name='contactus'),
    path('knowstat/', views.knowstat_view, name='knowstat'),
]
