from rest_framework import viewsets, filters
from django_filters import rest_framework as django_filters

from reviews.models import Title, Category, Genre
from .serializers import TitleReadSerializer, TitleWriteSerializer


class TitleFilter(filters.FilterSet):
    """Фильтр для произведений."""
    category = filters.CharFilter(field_name='category__slug')
    genre = filters.CharFilter(field_name='genre__slug')
    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    year = filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filterset_class = TitleFilter
    filter_backends = (django_filters.DjangoFilterBackend,)
    serializer_class = TitleWriteSerializer

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return self.serializer_class


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с категориями.

    list() - GET /categories/ - получение списка всех категорий
    create() - POST /categories/ - создание категории
    destroy() - DELETE /categories/{slug}/ - удаление категории

    Поддерживает поиск по названию категории через параметр search.
    Поля name и slug обязательны при создании.
    Поле slug должно быть уникальным.

    TODO:
    - Добавить serializer_class (CategorySerializer)
    - Добавить permissions_classes для разграничения доступа
    """
    queryset = Category.objects.all()
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ['get', 'post', 'delete']


class GenreViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с жанрами.

    list() - GET /genres/ - получение списка всех жанров
    create() - POST /genres/ - создание жанра
    destroy() - DELETE /genres/{slug}/ - удаление жанра

    Поддерживает поиск по названию жанра через параметр search.
    Поля name и slug обязательны при создании.
    Поле slug должно быть уникальным.

    TODO:
    - Добавить serializer_class (GenreSerializer)
    - Добавить permissions_classes для разграничения доступа
    """
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ['get', 'post', 'delete']
