from __future__ import annotations

from typing import Optional

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def create_user(
        self, email: str, password: Optional[str] = None, **extra_fields
    ) -> User:
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: Optional[str] = None, **extra_fields
    ) -> User:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def get_or_create_token(self) -> Token:
        token = Token.objects.filter(user=self).first()
        if not token:
            token = Token.objects.create(user=self)
        return token.key

    def __str__(self):
        return self.email

    class Meta:
        app_label = "user"
