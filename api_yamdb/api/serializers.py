from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from api_yamdb.settings import EMAIL, USERNAME_NAME
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from users.validators import ValidateUsername


class UserSerializer(serializers.ModelSerializer, ValidateUsername):
    """Сериализатор модели User"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        lookup_field = ('username',)


class RegistrationSerializer(serializers.Serializer, ValidateUsername):
    """Сериализатор регистрации User"""

    username = serializers.CharField(required=True, max_length=USERNAME_NAME)
    email = serializers.EmailField(required=True, max_length=EMAIL)


class TokenSerializer(serializers.Serializer, ValidateUsername):
    """Сериализатор токена"""

    username = serializers.CharField(required=True, max_length=USERNAME_NAME)
    confirmation_code = serializers.CharField(required=True)


class UserEditSerializer(UserSerializer):
    """Сериализатор модели User для get и patch"""

    role = serializers.CharField(read_only=True)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров"""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""

    class Meta:
        model = Category
        fields = ('name', 'slug')


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

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'category',
            'genre',
        )


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'category',
            'genre',
        )
        read_only_fields = (
            'id',
            'name',
            'year',
            'description',
            'category',
            'genre',
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    def validate(self, data):

        if (self.context.get('request').method == 'POST'
            and Review.objects.filter(
                author=self.context.get('request').user,
                title=get_object_or_404(Title,
                                        id=self.context.get('view').kwargs.get(
                                            'title_id'))).
           exists()):
            raise serializers.ValidationError('Повторный отзыв запрещен.')
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
