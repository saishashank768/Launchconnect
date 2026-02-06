from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
    path('verification-pending/<str:username>/', views.verification_pending, name='verification_pending'),
    path('resend-verification/<str:username>/', views.resend_verification, name='resend_verification'),
]
