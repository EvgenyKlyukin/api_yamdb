from rest_framework import viewsets, generics, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model
from api.permissions import IsAdmin

from .serializers import (
    UserSerializer
)

User = get_user_model()


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()  # .order_by('username')
    serializer_class = UserSerializer
    # permission_classes = [IsAdmin]
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'delete', 'patch']

    # def get_object(self):
    #     username = self.kwargs.get('username')
    #     try:
    #         return User.objects.get(username=username)
    #     except User.DoesNotExist:
    #         raise NotFound('Пользователь с таким именем не найден')


class UserMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user



# class SignUpView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = SignUpSerializer
#     permission_classes = [permissions.AllowAny]

# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer
