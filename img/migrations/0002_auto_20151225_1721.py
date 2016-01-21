# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('img', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagefile',
            name='owner',
            field=models.ForeignKey(related_name='owned_img', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
