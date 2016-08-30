from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if dictionary:
        return dictionary[key]

    return None
