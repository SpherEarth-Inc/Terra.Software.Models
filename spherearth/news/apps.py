from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spherearth.news'
    label = 'news'
    verbose_name = 'News'
