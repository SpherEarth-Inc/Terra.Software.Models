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
    """Links a staff user to a platform with an optional role and/or direct grants."""

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
        null=True,
        blank=True,
        help_text='Optional permission bundle. Null means extras-only access.',
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
        role_label = self.role.name if self.role_id else 'custom'
        return f'{self.user} @ {self.platform} ({role_label})'

    def role_permission_codenames(self) -> list[str]:
        if not self.role_id:
            return []
        return sorted(self.role.permissions.values_list('name', flat=True))

    def extra_permission_codenames(self) -> list[str]:
        return sorted(self.extra_permissions.values_list('permission__name', flat=True))

    def effective_permission_codenames(self) -> list[str]:
        return sorted(set(self.role_permission_codenames()) | set(self.extra_permission_codenames()))


class StaffPlatformPermission(models.Model):
    """Direct permission grant on a platform membership (additive extras beyond role)."""

    membership = models.ForeignKey(
        StaffPlatformMembership,
        on_delete=models.CASCADE,
        related_name='extra_permissions',
    )
    permission = models.ForeignKey(
        'account.Permission',
        on_delete=models.PROTECT,
        related_name='staff_platform_grants',
    )

    class Meta:
        db_table = 'StaffPlatformPermission'
        verbose_name = 'Staff Platform Permission'
        verbose_name_plural = 'Staff Platform Permissions'
        constraints = [
            models.UniqueConstraint(
                fields=['membership', 'permission'],
                name='uniq_staff_platform_permission_membership_permission',
            ),
        ]
        ordering = ['permission__name']

    def __str__(self):
        return f'{self.membership_id}: {self.permission.name}'
