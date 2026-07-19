"""Shared domain / API exceptions for Spherearth models consumers."""


class SpherearthError(Exception):
    """Base exception for Spherearth shared models."""


class ValidationError(SpherearthError):
    """Raised when domain validation fails outside of Django forms/serializers."""
