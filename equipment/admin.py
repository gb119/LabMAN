from django.contrib import admin
import nested_admin
from .models import Equipment,Equipment_Status
from img.admin import ImageInlineAdmin
from files.admin import FileInlineAdmin
from pages.admin import PageInlineAdmin
from bookings.admin import BookingPolicyInlineAdmin
from lm_utils.admin import UserListInlineAdmin
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

# Register your models here.

@admin.register(Equipment_Status)
class Equipment_Status_Admin(admin.ModelAdmin):
    list_display=("name","safe_description",Equipment_Status.cbox)

@admin.register(Equipment)
class Equipment_Admin(nested_admin.NestedModelAdmin):
    list_display=("name","safe_description",Equipment.cbox)
    inlines=[UserListInlineAdmin,BookingPolicyInlineAdmin,ImageInlineAdmin,PageInlineAdmin,FileInlineAdmin]

