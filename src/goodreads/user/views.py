from typing import Any
from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from user import serializers
from user.models import User as CustomUser


class SignupOrLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.User = get_user_model()

    @extend_schema(
        request=serializers.UserSerializer,
        responses=serializers.UserSignUpOrLoginResponseSerializer,
    )
    def post(self, request: Request) -> None:
        """
        API for signing up or log in a user.
        """
        serializer = serializers.UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer.user_exists(serializer.validated_data):
            return self._login(
                request,
                serializer.validated_data["email"],
                serializer.validated_data["password"],
            )

        user: CustomUser = serializer.create(serializer.validated_data)

        return Response(
            serializers.UserSignUpOrLoginResponseSerializer(
                {"message": "Sign up successful.", "token": user.get_or_create_token()}
            ).data,
            status=status.HTTP_201_CREATED,
        )

    def _login(self, request: Request, email: str, password: str) -> Response:
        user: CustomUser = authenticate(request, username=email, password=password)
        if not user:
            return Response(
                {"message": "Email or password is wrong."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            serializers.UserSignUpOrLoginResponseSerializer(
                {"message": "Login successful.", "token": user.get_or_create_token()}
            ).data
        )
