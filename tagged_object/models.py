from django.db import models
from django.conf import settings
from django.core.exceptions import NON_FIELD_ERRORS,ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey,ContentType
from tinymce.models import HTMLField
from django.utils.html import format_html

from util import LabMAN_linkable_objects



class CategoryLabels(models.Model):

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name=models.CharField(max_length=40)
    description = HTMLField()

    def __str__(self):
        return self.name
        
    @property
    def safe_description(self):
        return format_html(self.description)


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

