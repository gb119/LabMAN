from django.shortcuts import get_object_or_404, render
from django.core.servers.basehttp import FileWrapper
from django.http import StreamingHttpResponse,HttpResponseNotFound
from django.conf import settings
from models import ImageFile
from random import choice
import os

# Create your views here.

def show_image(request,pth):
    """Send the file."""

    tag=os.path.basename(pth)
    category=os.path.dirname(pth)
    obj=get_object_or_404(ImageFile,tag=tag,category__name=category)
    real_path=os.path.join(settings.MEDIA_ROOT,obj.content.name)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(real_path), chunk_size),
                           content_type=obj.mime_type)
    response['Content-Length'] = obj.size
    return response

def random_image(request,pth):
    """Selects an image of the correct category."""
    objs=ImageFile.objects.all().filter(category__name=pth)
    if len(objs)>0:
        obj=choice(objs)
        real_path=os.path.join(settings.MEDIA_ROOT,obj.content.name)
        chunk_size = 8192
        response = StreamingHttpResponse(FileWrapper(open(real_path), chunk_size),
                               content_type=obj.mime_type)
        response['Content-Length'] = obj.size

    else:
        response=HttpResponseNotFound("""
        <h1>No images found</h1>
        <p>No images of category {} were found in the database.</p>
        """.format(pth))
    return response