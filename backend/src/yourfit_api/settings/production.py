# yourfit-saas/backend/src/yourfit_api/settings/production.py

from .base import *
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Production ALLOWED_HOSTS must be explicitly defined
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')
if not ALLOWED_HOSTS:
    raise ValueError("ALLOWED_HOSTS must be configured in production.")


# Database for production (PostgreSQL on AWS RDS will be configured here)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432', cast=int),
        'CONN_MAX_AGE': 600, # persistent connections
    }
}

# Static files storage in production (S3 or similar)
# You will install django-storages and boto3 later: pip install django-storages boto3
# AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
# AWS_S3_SIGNATURE_VERSION = 's3v4'
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None # Or 'public-read' if specific files need public access

# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com' # Or your CloudFront domain
# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# Production Security Headers
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int) # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=False, cast=bool) # Set to True after successful preload submission

SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool) # Redirect all HTTP to HTTPS

SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
SESSION_COOKIE_HTTPONLY = True # Prevent client-side JS access to session cookie
CSRF_COOKIE_HTTPONLY = True # Prevent client-side JS access to CSRF cookie

X_FRAME_OPTIONS = 'DENY' # Prevents clickjacking

# CORS Headers (Stricter in production)
CORS_ALLOW_ALL_ORIGINS = False # MUST be False in production!
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='' # Comma-separated list of allowed origins from .env
).split(',')
if not CORS_ALLOWED_ORIGINS and not CORS_ALLOW_ALL_ORIGINS:
    raise ValueError("CORS_ALLOWED_ORIGINS must be configured in production (or CORS_ALLOW_ALL_ORIGINS set to True, which is highly discouraged).")

# Logging (example - configure for your needs)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'yourfit_api': { # Your project's top-level logger
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}