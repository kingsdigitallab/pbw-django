from django import forms
from django.utils.safestring import mark_safe
from haystack.forms import FacetedSearchForm

class PBWFacetedSearchForm(FacetedSearchForm):
    dignityoffice = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'autocomplete'}))

    location = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'autocomplete'}))


    def no_query_found(self):
        """Determines the behaviour when no query was found; returns all the
        results."""
        return self.searchqueryset.all()

    def search(self):
        sqs = super(PBWFacetedSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        if self.is_bound:
            data = self.cleaned_data
            for field in ('dignityoffice', 'location'):
                    if field in data:
                        if data.get(field):
                            sqs = sqs.narrow('{}:{}'.format(
                                field, data.get(field)))

        return sqs