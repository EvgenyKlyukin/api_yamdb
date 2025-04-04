from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TokenObtainView, UserSignUpView, UserViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', UserSignUpView.as_view(), name='signup'),
    path('auth/token/', TokenObtainView.as_view(), name='token'),
    path('', include(router_v1.urls)),
]
