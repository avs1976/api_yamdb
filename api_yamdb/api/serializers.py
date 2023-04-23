from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from users.models import User
from users.validators import username_me


class SignUpSerializer(serializers.Serializer):
    username = serializers.RegexField(max_length=settings.LIMIT_USERNAME,
                                      regex=r'^[\w.@+-]+\Z', required=True)
    email = serializers.EmailField(required=True)

    def validate_username(self, value):
        return username_me(value)


class TokenRegSerializer(serializers.Serializer):
    username = serializers.RegexField(max_length=settings.LIMIT_USERNAME,
                                      regex=r'^[\w.@+-]+\Z', required=True)
    confirmation_code = serializers.CharField(max_length=settings.LIMIT_CHAT,
                                              required=True)

    def validate_username(self, value):
        return username_me(value)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(max_length=settings.LIMIT_USERNAME,
                                      regex=r'^[\w.@+-]+\Z', required=True)

    class Meta:
        abstract = True
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_username(self, value):
        if (
            self.context.get('request').method == 'POST'
            and User.objects.filter(username=value).exists()
        ):
            raise ValidationError(
                'Пользователь с таким именем уже существует.'
            )
        return username_me(value)


class UserEditSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


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
        lookup_field = 'slug'


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


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(default=1)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category',
                  )
        read_only_fields = ('id', 'name', 'year', 'rating',
                            'description', 'genre', 'category',
                            )


class ReviewSerializer(serializers.ModelSerializer):
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
