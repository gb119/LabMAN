from django.db import models
from tagged_object.models import Tagged_Object
import magic
from mimetypes import guess_type

# Create your models here.

class Mime_Typed_Object(Tagged_Object):

    class Meta:
        abstract = True


    mime_type = models.CharField(max_length=50,blank=True)
    size = models.PositiveIntegerField(blank=True)
    content = models.FileField(upload_to="%(app_label)s/%Y-%m/")

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

