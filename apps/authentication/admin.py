from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount

class UserAccountAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'email',
                'username',
                'password',
                'verified'
            )
        }),
        ('Personal Info', {
            'fields': (
                'first_name',
                'last_name'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        ('Important Dates', {
            'fields': (
                'last_login',
                'created_at',
                'updated_at'
            )
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')

    list_display = (
        'email',
        'verified',
        'is_staff',
        'is_active'
    )

admin.site.register(UserAccount, UserAccountAdmin)