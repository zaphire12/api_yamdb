from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


@admin.register(User)
class LocationAdmin(UserAdmin):
    filter_horizontal = ('user_permissions', 'groups')
    list_filter = ("is_staff", "is_superuser", "is_active")
    description = "Пользователи"
    fieldsets = (
        (None, {"fields": ('username', 'password',)}),
        ("Личная информация", {"fields": ('first_name', 'last_name', 'email', 'bio')}),
        (
            "Разрешения",
            {
                "fields": (
                    'role',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        ("Важные даты", {"fields": ('last_login', 'date_joined')}),
    )
