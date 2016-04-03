from django.contrib import admin
import nested_admin
from .models import BookingPolicy, BookingRights
from django.contrib.contenttypes.admin import GenericStackedInline


class BookingRightsInlineAdmin(nested_admin.NestedStackedInline):
    """An inline editor form for Images."""
    model = BookingRights
    verbose_name="user right"
    verbose_name_plural="user rights"
    extra=0

class BookingPolicyInlineAdmin(nested_admin.NestedGenericStackedInline):
    """An inline editor form for Images."""
    model = BookingPolicy
    verbose_name="booking policy"
    verbose_name_plural="booking policies"
    extra=0
    max_num=0
    inlines=[BookingRightsInlineAdmin]

