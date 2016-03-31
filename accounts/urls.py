# -*- coding: utf-8 -*-

from django.conf.urls import  url
from django.conf import settings
from accounts.views import MyAccountView

urlpatterns = [
    url(r'^myaccount$', MyAccountView.as_view()),

]