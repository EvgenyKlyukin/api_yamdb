from rest_framework import viewsets, generics, filters
from django_filters import rest_framework as django_filters
from .models import Title, Category


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


class CategoryListCreate(generics.ListCreateAPIView):
    """
    View для работы со списком категорий.

    get() - GET /categories/ - получение списка всех категорий
    post() - POST /categories/ - создание новой категории

    Поддерживает поиск по названию категории через параметр search.
    Поля name и slug обязательны при создании.
    Поле slug должно быть уникальным.

    TODO:
    - Добавить serializer_class (CategorySerializer)
    - Добавить permissions_classes для разграничения доступа
    """
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryDestroy(generics.DestroyAPIView):
    """
    View для удаления категории.

    delete() - DELETE /categories/{slug}/ - удаление категории

    TODO:
    - Добавить serializer_class (CategorySerializer)
    - Добавить permissions_classes для разграничения доступа
    """
    queryset = Category.objects.all()
    lookup_field = 'slug'
