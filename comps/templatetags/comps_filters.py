from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if key is None:
        return '-'
    return dictionary.get(int(key))


@register.filter
def get_item_string_key(dictionary, key):
    if key is None:
        return '-'
    return dictionary.get(key)


@register.filter
@stringfilter
def boolToWord(string):
    if string == '1':
        result = 'ANO'
    else:
        result = 'NE'
    return result
