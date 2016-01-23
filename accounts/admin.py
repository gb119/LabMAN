from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.utils.translation import  ugettext_lazy as _

from accounts.models import Person
from img.admin import ImageInlineAdmin
from files.admin import FileInlineAdmin
from pages.admin import PageInlineAdmin


# Define a new User admin
@register(Person)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (_('Personal info'), {'fields': [('username', 'password'),('first_name', 'last_name', 'email')]}),
        (_('Permissions'), {'classes': ('grp-collapse grp-closed',),
                             'fields': (('is_active', 'is_staff', 'is_superuser'),
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'classes': ('grp-collapse grp-closed',),
                                 'fields': (('last_login', 'date_joined'),)}),
        ('Profile',{'classes': ('grp-collapse grp-closed',),
                    'fields':(("job_title","boss"),("address","phone"),),
                    }),
    )
    inlines=(ImageInlineAdmin,PageInlineAdmin,FileInlineAdmin)

