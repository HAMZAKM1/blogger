# blogger/settings.py

from pathlib import Path
import os
from django.contrib.messages import constants as messages

# === Base Directory ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === Security ===
SECRET_KEY = 'django-insecure-k*508vkl5mb+p*2od38c@^mirp*$ruu(c5oa$pur2#zr=wx91u'
DEBUG = True
ALLOWED_HOSTS = []

# === Installed Apps ===
INSTALLED_APPS = [
    # Django Default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Third-party
    'debug_toolbar',

    # Local apps
    'blog',
    'users',
    'notifications',
]

# === Middleware ===
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# === Root URL Configuration ===
ROOT_URLCONF = 'blogger.urls'

# === Templates ===
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',              # shared templates folder (optional)
            BASE_DIR / 'users' / 'templates',
            BASE_DIR / 'blog' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Required for auth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# === WSGI Application ===
WSGI_APPLICATION = 'blogger.wsgi.application'

# === Database ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# === Custom User Model ===
AUTH_USER_MODEL = 'users.CustomUser'

# === Authentication Redirects (✅ NAMESPACED)
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'blog:post_list'
# settings.py

LOGOUT_REDIRECT_URL = 'users:login'

# === Password Validation ===
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# === Internationalization ===
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# === Static Files ===
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'blogger' / 'static',
]

# === Media Files ===
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# === Default Primary Key Field Type ===
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# === Messages Framework ===
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# === Email Backend ===
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@blogger.com'

# === Caching ===
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# === Debug Toolbar ===
INTERNAL_IPS = [
    "127.0.0.1",
]

# === Logging ===
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# === Optional Production Settings ===
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
# X_FRAME_OPTIONS = 'DENY'
