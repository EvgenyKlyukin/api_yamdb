from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):

    username = models.CharField(unique=True, max_length=150,
                                verbose_name='имя пользователя')
    email = models.EmailField(unique=True, max_length=254,
                              verbose_name='e-mail')
    first_name = models.CharField(max_length=150, verbose_name='имя')
    last_name = models.CharField(max_length=150, verbose_name='фамилия')
    bio = models.TextField(verbose_name='биография')
    role = models.CharField(choices=ROLE_CHOICES, max_length=20)

    def has_role(self, role):
        return self.role == role

    @property
    def is_moderator(self):
        return self.has_role('moderator')

    @property
    def is_admin(self):
        return self.has_role('admin') or self.is_superuser or self.is_staff

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username
