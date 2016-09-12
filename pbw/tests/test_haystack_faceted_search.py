#Test cases for the Haystack faceted search
#Currently assumes a running, populated Solr instance
#Elliott Hall 25/08/2016

from django.test import TestCase
import unittest


class HaystackTest(TestCase):

    def setUp(self):
        pass

# def test_work_getSources(self):
#         work=Work.objects.get(id=6337)
#         self.assertEqual(1, work.getSources().count())
#         first=work.getSources()[0]
#         self.assertEqual(u"GFE: first impression (G)",first.label)

#Test Letter Facet
    def test_letter(self):
        letter = 'I'
        sqs = SearchQuerySet().facet('letter')
        pass


#Test Person Facet
    def test_person(self):
        pass

#Test Factoid Facet
    #Current factoid keys [6, 8, 9, 12, 13, 11, 17]
    def test_factoid_types(self):
        pass
    # Ethnicity 8

    # Dignity 6

    # Location 12


#Test Source Facet
