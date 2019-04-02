from django import template
from django.template.defaultfilters import stringfilter

from conf import strings
import datetime

register = template.Library()

ISO8601_FMT = '%Y-%m-%dT%H:%M:%SZ'


@register.simple_tag
def get_string(value):
    return strings.constants.get(value, 'COULDN\'T FIND STRING')


@register.filter
@stringfilter
def str_date(value):
    return datetime.datetime.strptime(value, ISO8601_FMT)
