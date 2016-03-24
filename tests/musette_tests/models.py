import os

from django.db import models
from django.utils.translation import ugettext_lazy as _

from musette.models import AbstractProfile

class Profile(AbstractProfile):

	location = models.CharField(_("location"), max_length=200, null=True, blank=True)
	company = models.CharField(_("company"), max_length=150, null=True, blank=True)