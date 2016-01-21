from django.db import models
from django.contrib.flatpages.models import FlatPage
from tagged_object.models import Tagged_Object

# Create your models here.

class Page(Tagged_Object,FlatPage):
    """A Custom flatpage subclass."""

    def save(self,*args,**kargs):
        """Overide the save method to calculate the URL field."""
        tag=self.tag.strip("/")
        category=self.category.strip("/")
        self.url="/".join(["","pages",category,tag,""])
        super(Page,self).save(*args,**kargs)