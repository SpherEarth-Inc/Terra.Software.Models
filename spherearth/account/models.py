from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


class Permission(models.Model):
    """Permission codename (e.g. website.news.update, soccer.media.upload)."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Permission'
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'
        ordering = ['name']

    def __str__(self):
        return self.name


class Role(models.Model):
    """Named set of permissions (e.g. Website News Editor, Soccer Admin)."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_system = models.BooleanField(
        default=False,
        help_text='Seeded/system roles cannot be deleted.',
    )
    permissions = models.ManyToManyField(
        Permission,
        related_name='roles',
        blank=True,
        help_text='Permissions granted by this role.',
    )

    class Meta:
        db_table = 'Roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['name']

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_super_admin', False)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_super_admin'] = True
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into staff APIs.',
    )
    is_active = models.BooleanField(default=True)
    is_super_admin = models.BooleanField(
        default=False,
        help_text='Bypasses permission checks; full access to all products.',
    )
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'User'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    """Staff/user profile details and photo (photo path uses profile id)."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    first_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=40, blank=True)
    job_title = models.CharField(max_length=150, blank=True)
    photo_url = models.URLField(max_length=1000, blank=True, null=True)
    photo_object_name = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'UserProfile'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        name = ' '.join(p for p in (self.first_name, self.last_name) if p).strip()
        return name or str(self.user)

    @property
    def display_name(self):
        name = ' '.join(p for p in (self.first_name, self.last_name) if p).strip()
        return name or self.user.email


class StaffAccess(models.Model):
    """
    Staff access for a user: optional role plus additive extras on the user.
    Product boundaries are encoded in permission names (website.* / soccer.*).
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='staff_access',
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name='staff_accesses',
        null=True,
        blank=True,
        help_text='Optional permission bundle. Null means extras-only access.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'StaffAccess'
        verbose_name = 'Staff Access'
        verbose_name_plural = 'Staff Access'

    def __str__(self):
        role_label = self.role.name if self.role_id else 'custom'
        return f'{self.user} ({role_label})'

    def role_permission_codenames(self) -> list[str]:
        if not self.role_id:
            return []
        return sorted(self.role.permissions.values_list('name', flat=True))

    def extra_permission_codenames(self) -> list[str]:
        return sorted(
            StaffPermission.objects.filter(user_id=self.user_id).values_list(
                'permission__name', flat=True
            )
        )

    def effective_permission_codenames(self) -> list[str]:
        return sorted(
            set(self.role_permission_codenames()) | set(self.extra_permission_codenames())
        )


class StaffPermission(models.Model):
    """Direct permission grant on a staff user (additive extras beyond role)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='staff_permissions',
    )
    permission = models.ForeignKey(
        Permission,
        on_delete=models.PROTECT,
        related_name='staff_grants',
    )

    class Meta:
        db_table = 'StaffPermission'
        verbose_name = 'Staff Permission'
        verbose_name_plural = 'Staff Permissions'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'permission'],
                name='uniq_staff_permission_user_permission',
            ),
        ]
        ordering = ['permission__name']

    def __str__(self):
        return f'{self.user_id}: {self.permission.name}'
