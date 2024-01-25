from rest_framework import serializers
from reviews.models import CustomUser
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all()),
            RegexValidator(
                regex=r'^[\w.@+-]+$',
            )
        ]
    )

    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'role',
            'confirmation_code', 'is_verified'
        )
        read_only_fields = ('confirmation_code', 'is_verified')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError("Имя 'me' недопустимо.")
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.IntegerField()
