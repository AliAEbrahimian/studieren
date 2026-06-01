from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """امکان دسترسی به مقدار یک دیکشنری با کلید متغیر در قالب جنگو"""
    if not dictionary:
        return None
    return dictionary.get(key)