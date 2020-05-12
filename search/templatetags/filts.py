from django import template

register = template.Library()

@register.filter
def getvalue(dic, key):
    return dic.get(key)

# 딕셔너리 개체 내용만 반환
@register.filter
def getcontents(dic):
    try:
        lst = []
        for key, value in dic.items():
            if key == 'contentId': break
            lst.append(value)
        string = ''
        for elm in lst:
            string += elm+'. '
    except:
        string = ''

    return string
