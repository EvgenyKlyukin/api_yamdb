from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message=(
                    'Username может содержать только буквы, цифры и @/./+/-/_')
            )
        ]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254
    )
    first_name = serializers.CharField(
        required=False,
        max_length=150,
        allow_blank=True
    )
    last_name = serializers.CharField(
        required=False,
        max_length=150,
        allow_blank=True
    )
    bio = serializers.CharField(
        required=False,
        allow_blank=True
    )
    role = serializers.ChoiceField(
        choices=User.Role.choices if hasattr(User, 'Role') else [
            ('user', 'user'),
            ('moderator', 'moderator'),
            ('admin', 'admin')
        ],
        default='user',
        required=False
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует.'
            )
        return value


# class SignUpSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True,
#                                      validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password', 'password2',
#                   'first_name', 'last_name', 'bio')
#         extra_kwargs = {
#             'first_name': {'required': True},
#             'last_name': {'required': True}
#         }

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError(
#                 {"password": "Password fields didn't match."})
#         return attrs

#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#             bio=validated_data.get('bio', '')
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['username'] = user.username
#         token['role'] = user.role
#         return token
