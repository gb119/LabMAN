from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import signals

# Create your models here.

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance,boss=instance)


class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, swappable=True, on_delete=models.SET(get_sentinel_user))
    job_title = models.CharField(max_length=100)
    boss = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name="underling")


signals.post_save.connect(create_user_profile, sender=User)

