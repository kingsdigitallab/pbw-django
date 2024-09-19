import re
from django.conf import settings as settings
from django.db.models import Q
from haystack import indexes
from haystack.fields import FacetMultiValueField
from .models import Person, Factoid, Factoidtype, Location, Ethnicity, \
    Dignityoffice, Languageskill, Occupation, Source, Narrativefactoid, \
    Narrativeunit
import pbw.models as pbw_models
from .settings import DISPLAYED_FACTOID_TYPES
from django.db.models.functions import Length
import pbw.templatetags.pbw_tags as pbw_tags
import pdb


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
        eunuch, created = pbw_models.Sexauth.objects.get_or_create(
            sexvalue="Eunuch")
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


def filter_queryset_by_factoidtype(queryset, typename):
    factoidtype = Factoidtype.objects.filter(typename=typename)
    if factoidtype.count() > 0:
        return queryset.filter(factoidtype=factoidtype[0])
    return queryset


def get_order_field(factoid, typename):
    auth_order = ""
    if typename == "Ethnic label":
        eths = pbw_models.Ethnicityfactoid.objects.filter(factoid=factoid)
        if eths.count() > 0:
            eth = eths[0]
            if eth.ethnicity:
                auth_order = eth.ethnicity.ethname
        # auth_order = 'factoidlocation__location'
    elif typename == "Location":
        # auth_order = 'factoidlocation__location'
        subs = pbw_models.Factoidlocation.objects.filter(factoid=factoid)
        if subs.count() > 0:
            sub = subs[0]
            if sub.location:
                auth_order = sub.location.locname
    elif typename == "Dignity/Office":
        # auth_order = 'dignityfactoid__dignityoffice'
        subs = pbw_models.Dignityfactoid.objects.filter(factoid=factoid)
        if subs.count() > 0:
            sub = subs[0]
            if sub.dignityoffice:
                auth_order = sub.dignityoffice.stdname
    elif typename == "Occupation/Vocation":
        # auth_order = 'occupationfactoid__occupation'
        subs = pbw_models.Occupationfactoid.objects.filter(factoid=factoid)
        if subs.count() > 0:
            sub = subs[0]
            if sub.occupation:
                auth_order = sub.occupation.occupationname
    elif typename == "Language Skill":
        # auth_order = 'langfactoid__languageskill'
        subs = pbw_models.Langfactoid.objects.filter(factoid=factoid)
        if subs.count() > 0:
            sub = subs[0]
            if sub.languageskill:
                auth_order = sub.languageskill.languagename
    elif typename == "Alternative Name":
        # auth_order = 'vnamefactoid__variantname'
        subs = pbw_models.Vnamefactoid.objects.filter(factoid=factoid)
        if subs.count() > 0:
            sub = subs[0]
            if sub.variantname:
                auth_order = sub.variantname.name
    elif typename == "Religion":
        # auth_order = 'religionfactoid__religion'
        subs = pbw_models.Religionfactoid.objects.filter(factoid=factoid)
        if subs.count() > 0:
            sub = subs[0]
            if sub.religion:
                auth_order = sub.religion.religionname
    elif typename == "Possession":
        # auth_order = 'possessionfactoid'
        subs = pbw_models.Possessionfactoid.objects.filter(factoid=factoid)
        if subs.count() > 0:
            sub = subs[0]
            auth_order = sub.possessionname
    elif typename == "Second Name":
        # auth_order = 'famnamefactoid__familyname'
        subs = pbw_models.Famnamefactoid.objects.filter(factoid=factoid)
        if subs.count() > 0:
            sub = subs[0]
            if sub.familyname:
                auth_order = sub.familyname.famname
    elif typename == "Kinship":
        # auth_order = 'kinfactoid__kinship'
        subs = pbw_models.Kinfactoid.objects.filter(factoid=factoid)
        if subs.count() > 0:
            sub = subs[0]
            if sub.kinship:
                auth_order = sub.kinship.gspecrelat
    elif typename == "Narrative":
        auth_order = "9999"
        dates = pbw_models.Scdate.objects.filter(factoid=factoid).order_by(
            'year')
        if dates.count() > 0:
            date = dates[0]
            auth_order = date.year
    else:
        # todo may be scdate
        auth_order = factoid.engdesc
    return auth_order


class FactoidIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    record_type = indexes.FacetCharField()
    person_id = indexes.IntegerField()
    factoid_id = indexes.IntegerField(model_attr='id')
    # this is relative to factoid type
    order_field = indexes.CharField(faceted=True)
    boulloterion_id = indexes.IntegerField()
    sourceid = indexes.CharField()
    sourceref = indexes.CharField(model_attr='sourceref')
    factoidtype_id = indexes.IntegerField()
    typename = indexes.CharField()  # model_attr='factoidtype__typename'
    # Field name made lowercase.
    engdesc = indexes.CharField(model_attr='engdesc')
    authority = indexes.CharField()
    # Field name made lowercase.
    olangkey = indexes.IntegerField(model_attr="olangkey")
    # Field name made lowercase.
    origldesc = indexes.CharField(
        model_attr='origldesc')
    sc_dates = indexes.MultiValueField()
    pleiades = indexes.CharField()
    geonames = indexes.CharField()

    def index_queryset(self, using=None):
        # kept here for testing large records Basilkeos 2
        # queryset = self.get_model().objects.filter(
        #     factoidperson__person__id=106749).filter(
        #     factoidperson__factoidpersontype__fptypename="Primary",
        # ).distinct()
        queryset = self.get_model().objects.filter(factoidperson__person__id__gt=0)
        return queryset

    def get_model(self):
        return Factoid

    def prepare(self, obj):
        self.prepared_data = super(FactoidIndex, self).prepare(obj)
        #print(obj.id)
        if obj.source:
            self.prepared_data['sourceid'] = obj.source.sourceid
        if obj.boulloterion:
            self.prepared_data['boulloterion_id'] = obj.boulloterion.boulloterionkey
        self.prepared_data['sc_dates'] = self.prepare_scdates(obj)
        self.prepared_data['authority'] = pbw_tags.get_authority_list(obj)
        #self.prepared_data['authority_persreflinks'] = pbw_tags.add_persref_links(pbw_tags.get_authority_list(obj))
        self.prepared_data['person_id'] = 0
        self.prepared_data['record_type'] = "factoid"
        if obj.person:
            self.prepared_data['person_id'] = obj.person.id
        else:
            print("No person for factoid {}".format(obj.id))
        self.prepared_data['typename'] = ""
        if obj.factoidtype:
            self.prepared_data['typename'] = obj.factoidtype.typename
            self.prepared_data['factoidtype_id'] = obj.factoidtype.id
            self.prepared_data['order_field'] = get_order_field(
                obj, obj.factoidtype.typename)
        linkdict = pbw_tags.get_linked_location_uris(obj)
        self.prepared_data['pleiades'] = ""
        self.prepared_data['geonames'] = ""
        if 'pleiades' in linkdict:
            self.prepared_data['pleiades'] = linkdict['pleiades']
        if 'geonames' in linkdict:
            self.prepared_data['geonames'] = linkdict['geonames']
        return self.prepared_data

    # def prepare_engdesc_persreflinks(self, obj):
    #     if obj.engdesc:
    #         return pbw_tags.add_persref_links(obj.engdesc)
    #     return ''
    #
    # def prepare_origldesc_persreflinks(self, obj):
    #     if obj.origldesc:
    #         return pbw_tags.add_persref_links(obj.origldesc)
    #     return ''

    def prepare_scdates(self, obj):
        dates = []
        for date in pbw_models.Scdate.objects.filter(factoid=obj):
            dates.append(date.year)
        return dates



# , indexes.Indexable
class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    record_type = indexes.FacetCharField()
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
        self.prepared_data['record_type'] = "person"
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
        # for testing large records: id=106749,
        index_q = self.get_model().objects.annotate(
            name_length=Length('name')).filter(
            mdbcode__gt=0,
            name_length__gt=0,
            factoidperson__factoid__factoidtype__in=factoidtypekeys).order_by(
            'name', 'mdbcode'
        ).distinct()
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
