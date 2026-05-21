from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Department


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "id",
        "username",
        "email",
        "role",
        "department",
        "is_verified",
        "is_staff",
    )

    list_filter = (
        "role",
        "department",
        "is_verified",
        "is_staff",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "role",
                    "department",
                    "phone_number",
                    "is_verified",
                ),
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "email",
                    "role",
                    "department",
                    "phone_number",
                    "is_verified",
                ),
            },
        ),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")