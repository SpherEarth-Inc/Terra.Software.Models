"""Abstract CMS bases shared by website and soccer products."""

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class NewsStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PUBLISHED = 'published', 'Published'


class CategoryBase(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class NewsBase(models.Model):
    """Product news article with TipTap JSON content (no platform FK)."""

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    summary = models.TextField(blank=True)
    featured_image = models.URLField(blank=True, null=True, max_length=500)
    content = models.JSONField(
        help_text='TipTap document JSON, e.g. {"type": "doc", "content": [...]}',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_articles',
    )
    status = models.CharField(
        max_length=20,
        choices=NewsStatus.choices,
        default=NewsStatus.DRAFT,
        db_index=True,
    )
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = None

        if not self.slug:
            base_slug = slugify(self.title) or 'news'
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S%f')
            slug = f'{base_slug}-{timestamp}'
            original = slug
            counter = 1
            model = self.__class__
            while model.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{original}-{counter}'
                counter += 1
            self.slug = slug

        if self.status == NewsStatus.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)


class MediaBase(models.Model):
    """Metadata for a file stored in object storage (e.g. MinIO)."""

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
        related_name='%(class)s_uploads',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return self.file_name
