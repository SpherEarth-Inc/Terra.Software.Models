from django.db import models

from spherearth.shared.cms.models import CategoryBase, NewsBase, NewsStatus

__all__ = ['SoccerCategory', 'SoccerNews', 'NewsStatus']


class SoccerCategory(CategoryBase):
    class Meta(CategoryBase.Meta):
        db_table = 'SoccerCategory'
        verbose_name = 'Soccer Category'
        verbose_name_plural = 'Soccer Categories'


class SoccerNews(NewsBase):
    category = models.ForeignKey(
        SoccerCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='news',
    )

    class Meta(NewsBase.Meta):
        db_table = 'SoccerNews'
        verbose_name = 'Soccer News'
        verbose_name_plural = 'Soccer News'
