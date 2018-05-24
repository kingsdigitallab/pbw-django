# Test cases for the Haystack faceted search
#Currently assumes a running, populated Solr instance
#Elliott Hall 25/08/2016

from django.test import TestCase

from pbw.models import Person, Factoid

#TODO complete and refactor foe haystack 2.6
class HaystackTest(TestCase):
    fixtures = ['person_107447.json','factoids_person_107447.json']


    #Test Letter Facet
    #Find the letter I, count 1
    # def test_letter(self):
    #     letter = 'I'
    #     queryset = GroupedSearchQuerySet().models(
    #         Person, Factoid).group_by('person_id').filter(letter=letter)
    #     self.assertEqual(1, queryset.count())
    #
    #
    # #Test Person Facet
    # def test_name(self):
    #     person_name = 'Isaakios'
    #     queryset = GroupedSearchQuerySet().models(
    #         Person, Factoid).group_by('person_id').filter(name=person_name)
    #     self.assertEqual(1, queryset.count())


    #Test Factoid Facet
    #Current factoid keys [6, 8, 9, 12, 13, 11, 17]
    #def test_factoid_types(self):
        #pass
        # Ethnicity 8

        # Dignity 6

        # Location 12


#Test Source Facet
