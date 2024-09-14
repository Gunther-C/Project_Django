from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'date', 'is_superuser', 'is_active',)
    list_filter = ('date', 'is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_superuser', 'is_staff', 'is_active')
        }),
    )
    search_fields = ('email',)
    ordering = ('date',)


admin.site.register(User, CustomUserAdmin)
