from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import User
from django.contrib.auth.tokens import default_token_generator


class UserSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email',
            'role', 'bio', 'confirmation_code'
        )
        read_only_fields = ['is_verified']

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не допускается.'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not username:
            raise serializers.ValidationError(
                'Поле "username" обязательно для заполнения.',
                code='invalid'
            )

        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError(
                'Неверный код подтверждения.'
            )

        return data
