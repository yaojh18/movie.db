from django import template
import math, re
register = template.Library()

@register.filter
def get_integral(value):
    return str(value).split('.')[0]

@register.filter
def get_decimal(value):
    return str(value).split('.')[1]

@register.filter
def replace_comma(value):
    if (value is None):
        return ""
    else:
        return re.sub(',', ' / ', value)


@register.filter
def replace_br(value):
    if (value is None):
        return ""
    else:
        return re.sub('<br/>', '\n', value)

@register.filter
def get_first_sentence(value):
    for i in range(len(value)):
        if (value[i] not in ['0','1','2','3','4','5','6','7','8','9','.',' ','“','/','，','。','：','！','.','~','、','?','+','（','）']):
            value = value[i:]
            break
    return re.split('[，。： ！.~、?+/]',value)[0]