__author__ = 'elliotthall'
#Basic admin objects to fix typos etc in perons, factoids
#Will be expanded incrementally into a proper dbmi as resource permits

from django.contrib import admin
from models import Person,Factoid,Source,Factoidperson,Boulloterion
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.options import *
from forms import FactoidForm

admin.site.register(Source)
admin.site.register(Boulloterion)

class FactoidInline(admin.StackedInline):
    model = Factoid

class FactoidPersonInline(admin.StackedInline):
    raw_id_fields = ('factoid',)
    model = Person.factoids.through
    extra = 1




@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'mdbcode','descname')


@admin.register(Factoid)
class FactoidAdmin(admin.ModelAdmin):
    list_display = ('person','factoidtype','engdesc')
