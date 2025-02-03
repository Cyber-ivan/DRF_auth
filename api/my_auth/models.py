from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid
from django.conf import settings
from django.db import models
from django.utils.timezone import now, timedelta
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken


# class Refresh_Token(models.Model):
#     token = models.CharField(unique=True,not_null=True)
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='refresh_tokens'
#     )
#
#
#     def is_valid(self):
#
#         return now() < self.expires_at
#
#     def blacklist(self):
#         self.delete()
#
#     @staticmethod
#     def for_user(user):
#         """Генерирует новый Refresh Token и Access Token для пользователя."""
#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)
#         refresh_token = str(refresh)
#         save_token = Refresh_Token(refresh_token, user)
#         save_token.save()
#         return {
#             'refresh': str(refresh_token),
#             'access_token': str(access_token),
#         }

class User(AbstractUser):
    username = models.CharField(max_length=150, null=True, blank=True)
    refresh_token = models.CharField(blank=True, max_length=300)
    email = models.EmailField(
        _('email address'),
        unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
