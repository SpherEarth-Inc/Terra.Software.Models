from django.conf import settings
from django.db import models


class Media(models.Model):
    """Metadata for a file stored in object storage (e.g. MinIO)."""

    platform = models.ForeignKey(
        'platforms.Platform',
        on_delete=models.CASCADE,
        related_name='media',
    )
    file_name = models.CharField(max_length=255)
    object_name = models.CharField(
        max_length=500,
        help_text='Object path in the storage bucket.',
    )
    url = models.URLField(max_length=1000)
    mime_type = models.CharField(max_length=150, blank=True)
    size = models.PositiveBigIntegerField(default=0, help_text='File size in bytes.')
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_media',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Media'
        verbose_name = 'Media'
        verbose_name_plural = 'Media'
        ordering = ['-created_at']

    def __str__(self):
        return self.file_name
