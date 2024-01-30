from django.urls import include, path
from rest_framework import routers
from .views import (
    UserRegisterViewSet,
    TokenValidationViewSet,
    UserListViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
)

API_VERSION = 'v1'

router = routers.DefaultRouter()
router.register('genres', GenreViewSet, basename='genres')
router.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router.register('titles', TitleViewSet, basename='titles')
router.register('auth/signup', UserRegisterViewSet, basename='register')
router.register('auth/token', TokenValidationViewSet, basename='auth')
router.register('users', UserListViewSet, basename='users')

urlpatterns = [
    path(
        f'{API_VERSION}/', include(router.urls)
    )
]
