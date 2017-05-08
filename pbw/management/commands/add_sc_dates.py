from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from pbw.models import Scdate, Scsource, Datetypes, Narrativefactoid


class Command(BaseCommand):
    help = 'Uses Narrative units to populate empty scdates'

    def handle(self, *args, **options):
        # Get all factoids without scdates
        paginate = 100
        limit = paginate
        counter = 0
        offset = 0
        total = 10000  # Factoid.objects.count()
        nssource = Scsource.objects.get_or_create(ssourceid='Narrative Units',ssourcefullref='')
        while offset < total:
            for nf in Narrativefactoid.objects.filter(narrativeunit__yearorder__gt=0)[offset:limit]:
                try:
                    if not Scdate.objects.filter(factoid=nf.factoid).exists():
                        # Find an attached narrative unit if it exists
                        # (split these up because both at once caused performance problems)
                        # years = Narrativeunit.objects.filter(narrativefactoid__factoid=nf.factoid, yearorder__gt=0)
                        # if years.count() > 1:
                        #     print ("Multiple units for factoid {}\n".format(nf.factoid.pk))
                        #     for year in years:
                        #         print ("{}: {}\n\n".format(year.pk, year.yearorder))
                        # elif years.count() > 0:
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
                                          datetype=date_type)
                        new_date.save()
                        print("New date for P{}".format(nf.factoid.pk))
                    counter += 1
                except IntegrityError as IE:
                    import pdb; pdb.set_trace()
                    print "Integrity Error factoid: {}".format(nf.factoid.pk)

            offset = limit
            limit += paginate

            print "Processed {}\n".format(counter)



            # Set certainty
            # save
