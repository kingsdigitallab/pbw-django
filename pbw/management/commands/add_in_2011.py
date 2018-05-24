import os
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from pbw.models import Person
from pbw.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Adds in 2011 boolean for links to old site'


    def handle(self, *args, **options):
        data_path = os.path.join(BASE_DIR, 'pbw', 'data')
        key_file_path = os.path.join(data_path, "person_keys.sql")
        x = 0
        with open(key_file_path, "r") as key_file:
            keys = key_file.read()
            for key_line in keys.split(",\n"):
                try:
                    key=int(key_line.replace('\n',''))
                    person = Person.objects.get(id=key)
                    person.in_2011 = True
                    x += 1
                    person.save()
                except ValueError:
                    print ("bad key line {}".format(key_line))
                except ObjectDoesNotExist:
                    print ("Person {} not found".format(key_line))
        print ("{} persons found".format(x))