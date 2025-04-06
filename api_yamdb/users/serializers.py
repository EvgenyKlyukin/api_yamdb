import re

from django.core.exceptions import ValidationError
from rest_framework import serializers

from users.models import User

CHARACTER_RESTRICTION_EMAIL = 254
CHARACTER_RESTRICTION_USERNAME = 150


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""

    email = serializers.EmailField(max_length=CHARACTER_RESTRICTION_EMAIL)
    username = serializers.CharField(max_length=CHARACTER_RESTRICTION_USERNAME)

    class Meta:
        fields = ('username', 'email')
        model = User

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError('Username "me" is not allowed')
        if not re.match(r'^[\w.@+-]+$', value):
            raise ValidationError(
                'Username может содержать только буквы, цифры и @/./+/-/_'
            )
        return value

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if User.objects.filter(email=email, username=username).exists():
            return data

        if User.objects.filter(
            email=email
        ).exclude(
            username=username
        ).exists():
            raise ValidationError(
                {'email': ['Email уже используется']}
            )

        if User.objects.filter(
            username=username
        ).exclude(
            email=email
        ).exists():
            raise ValidationError(
                {'username': ['Пользователь с таким именем уже существует']}
            )

        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT токена."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким username не найден',
                code='not_found'
            )
        return value

    def validate(self, data):
        username = data['username']
        confirmation_code = data['confirmation_code']
        user = User.objects.get(username=username)
        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError({
                'confirmation_code': 'Неверный код подтверждения'
            })
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для управления пользователями."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class UserEditSerializer(serializers.ModelSerializer):
    """Сериализатор для редактирования профиля пользователя."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)
