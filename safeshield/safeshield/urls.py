
from django.contrib import admin
from django.urls import path
from django.shortcuts import render

from safeshieldapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), 
    path('login/', views.user_login, name='login'),  
    path('signup/', views.signup, name='signup'),  
    path('verify_otp/', views.verify_otp, name='verify_otp'),
]
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include



urlpatterns += [
    path('', include('safeshieldapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



