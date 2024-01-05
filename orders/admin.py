from django.contrib import admin
from .models import *

admin.site.register(PromoCodeModel)


# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItemModel
    autocomplete_fields = ['product']


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['total_cost']
    inlines = [OrderItemInline]
