from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from django.db.models import signals
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance,boss=instance)


class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, swappable=True, on_delete=models.SET(get_sentinel_user))
    job_title = models.CharField(max_length=100)
    address = models.TextField(blank=True,null=True)
    phone = PhoneNumberField(blank = True)
    boss = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name="underling")

    def __init__(self,*args,**kargs):
        super(Person,self).__init__(*args,**kargs)
        try:
            from img.models import ImageFile
            get_user_model().images = GenericRelation(ImageFile,null=True, blank=True, default=None)
        except ImportError:
            pass
        try:
            from pages.models import Page
            get_user_model().pages = GenericRelation(Page,null=True, blank=True, default=None)
        except ImportError:
            pass
        try:
            from files.models import UserFile
            get_user_model().files = GenericRelation(UserFile,null=True, blank=True, default=None)
        except ImportError:
            pass

    def repr(self):
        return "{} {}'s profile".format(self.user.first_name,self.user.last_name)

signals.post_save.connect(create_user_profile, sender=User)

