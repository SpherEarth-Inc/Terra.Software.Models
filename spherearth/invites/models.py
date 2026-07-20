import uuid

from django.conf import settings
from django.db import models


class StaffInvite(models.Model):
    """Invite for a staff user with a specific role (product access via role perms)."""

    email = models.EmailField(db_index=True)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    role = models.ForeignKey(
        'account.Role',
        on_delete=models.PROTECT,
        related_name='invites',
    )
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_invites',
    )
    expires_at = models.DateTimeField()
    accepted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'StaffInvite'
        verbose_name = 'Staff Invite'
        verbose_name_plural = 'Staff Invites'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.email} → {self.role}'

    @property
    def is_accepted(self) -> bool:
        return self.accepted_at is not None
