# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-05-05 16:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pbw', '0035_populate_narrative_factoid'),
    ]

    operations = [
        migrations.AddField(
            model_name='narrativeunit',
            name='yearorder',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
