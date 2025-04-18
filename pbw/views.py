# New faceted search for main PBW browse
# Elliott Hall 16/8/2016
# facet('name').facet('letter').
from itertools import permutations

import django.views.generic
import urllib3
import requests
import mimetypes
from django.views.generic.base import RedirectView

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404, HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from haystack.generic_views import FacetedSearchView
from haystack.query import SearchQuerySet
from requests import request
from requests.packages import target

from .forms import PBWFacetedSearchForm
from .models import (Person, Factoid, Factoidperson, Boulloterion, Seal,
                     Published, Factoidtype, Narrativeunit,
                     Collection, Bibliography
                     )
from .settings import DISPLAYED_FACTOID_TYPES
from .utils import get_auth_field


class PBWFacetedSearchView(FacetedSearchView):
    template_name = 'search/browse.html'
    queryset = SearchQuerySet()
    load_all = True
    form_class = PBWFacetedSearchForm
    facet_fields = ['name', 'letter', 'sex', 'floruit']
    autocomplete_facets = [
        'location',
        'dignityoffice',
        'ethnicity',
        'language',
        'occupation',
        'source']

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
        self.request.session[
            'query_string'] = self.request.META['QUERY_STRING']
        context['centuries'] = ['IX', 'XI', 'XII', 'XIII']
        context['periods'] = ['E', 'M', 'L']
        context['genders'] = ['Male', 'Female', 'Eunuch']

        return context

    def get_queryset(self):
        queryset = super(PBWFacetedSearchView, self).get_queryset().filter(record_type='person')
        all_facets = self.autocomplete_facets + self.facet_fields
        # Massive number for ALL but can be reduced if performance hit
        options = {"size": 10000}
        for facet in all_facets:
            # only return results with a mincount of 1
            queryset = queryset.facet(facet, **options)
        queryset.order_by('name_sort', 'mdbcode')
        return queryset


class FactoidGroup:
    def __init__(self, type, factoids):
        self.factoidtype = type
        self.factoids = factoids


# The detailed view of a single person in the Prosopography
class PersonDetailView(DetailView):
    model = Person
    template_name = 'includes/person_detail.html'
    loadAllThreshold = 200
    loadAll = False

    def get_context_data(self, **kwargs):  # noqa
        context = super(
            PersonDetailView, self).get_context_data(**kwargs)
        context['factoidGroups'] = self.get_factoid_groups(
            DISPLAYED_FACTOID_TYPES)
        context['lastAuthority'] = ''
        context['loadAll'] = self.loadAll
        # Get referred search from session to go back
        try:
            query = self.request.session['query_string']
            context['query'] = query
        except Exception:
            context['query'] = None
        return context

    def get_factoid_groups(self, factoidtypes):
        groups = list()
        self.factoidtypes = factoidtypes
        person = self.get_object()
        # Set up factoid groups by order in settings
        total = 0
        for type_id in factoidtypes:
            try:
                type = Factoidtype.objects.get(id=type_id)
                factoids = self.get_factoid_group(person, type)
                if factoids.count() > 0:
                    groups.append(FactoidGroup(type, factoids))
                    total += factoids.count()
            except ObjectDoesNotExist:
                pass

        return groups



    def get_factoid_group(self, person, type):
        # moved to search index
        # authOrder = get_auth_field(type.typename)
        #     # kinship,education,authorship,death,narrative
        # factoids = Factoid.objects.filter(
        #     factoidperson__person=person).filter(
        #     factoidperson__factoidpersontype__fptypename="Primary")
        # factoids = factoids.filter(factoidtype=type).order_by(
        #     authOrder).distinct()

        factoids = SearchQuerySet().filter(record_type="factoid")
        factoids = factoids.filter(person_id=person.id).filter(
            factoidtype_id=type.id)
        return factoids


