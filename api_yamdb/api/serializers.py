from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comments, Genre, Review, Title

User = get_user_model()


class UserSignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователей."""
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.RegexField(
        max_length=150,
        required=True,
        regex=r'^[\w.@+-]+$',
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return value


class TokenObtainSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    username = serializers.RegexField(
        max_length=150,
        required=True,
        regex=r'^[\w.@+-]+$'
    )
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

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


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для редактирования профиля пользователя."""
    role = serializers.CharField(read_only=True)

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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        read_only_fields = ('id', 'author', 'pub_date', 'title')
        extra_kwargs = {
            'score': {
                'validators': [
                    MinValueValidator(1),
                    MaxValueValidator(10)
                ]
            }
        }

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method == 'POST':
            title = self.context['view'].get_title()
            if Review.objects.filter(
                author=request.user,
                title=title
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли отзыв на это произведение.'
                )
        return data

    def create(self, validated_data):
        validated_data['title'] = self.context['view'].get_title()
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    review_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'review_id', 'pub_date')
        read_only_fields = ('id', 'author', 'review_id', 'pub_date')
        extra_kwargs = {
            'text': {'required': True}
        }

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method == 'POST':
            review = self.context['view'].get_review()
            if Comments.objects.filter(
                author=request.user,
                review_id=review
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли комментарий к этому отзыву.'
                )
        return data

    def create(self, validated_data):
        validated_data['review_id'] = self.context['view'].get_review()
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
