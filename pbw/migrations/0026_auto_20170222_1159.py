# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-02-22 11:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbw', '0025_possessionfactoid_factoid'),
    ]

    operations = [
    	migrations.RunSQL(["update PossessionFactoid set factoid_id=factoidKey where factoidKey > 0"]),
    ]
