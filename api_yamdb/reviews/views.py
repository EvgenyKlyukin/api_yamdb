from rest_framework import viewsets
from django_filters import rest_framework as filters
from .models import Title


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
    filter_backends = (filters.DjangoFilterBackend,)
