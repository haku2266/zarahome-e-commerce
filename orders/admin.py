from django.contrib import admin
from orders.models import *

admin.site.register(PromoCodeModel)


# Register your models here.

@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('price', 'real_price')
