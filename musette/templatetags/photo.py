# encoding:utf-8
from django import template

from ..utils import get_photo_profile

register = template.Library()


@register.filter
def get_photo(user):
    """
    This tag return the path photo profile
    """
    field_photo = get_photo_profile(user)
    return field_photo
