from django import template
from django.utils.safestring import mark_safe
from shop.models import ProductVariations
register = template.Library()


@register.filter
def highlight_search(text, search):
    highlighted = str(text.replace(str(search), '<span class="highlight text-underline">{}</span>'.format(str(search))))
    return mark_safe(highlighted)


@register.filter
def focus_variations(var_id):
    return ProductVariations.objects.get(id=int(var_id))
