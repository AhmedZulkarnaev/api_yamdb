from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from reviews.models import CustomUser
from .serializers import UserSerializer, TokenSerializer
import random
from rest_framework import generics
from .permissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def generate_confirmation_code(self):
        return random.randint(100000, 999999)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            confirmation_code = self.generate_confirmation_code()
            user.confirmation_code = confirmation_code
            user.save()

            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения: {confirmation_code}',
                'noreply@example.com',
                [user.email],
                fail_silently=False,
            )

            return Response(
                {
                    'email': user.email,
                    'username': user.username,
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenValidationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
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
            confirmation_code = int(confirmation_code)
            if confirmation_code != user.confirmation_code:
                return Response(
                    {'error': 'Неверный код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.is_verified = True
            user.save()
            refresh = RefreshToken.for_user(user)
            token = {'token': str(refresh.access_token)}
            return Response(token, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username']
    lookup_field = 'username'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        role = self.request.data.get('role', 'user')
        serializer.save(role=role)
