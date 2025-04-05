import uuid

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdmin
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from users.models import User
from users.serializers import (TokenSerializer, UserCreateSerializer,
                               UserEditSerializer, UserSerializer)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    """Регистрация пользователя."""
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    email = serializer.validated_data['email']

    if User.objects.filter(email=email).exclude(username=username).exists():
        return Response(
            {'email': ['Email уже используется']},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exclude(email=email).exists():
        return Response(
            {
                'username': [
                    'Пользователь с таким именем уже существует'
                ]
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    user, _ = User.objects.get_or_create(username=username, email=email)

    code = str(uuid.uuid4())
    user.confirmation_code = code
    user.save()

    send_mail(
        'Код подтверждения YaMDb',
        f'Код подтверждения: {code}',
        DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    """Получение токена."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )

    conf_code = serializer.validated_data['confirmation_code']
    if user.confirmation_code != conf_code:
        return Response(
            {'confirmation_code': ['Неверный код']},
            status=status.HTTP_400_BAD_REQUEST
        )

    token = AccessToken.for_user(user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки запросов к модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated],
        url_path='me'
    )
    def get_current_user_info(self, request):
        serializer = UserEditSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UserEditSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
