from rest_framework import serializers
from django.utils.timezone import now

from reviews.models import (
    Genre, Title, TitleGenre, Review, Comment, User, Category
)


class UserSerializers(serializers.ModelSerializer):
    pass


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault(),
    )


class CommentSerializer(serializers.ModelSerializer):
    pass
