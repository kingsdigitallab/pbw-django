from django import forms
from django.utils.safestring import mark_safe
from haystack.forms import FacetedSearchForm

class PBWFacetedSearchForm(FacetedSearchForm):
    def no_query_found(self):
        """Determines the behaviour when no query was found; returns all the
        results."""
        return self.searchqueryset.all()

    def search(self):
        sqs = super(PBWFacetedSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        return sqs