from django.contrib.auth.models import AbstractUser
from django.db import models

TEXT_RESTRICTION_EMAIL = 254
TEXT_RESTRICTION_ROLE = 20
TEXT_RESTRICTION_CONFIRMATION_CODE = 255


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLE_CHOICES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    email = models.EmailField(
        max_length=TEXT_RESTRICTION_EMAIL,
        unique=True,
        verbose_name='Email address'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Biography'
    )
    role = models.CharField(
        max_length=TEXT_RESTRICTION_ROLE,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='User role'
    )
    confirmation_code = models.CharField(
        max_length=TEXT_RESTRICTION_CONFIRMATION_CODE,
        blank=True,
        null=True,
        verbose_name='Confirmation code'
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ['id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
