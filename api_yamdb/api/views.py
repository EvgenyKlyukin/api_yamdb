import uuid

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from .permissions import IsAdmin
from .serializers import (
    TokenObtainSerializer, UserProfileSerializer, UserSerializer,
    UserSignUpSerializer
)

from django.shortcuts import get_object_or_404
from django_filters import rest_framework as django_filters
from rest_framework import filters, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleReadSerializer, TitleWriteSerializer)
from reviews.models import Category, Comments, Genre, Review, Title

User = get_user_model()


class UserSignUpView(APIView):
    """
    Регистрация пользователя и отправка кода подтверждения на email.
    Права доступа: Доступно без токена.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']

        user, created = User.objects.get_or_create(
            username=username,
            email=email
        )

        confirmation_code = str(uuid.uuid4())
        user.confirmation_code = confirmation_code
        user.save()

        send_mail(
            subject='YaMDb registration',
            message=f'Your confirmation code: {confirmation_code}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenObtainView(APIView):
    """
    Получение JWT-токена в обмен на username и confirmation code.
    Права доступа: Доступно без токена.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']

        user = get_object_or_404(User, username=username)

        if not confirmation_code == user.confirmation_code:
            return Response(
                {'confirmation_code': ['Неверный код подтверждения']},
                status=status.HTTP_400_BAD_REQUEST
            )

        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    Работа с пользователями.
    Права доступа: Администратор.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated,),
        serializer_class=UserProfileSerializer,
    )
    def me(self, request):
        """Получение и изменение данных своей учетной записи."""
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

      
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

    Поддерживает фильтрацию:
    - category - фильтр по slug категории
    - genre - фильтр по slug жанра
    - name - фильтр по названию произведения
    - year - фильтр по году выпуска

    TODO:
    - Добавить permissions_classes для разграничения доступа
      (GET - для всех, остальное - только для админа)
    """
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
    - Добавить permissions_classes для разграничения доступа
      (GET - для всех, POST/DELETE - только для админа)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
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
    - Добавить permissions_classes для разграничения доступа
      (GET - для всех, POST/DELETE - только для админа)
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ['get', 'post', 'delete']


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с отзывами."""
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return (
            Review.objects
            .filter(title_id=self.kwargs['title_id'])
            .select_related('author', 'title')
            .order_by('-pub_date')
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, pk=self.kwargs['title_id'])
        )

    def create(self, request, *args, **kwargs):
        if self.get_queryset().filter(author=request.user).exists():
            raise ValidationError(
                {'detail': 'Вы уже оставляли отзыв на это произведение.'},
                code=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['title'] = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return context


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с комментариями."""
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return (
            Comments.objects
            .filter(review_id=self.kwargs['review_id'])
            .select_related('author', 'review')
            .order_by('pub_date')
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(
                Review,
                pk=self.kwargs['review_id'],
                title_id=self.kwargs['title_id']
            )
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['review'] = get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title_id=self.kwargs['title_id']
        )
        return context