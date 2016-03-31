from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from django.contrib.sites.shortcuts import get_current_site

from lm_utils.models import CategoryLabels,DescribedItem
from img.models import ImageFile
from pages.models import Page
from files.models import UserFile
from locations.models import Location


# Create your models here.

class StatusLabels(DescribedItem):
    
    class Meta:
        verbose_name="status label"
        verbose_name_plural = "status labels"

    @property
    def status(self):
        return self.name

class Department(DescribedItem):
    pass

class JobTitle(DescribedItem):
    
    @property
    def title(self):
        return self.name

class Title(DescribedItem):

    @property
    def title(self):
        return self.name



class Person(AbstractUser):

    USERNAME_FIELD = "username"



    title=models.ForeignKey(Title,null=True,blank=True,related_name="people")
    job_title = models.ForeignKey(JobTitle,null=True,blank=True,related_name="people")
    status = models.ForeignKey(StatusLabels,null=True,blank=True,related_name="pople")
    department = models.ForeignKey(Department,null=True,blank=True,related_name="pople")
    office = models.ForeignKey(Location,null=True,blank=True,related_name="inhabitants")
    address = models.TextField(blank=True,default="")
    phone = PhoneNumberField(blank = True,default="")
    project = models.CharField(max_length=80,default="",blank=True)
    boss = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name="underlings")

    images = GenericRelation(ImageFile,null=True, blank=True, default=None)
    pages = GenericRelation(Page,null=True, blank=True, default=None)
    files = GenericRelation(UserFile,null=True, blank=True, default=None)


    def __repr__(self):
        return "{} {} <{}>".format(self.first_name,self.last_name,self.email)


    @property
    def display_name(self):
        if self.title is not None:
            ret = "{} {} {}".format(self.title,self.first_name,self.last_name)
        else:
            ret = "{} {}".format(self.first_name,self.last_name)
        return ret

    @property
    def profile_image(self):
        try:
            image=self.images.get(content_type__model='person',category__name="profile",object_id=self.id)
        except ObjectDoesNotExist:
            image=ImageFile.objects.get(category__name="profile",tag="default")
        except MultipleObjectsReturned:
            images=self.images.filter(content_type__model='person',category__name="profile",object_id=self.id)[0]           
        return image

    @property
    def profile_page(self):
        try:
            page=self.pages.get(content_type__model='person',category__name="profile",object_id=self.id)
        except ObjectDoesNotExist:
            profile=CategoryLabels.objects.get(name="profile")
            page=Page.objects.create(title=self.display_name,category=profile,tag=self.username,published=date.today(),
                                     owner=self,content_type=Person,content_object=self)
            page.sites.add(get_current_site())
            page.save()
        except MultipleObjectsReturned:
            page=self.pages.filter(content_type__model='person',category__name="profile",object_id=self.id)[0]
        return page
