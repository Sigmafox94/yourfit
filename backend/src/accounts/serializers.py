# yourfit-saas/backend/src/accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

User = get_user_model() # Get the custom User model

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles creating a new user with hashed password.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2') # Remove password2 as it's not a model field
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for handling user login (username/email and password) to get a token.
    """
    username_or_email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username_or_email = attrs.get('username_or_email')
        password = attrs.get('password')

        if username_or_email and password:
            # Try to authenticate with username first
            user = authenticate(request=self.context.get('request'),
                                username=username_or_email, password=password)

            if not user:
                # If username failed, try with email
                try:
                    user_by_email = User.objects.get(email=username_or_email)
                    user = authenticate(request=self.context.get('request'),
                                        username=user_by_email.username, password=password)
                except User.DoesNotExist:
                    pass # User not found by email either

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username_or_email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing and updating user profile data.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login')
        read_only_fields = ('id', 'username', 'email', 'date_joined', 'last_login') # Email can be read, but not updated via profile endpoint if it's the unique identifier.