import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'USER', _('User')
        ADMIN = 'ADMIN', _('Admin')
        MODERATOR = 'MODERATOR', _('Moderator')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER
    )
    avatar_url = models.TextField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    # password_hash is handled by AbstractUser (password field)
    # is_active is handled by AbstractUser
    # last_login_at is handled by AbstractUser (last_login)
    # created_at is handled by AbstractUser (date_joined)

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username
