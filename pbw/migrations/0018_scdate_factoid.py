# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-23 14:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pbw', '0017_auto_20170123_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='scdate',
            name='factoid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pbw.Factoid'),
        ),
    ]