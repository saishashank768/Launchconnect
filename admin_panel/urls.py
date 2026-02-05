from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard_custom'),
    path('verify/<int:startup_id>/', views.verify_startup, name='verify_startup'),
]
