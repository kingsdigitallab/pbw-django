# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-06-08 16:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbw', '0047_location_order'),
    ]

    operations = [
        migrations.RunSQL(["ALTER TABLE LangFactoid DROP PRIMARY KEY;"]),
        migrations.RunSQL(["ALTER TABLE ReligionFactoid DROP PRIMARY KEY;"]),
        migrations.RunSQL(["ALTER TABLE PossessionFactoid DROP PRIMARY KEY;"]),
        migrations.RunSQL(["alter table LangFactoid ADD COLUMN id int(11) AUTO_INCREMENT primary key FIRST;"]),
        migrations.RunSQL(["alter table ReligionFactoid ADD COLUMN id int(11) AUTO_INCREMENT primary key FIRST;"]),
        migrations.RunSQL(["alter table PossessionFactoid ADD COLUMN id int(11) AUTO_INCREMENT primary key FIRST;"]),
    ]
