import os

from django.db import models
# from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from musette.models import AbstractProfile


"""
class User(AbstractBaseUser):
zip_code = models.CharField(_("Zip code"), max_length=200, null=True, blank=True)
username = models.CharField(_("Username"), max_length=200, null=True, blank=True)
last_name = models.CharField(_("Last name"), max_length=200, null=True, blank=True)
first_name = models.CharField(_("First name"), max_length=200, null=True, blank=True)
email = models.EmailField(_("Email"), max_length=200, null=True, blank=True)
"""


class Profile(AbstractProfile):

	location = models.CharField(
		_("location"), max_length=200, null=True, blank=True
	)
	company = models.CharField(
		_("company"), max_length=150, null=True, blank=True
	)
