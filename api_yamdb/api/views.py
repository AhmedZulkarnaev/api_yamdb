import random

from django.core.cache import cache
from django.core.mail import send_mail

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import CustomUser
from .permissions import IsAdminOrSuperUser, isAdmin
from .pagination import CustomPagination
from .serializers import TokenSerializer, UserSerializer


class UserRegisterViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (isAdmin,)

    def generate_confirmation_code(self):
        return str(random.randint(100000, 999999))

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        username = request.data.get('username')
        user = CustomUser.objects.filter(
            email=email, username=username).first()
        if user is not None:
            return Response(
                status=status.HTTP_200_OK
            )
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            confirmation_code = self.generate_confirmation_code()
            cache.set(
                f'confirmation_code_{user.id}', confirmation_code, timeout=300)
            self.send_confirmation_code(user.email, confirmation_code)
            return Response(
                {
                    'email': user.email,
                    'username': user.username,
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_confirmation_code(self, email, confirmation_code):
        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email='noreply@example.com',
            recipient_list=[email],
            fail_silently=False,
        )


class TokenValidationViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = CustomUser.objects.get(
                    username=serializer.validated_data['username']
                )
            except CustomUser.DoesNotExist:
                return Response(
                    {'error': 'Пользователь не найден'},
                    status=status.HTTP_404_NOT_FOUND
                )
            confirmation_code = serializer.validated_data.get(
                'confirmation_code'
            )
            if not confirmation_code:
                return Response(
                    {'error': 'Требуется код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            stored_code = cache.get(f'confirmation_code_{user.id}')
            if confirmation_code != stored_code:
                return Response(
                    {'error': 'Неверный код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.save()
            refresh = RefreshToken.for_user(user)
            token = {'token': str(refresh.access_token)}
            return Response(token, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperUser, IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = CustomPagination
    http_method_names = ['get', 'post', 'delete', 'patch']
    lookup_field = 'username'
    lookup_value_regex = r'[\w\@\.\+\-]+'

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def get_current_user_info(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @get_current_user_info.mapping.patch
    def update_current_user_info(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['role'] = request.user.role
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
