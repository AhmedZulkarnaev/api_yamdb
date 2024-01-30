from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, Review


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
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['title', 'author']),]

    def validate(self, data):
        if self.instance is None and Review.objects.filter(
                title=data['title'],
                author=self.context['request'].user).exists():
            raise ValidationError('Вы уже оставляли отзыв '
                                  'на это произведение!')
        return data
