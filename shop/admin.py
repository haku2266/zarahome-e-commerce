from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from .forms import ColorModelAdminForms

admin.site.register(CategoryModel)
admin.site.register(TypeModel)
admin.site.register(ProductClassModel)
admin.site.register(SizeModel)


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    readonly_fields = ('real_price', 'slug')


@admin.register(CartItemModel)
class CartItemModelAdmin(admin.ModelAdmin):
    readonly_fields = ('price',)


@admin.register(ColorModel)
class ColorModelAdmin(admin.ModelAdmin):
    list_display = ['code', 'color']
    list_display_links = ['code']
    search_fields = ['code']
    form = ColorModelAdminForms

    @staticmethod
    def color(obj):
        free_space = '&nbsp;' * 5
        return mark_safe(f"<div style='background-color:{obj.code}; width:200px;'>{free_space}</div>")

