# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2019-04-07 15:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0006_auto_20190407_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='page',
            name='url',
            field=models.URLField(),
        ),
    ]