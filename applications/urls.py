from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('update-status/<int:application_id>/', views.update_status, name='update_application_status'),
    path('convert-to-job/<int:application_id>/', views.convert_to_job, name='convert_to_job'),
]
