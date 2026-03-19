from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'email_verified')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'email_verified')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('role', 'avatar_url', 'bio', 'email_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('role', 'avatar_url', 'bio', 'email_verified')}),
    )
