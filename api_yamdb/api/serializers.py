from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Categorie, Genre, Title


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        exclude = ('id',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorieSerializer()
    #rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), many=True, slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Categorie.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Title
        fields = '__all__'

    def to_representation(self, title):
        serializer = TitleGetSerializer(title)
        return serializer.data

