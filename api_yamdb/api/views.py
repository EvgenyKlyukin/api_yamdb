from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as django_filters
from rest_framework import filters, mixins, viewsets

from api.permissions import IsAdminOrReadOnly, IsAdminModeratorAuthorOrReadOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleReadSerializer, TitleWriteSerializer)
from reviews.models import Category, Comments, Genre, Review, Title


class TitleFilter(django_filters.FilterSet):
    """Фильтр для произведений."""
    category = django_filters.CharFilter(field_name='category__slug')
    genre = django_filters.CharFilter(field_name='genre__slug')
    name = django_filters.CharFilter(field_name='name', lookup_expr='contains')
    year = django_filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']


class TitleViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с произведениями.

    list() - GET /titles/ - получение списка всех произведений
    create() - POST /titles/ - добавление произведения
    retrieve() - GET /titles/{id}/ - получение произведения
    partial_update() - PATCH /titles/{id}/ - частичное обновление произведения
    destroy() - DELETE /titles/{id}/ - удаление произведения

    Поддерживает фильтрацию:
    - category - фильтр по slug категории
    - genre - фильтр по slug жанра
    - name - фильтр по названию произведения
    - year - фильтр по году выпуска
    """
    queryset = Title.objects.all()
    filterset_class = TitleFilter
    filter_backends = (django_filters.DjangoFilterBackend,)
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitleWriteSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return self.serializer_class

    def get_queryset(self):
        return Title.objects.annotate(
            rating=Avg('title_reviews__score')
        ).order_by('name')


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Базовый ViewSet для операций list, create, destroy."""
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    """
    ViewSet для работы с категориями (list, create, destroy).
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(ListCreateDestroyViewSet):
    """
    ViewSet для работы с жанрами (list, create, destroy).
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с отзывами.

    Поддерживает операции:
    - GET /titles/{title_id}/reviews/ - получение списка отзывов
    - POST /titles/{title_id}/reviews/ - добавление отзыва
    - GET /titles/{title_id}/reviews/{review_id}/ - получение отзыва
    - PATCH /titles/{title_id}/reviews/{review_id}/ - частичное обновление
      отзыва
    - DELETE /titles/{title_id}/reviews/{review_id}/ - удаление отзыва
    """
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        title = self.get_title()
        return (
            Review.objects
            .filter(title=title)
            .select_related('author', 'title')
            .order_by('-pub_date')
        )

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(
            author=self.request.user,
            title=title
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['title'] = self.get_title()
        return context


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с комментариями.

    Поддерживает операции:
    - GET /titles/{title_id}/reviews/{review_id}/comments/ - получение списка
      комментариев
    - POST /titles/{title_id}/reviews/{review_id}/comments/ - добавление
      комментария
    - GET /titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ -
      получение комментария
    - PATCH /titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ -
      частичное обновление комментария
    - DELETE /titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ -
      удаление комментария
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title=title
        )

    def get_queryset(self):
        review = self.get_review()
        return (
            Comments.objects
            .filter(review=review)
            .select_related('author', 'review')
            .order_by('pub_date')
        )

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(
            author=self.request.user,
            review=review
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['review'] = self.get_review()
        return context
