# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-30 17:10


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pbw', '0021_auto_20170130_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='kinshiptype',
            name='kinorder',
            field=models.SmallIntegerField(default=1),
        ),
    ]
