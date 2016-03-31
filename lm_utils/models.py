from django.db import models
from django.conf import settings
from django.core.exceptions import NON_FIELD_ERRORS,ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey,ContentType
from tinymce.models import HTMLField
from django.utils.html import format_html
import magic
from mimetypes import guess_type
import os.path as path
from random import randint


from util import LabMAN_linkable_objects

class DescribedItem(models.Model):

    class Meta:
        abstract = True

    name=models.CharField(max_length=40,blank=True)
    description = HTMLField(default="&nbsp;")

    def __str__(self):
        return self.name

    def safe_description(self):
        return format_html(self.description)
    safe_description.short_description="Description"

class CategoryLabels(DescribedItem):

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Tagged_Object(models.Model):

    class Meta:
        abstract = True

    def validate_unique(self, *args, **kwargs):
        super(Tagged_Object, self).validate_unique(*args, **kwargs)

        qs = self.__class__._default_manager.filter(
            tag__exact=self.tag,
            category__exact=self.category
        )

        if not self._state.adding and self.pk is not None:
            qs = qs.exclude(pk=self.pk)

        if qs.exists():
            raise ValidationError({
                NON_FIELD_ERRORS: ['category and tag not unique',],
            })

    tag =  models.SlugField(max_length=20,default="")
    category = models.ForeignKey(CategoryLabels)
    description = HTMLField(blank=True)
    published = models.DateField(verbose_name="published date",null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='owned_%(app_label)s',null=True,on_delete=models.SET_NULL,blank=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name="%(app_label)s",
                                     on_delete=models.SET_NULL,limit_choices_to=LabMAN_linkable_objects())
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id",for_concrete_model=True)

    def __str__(self):
        return "{}/{}".format(self.category,self.tag)

    def safe_description(self):
        return format_html(self.description)
    safe_description.short_description="Description"


def _custom_upload_to(instance,filename):
    """Provide a means for per app file upload paths"""
    model=instance.__class__.__name__
    app=instance._meta.app_label
    pth="{}/{}/{}".format(app,model,filename)
    while path.exists(pth):
        basename,ext=path.splitext(filename)
        basename+="-{}".format(randint(1,1000000))
        pth="{}/{}/{}{}".format(app,model,basename,ext)
    return pth


class Mime_Typed_Object(Tagged_Object):

    class Meta:
        abstract = True


    mime_type = models.CharField(max_length=50,blank=True)
    size = models.PositiveIntegerField(blank=True)
    content = models.FileField(upload_to=_custom_upload_to)

    def save(self,*args,**kargs):
        """Override save to get size and content-type."""
        self.mime=self.get_mime(self.content)
        self.size=self.content.size
        super(Mime_Typed_Object,self).save(*args,**kargs)

    @classmethod
    def get_mime(cls,content):
        """Get the mime type of the current file as a string.

        if content is None, use self.content as the file."""


        try:
            with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as mimemagic:
                for chunk in content.chunks():
                    mime=mimemagic.id_buffer(chunk)
                    break
        except AttributeError:
            mime=guess_type(content.name)[0]

        return mime

