from django.contrib import admin
from django.db.models import TextField
from django import forms
from models import Page
from django.contrib.flatpages.models import FlatPage
from django.contrib.contenttypes.admin import GenericStackedInline
from tinymce.widgets import TinyMCE
import util
# Register your models here.

class PageAdminForm(forms.ModelForm):
    """Provide new Admin form for FlatPage"""
    class Meta:
        model=Page
        exclude=("url",)

    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    def get_changeform_initial_data(self,request):
        ret=super(self,PageAdminForm).get_changeform_initial_data(request)
        ret["template"]=ret.pop("template","pages/default.html")
        return ret

    def clean_content(self):
        return util.clean_html(self.cleaned_data["content"])

    def clean(self,*args,**kargs):
        print self.cleaned_data
        tag=self.cleaned_data["tag"].strip("/")
        category=self.cleaned_data["category"].name.strip("/")
        self.cleaned_data["url"]="/".join(["",category,tag,""])
        print self.cleaned_data["url"]
        ret = super(PageAdminForm,self).clean(*args,**kargs)
        print self.errors
        print self.non_field_errors()
        return ret



class PageInlineAdmin(GenericStackedInline):
    """An inline editor form for Images."""
    model = Page
    form = PageAdminForm
    exclude=["url","enable_comments", "require_registration", "template_name","published","sites"]
    can_delte=False
    verbose_name="Page"
    verbose_name_plural="Pages"
    extra=0
    fieldsets=(
        (None, {"fields": (("category","tag","title"),)}),
        (None, {"fields": ("content",)}),
        ("linking",{"fields":("owner",),'classes': ('grp-collapse grp-closed',)}),
    )

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm
    exclude=["url"]
    list_display=("category","tag","title")
    related_lookup_fields = {
        'fk': ['owner'],
        'generic': [['content_type', 'object_id'], ],
    }
    fieldsets=(
        (None, {"fields": (("category","tag","title"),)}),
        (None, {"fields": ("content",)}),
        ("Linking",{"fields":("owner",("content_type","object_id"),),'classes': ('grp-collapse grp-closed',)}),
        ("Advanced",{"fields":("published","sites","template_name"),'classes': ('grp-collapse grp-closed',)})
    )