# Slight variation on person detail to accept the universal URI
class PersonPermalinkDetailView(PersonDetailView):
    name_url_kwarg = 'name'
    code_url_kwarg = 'code'

    def get_object(self, queryset=None):
        name = self.kwargs.get(self.name_url_kwarg)
        code = self.kwargs.get(self.code_url_kwarg)

        if name is None and code is None:
            raise AttributeError(
                "Person URI must be called with name and code" %
                self.__class__.__name__)

        try:
            # Get the single item from the filtered queryset
            obj = Person.objects.get(name=name, mdbcode=code)
        except queryset.model.DoesNotExist:
            raise Http404("No persons found matching the name/code")

        return obj


# Output a person and their relevant(as in current displayed subset) factoids
# Written to make test fixtures but may be useful later if we make an API
class PersonJsonView(PersonDetailView):
    template_name = "includes/tojson.html"
    format = 'json'

    def get_context_data(self, **kwargs):  # noqa
        context = super(
            PersonDetailView, self).get_context_data(**kwargs)
        person = self.get_object()
        person.serialize_to_fixture()
        person_data = serializers.serialize(
            self.format, Person.objects.filter(id=person.id))
        factoid_data = serializers.serialize(
            self.format, person.getFilteredFactoids())
        context['toJSON'] = person_data + factoid_data
        return context


# Displays one factoid type
# As a nested list if authority list


class FactoidGroupView(PersonDetailView):
    template_name = 'ajax/factoid_group.html'

    # results_per_page = 1000

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.type = Factoidtype.objects.get(id=kwargs['type_id'])
        self.page_number = request.GET.get('page')
        context = self.get_context_data(object=self.object, type=self.type)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):  # noqa
        context = super(
            PersonDetailView, self).get_context_data(**kwargs)
        person = self.get_object()

        # factoids = SearchQuerySet().filter(record_type='factoid').filter(
        #     person_id=person.id)
        factoids = SearchQuerySet().filter(
            record_type='factoid').filter(person_id=person.id).filter(factoidtype_id=self.type.id).order_by('factoidtype_id', 'order_number','order_field_exact')
        context['factoids'] = factoids  # page
        return context


class AutoCompleteView(django.views.generic.ListView):
    template_name = "ajax/autocomplete.html"

    def get_context_data(self, **kwargs):  # noqa
        context = super().get_context_data(**kwargs)
        if self.request.GET.get("facet"):
            facet = self.request.GET.get("facet")
            context["ajax_facet"] = facet
            queryset =  self.get_queryset()
            context['queryset'] = queryset
            query = self.request.GET.get(facet)
            facet_counts = queryset.facet_counts()
            if query and facet in facet_counts['fields']:
                results = facet_counts['fields'][facet]
                filteredResults = []
                for result in results:
                    if result[0].startswith(query.replace('*','').capitalize()):
                        filteredResults.append(result)
                context['results'] = filteredResults
        return context

    @staticmethod
    def __facet_by_group(queryset, group):
        """Apply a list of fields as facets to queryset"""
        # , sort='index', limit=-1, mincount=1
        options = {"size": 10000}
        for field_name in group:
            queryset = queryset.facet(
                field_name, **options
            )
        return queryset

    def get_queryset(self):
        queryset = SearchQuerySet()
        #queryset = super().get_queryset()
        queryset = queryset.filter(record_type='person')
        if self.request.GET.get("facet"):
            facet = self.request.GET.get("facet")
            query = self.request.GET.get(facet)
            options = {"size": 10000}
            queryset = queryset.facet(
                facet, **options
            )

            querykwargs = {
                facet+'__startswith':query.replace('*','').capitalize()
            }
            testkwargs={ 'location__startswith':'H'}
            queryset = queryset.filter(**querykwargs)

        return queryset


# A detail page to view seal information
class BoulloterionDetailView(DetailView):
    model = Boulloterion
    template_name = 'includes/boulloterion_detail.html'

    def get_context_data(self, **kwargs):  # noqa
        context = super(
            BoulloterionDetailView,
            self).get_context_data(
            **kwargs)

        # Add seals
        seals = Seal.objects.filter(boulloterion=self.get_object())
        # Add Publication history
        published = Published.objects.filter(boulloterion=self.get_object())
        # Person id for linkback
        person_id = 0
        if self.request.GET.get("person_id"):
            person_id = int(self.request.GET.get("person_id"))
        context['person_id'] = person_id
        context['seals'] = seals
        context['published'] = published

        try:
            query = self.request.GET.urlencode()
            context['query'] = query
        except Exception:
            context['query'] = None
        return context


