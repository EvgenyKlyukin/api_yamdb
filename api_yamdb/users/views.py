import uuid

from django.core.mail import send_mail
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

    if not serializer.is_valid():
        if 'username' in serializer.errors and (
            serializer.errors['username'][0].code == 'not_found'
        ):
            return Response(serializer.errors,
                            status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.validated_data['user']
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
