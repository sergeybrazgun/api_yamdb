import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError('Недопустимое имя пользователя.')
    if not re.match(r'^[\w.@+-]+$', value):
        raise ValidationError('Некорректные символы.')
    return value
