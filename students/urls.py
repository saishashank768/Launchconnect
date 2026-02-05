from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='student_dashboard'),
    path('profile/edit/', views.profile_edit, name='student_profile_edit'),
]
