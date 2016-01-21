from django.shortcuts import get_object_or_404, render
from django.core.servers.basehttp import FileWrapper
from django.http import StreamingHttpResponse
from django.conf import settings
from models import UserFile
import os

# Create your views here.

def stream_file(request,pth):
    """Send the file."""

    tag=os.path.basename(pth)
    category=os.path.dirname(pth)
    obj=get_object_or_404(UserFile,tag=tag,category__name=category)
    real_path=os.path.join(settings.MEDIA_ROOT,obj.content.name)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(real_path), chunk_size),
                           content_type=obj.mime_type)
    response['Content-Length'] = obj.size
    return response
