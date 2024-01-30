from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError


def year_validator(value):
    """
    Валидатор года выхода произведения.
    """
    timezone.activate(settings.TIME_ZONE)
    if value > timezone.now().year:
        raise ValidationError('Год выхода не должен быть больше нынешнего.')
