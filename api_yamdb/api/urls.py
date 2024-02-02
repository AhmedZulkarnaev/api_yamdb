from django.urls import include, path
from rest_framework import routers

from .views import (
    UserRegisterAPIView,
    TokenValidationAPIView,
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
