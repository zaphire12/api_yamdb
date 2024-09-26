from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError('Имя пользователя не может быть me.')
    regex_validator = RegexValidator(
        regex=r'^[\w.@+-]+$',
        message='Имя пользователя содержит недопустимый символ.'
    )
    regex_validator(value)
