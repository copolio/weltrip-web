from django import template

register = template.Library()

@register.filter
def getvalue(dic, key):
    return dic.get(key)

