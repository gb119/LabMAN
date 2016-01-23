# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorful.fields
from django.conf import settings
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', tinymce.models.HTMLField()),
                ('owner', models.ForeignKey(related_name='Owned_Equipment', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'equipment',
            },
        ),
        migrations.CreateModel(
            name='Equipment_Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('description', tinymce.models.HTMLField()),
                ('status', colorful.fields.RGBColorField()),
            ],
            options={
                'verbose_name': 'equipment status label',
            },
        ),
        migrations.CreateModel(
            name='UserList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('equipment', models.ForeignKey(to='equipment.Equipment')),
            ],
        ),
        migrations.CreateModel(
            name='UserList_level',
            fields=[
                ('name', models.CharField(max_length=40)),
                ('description', tinymce.models.HTMLField()),
                ('level', models.IntegerField(unique=True, serialize=False, primary_key=True)),
            ],
            options={
                'verbose_name': 'user level label',
            },
        ),
        migrations.AddField(
            model_name='userlist',
            name='level',
            field=models.ForeignKey(to='equipment.UserList_level', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='userlist',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='equipment',
            name='status',
            field=models.ForeignKey(to='equipment.Equipment_Status'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='equipment.UserList'),
        ),
    ]
