"""Integrate DjangoUseEmailAsUsername with admin module."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUserModel, ClientDetails

admin.site.register(ClientDetails)


class BaseUserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ('phone_number',
                                         )}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    list_display = (
        "email", "is_staff",)
    list_display_links = ('email',)
    search_fields = ("email",)
    ordering = ("-date_joined",)


admin.site.register(CustomUserModel, BaseUserAdmin)
