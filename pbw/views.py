#New faceted search for main PBW browse
#Elliott Hall 16/8/2016
#facet('name').facet('letter').
from django.views.generic.detail import DetailView
from haystack.generic_views import FacetedSearchView
from forms import PBWFacetedSearchForm
from settings import DISPLAYED_FACTOID_TYPES,BASE_DIR
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from solr_backends.solr_backend_field_collapsing import \
    GroupedSearchQuerySet
import os
from models import Person,Factoid,Source
from django.core import serializers
from django.core.urlresolvers import reverse


class PBWFacetedSearchView(FacetedSearchView):
    queryset = GroupedSearchQuerySet().models(
        Person, Factoid).group_by('person_id')
    load_all=True
    form_class=PBWFacetedSearchForm
    facet_fields = ['name','letter','sex','floruit','secondaryname']
    autocomplete_facets = ['location','dignityoffice','ethnicity','language','occupation']

    def build_page(self):
        # Override Haystack's pagination logic so that invoking a
        # facet that reduces the number of pages of results below the
        # current page does not result in a 404.
        #
        # This is essentially the same code as Django 1.4's pagination
        # example.
        paginator = Paginator(self.results, self.results_per_page)
        page_number = self.request.GET.get('page')
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        return (paginator, page)

    def get_context_data(self, **kwargs):  # noqa
        context = super(
            PBWFacetedSearchView, self).get_context_data(**kwargs)
        context['querydict'] = self.request.GET

        if self.request.GET.getlist('selected_facets'):
            context['selected_facets'] = self.request.GET.getlist(
                'selected_facets')
        # used to generate the lists for the autocomplete dictionary
        context['autocomplete_facets'] = self.autocomplete_facets

        for afacet in context['autocomplete_facets']:

            if self.request.GET.get(afacet):
                qs = self.request.GET.copy()
                qs.pop(afacet)

                url = reverse('haystack_search')

                if len(qs):
                    url = '?{0}'.format(qs.urlencode())

                context[afacet] = (url, self.request.GET.get(afacet))
        return context

    def get_queryset(self):
        queryset = super(PBWFacetedSearchView, self).get_queryset()
        all_facets = self.autocomplete_facets + self.facet_fields
        #
        for facet in all_facets:
            # only return results with a mincount of 1
            queryset = queryset.facet(facet, limit=30, mincount=1,sort='index')

        return queryset


# Conveneince class for person detail to group factoids by type for display
class FactoidGroup:
    groups={}

    def __init__(self,person,factoidtypes):
        self.person = person
        self.groups={}
        factoids = Factoid.objects.filter(factoidperson__person=person).filter(factoidtype__in=factoidtypes)
        for f in factoids:
            try:
                self.groups[f.factoidtype.typename].append(f)
            except KeyError:
                self.groups[f.factoidtype.typename] = []
                self.groups[f.factoidtype.typename].append(f)

        # self.groups.
        # self.factoidtype = factoidtype
        # self.factoids = factoids
        # self.factoidtype_id= factoidtype.id


#The detailed view of a single person in the Prosopography
class PersonDetailView(DetailView):
    model = Person
    template_name = 'includes/person_detail.html'

    def get_context_data(self, **kwargs):  # noqa
        context = super(
            PersonDetailView, self).get_context_data(**kwargs)
        person = self.get_object()
        group=FactoidGroup(person,DISPLAYED_FACTOID_TYPES).groups
        context['factoidGroups'] = group
        return context

#Output a person and their relevant(as in current displayed subset) factoids
#Written to make test fixtures but may be useful later if we make an API
class PersonJsonView(PersonDetailView):
    template_name = "includes/tojson.html"
    format='json'


    def get_context_data(self, **kwargs):  # noqa
        context = super(
            PersonDetailView, self).get_context_data(**kwargs)
        person = self.get_object()
        person.serialize_to_fixture()
        person_data = serializers.serialize(self.format, Person.objects.filter(id=person.id))
        factoid_data = serializers.serialize(self.format, person.getFilteredFactoids())
        context['toJSON'] = person_data+factoid_data
        return context
