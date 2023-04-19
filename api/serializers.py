from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.forms import ValidationError
from django.shortcuts import get_object_or_404

from users.models import User

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров"""

    class Meta:
        model = Genre
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""

    class Meta:
        model = Category
        exclude = ('id',)


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор записи произведения"""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    def validate(self, data):
        if not data.get('genre'):
            raise serializers.ValidationError(
                'Необходимо указать жанры'
            )
        if not data.get('category'):
            raise serializers.ValidationError(
                'Необходимо указать категории'
            )
        return data

    class Meta:
        model = Title
        fields = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = '__all__'


class TitleGenreReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()

    class Meta:
        model = TitleGenre
        fields = ('id', 'genre',)


class TitleGenreWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleGenre
        fields = ('id', 'genre', 'title')

    def validate_genre(self, value):
        try:
            genre = Genre.objects.get(id=value['id'])
        except Genre.DoesNotExist:
            raise serializers.ValidationError(
                "Недопустимый идентификатор жанра"
            )
        return genre

    def create(self, validated_data):
        genre_data = validated_data.pop('genre')
        genre = Genre.objects.get(id=genre_data['id'])
        title_genre = TitleGenre.objects.create(genre=genre, **validated_data)
        return title_genre

    def update(self, instance, validated_data):
        genre_data = validated_data.pop('genre')
        instance.genre = Genre.objects.get(id=genre_data['id'])
        instance.save()
        return instance


class ReviewsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['title', 'author'],
                message='Повторный отзыв запрешен',
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author', 'pub_date')


class UserSerializer(serializers.ModelSerializer):
    """Serializer модели User."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer создания нового пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                "Использовать имя 'me' в качестве username запрещено!"
            )
        return data


class CreateTokenSerializer(serializers.ModelSerializer):
    """Serializer создания JWT-токена для пользователей."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)