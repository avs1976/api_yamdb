"""Валидаторы для username."""
import re

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_username(username):
    pattern = re.compile(r'^[\w.@+-]+')
    if not re.match(pattern, username):
        raise ValidationError(f'{username} содержит запрещенные символы!')
    if username.lower() == settings.NO_REGISTER_USERNAME:
        raise ValidationError(
            f'Ник {settings.NO_REGISTER_USERNAME} нельзя регистрировать!')
