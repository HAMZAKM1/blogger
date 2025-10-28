from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ Enables login, logout, password_reset, password_change
    path('accounts/', include('django.contrib.auth.urls')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    # ✅ Your custom apps
    path('users/', include('users.urls', namespace='users')),
    path('', include('blog.urls', namespace='blog')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
