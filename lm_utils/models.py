from django.db import models
from django.conf import settings
from django.utils.text import capfirst
from django.core.exceptions import NON_FIELD_ERRORS,ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey,ContentType
from django.contrib.contenttypes.fields import GenericRelation
from tinymce.models import HTMLField
from django.utils.html import format_html
import magic
from mimetypes import guess_type
import os.path as path
from random import randint

from .forms import MultiSelectFormField
from util import LabMAN_select_objects

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
        unique_together = (("tag","category","content_type"),) # Only one categrory/tag per ovbject type

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
                                     on_delete=models.SET_NULL,limit_choices_to=LabMAN_select_objects("link"))
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

# New version of this snippet http://djangosnippets.org/snippets/1200/
# tested with Django 1.4

class MultiSelectField(models.Field):
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return "CharField"

    def get_choices_default(self):
        return self.get_choices(include_blank=False)

    def _get_FIELD_display(self, field):
        value = getattr(self, field.attname)
        choicedict = dict(field.choices)

    def formfield(self, **kwargs):
        # don't call super, as that overrides default widget if it has choices
        defaults = {'required': not self.blank, 'label': capfirst(self.verbose_name),
                    'help_text': self.help_text, 'choices': self.choices}
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return MultiSelectFormField(**defaults)

    def get_prep_value(self, value):
        return value

    def get_db_prep_value(self, value, connection=None, prepared=False):
        if isinstance(value, basestring):
            return value
        elif isinstance(value, list):
            return ",".join(value)

    def to_python(self, value):
        if value is not None:
            return value if isinstance(value, list) else value.split(',')
        return ''

    def contribute_to_class(self, cls, name):
        super(MultiSelectField, self).contribute_to_class(cls, name)
        if self.choices:
            func = lambda self, fieldname = name, choicedict = dict(self.choices): ",".join([choicedict.get(value, value) for value in getattr(self, fieldname)])
            setattr(cls, 'get_%s_display' % self.name, func)

    def validate(self, value, model_instance):
        arr_choices = self.get_choices_selected(self.get_choices_default())
        for opt_select in value:
            if (int(opt_select) not in arr_choices):  # the int() here is for comparing with integer choices
                raise ValidationError(self.error_messages['invalid_choice'] % value)
        return

    def get_choices_selected(self, arr_choices=''):
        if not arr_choices:
            return False
        list = []
        for choice_selected in arr_choices:
            list.append(choice_selected[0])
        return list

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class UserList_level(DescribedItem):
    """Represents a possible User level."""

    class Meta:
        verbose_name = "user level label"

    level=models.IntegerField(unique=True, primary_key=True,null=False)


    def __str__(self):
        return self.name

class UserList(models.Model):
    """Handle the linkages between a peice of equipment and a user."""

    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="userOf")
    content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name="%(app_label)s",
                                     on_delete=models.SET_NULL,limit_choices_to=LabMAN_select_objects("users"))
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id",for_concrete_model=True)
    level=models.ForeignKey(UserList_level,on_delete=models.PROTECT,related_name="+")

    def __str__(self):
        return "{} - {} ( {} )".format(self.user.username,self.content_object.name,self.level)

class HasUsers(object):
    """Mixin that adds userlist management functions to a django model."""

    userlist = GenericRelation(UserList,null=True, blank=True, default=None)

    @property
    def users(self):
        """Get a list of User objects from the userlist generic object."""
        return [x.user for x in self.userlist.all()]

    def get_user_level(self,user):
        """Checks whether user is a user of this equipment and if so, returns the user level."""
        if user in self.users:
            entry = self.useflist.get(user=user)
            return entry.level

    def is_user(self,user):
        return user in self.users

    def is_manager(self,user):
        try:
            mgr=UserList_level.objects.get(name="Manager")
        except:
            return False
        return self.get_user_level(user)==mgr
