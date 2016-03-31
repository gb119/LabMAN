from django import template
from django.utils.html import format_html
from img.models import ImageFile


register = template.Library()

@register.simple_tag
def img_tag(image,min_width=200,min_height=200):
    if not isinstance(image,ImageFile):
        return ""
    else:
        return format_html(u'<img src="{}" style="max-width: {}px; max-height: {}px;" />',image.content.url,min_width,min_height)