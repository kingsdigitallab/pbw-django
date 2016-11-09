from haystack import indexes

from settings import DISPLAYED_FACTOID_TYPES
from models import Person, Factoid, Location, Ethnicity,Dignityoffice, Variantname, Languageskill, Occupation,Source


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    description = indexes.CharField(model_attr='descname',default='')
    name = indexes.CharField(model_attr='name', faceted=True)
    origldesc = indexes.CharField(model_attr='nameol')
    letter = indexes.FacetCharField()
    source = indexes.FacetMultiValueField()
    person = indexes.CharField()
    sex = indexes.FacetCharField(model_attr='sex__sexvalue')
    person_id = indexes.IntegerField(model_attr='id')
    floruit = indexes.CharField(model_attr='floruit', faceted=True)
    mdbcode = indexes.IntegerField(model_attr='mdbcode')
    oLangKey = indexes.IntegerField(model_attr='olangkey')
    tstamp = indexes.DateTimeField(model_attr='tstamp')

    def get_model(self):
        return Person

    def prepare_person(self, obj):
        return obj.name + " " + str(obj.mdbcode)

    def prepare_letter(self, obj):
        if len(obj.name) > 0:
            return obj.name[0].upper()

    def prepare_source(self, obj):
        sources = Source.objects.filter(factoid__factoidperson__person=obj,factoid__factoidtype__in=DISPLAYED_FACTOID_TYPES).distinct()
        return list(sources)

        # factoids = Factoid.objects.filter(factoidperson__person=obj,factoidtype__in=DISPLAYED_FACTOID_TYPES).distinct()
        # sources=[]
        # for f in factoids:
        #     try:
        #         sources.append(f.source.sourceid)
        #     except Exception as e:
        #         print "No source found for factoid "+f.id+" "+e.message
        # return list(set(sources))



    def index_queryset(self, using=None):
        """Used when the entire index for model is updated.
        Filter factoids by type for only those used in browser"""
        factoidtypekeys = DISPLAYED_FACTOID_TYPES
        return self.get_model().objects.filter(factoidperson__factoid__factoidtype__in=factoidtypekeys).distinct()


# The base class for the the various factoid types
class FactoidIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    description = indexes.CharField(model_attr='engdesc',default='')
    name = indexes.FacetCharField()
    origldesc = indexes.FacetCharField(model_attr='origldesc')
    factoidtype = indexes.CharField(model_attr='factoidtype__typename')
    factoidtypekey = indexes.IntegerField(
        model_attr='factoidtype__id', faceted=True)
    person = indexes.CharField()
    person_id = indexes.IntegerField()
    source_id = indexes.IntegerField(model_attr='source__id')
    source = indexes.FacetMultiValueField()
    sourceref = indexes.CharField(model_attr='sourceref')
    #Factoid Types
    location = indexes.FacetCharField()
    ethnicity = indexes.FacetCharField()
    dignityoffice = indexes.FacetCharField()
    language = indexes.FacetCharField()
    secondaryname = indexes.FacetCharField()
    occupation = indexes.FacetCharField()
    letter = indexes.FacetCharField()


    def get_model(self):
        return Factoid

    def prepare_person(self, obj):
        p = obj.person
        if p != None:
            return p.name + " " + unicode(p.mdbcode)
        else:
            print "ERROR No primary person found for factoid "+str(obj.id)
        return None

    def prepare_source(self, obj):
        #model_attr='source__sourceid'
        return [obj.source.sourceid]

    def prepare_person_id(self, obj):
        p = obj.person
        if p != None:
            return p.id
        else:
            return 0


    def prepare_name(self,obj):
        p = obj.person
        if p != None:
            return p.name
        else:
            return ""

    def prepare_letter(self, obj):
        p = obj.person
        if p != None:
            name = p.name
            if len(name) > 0:
                return name[0].upper()
        return ""

    def prepare_location(self, obj):
        #Location
        if self.factoidtype == "Location":
            locations = Location.objects.filter(factoidlocation__factoid=obj)
            if locations.count() > 0:
                for location in locations:
                    return location.locname
            else:
                return ""
        else:
            return ""

    def prepare_ethnicity(self, obj):
        #Ethnicity
        if self.factoidtype == "Ethnic label":
            ethnicities = Ethnicity.objects.filter(ethnicityfactoid__factoid=obj)
            if ethnicities.count() > 0:
                for eth in ethnicities:
                    return eth.ethname
            else:
                return ""
        else:
            return ""


    def prepare_dignityoffice(self, obj):
        if self.factoidtype == "Dignity/Office":
            digs = Dignityoffice.objects.filter(dignityfactoid__factoid=obj)
            if digs.count() > 0:
                for d in digs:
                    return d.stdname
            else:
                return ""
        else:
            return ""

    #Secondary names (= second names + alternative names)#}
    def prepare_secondaryname(self,obj):
        if self.factoidtype == "Alternative Name":
            secs = Variantname.objects.filter(vnamefactoid__factoid=obj)
            if secs.count() > 0:
                for s in secs:
                    return s.name
            return ""
        else:
            return ""

    def prepare_language(self,obj):
        if self.factoidtype == "Language Skill":
            langs = Languageskill.objects.filter(langfactoid__factoid=obj)
            if langs.count() > 0:
                for l in langs:
                    return l.languagename
            return ""
        else:
            return ""

    def prepare_occupation(self,obj):
        if self.factoidtype == "Occupation":
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
        return self.get_model().objects.filter(factoidperson__factoidpersontype__fptypename="Primary",factoidtype__in=factoidtypekeys).distinct()

