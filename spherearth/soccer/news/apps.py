from django.apps import AppConfig


class SoccerNewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spherearth.soccer.news'
    label = 'soccer_news'
    verbose_name = 'Soccer News'
