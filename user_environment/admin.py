from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import Ticket, Review, Follow

"""
class CustomUserAdmin(UserAdmin):
    model = Ticket
    list_display = ('username', 'email', 'date', 'is_superuser', 'is_active',)
    list_filter = ('date', 'is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_superuser', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('title',)
    ordering = ('date',)
"""


admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(Follow)
