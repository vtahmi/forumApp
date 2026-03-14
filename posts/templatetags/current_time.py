from datetime import datetime

from django import template


register = template.Library()
@register.simple_tag
def current_time():
    """Return the current time."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')