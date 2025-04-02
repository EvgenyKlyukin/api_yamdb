from rest_framework import viewsets, filters
from django_filters import rest_framework as django_filters
from .models import Title, Category, Genre


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
    update() - PUT /titles/{id}/ - обновление произведения
    partial_update() - PATCH /titles/{id}/ - частичное обновление произведения
    destroy() - DELETE /titles/{id}/ - удаление произведения

    Фильтрация:
    - category - фильтр по slug категории
    - genre - фильтр по slug жанра
    - name - фильтр по названию произведения
    - year - фильтр по году выпуска

    TODO:
    - Добавить serializer_class (TitleSerializer)
    - Добавить permissions_classes для разграничения доступа
    """
    queryset = Title.objects.all()
    filterset_class = TitleFilter
    filter_backends = (django_filters.DjangoFilterBackend,)


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
