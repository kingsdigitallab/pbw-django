# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-06-27 11:24


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pbw', '0051_bibliography_unicode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factoid',
            name='boulloterion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='factoids', to='pbw.Boulloterion'),
        ),
    ]
