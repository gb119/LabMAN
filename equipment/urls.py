# -*- coding: utf-8 -*-

from django.conf.urls import  url
from django.conf import settings
from equipment.views import EquipmentList

urlpatterns = [
    url(r'^$', EquipmentList.as_view()),
]