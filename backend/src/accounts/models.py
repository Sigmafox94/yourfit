# yourfit-saas/backend/src/accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model for YourFit.io.
    Extends Django's AbstractUser to allow for future customization.
    Using email as unique field for better user experience.
    """
    email = models.EmailField(unique=True, null=False, blank=False)

    # Add any custom fields here if needed in the future
    # For example:
    # phone_number = models.CharField(max_length=15, blank=True, null=True)
    # date_of_birth = models.DateField(blank=True, null=True)
    # fitness_goals = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.email # Or self.username if you prefer to identify by username