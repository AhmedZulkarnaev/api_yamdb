from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User
from .permissions import IsAdminOrSuperUser, IsAdmin
from .serializers import TokenSerializer, UserSerializer


class UserRegisterViewSet(viewsets.ViewSet):
    permission_classes = (IsAdmin,)

    def create(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        user = User.objects.filter(email=email, username=username).first()
        if user:
            confirmation_code = self.generate_confirmation_code(user)
            self.send_confirmation_code(user.email, confirmation_code)
            return Response(
                {'message': 'Код подтверждения отправлен.'},
                status=status.HTTP_200_OK
            )

        serializer = UserSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            confirmation_code = self.generate_confirmation_code(user)
            self.send_confirmation_code(user.email, confirmation_code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_confirmation_code(self, user):
        return default_token_generator.make_token(user)

    def send_confirmation_code(self, email, confirmation_code):
        send_mail(
            subject='Confirmation Code',
            message=f'Your confirmation code: {confirmation_code}',
            from_email='noreply@example.com',
            recipient_list=[email],
            fail_silently=False,
        )


class TokenValidationViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(
                User, username=serializer.validated_data['username'])
            user.is_verified = True
            user.save()
            refresh = RefreshToken.for_user(user)
            token = {'token': str(refresh.access_token)}
            return Response(token, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperUser, IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

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
