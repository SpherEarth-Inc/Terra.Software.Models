from django.db import models

from spherearth.shared.cms.models import MediaBase


class WebsiteMedia(MediaBase):
    class Meta(MediaBase.Meta):
        db_table = 'WebsiteMedia'
        verbose_name = 'Website Media'
        verbose_name_plural = 'Website Media'
