# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('description', tinymce.models.HTMLField()),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='department',
            field=models.ForeignKey(related_name='pople', blank=True, to='accounts.Department', null=True),
        ),
    ]
