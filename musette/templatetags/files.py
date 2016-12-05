from django import template
from django.template.defaultfilters import stringfilter

from ..utils import basename

register = template.Library()


@register.filter(name='basename')
@stringfilter
def basename(value):
    return basename(value)