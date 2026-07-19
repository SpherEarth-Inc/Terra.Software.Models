from django.core.management.base import BaseCommand
from django.db import transaction

from spherearth.account.models import Permission, Role
from spherearth.platforms.models import Platform

PERMISSIONS = [
    ('news.view', 'View news'),
    ('news.create', 'Create news'),
    ('news.update', 'Update news'),
    ('news.delete', 'Delete news'),
    ('media.view', 'View media library'),
    ('media.upload', 'Upload media'),
    ('staff.invite', 'Invite staff to a platform'),
    ('players.view', 'View players'),
    ('players.manage', 'Manage players'),
]

NEWS_EDITOR_PERMS = {
    'news.view',
    'news.create',
    'news.update',
    'media.view',
    'media.upload',
}

PLATFORM_ADMIN_PERMS = {codename for codename, _ in PERMISSIONS}

PLATFORMS = [
    'Website',
    'Soccer Academy',
]


class Command(BaseCommand):
    help = 'Seed default platforms, permissions, and roles for Spherearth.'

    @transaction.atomic
    def handle(self, *args, **options):
        perm_by_name = {}
        for name, description in PERMISSIONS:
            perm, created = Permission.objects.update_or_create(
                name=name,
                defaults={'description': description},
            )
            perm_by_name[name] = perm
            self.stdout.write(
                f'{"Created" if created else "Updated"} permission: {name}'
            )

        for name in PLATFORMS:
            platform, created = Platform.objects.update_or_create(
                name=name,
                defaults={'is_active': True},
            )
            self.stdout.write(
                f'{"Created" if created else "Updated"} platform: {platform.name}'
            )

        news_editor, created = Role.objects.update_or_create(
            name='News Editor',
            defaults={
                'description': 'Can view/create/update news and upload media for a platform.',
            },
        )
        news_editor.permissions.set(
            [perm_by_name[n] for n in NEWS_EDITOR_PERMS]
        )
        self.stdout.write(
            f'{"Created" if created else "Updated"} role: {news_editor.name}'
        )

        platform_admin, created = Role.objects.update_or_create(
            name='Platform Admin',
            defaults={
                'description': 'Full permissions for a single platform, including invites and players.',
            },
        )
        platform_admin.permissions.set(
            [perm_by_name[n] for n in PLATFORM_ADMIN_PERMS]
        )
        self.stdout.write(
            f'{"Created" if created else "Updated"} role: {platform_admin.name}'
        )

        self.stdout.write(self.style.SUCCESS('Spherearth defaults seeded.'))
