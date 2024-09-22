from django.utils import timezone

from django.forms import ValidationError


def validate_year_release(value):
    """Год выпуска не может быть больше текущего."""
    if value > timezone.now().year:
        raise ValidationError(
            ('Год выпуска не может быть больше текущего'),
            params={'value': value},
        )
