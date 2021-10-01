from django.contrib import admin

from .models import Ethnicity, Dignityoffice, Kinshiptype, Languageskill, Occupation
from .models import Factoidperson, Boulloterion, Bibliography, Factoidtype
from .models import Person, Factoid, Source, Location, Seal, Collection, Scdate, Narrativefactoid, Narrativeunit
from django.forms import inlineformset_factory

__author__ = 'elliotthall'
# Basic admin objects to fix typos etc in perons, factoids
# Will be expanded incrementally into a proper dbmi as resource permits


admin.site.register(Source)

admin.site.register(Bibliography)
admin.site.register(Ethnicity)
admin.site.register(Dignityoffice)
admin.site.register(Kinshiptype)
admin.site.register(Languageskill)
admin.site.register(Occupation)
admin.site.register(Factoidtype)
admin.site.register(Scdate)
admin.site.register(Narrativefactoid)


class FactoidInline(admin.StackedInline):
    # fk_name = 'factoidKey'

    model = Factoid
    extra = 1


class FactoidPersonInline(admin.StackedInline):
    verbose_name = 'Factoid-Person'
    verbose_name_plural = 'Factoid-Person links'
    model = Person.factoids.through
    raw_id_fields = ('person', 'factoid')


class ScdateInline(admin.StackedInline):
    model = Scdate
    extra = 1
    show_change_link = True


class NarrativeFactoidInline(admin.StackedInline):
    model = Narrativeunit.factoids.through
    verbose_name = 'Narrative Factoid'
    verbose_name_plural = 'Narrative Factoids'
    raw_id_fields = ("factoid", "narrativeunit")


@admin.register(Location)
class LocationAdin(admin.ModelAdmin):
    list_display = ('locname', 'locnameol', 'pleiades_id', 'geonames_id')
    search_fields = ['locname']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'mdbcode', 'descname')
    search_fields = ['name', 'mdbcode']

    inlines = [
        FactoidPersonInline,
    ]

@admin.register(Boulloterion)
class BoulloterionAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'origltext')
    search_fields = ['title', 'text', 'origltext']


@admin.register(Factoid)
class FactoidAdmin(admin.ModelAdmin):
    list_display = ('id', 'person', 'factoidtype', 'engdesc')
    search_fields = ['engdesc']

    inlines = [
        FactoidPersonInline,
        NarrativeFactoidInline,
        ScdateInline,
    ]


@admin.register(Narrativeunit)
class NarrativeunitAdmin(admin.ModelAdmin):
    model = Narrativeunit
    list_display = ('description', 'summary', 'yearorder',)
    search_fields = ('description', 'summary', 'yearorder',)
    inlines = [
        NarrativeFactoidInline
    ]


@admin.register(Factoidperson)
class FactoidPersonAdmin(admin.ModelAdmin):
    raw_id_fields = ("person", "factoid")
    # inlines = [FactoidInline]


@admin.register(Seal)
class SealAdmin(admin.ModelAdmin):
    list_display = ('boulloterion', 'collection', 'collectionref')
    readonly_fields = ['sealkey', ]
    search_fields = ['boulloterion', 'collection', 'collectionref']

    fields = (
        ('sealkey', 'sealorder'),
        ('boulloterion',),
        ('collection', 'collectionref',),
        ('url','link_name',),
    )


class SealInline(admin.StackedInline):
    model = Seal
    show_change_link = True
    extra = 1
    max_num = 50
    ordering = ('sealorder',)
    formset = inlineformset_factory(
        Collection,
        Seal,
        fields=(
            'sealorder',
            'boulloterion',
            'collection',
            'collectionref',
        ),
        max_num=30)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    search_fields = ['collectionname', 'shortname']
    list_display = ('collectionname', 'shortname')
    inlines = (SealInline,)
