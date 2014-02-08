from django import template

register = template.Library()


@register.filter(name='zip')
def zip_lists(a, b):
    return zip(a, b)


@register.filter
def get_range(value):
    return range(1, value+1)
