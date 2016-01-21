from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

from user_profile.models import Person

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class PersonInline(admin.StackedInline):
    model = Person
    can_delete = False
    fk_name = 'user'
    verbose_name_plural = 'people'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (PersonInline, )
    fieldsets = (
        (_('Personal info'), {'fields': [('username', 'password'),('first_name', 'last_name', 'email')]}),
        (_('Permissions'), {'classes': ('grp-collapse grp-closed',),
                             'fields': (('is_active', 'is_staff', 'is_superuser'),
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'classes': ('grp-collapse grp-closed',),
                                 'fields': (('last_login', 'date_joined'),)}),
    )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
