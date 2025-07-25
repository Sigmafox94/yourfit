# yourfit-saas/backend/src/yourfit_api/settings/__init__.py

import os

# Determine which settings file to load based on DJANGO_SETTINGS_MODULE environment variable.
# If not set, default to development.
if os.environ.get('DJANGO_SETTINGS_MODULE') is None:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourfit_api.settings.development')