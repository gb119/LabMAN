# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20160214_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='project',
            field=models.CharField(default=b'', max_length=80, blank=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='description',
            field=tinymce.models.HTMLField(default=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='jobtitle',
            name='description',
            field=tinymce.models.HTMLField(default=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='statuslabels',
            name='description',
            field=tinymce.models.HTMLField(default=b'', blank=True),
        ),
    ]
