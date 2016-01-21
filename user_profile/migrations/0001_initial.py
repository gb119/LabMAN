# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import user_profile.models
import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job_title', models.CharField(max_length=100)),
                ('address', models.TextField(null=True, blank=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, blank=True)),
                ('boss', models.ForeignKey(related_name='underling', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.OneToOneField(on_delete=models.SET(user_profile.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
