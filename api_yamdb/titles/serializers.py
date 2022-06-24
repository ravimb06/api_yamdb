from rest_framework import serializers

from .models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadOnlySerializer(serializers.ModelSerializer):
    """Сериализатор только для чтения модели Title."""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        read_only_fields = ('__all__',)
        fields = '__all__'


class TitleAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для администратора модели Title."""
    category = serializers.SlugRelatedField(
        quaryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'description', 'genre', 'year', 'category', 'rating'
        )
