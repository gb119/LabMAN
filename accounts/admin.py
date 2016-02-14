from django.contrib.admin import register,ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.utils.translation import  ugettext_lazy as _

from accounts.models import Person,StatusLabels,JobTitle,Department,Title

from django import forms
import util

from img.admin import ImageInlineAdmin
from files.admin import FileInlineAdmin
from pages.admin import PageInlineAdmin

class StatusLabels_AdminForm(forms.ModelForm):
    class Meta:
        model=StatusLabels
        exclude=()

    def clean_description(self):
        return util.clean_html(self.cleaned_data['description'])

@register(StatusLabels)
class StatusLabels_Admin(ModelAdmin):
    list_display=(["status","description"])

class Department_AdminForm(forms.ModelForm):
    class Meta:
        model=Department
        exclude=()

    def clean_description(self):
        return util.clean_html(self.cleaned_data['description'])

@register(Department)
class Department_Admin(ModelAdmin):
    list_display=(["name","description"])



class JobTitle_AdminForm(forms.ModelForm):
    class Meta:
        model=JobTitle
        exclude=()

    def clean_description(self):
        return util.clean_html(self.cleaned_data['description'])

@register(JobTitle)
class Title_Admin(ModelAdmin):
    list_display=(["title","description"])

class Title_AdminForm(forms.ModelForm):
    class Meta:
        model=Title
        exclude=()

    def clean_description(self):
        return util.clean_html(self.cleaned_data['description'])

@register(Title)
class Title_Admin(ModelAdmin):
    list_display=(["title","description"])



class UserAdminForm(forms.ModelForm):
    class Meta:
            model=Person
            widgets = { 'first_name': forms.TextInput(attrs={'size': 10}),
                       'last_name': forms.TextInput(attrs={'size': 10}),
                       }
            exclude=()

# Define a new User admin
@register(Person)
class UserAdmin(BaseUserAdmin):
    form = UserAdminForm
    fieldsets = (
        (_('Personal info'), {'fields': [('username', 'password'),('title', 'first_name', 'last_name', 'email')]}),
        (_('Permissions'), {'classes': ('grp-collapse grp-closed',),
                             'fields': (('is_active', 'is_staff', 'is_superuser'),
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'classes': ('grp-collapse grp-closed',),
                                 'fields': (('last_login', 'date_joined'),)}),
        ('Profile',{'classes': ('grp-collapse grp-closed',),
                    'fields':(("status","job_title","department","boss",),("address","phone"),"project",),
                    }),
    )
    inlines=(ImageInlineAdmin,PageInlineAdmin,FileInlineAdmin)
    list_display=(["username","display_name","department","status",'is_active', 'is_staff', 'is_superuser'])
    list_filter = ("department","status",'is_active', 'is_staff', 'is_superuser')


