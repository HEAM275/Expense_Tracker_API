from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from apps.common.models import AuditableMixins
# Create your models here.


class User(AbstractUser, AuditableMixins):

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('User')

    def __str__(self):
        return f' {self.first_name} {self.last_name}'
