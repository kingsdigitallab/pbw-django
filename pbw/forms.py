from django import forms
from haystack.forms import FacetedSearchForm
from models import Factoid, Narrativeunit


class PBWFacetedSearchForm(FacetedSearchForm):

    name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'autocomplete'}))

    letter = forms.CharField(required=False, widget=forms.HiddenInput(
        attrs={}))

    floruit = forms.CharField(required=False, widget=forms.HiddenInput(
        attrs={}))

    sex = forms.CharField(required=False, widget=forms.HiddenInput(
        attrs={}))

    source = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'autocomplete'}))

    dignityoffice = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'autocomplete'}))

    location = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'autocomplete'}))

    ethnicity = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'autocomplete'}))

    language = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'autocomplete'}))

    occupation = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'autocomplete'}))

    def no_query_found(self):
        """Determines the behaviour when no query was found; returns all the
        results."""
        return self.searchqueryset.all()

    def search(self):
        sqs = super(PBWFacetedSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        data = self.cleaned_data
        if "selected_facets" in data:
            if data.get("selected_facets"):
                print (data.get("selected_facets"))

        for field in (
            'dignityoffice',
            'location',
            'ethnicity',
            'language',
            'occupation',
            'name',
            'letter',
            'sex',
            'source',
                'floruit'):
            if field in data:
                if data.get(field):
                    sqs = sqs.narrow('{}:{}'.format(
                        field, data.get(field)))
        # default order by name
        sqs = sqs.order_by('person')
        return sqs

    def __init__(self, *args, **kwargs):
        if 'data' not in kwargs:
            # this is enough to 'bind' the form, i.e. it will be processed
            kwargs['data'] = {}
        super(PBWFacetedSearchForm, self).__init__(
            *args, **kwargs)


class FactoidForm(forms.ModelForm):

    class Meta:
        model = Factoid
        fields = ['engdesc', 'source']
