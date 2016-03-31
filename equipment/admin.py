from django.contrib import admin
from .models import Equipment,Equipment_Status,UserList,UserList_level
from img.admin import ImageInlineAdmin
from files.admin import FileInlineAdmin
from pages.admin import PageInlineAdmin
from django import forms
import util


class EquipmentAdminForm(forms.ModelForm):
    class Meta:
        model=Equipment
        exclude=()

    def clean_description(self):
        return util.clean_html(self.cleaned_data['description'])

class EquipmentStatusAdminForm(forms.ModelForm):
    class Meta:
        model=Equipment_Status
        exclude=()

    def clean_description(self):
        return util.clean_html(self.cleaned_data['description'])

class UserListInlineAdmin(admin.StackedInline):
    """An inline editor form for Images."""
    model = UserList
    verbose_name="user user"
    verbose_name_plural="users"
    extra=0

class UserListLevelAdminForm(forms.ModelForm):
    class Meta:
        model=UserList_level
        exclude=()

    def clean_description(self):
        return util.clean_html(self.cleaned_data['description'])


# Register your models here.

@admin.register(Equipment_Status)
class Equipment_Status_Admin(admin.ModelAdmin):
    list_display=("name","safe_description",Equipment_Status.cbox)


@admin.register(UserList_level)
class UserList_Level_Admin(admin.ModelAdmin):
    list_display=("name","safe_description","level")


@admin.register(Equipment)
class Equipment_Admin(admin.ModelAdmin):
    list_display=("name","safe_description",Equipment.cbox)
    inlines=[UserListInlineAdmin,ImageInlineAdmin,PageInlineAdmin,FileInlineAdmin]

