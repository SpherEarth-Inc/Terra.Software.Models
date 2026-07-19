"""Shared field validators."""
import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

SLUG_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


def validate_slug_format(value: str) -> None:
    if not value or not SLUG_RE.match(value):
        raise ValidationError(
            _('Enter a valid slug (lowercase letters, numbers, and hyphens).'),
            code='invalid_slug',
        )
