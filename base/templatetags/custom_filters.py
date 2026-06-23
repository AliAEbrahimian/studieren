from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """به قالب اجازه می‌دهد با کلید متغیر از دیکشنری مقدار بگیرد"""
    if dictionary is None:
        return None
    return dictionary.get(key)