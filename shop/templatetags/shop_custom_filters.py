from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def highlight_search(text, search):
    print(text)
    print(search)

    highlighted = str(text.replace(str(search), '<span class="highlight text-underline">{}</span>'.format(str(search))))
    return mark_safe(highlighted)