# This view displays a simplified view of Michael's
# Narrative units, selected by a chronological slider
class NarrativeYearListView(ListView):
    model = Narrativeunit
    template_name = "narrative_year.html"
    paginate_by = 25
    first_year = 0
    last_year = 0

    def __init__(self, **kwargs):
        super(NarrativeYearListView, self).__init__(**kwargs)
        units = Narrativeunit.objects.filter(
            yearorder__gt=0).order_by('yearorder')
        # Get the earliest and last year currently in the database
        if units.count() > 0:
            self.first_year = units.first().yearorder
            self.last_year = units.last().yearorder

    def get_queryset(self):
        if 'current_year' in self.request.GET:
            current_year = self.request.GET.get("current_year")
        else:
            current_year = self.first_year
        return Narrativeunit.objects.filter(
            yearorder=current_year
        ).order_by(
            'hierarchyunit__lft',
            '-datetypekey'
        )

    def get_context_data(self, **kwargs):  # noqa
        context = super(
            NarrativeYearListView,
            self).get_context_data(
            **kwargs)
        context['first_year'] = self.first_year
        context['last_year'] = self.last_year
        if 'current_year' in self.request.GET:
            context['current_year'] = self.request.GET.get("current_year")
        else:
            context['current_year'] = self.first_year

        return context


# This view shows seals list by collection and bibliography
class SealsListView(ListView):
    model = Seal
    template_name = "seals.html"
    paginate_by = 30
    DEFAULT_LIST = "collection"

    def get_queryset(self):
        seals = Seal.objects.all().order_by('boulloterion__title')
        collection_id = None
        bibiliography_id = None
        if 'collection_id' in self.request.GET:
            try:
                collection_id = int(self.request.GET.get("collection_id"))
            except ValueError:
                pass
        elif collection_id is None and 'bibliography_id' in self.request.GET:
            try:
                bibiliography_id = int(self.request.GET.get("bibliography_id"))
            except ValueError:
                pass
        if collection_id:
            seals = seals.filter(
                collection_id=collection_id
            ).order_by(
                'collectionref'
            )
        elif bibiliography_id:
            seals = seals.filter(
                boulloterion__published__bibliography_id=bibiliography_id
            ).order_by('boulloterion__title')
        return seals

    def get_context_data(self, **kwargs):  # noqa
        context = super(
            SealsListView,
            self).get_context_data(
            **kwargs)

        list = self.DEFAULT_LIST
        if 'list' in self.request.GET:
            list = self.request.GET.get("list")
        if 'collection' in list:
            context['collections'] = Collection.objects.all()
            context['list'] = 'collection'
        elif 'bibliography' in list:
            context['bibliographies'] = Bibliography.objects.all().order_by(
                'shortname')
            context['list'] = 'bibliography'

        if 'collection_id' in self.request.GET:
            context['collection_id'] = self.request.GET.get("collection_id")
            context['collection'] = Collection.objects.get(
                id=self.request.GET.get("collection_id"))
        elif 'bibliography_id' in self.request.GET:
            context['bibliography_id'] = self.request.GET.get(
                'bibliography_id')
            context['bibliography'] = Bibliography.objects.get(
                bibkey=self.request.GET.get('bibliography_id'))

        return context

class Pbw2011PersonRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        request = self.request
        person_param = request.GET.get('personKey', '0')
        url = ''
        try:
            person_key = int(person_param)
        except ValueError:
            person_key = 0
        host = request.headers.get('Host', "localhost")
        url = request.scheme + "://" + host + "/pbw2011/jsp/person_" + str(
            person_key) + ".html"
        return url
