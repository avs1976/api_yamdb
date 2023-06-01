"""Валидаторы для username."""

import re

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_username(username):
    if re.compile(settings.PATTERN).fullmatch(username) is None:
        match = re.split(re.compile(settings.PATTERN), username)
        symbol = ''.join(match)
        raise ValidationError(f'Некорректные символы в username: {symbol}')
    if username.lower() == settings.NO_REGISTER_USERNAME:
        raise ValidationError(
            f'Ник {settings.NO_REGISTER_USERNAME} нельзя регистрировать!')
