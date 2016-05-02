import os

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='basename')
@stringfilter
def basename(value):
    return os.path.basename(value)