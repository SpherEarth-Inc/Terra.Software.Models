from django.conf import settings
from django.db import models


class Platform(models.Model):
    """A Spherearth platform/site (e.g. website, soccer-academy). No spaces in name."""

    name = models.CharField(max_length=150, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Platform'
        verbose_name = 'Platform'
        verbose_name_plural = 'Platforms'
        ordering = ['name']

    def __str__(self):
        return self.name


class StaffPlatformMembership(models.Model):
    """Links a staff user to a platform with a role."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='platform_memberships',
    )
    platform = models.ForeignKey(
        Platform,
        on_delete=models.CASCADE,
        related_name='memberships',
    )
    role = models.ForeignKey(
        'account.Role',
        on_delete=models.PROTECT,
        related_name='platform_memberships',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'StaffPlatformMembership'
        verbose_name = 'Staff Platform Membership'
        verbose_name_plural = 'Staff Platform Memberships'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'platform'],
                name='uniq_staff_platform_membership_user_platform',
            ),
        ]
        ordering = ['platform__name', 'user__email']

    def __str__(self):
        return f'{self.user} @ {self.platform} ({self.role})'
