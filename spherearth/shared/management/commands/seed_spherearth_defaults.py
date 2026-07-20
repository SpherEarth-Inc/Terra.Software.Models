from django.core.management.base import BaseCommand
from django.db import transaction

from spherearth.account.models import Permission, Role

PERMISSIONS = [
    ('website.news.view', 'View website news'),
    ('website.news.create', 'Create website news'),
    ('website.news.update', 'Update website news'),
    ('website.news.delete', 'Delete website news'),
    ('website.media.view', 'View website media library'),
    ('website.media.upload', 'Upload website media'),
    ('soccer.news.view', 'View soccer news'),
    ('soccer.news.create', 'Create soccer news'),
    ('soccer.news.update', 'Update soccer news'),
    ('soccer.news.delete', 'Delete soccer news'),
    ('soccer.media.view', 'View soccer media library'),
    ('soccer.media.upload', 'Upload soccer media'),
    ('staff.view', 'View staff / employees'),
    ('staff.invite', 'Invite staff'),
    ('soccer.players.view', 'View soccer players'),
    ('soccer.players.manage', 'Manage soccer players'),
]

WEBSITE_NEWS_EDITOR_PERMS = {
    'website.news.view',
    'website.news.create',
    'website.news.update',
    'website.media.view',
    'website.media.upload',
}

SOCCER_NEWS_EDITOR_PERMS = {
    'soccer.news.view',
    'soccer.news.create',
    'soccer.news.update',
    'soccer.media.view',
    'soccer.media.upload',
}

SOCCER_ADMIN_PERMS = {
    codename for codename, _ in PERMISSIONS if codename.startswith('soccer.')
} | {'staff.view'}

# Legacy role names to remove after product split
LEGACY_ROLE_NAMES = ('News Editor', 'Platform Admin')


class Command(BaseCommand):
    help = 'Seed default website/soccer permissions and roles for Spherearth.'

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

        # Drop obsolete platform-era permission codenames
        obsolete = Permission.objects.exclude(
            name__in=[n for n, _ in PERMISSIONS]
        )
        for perm in obsolete:
            self.stdout.write(f'Removing obsolete permission: {perm.name}')
            perm.delete()

        for legacy in LEGACY_ROLE_NAMES:
            deleted, _ = Role.objects.filter(name=legacy).delete()
            if deleted:
                self.stdout.write(f'Removed legacy role: {legacy}')

        website_editor, created = Role.objects.update_or_create(
            name='Website News Editor',
            defaults={
                'description': 'Can view/create/update website news and upload website media.',
                'is_system': True,
            },
        )
        website_editor.permissions.set(
            [perm_by_name[n] for n in WEBSITE_NEWS_EDITOR_PERMS]
        )
        self.stdout.write(
            f'{"Created" if created else "Updated"} role: {website_editor.name}'
        )

        soccer_editor, created = Role.objects.update_or_create(
            name='Soccer News Editor',
            defaults={
                'description': 'Can view/create/update soccer news and upload soccer media.',
                'is_system': True,
            },
        )
        soccer_editor.permissions.set(
            [perm_by_name[n] for n in SOCCER_NEWS_EDITOR_PERMS]
        )
        self.stdout.write(
            f'{"Created" if created else "Updated"} role: {soccer_editor.name}'
        )

        soccer_admin, created = Role.objects.update_or_create(
            name='Soccer Admin',
            defaults={
                'description': 'Full soccer product permissions, including players and staff view.',
                'is_system': True,
            },
        )
        soccer_admin.permissions.set(
            [perm_by_name[n] for n in SOCCER_ADMIN_PERMS]
        )
        self.stdout.write(
            f'{"Created" if created else "Updated"} role: {soccer_admin.name}'
        )

        self.stdout.write(self.style.SUCCESS('Spherearth defaults seeded.'))
