from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *
from .forms import ColorModelAdminForms


@admin.register(ProductVariations)
class ColorModelAdmin(admin.ModelAdmin):
    list_display = ['product', 'color']
    list_display_links = ['product']
    search_fields = ['code']
    autocomplete_fields = ['product']
    form = ColorModelAdminForms

    @staticmethod
    def color(obj):
        free_space = '&nbsp;' * 5
        return mark_safe(f"<div style='background-color:{obj.code}; width:100px;'>{free_space}</div>")


class TypeModelAdmin(admin.TabularInline):
    model = ProductTypeModel
    readonly_fields = ('slug',)


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    inlines = [TypeModelAdmin]


@admin.register(ProductClassModel)
class ProductClassModelAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)


admin.site.register(ProductSizeModel)


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    readonly_fields = ('real_price', 'slug', 'sale')
    search_fields = ('name',)
