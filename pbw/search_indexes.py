from django.db.models import Q
from haystack import indexes
import re

from pbw.models import Sexauth
from settings import DISPLAYED_FACTOID_TYPES
from models import Person, Factoid, Location, Ethnicity, Dignityoffice, Variantname, Languageskill, Occupation, Source

#Break down floruits into separate facets
#obj = person object
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

#Fold probable eunuchs into main eunuch facet
def get_sex(obj):
    sex = obj.sex
    if sex.sexvalue == "Eunuch (Probable)":
        return Sexauth.objects.get(sexvalue="Eunuch (Probable)")
    else:
        return sex

def get_names(person):
    names = list()
    if person is not None:
        factoids = Factoid.objects.filter(factoidperson__person=person).filter(Q(factoidtype__typename="Second Name")|Q(
                factoidtype__typename="Alternative Name"))        
        names.append(person.name)
        for f in factoids:
           if len(f.engdesc) > 1:
                 names.append(f.engdesc)
    return names

def get_letters(names):
    letters=list("")    
    for name in names:
       if name.upper() not in letters:
          letters.append(name[0].upper())
    return letters

class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    description = indexes.CharField(model_attr='descname', default='')
    name = indexes.FacetMultiValueField()  # indexes.CharField(model_attr='name', faceted=True)
    nameol = indexes.CharField(model_attr='nameol')
    letter = indexes.FacetMultiValueField()
    source = indexes.FacetMultiValueField()
    person = indexes.CharField()
    sex = indexes.FacetCharField()
    person_id = indexes.IntegerField(model_attr='id')
    floruit = indexes.FacetMultiValueField()
    mdbcode = indexes.IntegerField(model_attr='mdbcode')
    oLangKey = indexes.IntegerField(model_attr='olangkey')
    tstamp = indexes.DateTimeField(model_attr='tstamp')

    def get_model(self):
        return Person


    def prepare_person(self, obj):
        return obj.name + " " + str(obj.mdbcode)

    def prepare_sex(self, obj):
        return get_sex(obj)


    def prepare_floruit(self,obj):
        return get_floruits(obj)


    def prepare_name(self, obj):
        return get_names(obj)
        

    def prepare_letter(self, obj):
        return get_letters(get_names(obj))

    def prepare_source(self, obj):
        sources = Source.objects.filter(
            factoid__factoidperson__person=obj,
            factoid__factoidtype__in=DISPLAYED_FACTOID_TYPES).distinct()
        return list(sources)

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated.
        Filter factoids by type for only those used in browser"""
        factoidtypekeys = DISPLAYED_FACTOID_TYPES
        return self.get_model().objects.filter(
            factoidperson__factoid__factoidtype__in=factoidtypekeys).distinct()


# The base class for the the various factoid types
class FactoidIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    description = indexes.CharField(model_attr='engdesc', default='')
    name = indexes.FacetMultiValueField()
    origldesc = indexes.FacetCharField(model_attr='origldesc')
    sex = indexes.FacetCharField()
    floruit = indexes.FacetMultiValueField()
    nameol = indexes.CharField()
    factoidtype = indexes.CharField(model_attr='factoidtype__typename')
    factoidtypekey = indexes.IntegerField(
        model_attr='factoidtype__id', faceted=True)
    person = indexes.CharField()
    person_id = indexes.IntegerField()
    source_id = indexes.IntegerField(model_attr='source__id')
    source = indexes.FacetMultiValueField()
    sourceref = indexes.CharField(model_attr='sourceref')
    # Factoid Types
    location = indexes.FacetCharField()
    ethnicity = indexes.FacetCharField()
    dignityoffice = indexes.FacetCharField()
    language = indexes.FacetCharField()
    secondaryname = indexes.FacetCharField()
    occupation = indexes.FacetCharField()
    letter = indexes.FacetMultiValueField()

    def get_model(self):
        return Factoid

    def prepare_person(self, obj):
        p = obj.person
        if p is not None:
            return p.name + " " + unicode(p.mdbcode)
        else:
            print "ERROR No primary person found for factoid " + str(obj.id)
        return None

    def prepare_source(self, obj):
        # model_attr='source__sourceid'
        return [obj.source.sourceid]

    def prepare_person_id(self, obj):
        p = obj.person
        if p is not None:
            return p.id
        else:
            return 0

    def prepare_sex(self, obj):
        if obj.person != None:
            return get_sex(obj.person)


    def prepare_floruit(self,obj):
        if obj.person != None:
            return get_floruits(obj.person)


    def prepare_nameol(self, obj):
        p = obj.person
        if p is not None:
            return obj.person.nameol
        else:
            return ""

    def prepare_name(self, obj):
        return get_names(obj.person)

    def prepare_letter(self, obj):
        return get_letters(get_names(obj.person))


    def prepare_location(self, obj):
        # Location
        if obj.factoidtype.typename == "Location":
            locations = Location.objects.filter(factoidlocation__factoid=obj)
            if locations.count() > 0:
                for location in locations:
                    return location.locname
            else:
                return ""
        else:
            return ""

    def prepare_ethnicity(self, obj):
        # Ethnicity
        if obj.factoidtype.typename == "Ethnic label":
            ethnicities = Ethnicity.objects.filter(
                ethnicityfactoid__factoid=obj)
            if ethnicities.count() > 0:
                for eth in ethnicities:
                    return eth.ethname
            else:
                return ""
        else:
            return ""

    def prepare_dignityoffice(self, obj):
        if obj.factoidtype.typename == "Dignity/Office":
            digs = Dignityoffice.objects.filter(dignityfactoid__factoid=obj)
            if digs.count() > 0:
                for d in digs:
                    return d.stdname
            else:
                return ""
        else:
            return ""

    # Secondary names (= second names + alternative names)#}
    def prepare_secondaryname(self, obj):
        if obj.factoidtype.typename == "Second Name" or obj.factoidtype.typename == "Alternative Name":
            secs = Variantname.objects.filter(vnamefactoid__factoid=obj)
            if secs.count() > 0:
                for s in secs:
                    return s.name
            return ""
        else:
            return ""

    def prepare_language(self, obj):
        if obj.factoidtype.typename == "Language Skill":
            langs = Languageskill.objects.filter(langfactoid__factoid=obj)
            if langs.count() > 0:
                for l in langs:
                    return l.languagename
            return ""
        else:
            return ""

    def prepare_occupation(self, obj):
        if obj.factoidtype.typename == "Occupation/Vocation":
            occs = Occupation.objects.filter(occupationfactoid__factoid=obj)
            if occs.count() > 0:
                for o in occs:
                    return o.occupationname
            else:
                return ""
        else:
            return ""

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated.
        Filter factoids by type for only those used in browser"""
        factoidtypekeys = DISPLAYED_FACTOID_TYPES
        return self.get_model().objects.filter(
            factoidperson__factoidpersontype__fptypename="Primary",
            factoidtype__id__in=factoidtypekeys).distinct()
