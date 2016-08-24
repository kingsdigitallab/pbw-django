#New faceted search for main PBW browse
#Elliott Hall 16/8/2016
#facet('name').facet('letter').
from django.views.generic.detail import DetailView
from haystack.generic_views import FacetedSearchView
from models import Person
from settings import DISPLAYED_FACTOID_TYPES
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from solr_backends.solr_backend_field_collapsing import \
    GroupedSearchQuerySet
from haystack.forms import FacetedSearchForm
from models import Person,Factoid,Source



class PBWFacetedSearchView(FacetedSearchView):
    queryset = GroupedSearchQuerySet().models(
        Person, Factoid).group_by('person_id')
    load_all=True
    form_class=FacetedSearchForm
    facet_fields = ['name','letter']

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

    def get_queryset(self):
        queryset = super(PBWFacetedSearchView, self).get_queryset()
        all_facets =  self.facet_fields
        #
        for facet in all_facets:
            # only return results with a mincount of 1
            queryset = queryset.facet(facet, limit=-1, mincount=1)

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