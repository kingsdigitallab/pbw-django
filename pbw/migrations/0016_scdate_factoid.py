# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-07 11:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pbw', '0015_auto_20161201_1723'),
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
        # migrations.AddField(
        #     model_name='scdate',
        #     name='factoid',
        #     field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pbw.Factoid'),
        # ),
        migrations.RunSQL(["update ScDate set factoid_id=factoidKey where factoidKey > 0"]),
        migrations.RunPython(copy_factoidKeys),
    ]
