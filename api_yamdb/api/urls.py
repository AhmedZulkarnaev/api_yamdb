from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router = DefaultRouter()
router.register('genres', GenreViewSet, basename='genres')
router.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(router.urls))
]