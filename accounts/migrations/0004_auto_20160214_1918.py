# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20160214_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=40)),
                ('description', tinymce.models.HTMLField(default=b'', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='title',
            field=models.ForeignKey(related_name='people', blank=True, to='accounts.Title', null=True),
        ),
    ]
