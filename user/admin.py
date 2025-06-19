from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import CustomerUser  # <-- richtiger Klassenname

@admin.register(CustomerUser)
class CustomerUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Zusätzliche Daten',
            {
                'fields': ('phone', 'adress'),
            },
        ),
    )
    list_display = ('email', 'is_active', 'is_staff')
