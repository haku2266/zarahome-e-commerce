from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *
from .forms import ColorModelAdminForms


class TypeModelAdmin(admin.TabularInline):
    model = TypeModel
    readonly_fields = ('slug',)


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    inlines = [TypeModelAdmin]


@admin.register(ProductClassModel)
class ProductClassModelAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)


admin.site.register(SizeModel)


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    readonly_fields = ('real_price', 'slug', 'sale')
    search_fields = ('name',)


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
