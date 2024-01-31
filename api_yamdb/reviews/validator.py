from django.forms import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError("Username 'me' is not allowed.")
