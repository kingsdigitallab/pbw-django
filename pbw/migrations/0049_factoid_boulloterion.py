# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-06-21 10:03


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pbw', '0048_langfactoid_drop_old_primary'),
    ]

    operations = [
        migrations.AddField(
            model_name='factoid',
            name='boulloterion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='factoids', to='pbw.Boulloterion'),
        ),
    ]
