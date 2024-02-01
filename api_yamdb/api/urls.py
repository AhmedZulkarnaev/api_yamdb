from django.urls import include, path
from rest_framework import routers

from .views import (
    UserRegisterViewSet,
    TokenValidationViewSet,
    UserListViewSet,
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
)

API_VERSION_1 = 'v1'

router_v1 = routers.DefaultRouter()
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('auth/signup', UserRegisterViewSet, basename='register')
router_v1.register('auth/token', TokenValidationViewSet, basename='auth')
router_v1.register('users', UserListViewSet, basename='users')

urlpatterns = [
    path(
        f'{API_VERSION_1}/', include(router_v1.urls)
    )
]
