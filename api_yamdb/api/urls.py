from django.urls import path, include
from rest_framework import routers

from .views import (
    UserRegisterViewSet, TokenValidationViewSet, UserListViewSet,
)
API_VERSION = 'v1'

router = routers.DefaultRouter()
router.register('auth/signup', UserRegisterViewSet, basename='register')
router.register('auth/token', TokenValidationViewSet, basename='auth')
router.register('users', UserListViewSet, basename='users')

urlpatterns = [
    path(
        f'{API_VERSION}/', include(router.urls)
    )
]
