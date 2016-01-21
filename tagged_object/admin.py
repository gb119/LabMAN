from django.contrib import admin
from models import CategoryLabels
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
    list_display=(["name","description"])
