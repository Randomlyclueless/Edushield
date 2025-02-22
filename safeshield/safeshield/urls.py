
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
