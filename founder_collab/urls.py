from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='founder_feed'),
    path('post/', views.post_need, name='founder_post_need'),
    path('request/<int:need_id>/', views.send_request, name='founder_send_request'),
]
