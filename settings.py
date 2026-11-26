"""
Django settings for moonlight_hotel project.
"""

import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Uses environment variable in production, falls back to default key for local dev
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-=*0zj2l2x7#!ne%2w!m^9gwc#_5#zk^p&&x-%m17#-%bd#la@u')

# SECURITY WARNING: don't run with debug turned on in production!
# Set to 'False' in production environment variables
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Allow localhost for development and Render domain for production
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.onrender.com']

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "bookings",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'moonlight_hotel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'bookings.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'moonlight_hotel.wsgi.application'

# Database
# Automatically parses DATABASE_URL provided by Render. 
# Falls back to local postgres for development.
DATABASES = {
    'default': dj_database_url.config(
        default='postgres://moonlight_user:123@localhost:5432/moonlight_db',
        conn_max_age=600
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# --- MEDIA FILES (User Uploaded Images) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- REAL EMAIL SETTINGS (GMAIL) ---

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# IMPORTANT: Use Environment Variables for these in Production!
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'your_email@gmail.com')      
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'your_app_password') 

# --- AUTHENTICATION REDIRECTS ---
LOGIN_REDIRECT_URL = 'room_list'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'home'

# --- PRODUCTION SECURITY ---
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']