from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from users.models import User
from users.validators import ValidateUsername

from api_yamdb.settings import EMAIL, USERNAME_NAME


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

    def validate_slug(self, value):
        if Genre.objects.filter(slug=value).exists():
            raise serializers.ValidationError("Slug already exists")
        return value


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""

    class Meta:
        model = Category
        fields = ('name', 'slug')
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

    class Meta:
        model = Title
        fields = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

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
        if not value:
            return value
        try:
            genre = Genre.objects.get(slug=value['slug'])
        except Genre.DoesNotExist:
            raise serializers.ValidationError("Invalid genre slug")
        return genre

    def create(self, validated_data):
        genre_data = validated_data.pop('genre')
        genre = Genre.objects.create(**genre_data)
        title_genre = TitleGenre.objects.create(genre=genre, **validated_data)
        return title_genre

    def update(self, instance, validated_data):
        genre_data = validated_data.pop('genre')
        instance.genre = Genre.objects.get(slug=genre_data['slug'])
        instance.save()
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    title = SlugRelatedField(slug_field='id', read_only=True)

    def create(self, validated_data):
        if Review.objects.filter(
                author=self.context['request'].user,
                title=validated_data.get('title')).exists():
            raise serializers.ValidationError('Повторный отзыв запрещен.')
        return Review.objects.create(
            **validated_data,
        )

    class Meta:
        model = Review
        fields = ('id', 'text', 'title', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    review = serializers.SlugRelatedField(slug_field='id', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'review', 'author', 'pub_date')
