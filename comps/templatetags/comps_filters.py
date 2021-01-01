from django import template
from django.template.defaultfilters import stringfilter

from comps.models import Category, Registration
from polls import models

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if key is None:
        return '-'
    return dictionary.get(int(key))


@register.filter
def NoneToDash(item):
    if item is None:
        return '-'
    return item


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


@register.filter
def getCategory(racer, compId):
    categories = Category.objects.all().filter(comp_id=compId)

    if racer and categories:
        for category in categories:
            if category.year_to <= racer.born <= category.year_from and racer.sex == category.sex:
                return category

    return None


@register.filter
def getRegistration(racer, compId):
    return Registration.objects.all().filter(category=getCategory(racer=racer, compId=compId), racer=racer)


@register.filter
def getRacersByCategory(category):
    return Registration.objects.all().filter(category=category.id)


@register.simple_tag
def getPlace(array, ids: str, key: str):
    return array[ids][key]


@register.simple_tag
def setvar(val=None):
    return val
