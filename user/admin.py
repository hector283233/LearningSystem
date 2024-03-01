from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import gettext_lazy as _
from . models import User

class CustomUserChange(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class UserAdmin(AuthUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "user_type")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "user_type"),
            },
        ),
    )
    
    form = CustomUserChange
    list_display = ("username", "email", "first_name", "last_name", "is_staff", 'user_type')
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", 'user_type')
    search_fields = ("username", "first_name", "last_name", "email", 'user_type')


admin.site.register(User, UserAdmin)