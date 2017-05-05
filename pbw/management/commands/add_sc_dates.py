from django.core.management.base import BaseCommand, CommandError
from pbw.settings import FIXTURE_PERSON_IDS,BASE_DIR
from pbw.models import Factoid, Scdate,Narrativeunit
from django.core import serializers
import os

class Command(BaseCommand):
    help = 'Uses Narrative units to populate empty scdates'

    def handle(self, *args, **options):
        # Get all factoids without scdates
        factoids = Factoid.objects.filter(scdate__isnull=True)
        for factoid in factoids:
            # Find an attached narrative unit if it exists
            # (split these up because both at once caused performance problems)
            years = Narrativeunit.objects.filter(narrativefactoid_factoid=factoid)

            # Set the scdate to that year
            # Set certainty
            # save
