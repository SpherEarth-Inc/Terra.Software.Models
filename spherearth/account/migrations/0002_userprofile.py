# Generated manually for UserProfile

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def backfill_profiles(apps, schema_editor):
    User = apps.get_model('account', 'User')
    UserProfile = apps.get_model('account', 'UserProfile')
    for user in User.objects.all():
        UserProfile.objects.get_or_create(user_id=user.id)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=40)),
                ('job_title', models.CharField(blank=True, max_length=150)),
                ('photo_url', models.URLField(blank=True, max_length=1000, null=True)),
                ('photo_object_name', models.CharField(blank=True, max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
                'db_table': 'UserProfile',
            },
        ),
        migrations.RunPython(backfill_profiles, noop_reverse),
    ]
