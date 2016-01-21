from mime_typed_object.models import Mime_Typed_Object
from django.utils.safestring import SafeUnicode
# Create your models here.

class ImageFile(Mime_Typed_Object):

    def image_tag(self,min_width=200,min_height=200):
        return u'<img src="{}" style="max-width: {}px; max-height: {}px;" />'.format(self.content.url,min_width,min_height)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __unicode__(self):
        return SafeUnicode("{} : {}".format(self.category.name,self.tag,))
