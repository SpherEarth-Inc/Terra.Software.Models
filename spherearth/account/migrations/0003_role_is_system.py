from django.db import migrations, models


SYSTEM_ROLE_NAMES = ('News Editor', 'Platform Admin')


def mark_system_roles(apps, schema_editor):
    Role = apps.get_model('account', 'Role')
    Role.objects.filter(name__in=SYSTEM_ROLE_NAMES).update(is_system=True)


def unmark_system_roles(apps, schema_editor):
    Role = apps.get_model('account', 'Role')
    Role.objects.filter(name__in=SYSTEM_ROLE_NAMES).update(is_system=False)


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='is_system',
            field=models.BooleanField(
                default=False,
                help_text='Seeded/system roles cannot be deleted.',
            ),
        ),
        migrations.RunPython(mark_system_roles, unmark_system_roles),
    ]
