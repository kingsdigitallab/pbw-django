from haystack import indexes
from models import Person, Factoid


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name', faceted=True)
    letter = indexes.FacetCharField()
    person = indexes.FacetCharField()
    person_id = indexes.IntegerField(model_attr='personkey')
    floruit = indexes.CharField(model_attr='floruit', faceted=True)
    mdbcode = indexes.IntegerField(model_attr='mdbCode')
    sexKey = indexes.IntegerField(model_attr='sexKey')
    oLangKey = indexes.IntegerField(model_attr='oLangKey')
    tstamp = indexes.DateTimeField(model_attr='stamp')

    def get_model(self):
        return Person

    def prepare_person(self, obj):
        return obj.name + " " + str(obj.mdbCode)

    def prepare_letter(self, obj):
        if len(obj.name) > 0:
            return obj.name[0]


class FactoidIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    engDesc = indexes.EdgeNgramField(model_attr='engDesc', faceted=True)
    factoidtype = indexes.FacetCharField(model_attr='factoidtype__typename')
    factoidtypekey = indexes.IntegerField(
        model_attr='factoidtype__factoidTypeKey', faceted=True)
    person = indexes.FacetCharField()
    person_id = indexes.IntegerField(model_attr='Factoidperson__person__id')
    source_id = indexes.IntegerField(model_attr='sourcekey')
    source = indexes.FacetCharField(model_attr='source__sourceid')

    def get_model(self):
        return Factoid

    def prepare_person(self, obj):
        p = Person.objects.filter(Factoidperson__Factoid__id=obj.id)
        if p.count() > 0:
            return p.name + " " + str(p.mdbCode)
