from typing import Mapping

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data: Mapping[str, str]) -> AbstractBaseUser:
        user = User(email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user

    def user_exists(self, validated_data):
        return User.objects.filter(email=validated_data["email"]).exists()


class UserSignUpOrLoginResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    token = serializers.CharField()
