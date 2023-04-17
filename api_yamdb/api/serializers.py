from rest_framework import serializers
from reviews.models import Category, Genre, Review, Title, TitleGenre


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
