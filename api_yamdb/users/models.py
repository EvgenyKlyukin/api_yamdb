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

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username
