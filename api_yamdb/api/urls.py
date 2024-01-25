from django.urls import path

from .views import (
    SignUpView, TokenValidationView, UserListCreateView
)
API_VERSION = 'v1'

urlpatterns = [
    path(
        f'{API_VERSION}/auth/signup/',
        SignUpView.as_view(),
        name='register'
    ),
    path(
        f'{API_VERSION}/auth/token/',
        TokenValidationView.as_view(),
        name='validate-token'
    ),
    path(f'{API_VERSION}/users/', UserListCreateView.as_view()),
]
