from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (UserListCreateView, UserRetrieveUpdateDestroyView,
                    UserMeView)

router = DefaultRouter()

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/user/me/', UserMeView.as_view(), name='user-me'),
    path('v1/users/', UserListCreateView.as_view(), name='user-list-create'),
    path('v1/users/<str:username>/', UserRetrieveUpdateDestroyView.as_view(),
         name='user-retrive-update-destroy'),
    path('v1/auth/', include('djoser.urls.jwt'))
]
