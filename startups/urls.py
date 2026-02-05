from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='startup_dashboard'),
    path('profile/edit/', views.profile_edit, name='startup_profile_edit'),
    path('jobs/create/', views.job_create, name='job_create'),
    path('jobs/<int:job_id>/applicants/', views.job_applicants, name='job_applicants'),
]
