from django.db import models

from spherearth.shared.cms.models import CategoryBase, NewsBase, NewsStatus

__all__ = ['WebsiteCategory', 'WebsiteNews', 'NewsStatus']


class WebsiteCategory(CategoryBase):
    class Meta(CategoryBase.Meta):
        db_table = 'WebsiteCategory'
        verbose_name = 'Website Category'
        verbose_name_plural = 'Website Categories'


class WebsiteNews(NewsBase):
    category = models.ForeignKey(
        WebsiteCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='news',
    )

    class Meta(NewsBase.Meta):
        db_table = 'WebsiteNews'
        verbose_name = 'Website News'
        verbose_name_plural = 'Website News'
