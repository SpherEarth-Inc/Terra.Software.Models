from django.apps import AppConfig


class SharedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spherearth.shared'
    label = 'shared'
    verbose_name = 'Shared'
