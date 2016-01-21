from django.db import models
from tagged_object.models import Tagged_Object
import magic

# Create your models here.

class Mime_Typed_Object(Tagged_Object):

    class Meta:
        abstract = True


    mime_type = models.CharField(max_length=50,blank=True)
    size = models.PositiveIntegerField(blank=True)
    content = models.FileField(upload_to="%(app_label)s/%Y-%m/")

    def save(self,*args,**kargs):
        """Override save to get size and content-type."""
        self.mime_type=magic.from_buffer(self.content.chunks().next(),mime=True)
        self.size=self.content.size
        super(Mime_Typed_Object,self).save(*args,**kargs)
