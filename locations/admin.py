from django.contrib import admin
from django import forms

from img.admin import ImageInlineAdmin
from files.admin import FileInlineAdmin
from pages.admin import PageInlineAdmin
from .models import Location
import util
# Register your models here.

class LocationAdminForm(forms.ModelForm):
    class Meta:
        model=Location
        exclude=()

    def clean_description(self):
        return util.clean_html(self.cleaned_data['description'])
        
@admin.register(Location)
class Location_Admin(admin.ModelAdmin):
    list_display=("name","safe_description")
    inlines=[ImageInlineAdmin,PageInlineAdmin,FileInlineAdmin]

