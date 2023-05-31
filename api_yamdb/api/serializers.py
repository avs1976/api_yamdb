from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from users.validators import validate_username


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class RegistrationSerializer(serializers.Serializer):
    """Сериализатор регистрации User"""

    username = serializers.CharField(max_length=settings.USERNAME_NAME,
                                     required=True,
                                     validators=[validate_username])
    email = serializers.EmailField(max_length=settings.EMAIL)


class TokenSerializer(serializers.Serializer):
    """Сериализатор токена"""

    username = serializers.CharField(max_length=settings.USERNAME_NAME,
                                     required=True,
                                     validators=[validate_username])
    confirmation_code = serializers.CharField()


class UserEditSerializer(UserSerializer):
    """Сериализатор модели User для get и patch"""

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


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

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if not self.context.get('request').method == 'POST':
            return data
        if Review.objects.filter(
                author=self.context.get('request').user,
                title=get_object_or_404(Title, id=self.context.get('view')
                                        .kwargs.get('title_id'))).exists():
            raise serializers.ValidationError('Повторный отзыв запрещен.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
