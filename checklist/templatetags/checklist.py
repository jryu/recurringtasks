import json

from django import template
from django.utils.safestring import mark_safe

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
