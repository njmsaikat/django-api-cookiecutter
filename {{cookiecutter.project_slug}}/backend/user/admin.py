from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "user_type", "is_staff", "is_active")
    list_filter = ("user_type", "is_staff", "is_active")
    fieldsets = UserAdmin.fieldsets + (("Role", {"fields": ("user_type",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Role", {"fields": ("user_type",)}),)
