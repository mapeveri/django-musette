import os

from django.db import models

from musette.models import AbstractProfile

class Profile(AbstractProfile):

	location = models.CharField(max_length=200, null=True, blank=True)
	company = models.CharField(max_length=150, null=True, blank=True)
