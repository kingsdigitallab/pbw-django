from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
import pdb

from pbw.models import Scdate, Scsource, Factoid, Datetypes, Narrativefactoid


class Command(BaseCommand):
    help = 'Uses Narrative units to populate empty scdates'

    def handle(self, *args, **options):
        # Get all factoids without scdates
        paginate = 1000
        offset = 10000
        counter = offset
        limit = offset + paginate
        total = Factoid.objects.count()
        nssource = Scsource.objects.get_or_create(ssourceid='Narrative Units', ssourcefullref='')[0]
        while offset < total:
            for nf in Narrativefactoid.objects.filter(narrativeunit__yearorder__gt=0)[offset:limit]:
                try:
                    if not Scdate.objects.filter(factoid=nf.factoid).exists():
                        year = nf.narrativeunit
                        # Set the scdate to that year
                        if year.datetypekey:
                            date_type = Datetypes.objects.get(datetypekey=year.datetypekey)
                        else:
                            date_type = Datetypes.objects.get(datetypekey=2)
                        new_date = Scdate(factoid=nf.factoid, factoidkey=nf.factoid.pk,
                                          notes='Created from narrative dates',
                                          ssourcekey=nssource.ssourcekey,
                                          year=year.yearorder,
                                          yrorder=1,
                                          priority=1,
                                          acckey=1,
                                          datetype=date_type)
                        new_date.save()
                        print("New date for P{}".format(nf.factoid.pk))
                    counter += 1
                except IntegrityError as IE:
                    pdb.set_trace()
                    print ("Integrity Error factoid: {}".format(nf.factoid.pk))

            offset = limit
            limit += paginate

            print ("Processed {}\n".format(counter))
