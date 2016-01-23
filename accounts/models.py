from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Person(AbstractUser):

    USERNAME_FIELD = "username"



    job_title = models.CharField(max_length=100,default="")
    address = models.TextField(blank=True,default="")
    phone = PhoneNumberField(blank = True,default="")
    boss = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name="underling")

    def repr(self):
        return "{} {} <{}>".format(self.first_name,self.last_name,self.email)



