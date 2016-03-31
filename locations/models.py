from django.db import models
from tinymce.models import HTMLField
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.html import format_html
from lm_utils.models import DescribedItem

# Create your models here.

class Location(DescribedItem):
    """Represents a location that can be assigned to people, equuipment etc."""
    
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
