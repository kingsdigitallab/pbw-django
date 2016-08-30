
from django.core.management.base import BaseCommand, CommandError
from pbw.settings import FIXTURE_PERSON_IDS,BASE_DIR
from pbw.models import Person,Origlangauth,Factoidtype,Factoidpersontype,Sexauth
from django.core import serializers
import os

class Command(BaseCommand):
    help = 'Builds the necessary Fixtures for the unit tests'


    def handle(self, *args, **options):
        format = "json"
        Serializer = serializers.get_serializer(format)
        serializer=Serializer()
        fixture_path=os.path.join(BASE_DIR,'pbw','fixtures')
        auth_fixture=os.path.join(fixture_path,"authorities."+format)
        with open(auth_fixture, "w") as out:
            auths=list(Origlangauth.objects.all())+list(Factoidtype.objects.all())+list(Factoidpersontype.objects.all())+list(Sexauth.objects.all())
            serializer.serialize(auths,indent=2, stream=out)
            print "Serializing Miscellaneus authority lists"
        persons=Person.objects.filter(id__in=FIXTURE_PERSON_IDS)
        for person in persons:
            person.serialize_to_fixture()