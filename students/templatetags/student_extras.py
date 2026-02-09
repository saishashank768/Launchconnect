from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key=','):
    """
    Returns the string split by key.
    Usage: {{ value|split:"," }}
    """
    if value:
        return [v.strip() for v in value.split(key) if v.strip()]
    return []
