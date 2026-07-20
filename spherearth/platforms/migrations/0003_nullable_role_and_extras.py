import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_role_is_system'),
        ('platforms', '0002_remove_platform_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffplatformmembership',
            name='role',
            field=models.ForeignKey(
                blank=True,
                help_text='Optional permission bundle. Null means extras-only access.',
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='platform_memberships',
                to='account.role',
            ),
        ),
        migrations.CreateModel(
            name='StaffPlatformPermission',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'membership',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='extra_permissions',
                        to='platforms.staffplatformmembership',
                    ),
                ),
                (
                    'permission',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='staff_platform_grants',
                        to='account.permission',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Staff Platform Permission',
                'verbose_name_plural': 'Staff Platform Permissions',
                'db_table': 'StaffPlatformPermission',
                'ordering': ['permission__name'],
            },
        ),
        migrations.AddConstraint(
            model_name='staffplatformpermission',
            constraint=models.UniqueConstraint(
                fields=('membership', 'permission'),
                name='uniq_staff_platform_permission_membership_permission',
            ),
        ),
    ]
