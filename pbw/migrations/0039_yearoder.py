# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-05-08 12:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbw', '0038_scdate_datetype'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='narrativeunit',
            options={'ordering': ['yearorder']},
        ),
    ]