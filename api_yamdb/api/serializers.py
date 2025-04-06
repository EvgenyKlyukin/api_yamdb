from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from reviews.models import Category, Comments, Genre, Review, Title


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
            if request.user.user_reviews.filter(title=title).exists():
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
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'review', 'pub_date')
        read_only_fields = ('id', 'author', 'review', 'pub_date')
        extra_kwargs = {
            'text': {'required': True}
        }

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method == 'POST':
            review = self.context['view'].get_review()
            if request.user.user_comments.filter(review=review).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли комментарий к этому отзыву.'
                )
        return data

    def create(self, validated_data):
        validated_data['review'] = self.context['view'].get_review()
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
