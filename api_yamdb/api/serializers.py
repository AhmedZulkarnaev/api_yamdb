from rest_framework import serializers
from reviews.models import User


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
