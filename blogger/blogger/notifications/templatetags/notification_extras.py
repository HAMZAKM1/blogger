# notifications/templatetags/notification_extras.py
from django import template

register = template.Library()

@register.filter
def opacity(is_read):
    return "0.5" if is_read else "1"
