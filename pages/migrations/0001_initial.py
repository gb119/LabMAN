# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('tagged_object', '0001_initial'),
        ('flatpages', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('flatpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='flatpages.FlatPage')),
                ('tag', models.SlugField(default=b'', max_length=20)),
                ('description', tinymce.models.HTMLField(blank=True)),
                ('published', models.DateField(null=True, verbose_name=b'published date')),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('category', models.ForeignKey(to='tagged_object.CategoryLabels')),
                ('content_type', models.ForeignKey(related_name='pages', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='contenttypes.ContentType', null=True)),
                ('owner', models.ForeignKey(related_name='owned_pages', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('flatpages.flatpage', models.Model),
        ),
    ]
