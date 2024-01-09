from django.contrib import admin
from django.utils.safestring import mark_safe
from .forms import ColorModelAdminForms
from .models import *

admin.site.register(PromoCodeModel)


# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItemModel
    autocomplete_fields = ['product']
    fields = ('product', 'price', 'quantity', 'code', 'size')
    form = ColorModelAdminForms


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['total_cost']
    inlines = [OrderItemInline]
