from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField

# Create your models here.

class StatusLabels(models.Model):

    status=models.CharField(max_length=40)
    description = HTMLField(default="",blank=True)

    def __unicode__(self):
        return self.status

class Department(models.Model):

    name=models.CharField(max_length=40)
    description = HTMLField(default="",blank=True)

    def __unicode__(self):
        return self.name


class JobTitle(models.Model):

    title=models.CharField(max_length=40)
    description = HTMLField(default="",blank=True)

    def __unicode__(self):
        return self.title

class Title(models.Model):

    title=models.CharField(max_length=40)
    description = HTMLField(default="",blank=True)

    def __unicode__(self):
        return self.title



class Person(AbstractUser):

    USERNAME_FIELD = "username"



    title=models.ForeignKey(Title,null=True,blank=True,related_name="people")
    job_title = models.ForeignKey(JobTitle,null=True,blank=True,related_name="people")
    status = models.ForeignKey(StatusLabels,null=True,blank=True,related_name="pople")
    department = models.ForeignKey(Department,null=True,blank=True,related_name="pople")
    address = models.TextField(blank=True,default="")
    phone = PhoneNumberField(blank = True,default="")
    project = models.CharField(max_length=80,default="",blank=True)
    boss = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name="underlings")

    try:
        from img.models import ImageFile
        images = GenericRelation(ImageFile,null=True, blank=True, default=None)
    except ImportError:
        pass
    try:
        from pages.models import Page
        pages = GenericRelation(Page,null=True, blank=True, default=None)
    except ImportError:
        pass
    try:
        from files.models import UserFile
        files = GenericRelation(UserFile,null=True, blank=True, default=None)
    except ImportError:
        pass


    def repr(self):
        return "{} {} <{}>".format(self.first_name,self.last_name,self.email)

    @property
    def display_name(self):
        if self.title is not None:
            ret = "{} {} {}".format(self.title,self.first_name,self.last_name)
        else:
            ret = "{} {}".format(self.first_name,self.last_name)
        return ret



