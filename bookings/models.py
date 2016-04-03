from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey,ContentType
from tinymce.models import HTMLField
from django.conf import settings

from schedule.models.calendars import Calendar
from lm_utils.models import MultiSelectField
from util import LabMAN_select_objects
from lm_utils.models import UserList_level

WEEKDAYS=[(0,"Monday"),(1,"Tuesday"),(2,"Wednesday"),(3,"Thursday"),(4,"Friday"),(5,"Saturday"),(7,"Sunday")]


class BookingPolicy(Calendar):
    """A sub class of Calendar that provides the extra logic about making bookings.
    Also incorporates the logic of CalendarRelation but enforces a 1-1 linking."""

    class Meta:
        unique_together=(("content_type","object_id"),)

    content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name="%(app_label)s",
                                     on_delete=models.SET_NULL,limit_choices_to=LabMAN_select_objects("book"))
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id",for_concrete_model=True)

    instructions = HTMLField(blank=True,null=True)

    def get_effective_rights(self,user):
        """Returns the correct rights object for this user under this policy.

        The effective rights are the rights with the maximum level smaller than or equal to this users level."""

        level=BookingRights(policy=self,can_book=False,can_edit=False,can_edit_other=False,limit=0,immutable=0)
        try:
            if user in self.content_object.users:
                actual_level=self.content_object.get_user_level(user)
                for level in self.rights:
                    if level.user_level.level<=actual_level.level:
                        break
        except AttributeError:
            pass
        return level



class BookingRights(models.Model):
    """Represetns a User class rights limit."""

    class Meta:
        ordering = ["-user_level__level"]

    policy = models.ForeignKey(BookingPolicy,on_delete=models.CASCADE,related_name="rights")
    user_level=models.ForeignKey(UserList_level,on_delete=models.CASCADE,related_name="+",null=True)
    bookable_days=MultiSelectField(choices=WEEKDAYS,blank=True,null=True,max_length=13)
    limit = models.DurationField(blank=True,null=True)
    immutable = models.DurationField(blank=True,null=True)
    can_book = models.BooleanField(default=True)
    can_edit = models.BooleanField(default=True)
    can_edith_other = models.BooleanField(default=False)
    comment = models.CharField(max_length=80,blank=True,default="")

    def __str__(self):
        return "{} : {}".format(self.user_level.name,self.comment)





