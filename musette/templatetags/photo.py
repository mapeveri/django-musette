# encoding:utf-8
from django import template
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import get_object_or_404

from ..utils import get_id_profile, get_photo_profile

register = template.Library()


@register.filter
def get_photo(user):
	'''
	This tag return the path photo profile
	'''
	pr = get_id_profile(user)
	field_photo = get_photo_profile(pr)

	if not field_photo:
		field_photo = static("img/profile.png")
	else:
		field_photo = settings.MEDIA_URL + str(field_photo)

	return field_photo
