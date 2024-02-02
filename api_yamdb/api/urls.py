from django.urls import path, include
from rest_framework import routers

from .views import (
    UserRegisterAPIView, TokenValidationAPIView, UserListViewSet,
)
API_VERSION_1 = 'v1'

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserListViewSet, basename='users')

urlpatterns = [
    path(
        f'{API_VERSION_1}/', include([
            path(
                'auth/signup/',
                UserRegisterAPIView.as_view(), name='register'
            ),
            path(
                'auth/token/',
                TokenValidationAPIView.as_view(), name='auth'
            ),
        ])
    ),
    path(f'{API_VERSION_1}/', include(router_v1.urls)),
]
