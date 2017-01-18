Custom User model
-----------------

1) Use AbstractUser model, Because there are user model fields that are used and the model contains 
those fields. Example::

    from django.db import models
    from django.contrib.auth.models import AbstractUser
    from django.utils.translation import ugettext_lazy as _

    # Your custom model
    class User(AbstractUser):

        middle_name = models.CharField(_('Middle Name'), max_length=40, default="")
        is_admin = models.BooleanField(_('Is Admin'), default=False)
        is_deleted = models.BooleanField(_('Is Deleted'), default=False)
        change_password = models.CharField(
            _('Change Password'), max_length=1, null=False,
            blank=False, default='Y'
        )

2. In admin.py, custom your model User (fieldsets)::

    from django.contrib.auth.admin import UserAdmin
    from django.utils.translation import ugettext_lazy as _

    UserAdmin.list_display = (
        'email', 'first_name', 'last_name', 'is_active', 'date_joined',
        'is_staff', 'middle_name'
    )

    # Override fiels in form
    UserAdmin.fieldsets = (
            (None, {'fields': ('username', 'password')}),
            (_('Personal info'), {
                'fields': ('first_name', 'last_name', 'middle_name', 'email')}),
            (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                        'groups', 'user_permissions')}),
            (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        )

3. In settings.py add::

    AUTH_USER_MODEL = 'yourapp.User'

