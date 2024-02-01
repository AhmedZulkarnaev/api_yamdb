from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator

from reviews.models import Category, Genre, Title, User, Comment, Review


class UserSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email',
            'role', 'bio', 'confirmation_code'
        )
        read_only_fields = ['is_verified']


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
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        allow_null=False,
        allow_empty=False
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )
        model = Title

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        reviews = instance.reviews.all()
        if reviews.exists():
            representation['rating'] = int(
                reviews.aggregate(Avg('score'))['score__avg']
            )
        else:
            representation['rating'] = None
        representation.move_to_end('description')
        representation.move_to_end('genre')
        representation.move_to_end('category')
        return representation


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
        title = get_object_or_404(
            Title,
            pk=self.context['view'].kwargs.get('title_id'))
        if self.context['request'].method == 'POST' and Review.objects.filter(
                title=title,
                author=self.context['request'].user).exists():
            raise ValidationError('Вы уже оставляли отзыв '
                                  'на это произведение!')
        return data
