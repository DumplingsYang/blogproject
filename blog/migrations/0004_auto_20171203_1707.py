# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-03 09:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20171203_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='sluglookup',
            field=models.CharField(blank=True, max_length=15, unique=True),
        ),
    ]