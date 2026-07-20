from django.db import models

from spherearth.shared.cms.models import MediaBase


class SoccerMedia(MediaBase):
    class Meta(MediaBase.Meta):
        db_table = 'SoccerMedia'
        verbose_name = 'Soccer Media'
        verbose_name_plural = 'Soccer Media'
