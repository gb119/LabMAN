from django.db import models
from django.conf import settings
from colorful.fields import RGBColorField
from django.contrib.contenttypes.fields import GenericRelation
from rulez import registry
from django.utils.html import format_html

from accounts.models import Person
from locations.models import Location
from lm_utils.models import DescribedItem,HasUsers

class Equipment_Status(DescribedItem):
    """Represents a possible equipment status."""

    class Meta:
        verbose_name = "equipment status label"

    status=RGBColorField()

    def cbox(self):
        return format_html("<div style='height: 20px; width: 32px; max-width: 32px; background-color:{}'>&nbsp;</div>".format(self.status))

    cbox.short_description="Status"


class Equipment(DescribedItem,HasUsers):
    """Describes an item of equipment."""

    class Meta:
        verbose_name_plural="equipment"


    owner=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="Owned_Equipment")
    status=models.ForeignKey(Equipment_Status)
    location = models.ForeignKey(Location,null=True,blank=True,related_name="equipment")

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
    try:
        from bookings.models import BookingPolicy
        bookings = GenericRelation(BookingPolicy,null=True, blank=True, default=None)
    except ImportError:
        pass

    def cbox(self):
        return self.status.cbox()

    cbox.allow_tags=True
    cbox.short_description="Status"

    def is_owner(self,user):
        return user==self.owner


#Apply permissions
