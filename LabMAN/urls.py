"""LabMAN URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from filebrowser.sites import site
from django.contrib.flatpages import views as pageviews
from django.contrib.flatpages.models import FlatPage
from accounts.views import ProfileDetailView
import img.views
import files.views
import django.views.i18n
import django.views.static

js_info_dict = {
    'packages': ('django.conf',),
}

urlpatterns = [
   url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^inplaceeditform/', include('inplaceeditform.urls')),
    url(r'^jsi18n$', django.views.i18n.javascript_catalog, js_info_dict),
    url(r'^profile/(?P<slug>[a-z0-9]+)/', ProfileDetailView.as_view()),
    url(r'^account/',include('accounts.urls')),
    url(r'^equipment/',include('equipment.urls')),
    url(r'^image/(.*)',img.views.show_image),
    url(r'^gallery/(.*)',img.views.random_image),
    url(r'^file/(.*)',files.views.stream_file),
    url(r'^media/(?P<path>.*)$',django.views.static.serve,{'document_root': settings.MEDIA_ROOT, }),
    url(r'^pages/', include("django.contrib.flatpages.urls")),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^$', pageviews.flatpage, {'url': '/site/home/'}, name='Home'),

]
# Things here can happen after the admin site is registered fully
admin.site.unregister(FlatPage)