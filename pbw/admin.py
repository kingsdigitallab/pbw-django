__author__ = 'elliotthall'
#Basic admin objects to fix typos etc in perons, factoids
#Will be expanded incrementally into a proper dbmi as resource permits

from django.contrib import admin
from models import Person,Factoid,Source

admin.site.register(Person)
admin.site.register(Factoid)
admin.site.register(Source)
