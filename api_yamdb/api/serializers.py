import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Genre, Title, CustomUser, Comment, Review


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'username', 'first_name', 'last_name', 'email',
            'role', 'bio'
        )
        read_only_fields = ['confirmation_code', 'is_verified']

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


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        lookup_field = 'slug'
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        lookup_field = 'slug'
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title


class TitleEditSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        fields = (
            'id',
            'name',
            'description',
            'year',
            'category',
            'genre'
        )
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        fields = ['id', 'author', 'text', 'pub_date']
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='name')

    class Meta:
        fields = ['id', 'author', 'score', 'text', 'title', 'pub_date']
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'POST' and Review.objects.filter(
                title=self.context['view'].kwargs.get('title_id'),
                author=self.context['request'].user).exists():
            raise ValidationError('Вы уже оставляли отзыв '
                                  'на это произведение!')
        return data
