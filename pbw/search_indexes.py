import re
from django.conf import settings as settings
from django.db.models import Q
from haystack import indexes
from haystack.fields import FacetMultiValueField
from .models import Person, Factoid, Location, Ethnicity, Dignityoffice, Languageskill, Occupation, Source
from pbw.models import Sexauth
from .settings import DISPLAYED_FACTOID_TYPES
from django.db.models.functions import Length


# Break down floruits into separate facets
# obj = person object
def get_floruits(obj):
    floruits = list()
    floruit = obj.floruit
    # Todo break down E/M/L XII
    centuries = ['IX', 'XI', 'XII', 'XIII']
    periods = ['E', 'M', 'L']
    for p in periods:
        for c in centuries:
            if re.search(p + "\s+" + c, floruit) is not None:
                floruits.append(p + " " + c)
    return floruits


# Fold probable eunuchs into main eunuch facet
def get_sex(obj):
    sex = obj.sex
    if sex.sexvalue == "Eunuch (Probable)":
        eunuch, created = Sexauth.objects.get_or_create(sexvalue="Eunuch")
        return eunuch.sexvalue
    else:
        return sex.sexvalue


def get_names(person):
    names = list()
    if person is not None:
        factoids = Factoid.objects.filter(factoidperson__person=person).filter(
            Q(factoidtype__typename="Second Name") | Q(
                factoidtype__typename="Alternative Name"))
        names.append(person.name)
        for f in factoids:
            if len(f.engdesc) > 1:
                names.append(f.engdesc)
    return names


def get_letters(names):
    letters = list("")
    for name in names:
        if len(name) > 0 and name.upper() not in letters:
            letters.append(name[0].upper())
    return letters


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    description = indexes.CharField(model_attr='descname', default='')
    # primary name for sorting
    name_sort = indexes.CharField(model_attr='name', faceted=True)
    name = FacetMultiValueField()
    nameol = indexes.CharField(model_attr='nameol')
    letter = FacetMultiValueField()
    source = FacetMultiValueField()
    factoid_engdescs = indexes.MultiValueField()
    factoid_oldescs = indexes.MultiValueField()
    person = indexes.CharField()
    sex = indexes.FacetCharField()
    person_id = indexes.IntegerField(model_attr='id')
    floruit = FacetMultiValueField()
    mdbcode = indexes.IntegerField(model_attr='mdbcode')
    oLangKey = indexes.IntegerField(model_attr='olangkey')
    tstamp = indexes.DateTimeField(model_attr='tstamp')

    # Factoid Types
    location = FacetMultiValueField()
    ethnicity = FacetMultiValueField()
    dignityoffice = FacetMultiValueField()
    language = FacetMultiValueField()
    occupation = FacetMultiValueField()

    def prepare(self, obj):
        self.prepared_data = super(PersonIndex, self).prepare(obj)
        factoid_engdescs = list()
        factoid_oldescs = list()

        # Get all Factoid types
        factoids = Factoid.objects.filter(
            factoidperson__factoidpersontype__fptypename="Primary",
            factoidperson__person=obj)

        for factoid_descs in factoids.values('engdesc', 'origldesc'):
            # Append their descriptions so that they can be added
            # to the document
            if 'engdesc' in factoid_descs:
                factoid_engdescs.append(factoid_descs['engdesc'])
            if 'origldesc' in factoid_descs:
                factoid_oldescs.append(factoid_descs['origldesc'])

        self.prepared_data['factoid_engdescs'] = factoid_engdescs
        self.prepared_data['factoid_oldescs'] = factoid_oldescs

        return self.prepared_data

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated.
        Filter factoids by type for only those used in browser"""
        # __iregex=r'^.{7,}$'
        factoidtypekeys = DISPLAYED_FACTOID_TYPES

        index_q = self.get_model().objects.annotate(name_length=Length('name')).filter(
            mdbcode__gt=0,
            name_length__gt=0,
            factoidperson__factoid__factoidtype__in=factoidtypekeys).order_by(
            'name', 'mdbcode'
        ).distinct()  # The base class for the the various
        # factoid types
        if settings.PARTIAL_INDEX:
            index_q = index_q.filter(
                id__lt=settings.PARTIAL_INDEX_MAX_ID
            ).order_by('pk')

        return index_q
    def get_model(self):
        return Person

    def prepare_person(self, obj):
        return obj.name + " " + str(obj.mdbcode)

    def prepare_sex(self, obj):
        return get_sex(obj)

    def prepare_floruit(self, obj):
        return get_floruits(obj)

    def prepare_name(self, obj):
        return get_names(obj)

    def prepare_letter(self, obj):
        return get_letters(get_names(obj))

    def prepare_source(self, obj):
        sourcelist = list()
        sources = Source.objects.filter(
            factoid__factoidperson__person=obj,
            factoid__factoidtype__in=DISPLAYED_FACTOID_TYPES).distinct()
        if sources.count() > 0:
            for source in sources:
                if source.sourceid and len(source.sourceid) > 0:
                    sourcelist.append(source.sourceid)
        return list(set(sourcelist))

    def prepare_location(self, obj):
        # Location
        loclist = list()
        locations = Location.objects.filter(
            factoidlocation__factoid__factoidperson__factoidpersontype__fptypename="Primary",
            factoidlocation__factoid__factoidperson__person=obj)
        if locations.count() > 0:
            for location in locations:
                loclist.append(location.locname)
        return list(set(loclist))

    def prepare_ethnicity(self, obj):
        # Ethnicity
        ethlist = list("")
        ethnicities = Ethnicity.objects.filter(
            ethnicityfactoid__factoid__factoidperson__factoidpersontype__fptypename="Primary",
            ethnicityfactoid__factoid__factoidperson__person=obj)
        for eth in ethnicities:
            ethlist.append(eth.ethname)
        return ethlist

    def prepare_dignityoffice(self, obj):
        diglist = list("")
        digs = Dignityoffice.objects.filter(
            dignityfactoid__factoid__factoidperson__factoidpersontype__fptypename="Primary",
            dignityfactoid__factoid__factoidperson__person=obj)
        for d in digs:
            diglist.append(d.stdname)
        return list(set(diglist))

    def prepare_language(self, obj):
        langlist = list("")
        langs = Languageskill.objects.filter(
            langfactoid__factoid__factoidperson__factoidpersontype__fptypename="Primary",
            langfactoid__factoid__factoidperson__person=obj)
        for l in langs:
            langlist.append(l.languagename)
        return langlist

    def prepare_occupation(self, obj):
        occlist = list("")
        occs = Occupation.objects.filter(
            occupationfactoid__factoid__factoidperson__factoidpersontype__fptypename="Primary",
            occupationfactoid__factoid__factoidperson__person=obj)
        for o in occs:
            occlist.append(o.occupationname)

        return occlist
