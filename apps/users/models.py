from datetime import datetime

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.utils.translation import gettext_lazy as _

from apps.utils.models import DeletedMixin
from apps.users.managers import UserManager
from apps.utils.enums import RoleType


class User(AbstractBaseUser, DeletedMixin, PermissionsMixin):
    is_crm_user = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    username = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = 'username'
    objects = UserManager()

    def __str__(self):
        return self.username if self.username else self.pk


class CRMUser(DeletedMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='crm_user')
    name = models.CharField(max_length=64, null=True)
    role = models.CharField(choices=RoleType.choices, blank=True, null=True, max_length=255)

    ADMIN = 'admin'
    MANAGER = 'manager'

    class Meta:
        db_table = 'workers'


class MobileUser(DeletedMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mobile_user')
    phone = models.CharField(max_length=25, blank=True)
    first_name = models.CharField(max_length=25, default='')
    last_name = models.CharField(max_length=25, default='')
    birth_date = models.DateField(default=datetime.now)
