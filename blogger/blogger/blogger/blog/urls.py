from django.urls import path
from . import views

app_name = 'blog'  # Enables reverse('blog:post_list') etc.

urlpatterns = [
    # 📄 Blog Post Views
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('search/', views.post_search, name='post_search'),
    path('categories/', views.categories_view, name='categories'),
    path('category/<slug:slug>/', views.category_posts_view, name='category_posts'),
    # 🔔 Notifications
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-read/<int:pk>/', views.mark_read, name='mark_read'),
    path('notifications/mark-all-read/', views.mark_all_read, name='mark_all_read'),

    # 👤 Posts by specific user
    path('user/<str:username>/', views.user_posts, name='user_posts'),
]
