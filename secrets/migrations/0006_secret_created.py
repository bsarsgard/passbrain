# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-04 03:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('secrets', '0005_auto_20160402_0417'),
    ]

    operations = [
        migrations.AddField(
            model_name='secret',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 4, 4, 3, 14, 53, 778107, tzinfo=utc)),
            preserve_default=False,
        ),
    ]