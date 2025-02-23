
from django.contrib import admin
from django.urls import path
from django.shortcuts import render

from safeshieldapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), 
    path('login/', views.login_view, name='login'),  
    path('signup/', views.signup, name='signup'),  
    path('landing/', views.landing, name='landing'),
    path('contactus/', views.contactus, name='contactus'),
]
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include



urlpatterns += [
    path('', include('safeshieldapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



