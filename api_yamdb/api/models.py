from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    USER = 'user', 'Пользователь'
    MODERATOR = 'moderator', 'Модератор'
    ADMIN = 'admin', 'Администратор'


class User(AbstractUser):
    """Кастомная модель пользователя."""
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=255,
        blank=True,
        null=True,
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER,
    )

    USERNAME_FIELD = 'email'  # Используем email для входа
    # username все еще обязателен при создании через createsuperuser
    REQUIRED_FIELDS = ['username']

    @property
    def is_admin(self):
        return (
            self.role == UserRole.ADMIN
            or self.is_staff
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username
