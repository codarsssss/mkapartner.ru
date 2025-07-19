from django import template
import html
from django.utils.html import strip_tags

register = template.Library()

@register.filter
def unescape(value):
    return html.unescape(value)

@register.filter
def clean_excerpt(value, length=160):
    # Удаляет теги, декодирует сущности, обрезает и убирает начальные пробелы
    plain = strip_tags(value)
    plain = html.unescape(plain)
    plain = plain.lstrip()
    if len(plain) > length:
        return plain[:length].rstrip() + '...'
    return plain
