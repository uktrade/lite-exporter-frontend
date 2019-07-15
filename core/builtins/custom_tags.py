from django import template
from django.template.defaultfilters import stringfilter
from django.templatetags.tz import do_timezone

import datetime
import stringcase
from django.utils.safestring import mark_safe

from conf.constants import ISO8601_FMT
from core import strings

register = template.Library()


@register.simple_tag
def get_string(value):
    def get(d, keys):
        if "." in keys:
            key, rest = keys.split(".", 1)
            return get(d[key], rest)
        else:
            return d[keys]

    return get(strings.constants, value)


@register.filter
@stringfilter
def str_date(value):
    return_value = do_timezone(datetime.datetime.strptime(value, ISO8601_FMT), 'Europe/London')
    return return_value.strftime('%-I:%M') + return_value.strftime('%p').lower() + ' ' + return_value.strftime('%d %B %Y')


@register.filter
def sentence_case(value):
    return stringcase.sentencecase(value)


@register.filter
@stringfilter
@mark_safe
def highlight_text(value: str, term: str) -> str:
    if not term.strip():
        return value

    return value.replace(term, f'<span class="lite-filter-highlight">{term}</span>')
