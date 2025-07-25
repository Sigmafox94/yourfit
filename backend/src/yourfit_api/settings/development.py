# yourfit-saas/backend/src/yourfit_api/settings/development.py

from .base import *
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# For local development, allow specific IPs or all hosts for convenience
# BE CAREFUL: '*' is fine for local dev, but NEVER use in production.
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

# Database for development (SQLite for simplicity, will switch to Dockerized PostgreSQL later)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files (CSS, JavaScript, Images) for local development
STATIC_ROOT = BASE_DIR / 'staticfiles_dev' # Where collected static files will go in dev
MEDIA_ROOT = BASE_DIR / 'media_dev'       # Where user-uploaded files will go in dev

# CORS Headers (More permissive for local development)
CORS_ALLOW_ALL_ORIGINS = True # Allow all origins for local dev (frontend on different port)
CORS_ALLOW_CREDENTIALS = True # Allow cookies to be sent