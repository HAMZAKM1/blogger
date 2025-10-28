from django.urls import path
from . import views

app_name = 'blog'  # Namespacing URLs

urlpatterns = [
    # Home
    path('', views.home_view, name='home'),

    # Posts
    path('posts/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('categories/', views.categories_view, name='categories'),
    path('category/<slug:slug>/', views.category_posts_view, name='category_posts'),
    # Search
    path('search/', views.search_view, name='search'), 
    path('search/', views.post_search, name='post_search'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-read/<int:pk>/', views.mark_read, name='mark_read'),
    path('notifications/mark-all-read/', views.mark_all_read, name='mark_all_read'),
    path('categories/', views.categories_view, name='categories'),  # <-- add this
    # User posts
    path('user/<str:username>/', views.user_posts, name='user_posts'),
]
