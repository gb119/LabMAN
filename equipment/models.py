from django.db import models
from django.conf import settings
from colorful.fields import RGBColorField
from django.contrib.contenttypes.fields import GenericRelation
from tinymce.models import HTMLField
from img.models import ImageFile as ImageModel
from rulez import registry

class Equipment_Status(models.Model):
    """Represents a possible equipment status."""

    class Meta:
        verbose_name = "equipment status label"

    name=models.CharField(max_length=40)
    description = HTMLField()
    status=RGBColorField()


    def __unicode__(self):
        return self.name

    def cbox(self):
        return "<div style='height: 20px; width: 32px; max-width: 32px; background-color:{}'>&nbsp;</div>".format(self.status)

    cbox.allow_tags=True
    cbox.short_description="Status"


class Equipment(models.Model):
    """Describes an item of equipment."""

    class Meta:
        verbose_name_plural="equipment"

    name=models.CharField(max_length=50)
    description = HTMLField()
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="Owned_Equipment")
    status=models.ForeignKey(Equipment_Status)
    users=models.ManyToManyField(settings.AUTH_USER_MODEL,through="UserList")
    try:
        from img.models import ImageFile
        images = GenericRelation(ImageFile,null=True, blank=True, default=None)
    except ImportError:
        pass
    try:
        from pages.models import Page
        pages = GenericRelation(Page,null=True, blank=True, default=None)
    except ImportError:
        pass
    try:
        from files.models import UserFile
        files = GenericRelation(UserFile,null=True, blank=True, default=None)
    except ImportError:
        pass



    def __unicode__(self):
        return self.name

    def can_book(self, user_obj):
        """Implements a rule for a  booking permission right"""
        return self.owner==user_obj

    def cbox(self):
        return self.status.cbox()

    cbox.allow_tags=True
    cbox.short_description="Status"

class UserList_level(models.Model):
    """Represents a possible User level."""

    class Meta:
        verbose_name = "user level label"

    name=models.CharField(max_length=40)
    description = HTMLField()
    level=models.IntegerField(unique=True, primary_key=True,null=False)


    def __unicode__(self):
        return self.name


class UserList(models.Model):
    """Handle the linkages between a peice of equipment and a user."""

    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    equipment=models.ForeignKey(Equipment,on_delete=models.CASCADE)
    level=models.ForeignKey(UserList_level,on_delete=models.PROTECT)

    def __unicode__(self):
        return "{} - Level {}".format(self.user,self.level)

#Apply permissions
registry.register('can_book', Equipment,description="Bookings accepted for this user")