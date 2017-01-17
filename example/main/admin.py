# For custom User model
"""from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _


UserAdmin.list_display = (
    'email', 'first_name', 'last_name', 'is_active', 'date_joined',
    'is_staff', 'middle_name'
)

UserAdmin.fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'middle_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )"""
