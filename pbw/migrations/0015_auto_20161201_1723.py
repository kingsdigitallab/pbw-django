# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-01 17:23
from __future__ import unicode_literals


from django.db import migrations, models

# Fixes a load of legacy db issues with seal,published, and collection
#Makes the relations proper foreign keys and copies over the values from old to new
class Migration(migrations.Migration):
    dependencies = [
        ('pbw', '0014_auto_20161201_1721'),
    ]

    #Fixes dupe collections caused by no primary key
    def clear_collection_dupes(apps, schema_editor):
            x = 1
            Collection = apps.get_model("pbw", "Collection")
            for x in range(1, 1400, 1):
                colls = Collection.objects.filter(collectionkey=x)
                if colls.count() > 1:
                    for c in colls[1:]:
                        c.delete()

    def copy_published_keys(apps, schema_editor):
            Published = apps.get_model("pbw", "Published")
            #bibliography
            Bibliography = apps.get_model("pbw", "Bibliography")

            #Boulloterion
            Boulloterion = apps.get_model("pbw", "Boulloterion")

            for p in Published.objects.all():
                bibs=Bibliography.objects.filter(bibkey=p.bibkey)
                if bibs.count() > 0:
                    p.bibliography=bibs[0]
                bols=Boulloterion.objects.filter(boulloterionkey=p.boulloterionKey)
                if bols.count() > 0:
                    p.boulloterion=bols[0]
                p.save()


    def copy_seal_keys(apps, schema_editor):
        Boulloterion = apps.get_model("pbw", "Boulloterion")
        Seal = apps.get_model("pbw", "Seal")
        Collection = apps.get_model("pbw", "Collection")
        for s in Seal.objects.all():
            #boulloterion
            bols=Boulloterion.objects.filter(boulloterionkey=s.boulloterionkey)
            if bols.count() > 0:
                s.boulloterion=bols[0]
            #Collection
            cols=Collection.objects.filter(collectionkey=s.collectionKey)
            if cols.count() > 0:
                s.collection=cols[0]
            s.save()



    operations = [
        migrations.AddField(
            model_name='collection',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.RunPython(clear_collection_dupes),
        migrations.RunPython(copy_published_keys),
        migrations.RunPython(copy_seal_keys),
    ]
