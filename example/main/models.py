from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from musette.models import AbstractProfile


# For custom User model
"""class User(AbstractUser):

    middle_name = models.CharField(_('Middle Name'), max_length=40, default="")
    is_admin = models.BooleanField(_('Is Admin'), default=False)
    is_deleted = models.BooleanField(_('Is Deleted'), default=False)
    change_password = models.CharField(
        _('Change Password'), max_length=1, null=False,
        blank=False, default='Y'
    )"""


class Profile(AbstractProfile):

    location = models.CharField(
        _("location"), max_length=200, null=True, blank=True
    )
    company = models.CharField(
        _("company"), max_length=150, null=True, blank=True
    )
