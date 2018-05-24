# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-30 16:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pbw', '0019_auto_20170123_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='famnamefactoid',
            name='factoid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Factoid'),
        ),
        migrations.AddField(
            model_name='famnamefactoid',
            name='familyname',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='familyname', to='pbw.Factoid'),
        ),
    ]
