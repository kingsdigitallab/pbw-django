# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-06-21 10:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbw', '0049_factoid_boulloterion'),
    ]

    operations = [
        migrations.RunSQL(["update Factoid set boulloterion_id=boulloterionKey where boulloterionKey > 0"])
    ]