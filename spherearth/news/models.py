from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    platform = models.ForeignKey(
        'platforms.Platform',
        on_delete=models.CASCADE,
        related_name='categories',
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)

    class Meta:
        db_table = 'Category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        constraints = [
            models.UniqueConstraint(
                fields=['platform', 'slug'],
                name='uniq_category_platform_slug',
            ),
        ]
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.platform.name})'


class NewsStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PUBLISHED = 'published', 'Published'


class News(models.Model):
    """Platform news article with TipTap JSON content."""

    platform = models.ForeignKey(
        'platforms.Platform',
        on_delete=models.CASCADE,
        related_name='news',
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
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
        related_name='news_articles',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='news',
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
        db_table = 'News'
        verbose_name = 'News'
        verbose_name_plural = 'News'
        constraints = [
            models.UniqueConstraint(
                fields=['platform', 'slug'],
                name='uniq_news_platform_slug',
            ),
        ]
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
            while (
                News.objects.filter(platform_id=self.platform_id, slug=slug)
                .exclude(pk=self.pk)
                .exists()
            ):
                slug = f'{original}-{counter}'
                counter += 1
            self.slug = slug

        if self.status == NewsStatus.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)
