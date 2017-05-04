from django.contrib import admin
from models import Person, Factoid, Source, Location
from models import Factoidperson, Boulloterion, Bibliography, Factoidtype
from models import Ethnicity, Dignityoffice, Kinshiptype, Languageskill, Occupation
__author__ = 'elliotthall'
# Basic admin objects to fix typos etc in perons, factoids
# Will be expanded incrementally into a proper dbmi as resource permits


admin.site.register(Source)
admin.site.register(Boulloterion)
admin.site.register(Bibliography)
admin.site.register(Ethnicity)
admin.site.register(Dignityoffice)
admin.site.register(Kinshiptype)
admin.site.register(Languageskill)
admin.site.register(Occupation)
admin.site.register(Factoidtype)

class FactoidInline(admin.StackedInline):
    # fk_name = 'factoidKey'
    model = Factoid
    extra = 1

@admin.register(Location)
class LocationAdin(admin.ModelAdmin):
    list_display = ('locname','locnameol','pleiades_id','geonames_id')
    search_fields = ['locname']

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'mdbcode', 'descname')
    search_fields = ['name', 'mdbcode']


@admin.register(Factoid)
class FactoidAdmin(admin.ModelAdmin):
    list_display = ('person', 'factoidtype', 'engdesc')
    search_fields = ['engdesc']


@admin.register(Factoidperson)
class FactoidPersonAdmin(admin.ModelAdmin):
    raw_id_fields = ("person", "factoid")
    # inlines = [FactoidInline]
