# New faceted search for main PBW browse
# Elliott Hall 16/8/2016
# facet('name').facet('letter').
import os
from django.views.generic.base import View, TemplateView

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from haystack.generic_views import FacetedSearchView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from forms import PBWFacetedSearchForm
from settings import DISPLAYED_FACTOID_TYPES, BASE_DIR
from solr_backends.solr_backend_field_collapsing import \
    GroupedSearchQuerySet
from models import Person, Factoid, Source, Factoidtype, Boulloterion, Seal, Published, Collection, Factoidtype


class PBWFacetedSearchView(FacetedSearchView):
    template_name = 'search/browse.html'
    queryset = GroupedSearchQuerySet().models(
        Person, Factoid).group_by('person_id')
    load_all = True
    form_class = PBWFacetedSearchForm
    facet_fields = ['name', 'letter', 'sex', 'floruit', 'secondaryname']
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

        return context

    def get_queryset(self):
        queryset = super(PBWFacetedSearchView, self).get_queryset()
        all_facets = self.autocomplete_facets + self.facet_fields
        #
        for facet in all_facets:
            # only return results with a mincount of 1
            queryset = queryset.facet(facet, mincount=1, sort='index')

        return queryset


# Conveneince class for person detail to group factoids by type for display
class FactoidGroups:
    groups = {}
    factoidtypes = []

    # Sort the factoid types into the preferred order (See PBW-24)
    def factoidtypesort(self, factoids):
        type_id = factoids[0].factoidtype.id
        x = 0
        for ftype in self.factoidtypes:
            if ftype == type_id:
                return x
            x += 1

    def __init__(self, person, factoidtypes):
        self.person = person
        self.groups = list()
        self.factoidtypes = factoidtypes
        self.locations = self.getLocations()

        # Set up factoid groups by order in settings
        for type_id in factoidtypes:
            try:
                type = Factoidtype.objects.get(id=type_id)
                factoids = Factoid.objects.filter(
                    factoidperson__person=person,
                    factoidperson__factoidpersontype__fptypename="Primary") .filter(
                    factoidtype=type).order_by(
                    'scdate__year',
                    'scdate__yrorder')
                if factoids.count() > 0:
                    self.groups.append(FactoidGroup(type, factoids))
            except ObjectDoesNotExist:
                pass

    def getLocations(self):
        type = 12
        factoids = Factoid.objects.filter(
            factoidperson__person=self.person,
            factoidperson__factoidpersontype__fptypename="Primary") .filter(
            factoidtype_id=type).order_by(
            'factoidlocation__location',
            'scdate__year',
            'scdate__yrorder').distinct()
        print factoids.count()
        return factoids

    def getEthnicity(self):
        type = 8
        factoids = Factoid.objects.filter(
            factoidperson__person=self.person,
            factoidperson__factoidpersontype__fptypename="Primary") .filter(
            factoidtype_id=type).order_by(
            'ethnicityfactoid__ethnicity',
            'scdate__year',
            'scdate__yrorder')
        pass

    def getDignityOffice(self):
        type = 6
        factoids = Factoid.objects.filter(
            factoidperson__person=self.person,
            factoidperson__factoidpersontype__fptypename="Primary") .filter(
            factoidtype_id=type).order_by(
            'scdate__year',
            'scdate__yrorder')
        pass

    def getKinship(self):
        pass

    def getVariantName(self):
        pass

    def getNarrative(self):
        pass


class FactoidGroup:

    def __init__(self, type, factoids):
        self.factoidtype = type
        self.factoids = factoids


# The detailed view of a single person in the Prosopography
class PersonDetailView(DetailView):
    model = Person
    template_name = 'includes/person_detail.html'

    def get_context_data(self, **kwargs):  # noqa
        context = super(
            PersonDetailView, self).get_context_data(**kwargs)
        person = self.get_object()
        context['factoidGroups'] = FactoidGroups(
            person, DISPLAYED_FACTOID_TYPES)
        context['lastAuthority'] = ''
        # Get referred search from session to go back
        try:
            query = self.request.session['query_string']
            context['query'] = query
        except Exception:
            context['query'] = None
        return context

    def get_factoid_group(self, person, type):
        authOrder = ''
        if type.typename == "Ethnic label":
            authOrder = 'factoidlocation__location'
        elif type.typename == "Location":
            authOrder = 'factoidlocation__location'
        elif type.typename == "Dignity/Office":
            authOrder = 'dignityfaction__dignityoffice'
        elif type.typename == "Occupation":
            authOrder = 'occupationfactoid__ocupation'
        elif type.typename == "Language Skill":
            authOrder = 'langfactoid__languageskill'
        elif type.typename == "Alternative Name":
            authOrder = 'Dignityfaction__dignityoffice'
        elif type.typename == "Religion":
            authOrder = 'religionfactoid__religion'
        elif type.typename == "Possession":
            authOrder = 'possessionfactoid__possession'
        elif type.typename == "Second Name":
            authOrder = 'famnamefactoid__familyname'
        factoids = Factoid.objects.filter(
            factoidperson__person=person,
            factoidperson__factoidpersontype__fptypename="Primary") .filter(
            factoidtype=type).order_by(
            authOrder,
            'scdate__year',
            'scdate__yrorder').distinct()
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

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.type = Factoidtype.objects.get(id=kwargs['type_id'])
        context = self.get_context_data(object=self.object, type=self.type)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):  # noqa
        context = super(
            PersonDetailView, self).get_context_data(**kwargs)
        person = self.get_object()
        factoids = self.get_factoid_group(person=person, type=self.type)
        context['factoids'] = factoids
        return context


class AutoCompleteView(PBWFacetedSearchView):
    template_name = "ajax/autocomplete.html"

    def get_context_data(self, **kwargs):  # noqa
        context = super(
            PBWFacetedSearchView, self).get_context_data(**kwargs)
        if self.request.GET.get("facet"):
            facet = self.request.GET.get("facet")
            search = self.request.GET.get("search")

            context["ajax_facet"] = facet
            context['query'] = self.get_queryset()
        return context

    def get_queryset(self):
        queryset = super(PBWFacetedSearchView, self).get_queryset()
        all_facets = self.autocomplete_facets + self.facet_fields
        #
        for facet in all_facets:
            # only return results with a mincount of 1
            queryset = queryset.facet(facet, mincount=1, sort='index')
        # Apply any other facet selections to get properly filtered list
        try:
            query_string = self.request.session['query_string']
            for q in query_string.split('&'):
                hash = q.split('=')
                n = unicode(hash[1])
                queryset = queryset.narrow('source', n)

        except Exception:
            pass

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
        return context
