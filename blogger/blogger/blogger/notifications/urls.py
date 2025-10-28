# notifications/urls.py
from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='list'),
    path('mark_read/<int:pk>/', views.mark_read, name='mark_read'),
    path('mark_all_read/', views.mark_all_read, name='mark_all_read'),
    path('delete/<int:pk>/', views.delete_notification, name='delete'),
]
