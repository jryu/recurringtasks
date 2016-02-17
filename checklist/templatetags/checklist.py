import json
import string

from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import get_language_from_request

from ..models import Task

register = template.Library()

@register.filter
def interval_label(interval):
    return dict(Task.INTERVAL_CHOICES).get(interval)

@register.filter
def date_json(date):
    if date:
        return mark_safe(json.dumps({
            'year': date.year,
            'month': date.month,
            'day': date.day,
            }))
    else:
        return 'null'

@register.filter
def i18n_user_name(user):
    full_name = user.get_full_name()
    for letter in full_name:
        if letter in string.ascii_letters:
            return full_name

    # Assume that it is a Korean name.
    full_name = '%s%s' % (user.last_name, user.first_name)
    return full_name.strip()
