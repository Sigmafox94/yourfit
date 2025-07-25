# yourfit-saas/backend/src/accounts/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout # Import Django's login/logout functions

from .serializers import (
    UserRegistrationSerializer,
    AuthTokenSerializer,
    UserProfileSerializer,
)

User = get_user_model() # Get the custom User model

class UserRegistrationView(generics.CreateAPIView):
    """
    API view for user registration.
    Allows new users to create an account.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,) # Anyone can register

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Optionally log the user in after registration
        # login(request, user) # Use if you want session authentication too
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "message": "User registered successfully.",
            "user": UserRegistrationSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)

class UserLoginView(ObtainAuthToken):
    """
    API view for user login.
    Extends DRF's ObtainAuthToken to return user data along with the token.
    """
    serializer_class = AuthTokenSerializer # Custom serializer to handle username/email
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        # Optionally log the user in for session authentication
        # login(request, user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating user profile.
    Requires authentication.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        # Return the profile of the currently authenticated user
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # Partial update
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # Full update
        return self.update(request, *args, **kwargs)

class UserLogoutView(APIView):
    """
    API view for user logout.
    Deletes the user's authentication token.
    Requires authentication.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        if request.user.auth_token:
            request.user.auth_token.delete()
        # Optionally log out of sessions
        # logout(request)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)