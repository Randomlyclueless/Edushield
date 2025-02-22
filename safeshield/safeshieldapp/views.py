from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout

# Create your views here.
def home(request):
    return render(request, 'home.html')

def user_login(request):  # Renamed function to avoid conflict
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')
