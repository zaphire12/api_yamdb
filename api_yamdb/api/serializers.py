from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


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

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError('Username не может быть "me".')
        return username


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Пользователь с таким email уже существует'
            )
        ]
    )
    username = serializers.SlugField(
        max_length=150,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Пользователь с таким username уже существует'
            ),
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Имя пользователя может содержать только буквы, цифры и символы: . @ + - _'
            )
        ]
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Использовать имя "me" запрещено')
        return value


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

