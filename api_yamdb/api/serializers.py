from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    # rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), many=True, slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Title
        fields = '__all__'

    def to_representation(self, title):
        serializer = TitleGetSerializer(title)
        return serializer.data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True,
        error_messages={
            'invalid': ('Имя пользователя может содержать '
                        'только буквы, цифры и символы: . @ + - _'),
        }
    )
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть me'
            )
        return username

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        user_with_same_username = (
            User.objects.filter(username=username).first()
        )
        user_with_same_email = (
            User.objects.filter(email=email).first()
        )
        message_error = {}
        if user_with_same_username and user_with_same_username.email != email:
            message_error['username'] = (f'Имя пользователя {username}'
                                         'уже занято другим пользователем.')
        if user_with_same_email and user_with_same_email.username != username:
            message_error['email'] = (
                f'Адрес электронной почты {email}'
                ' уже используется другим пользователем.'
            )
        if len(message_error) > 0:
            raise serializers.ValidationError(message_error)
        return data


class UserTokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('author', 'title', )

#        def create(self, validated_data):
#            user = self.context['request'].user
#            validated_data['author'] = user
#            return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'review_id', )
