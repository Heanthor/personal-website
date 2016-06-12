# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-22 22:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('personal_website', '0002_item_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 22, 22, 37, 49, 268407, tzinfo=utc), verbose_name='date added to list'),
        ),
    ]
