# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-03 19:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import lm_utils.models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lm_utils', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.SlugField(default=b'', max_length=20)),
                ('description', tinymce.models.HTMLField(blank=True)),
                ('published', models.DateField(null=True, verbose_name=b'published date')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('mime_type', models.CharField(blank=True, max_length=50)),
                ('size', models.PositiveIntegerField(blank=True)),
                ('content', models.FileField(upload_to=lm_utils.models._custom_upload_to)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lm_utils.CategoryLabels')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='files', to='contenttypes.ContentType')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_files', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
