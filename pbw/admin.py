__author__ = 'elliotthall'
#Basic admin objects to fix typos etc in perons, factoids
#Will be expanded incrementally into a proper dbmi as resource permits

from django.contrib import admin
from models import Person,Factoid,Source,Factoidperson,Boulloterion,Bibliography
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.options import *
from forms import FactoidForm

admin.site.register(Source)
admin.site.register(Boulloterion)
admin.site.register(Bibliography)


class FactoidInline(admin.StackedInline):
    #fk_name = 'factoidKey'
    model = Factoid
    extra = 1






@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'mdbcode','descname')
    search_fields = ['name', 'mdbcode']


@admin.register(Factoid)
class FactoidAdmin(admin.ModelAdmin):
    list_display = ('person','factoidtype','engdesc')
    search_fields = ['engdesc']

@admin.register(Factoidperson)
class FactoidPersonAdmin(admin.ModelAdmin):
    raw_id_fields = ("person","factoid")
    #inlines = [FactoidInline]
