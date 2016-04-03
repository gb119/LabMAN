from django.contrib import admin
from .models import CategoryLabels,UserList,UserList_level
from django.contrib.contenttypes.admin import GenericStackedInline
from django import forms
import util

class CategoryLabels_AdminForm(forms.ModelForm):
    class Meta:
        model=CategoryLabels
        exclude=()

    def clean_description(self):
        return util.clean_html(self.cleaned_data['description'])

@admin.register(CategoryLabels)
class CategoryLabels_Admin(admin.ModelAdmin):
    list_display=(["name","safe_description"])

class UserListInlineAdmin(GenericStackedInline):
    """An inline editor form for Images."""
    model = UserList
    verbose_name="User"
    verbose_name_plural="Users"
    extra=0

class UserListLevelAdminForm(forms.ModelForm):
    class Meta:
        model=UserList_level
        exclude=()

    def clean_description(self):
        return util.clean_html(self.cleaned_data['description'])

@admin.register(UserList_level)
class UserList_Level_Admin(admin.ModelAdmin):
    list_display=("name","safe_description","level")

