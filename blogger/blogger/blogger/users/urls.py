from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # 🔐 Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # 👤 Profile & Settings
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),  # ✅ more descriptive URL
    path('settings/', views.settings_view, name='settings'),

    # ❌ Delete Account
    path('delete-account/', views.delete_account, name='delete_account'),

    # 🔔 Notifications
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/mark-read/<int:pk>/', views.mark_read, name='mark_read'),
    path('notifications/mark-all-read/', views.mark_all_read, name='mark_all_read'),

    # 📝 Posts by specific user
    path('user/<str:username>/', views.user_posts, name='user_posts'),
]
