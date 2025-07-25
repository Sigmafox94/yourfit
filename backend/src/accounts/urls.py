# yourfit-saas/backend/src/accounts/urls.py

from django.urls import path
from accounts.views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserLogoutView,
)

app_name = 'accounts' # Namespace for accounts app URLs

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]