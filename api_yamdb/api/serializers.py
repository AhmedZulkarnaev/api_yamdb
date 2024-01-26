from rest_framework import serializers
from reviews.models import CustomUser
import re
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all())
        ]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all())
        ]
    )
    first_name = serializers.CharField(
        max_length=150,
        required=False,
    )
    last_name = serializers.CharField(
        max_length=150,
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'role',
            'is_verified', 'first_name', 'last_name'
        )
        read_only_fields = ['is_verified']

    def validate_name(self, value):
        if len(value) > 150:
            raise serializers.ValidationError(
                'Длина поля не должна превышать 150 символов.'
            )
        return value

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                'Имя пользователя может содержать только буквы, '
                'цифры и символы: @/./+/-/_.'
            )
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не допускается.'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.IntegerField()
