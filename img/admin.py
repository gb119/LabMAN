from django.contrib import admin
from django import forms
from models import ImageFile
from django.contrib.contenttypes.admin import GenericStackedInline
import magic
import util


class ImageFileForm(forms.ModelForm):
    class Meta:
        model=ImageFile

        exclude = ("size", "mime_type", )

    def clean(self,*args, **kwargs):
        """Custom validation method to update mime-type and size fields."""
        data=super(ImageFileForm,self).clean(*args, **kwargs)
        try:
            with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as mimemagic:
                mime=mimemagic.id_buffer(data["content"].chunks().next())
            if not mime.startswith("image"):
                raise forms.ValidationError("File had a mime-type of {} - which does not appear to be an image !".format(mime))
            data["mime_type"]=mime
            data["size"]=data["content"].size
        except AttributeError:
            raise forms.ValidationError("Could not determine file's mime type")

    def clean_description(self):
        return util.clean_html(self.cleaned_data['description'])




class ImageInlineAdmin(GenericStackedInline):
    """An inline editor form for Files."""
    model = ImageFile
    exclude=["mime_type","size"]
    readonly_fields = ('image_tag',)
    form = ImageFileForm
    can_delte=False
    verbose_name="Image"
    verbose_name_plural="Images"
    extra=0
    fieldsets=(
        (None,{"fields":(("category","tag","owner"),"description",("content","image_tag"))}),
    )



# Register your models here.
@admin.register(ImageFile)
class ImageFile_Admin(admin.ModelAdmin):

    exclude = ("mime_type","size",)
    list_display = ("category","tag","mime_type",)
    readonly_fields = ('image_tag',)
    form = ImageFileForm
    related_lookup_fields = {
        'fk': ['owner'],
        'generic': [['content_type', 'object_id'], ],
    }
    fieldsets=(
        (None,{"fields":(("category","tag"),"description",("content","image_tag"))}),
        ("Linking",{"fields":("owner",("content_type","object_id"),),'classes': ('grp-collapse grp-closed',)}),

    )
