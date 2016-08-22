from haystack import indexes
from settings import DISPLAYED_FACTOID_TYPES
from models import Person, Factoid


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name', faceted=True)
    letter = indexes.FacetCharField()
    person = indexes.FacetCharField()
    person_id = indexes.IntegerField(model_attr='personkey')
    floruit = indexes.CharField(model_attr='floruit', faceted=True)
    mdbcode = indexes.IntegerField(model_attr='mdbcode')
    sexKey = indexes.IntegerField(model_attr='sexkey')
    oLangKey = indexes.IntegerField(model_attr='olangkey')
    tstamp = indexes.DateTimeField(model_attr='stamp')

    def get_model(self):
        return Person

    def prepare_person(self, obj):
        p = Person.objects.filter(factoidperson__factoid__id=obj.id)
        if p.count() > 0:
            return p[0].name + " " + str(p[0].mdbcode)

    def prepare_letter(self, obj):
        if len(obj.name) > 0:
            return obj.name[0]


class FactoidIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    engDesc = indexes.EdgeNgramField(model_attr='engdesc')
    factoidtype = indexes.FacetCharField(model_attr='factoidtype__typename')
    factoidtypekey = indexes.IntegerField(
        model_attr='factoidtype__id', faceted=True)
    person = indexes.FacetCharField()
    person_id = indexes.IntegerField()
    source_id = indexes.IntegerField(model_attr='source__id')
    source = indexes.FacetCharField(model_attr='source__sourceid')

    def get_model(self):
        return Factoid

    def prepare_person(self, obj):
        p = Person.objects.filter(factoidperson__factoid__id=obj.id)
        if p.count() > 0:
            return p[0].name + " " + str(p[0].mdbcode)

    def prepare_person_id(self, obj):
        p = Person.objects.filter(factoidperson__factoid__id=obj.id)
        if p.count() > 0:
            return p[0].id

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated.
        Filter factoids by type for only those used in browser"""
        factoidtypekeys = DISPLAYED_FACTOID_TYPES
        return self.get_model().objects.filter(factoidtype__in=factoidtypekeys)
