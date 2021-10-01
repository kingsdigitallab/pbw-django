# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-05 09:23


from django.db import migrations

from django.db import migrations,models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('pbw', '0006_auto_20161005_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='dignityfactoid',
            name='factoid',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Factoid'),
        ),
        migrations.AddField(
            model_name='ethnicityfactoid',
            name='ethnicity',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Ethnicity'),
        ),
        migrations.AddField(
            model_name='ethnicityfactoid',
            name='factoid',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Factoid'),
        ),
        migrations.AddField(
            model_name='factoid',
            name='factoidtype',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Factoidtype'),
        ),
        migrations.AddField(
            model_name='factoid',
            name='source',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Source'),
        ),
        migrations.AddField(
            model_name='factoidlocation',
            name='factoid',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Factoid'),
        ),
        migrations.AddField(
            model_name='factoidlocation',
            name='location',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Location'),
        ),
        migrations.AddField(
            model_name='factoidperson',
            name='factoid',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Factoid'),
        ),
        migrations.AddField(
            model_name='factoidperson',
            name='factoidpersontype',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Factoidpersontype'),
        ),
        migrations.AddField(
            model_name='factoidperson',
            name='person',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Person'),
        ),
        migrations.AddField(
            model_name='kinfactoid',
            name='factoid',
            field=models.ForeignKey( blank=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Factoid'),
        ),
        migrations.AddField(
            model_name='kinfactoid',
            name='kinship',
            field=models.ForeignKey( blank=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Kinshiptype'),
        ),
        migrations.AddField(
            model_name='langfactoid',
            name='factoid',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Factoid'),
        ),
        migrations.AddField(
            model_name='langfactoid',
            name='languageskill',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Languageskill'),
        ),
        migrations.AddField(
            model_name='occupationfactoid',
            name='factoid',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Factoid'),
        ),
        migrations.AddField(
            model_name='occupationfactoid',
            name='occupation',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Occupation'),
        ),
        migrations.AddField(
            model_name='person',
            name='sex',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Sexauth'),
        ),
        migrations.AddField(
            model_name='religionfactoid',
            name='factoid',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Factoid'),
        ),
        migrations.AddField(
            model_name='religionfactoid',
            name='religion',
            field=models.ForeignKey( blank=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Religion'),
        ),
        migrations.AddField(
            model_name='vnamefactoid',
            name='factoid',
            field=models.ForeignKey( blank=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Factoid'),
        ),
        migrations.AddField(
            model_name='vnamefactoid',
            name='variantname',
            field=models.ForeignKey( blank=True, on_delete=django.db.models.deletion.CASCADE, to='pbw.Variantname'),
        ),
    ]
