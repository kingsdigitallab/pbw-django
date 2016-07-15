__author__ = 'elliotthall'
from haystack import indexes

from models import Person,Factoid,Source

class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name',faceted=True)
    floruit = indexes.CharField(model_attr='floruit',faceted=True)
    mdbcode = indexes.IntegerField(model_attr='mdbCode')
    sexKey = indexes.IntegerField(model_attr='sexKey')
    oLangKey = indexes.IntegerField(model_attr='oLangKey')
    tstamp = indexes.DateTimeField(model_attr='stamp')

    def get_model(self):
        return Person


class FactoidIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    factoidtypekey = indexes.IntegerField(model_attr='factoidTypeKey',faceted=True)


class SourceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    source = indexes.CharField(model_attr='sourceID',faceted=True)

#from haystack.query import SearchQuerySet
#sqs = SearchQuerySet().facet('name')
#sqs.facet_counts()