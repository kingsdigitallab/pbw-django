
from django.core.management.base import BaseCommand, CommandError
from settings import FIXTURE_PERSON_IDS
from pbw.models import Person


class Command(BaseCommand):
    help = 'Builds the necessary Fixtures for the unit tests'



    def handle(self, *args, **options):

        for person in persons: