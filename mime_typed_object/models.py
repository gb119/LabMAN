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
        with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as mimemagic:
            self.mime_type = mimemagic.id_buffer(self.content.chunks().next())
        self.size=self.content.size
        super(Mime_Typed_Object,self).save(*args,**kargs)
