import os

from django import template

register = template.Library()


@register.filter(name='basename')
@stringfilter
def basename(value):
    return os.path.basename(value)
