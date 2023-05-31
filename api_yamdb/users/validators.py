import re
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
"""Валидаторы для username."""


def validate_username(username):
    if not re.match(r'^[\w.@+-]+\Z', username):
        raise ValidationError(_(f'{username} содержит запрещенные символы!'))
    if username.lower() == settings.NO_REGISTER_USERNAME:
        raise ValidationError(
            f'Ник {settings.NO_REGISTER_USERNAME} нельзя регистрировать!')
