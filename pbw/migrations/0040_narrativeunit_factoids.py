# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-05-09 11:26


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pbw', '0039_yearoder'),
    ]

    operations = [
        migrations.AddField(
            model_name='narrativeunit',
            name='factoids',
            field=models.ManyToManyField(related_name='narrativeunits', through='pbw.Narrativefactoid', to='pbw.Factoid'),
        ),
    ]
