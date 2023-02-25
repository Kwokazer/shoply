from django import template
from shop.models import *

register = template.Library()


@register.simple_tag()
def join_items(items):
    return ','.join([str(i) for i in items.all()])

