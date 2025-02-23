from django.urls import path
from safeshieldapp import views
from .views import send_sms_view, send_otp_view, verify_otp_view

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_file, name='upload_file'),
    path('success/', views.success, name='success'),
    path('login/', views.login_view, name='login'),  
    path('signup/', views.signup, name='signup'),
    path('landing/', views.landing, name='landing'),
    path('contactus/', views.contactus, name='contactus'),
    path('knowstat/', views.knowstat_view, name='knowstat'),
    path('safespace/', views.safespace_view, name='safespace'),
    
    path("send-sms/", send_sms_view, name="send_sms"),
    path("send-otp/", send_otp_view, name="send_otp"),
    path("verify-otp/", verify_otp_view, name="verify_otp"),
]
