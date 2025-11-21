"""
Django settings for careconnect project.
"""

import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file (Local Laptop Only)
# This is how your laptop finds the Render Database URL without putting it in Git
load_dotenv(os.path.join(BASE_DIR, '.env'))

# ==============================================================================
# ENVIRONMENT CONFIGURATION
# ==============================================================================

# Detect if running on Render (Cloud)
# Render automatically sets the 'RENDER' variable.
ON_RENDER = os.environ.get('RENDER')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key-for-dev-only')

# SECURITY WARNING: don't run with debug turned on in production!
if ON_RENDER:
    DEBUG = False
else:
    # On local, default to True
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ALLOWED HOSTS
if ON_RENDER:
    # Your Render URL
    ALLOWED_HOSTS = ['careconnect-q369.onrender.com'] 
else:
    # Local development hosts
    # 10.0.2.2 is required for Android Emulator to talk to Localhost
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '10.0.2.2']

if ON_RENDER:
    # Your Render URL
    ALLOWED_HOSTS = ['careconnect-q369.onrender.com'] 
else:
    # Local development hosts (Allows Android Emulator 10.0.2.2)
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files handler
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'careconnect.urls'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Custom Apps
    'core',
    'rest_framework', # For Flutter API
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'careconnect.wsgi.application'

# ==============================================================================
# DATABASE CONNECTION (The Critical Part)
# ==============================================================================

DATABASES = {
    'default': dj_database_url.config(
        # 1. On Render: Automatically finds 'DATABASE_URL' from system environment.
        # 2. On Laptop: Finds 'DATABASE_URL' from your .env file.
        # 3. Safety: If missing, it crashes (won't create fake SQLite DB).
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
        # Render requires SSL
        ssl_require=True if ON_RENDER or 'postgres' in os.environ.get('DATABASE_URL', '') else False
    )
}

# ==============================================================================
# VALIDATORS & I18N
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==============================================================================
# STATIC FILES
# ==============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = []
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'core.User'

# Login/Logout redirects
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# ==============================================================================
# LOCALHOST SECURITY OVERRIDE
# ==============================================================================
# This ensures you can log in on localhost even when using the Production DB
if not ON_RENDER:
    CSRF_TRUSTED_ORIGINS = [
        'http://localhost:8000', 
        'http://127.0.0.1:8000',
        'http://10.0.2.2:8000'
    ]
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False