from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            f'Сейчас {current_year} год. А ваше произведение {value} года.'
        )
