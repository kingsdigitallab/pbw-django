# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-23 14:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbw', '0018_scdate_factoid'),
    ]

    def copy_factoidKeys(apps, schema_editor):
        Scdate = apps.get_model("pbw", "Scdate")
        Factoid = apps.get_model("pbw", "Factoid")
        for sc in Scdate.objects.all():
            fs=Factoid.objects.filter(id=sc.factoidkey)
            if fs.count() > 0:
                f=fs[0]
                sc.factoid=f
                sc.save()

    operations = [
        migrations.RunSQL(["update ScDate set factoid_id=factoidKey where factoidKey > 0"]),
        #migrations.RunPython(copy_factoidKeys),
    ]
