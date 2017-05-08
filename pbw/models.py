from __future__ import unicode_literals
from settings import DISPLAYED_FACTOID_TYPES, BASE_DIR
from django.db import models
import os
from django.core import serializers
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsearch import index
from django.utils.functional import cached_property


class Accuracy(models.Model):
    # Field name made lowercase.
    acckey = models.AutoField(db_column='accKey', primary_key=True)
    # Field name made lowercase.
    accuracyname = models.CharField(db_column='accuracyName', max_length=100)

    class Meta:
        app_label = 'pbw'
        db_table = 'Accuracy'


class Activityfactoid(models.Model):
    # Field name made lowercase.
    factoidkey = models.IntegerField(db_column='factoidKey', primary_key=True)
    # Field name made lowercase.
    sourcedate = models.TextField(
        db_column='sourceDate', blank=True, null=True)
    # Field name made lowercase.
    olangkey = models.IntegerField(db_column='oLangKey')
    # Field name made lowercase.
    sourcedateol = models.TextField(
        db_column='SourceDateOL', blank=True, null=True)
    tstanp = models.DateTimeField()

    class Meta:
        db_table = 'ActivityFactoid'


class Attrdatetype(models.Model):
    # Field name made lowercase.
    attrdtkey = models.IntegerField(db_column='attrDTKey', primary_key=True)
    # Field name made lowercase.
    adtname = models.CharField(db_column='aDTName', max_length=20)

    class Meta:
        db_table = 'AttrDateType'


class Audit(models.Model):
    # Field name made lowercase.
    auditkey = models.SmallIntegerField(db_column='auditKey', primary_key=True)
    # Field name made lowercase.
    colldbkey = models.IntegerField(db_column='CollDBKey')
    # Field name made lowercase.
    factoidtypekey = models.SmallIntegerField(db_column='factoidTypeKey')
    # Field name made lowercase.
    dcdcount = models.SmallIntegerField(db_column='DCDCount')
    # Field name made lowercase.
    mdbcount = models.SmallIntegerField(db_column='MDBcount')
    # Field name made lowercase.
    personcount = models.SmallIntegerField(db_column='personCount')
    # Field name made lowercase.
    subcount = models.SmallIntegerField(db_column='subCount')
    problem = models.IntegerField()

    class Meta:
        db_table = 'Audit'


class Bibliography(models.Model):
    # Field name made lowercase.
    bibkey = models.IntegerField(db_column='bibKey', primary_key=True)
    # Field name made lowercase.
    latinbib = models.TextField(db_column='latinBib', blank=True, null=True)
    # Field name made lowercase.
    greekbib = models.TextField(db_column='greekBib', blank=True, null=True)
    reference = models.TextField(blank=True, null=True)
    date = models.SmallIntegerField()
    red = models.IntegerField()
    # Field name made lowercase.
    shortname = models.TextField(db_column='shortName', blank=True, null=True)

    def __unicode__(self):
        return self.shortname

    class Meta:
        ordering = ['latinbib']
        db_table = 'Bibliography'


class Boulloterion(models.Model):
    # Field name made lowercase.
    boulloterionkey = models.IntegerField(
        db_column='boulloterionKey', primary_key=True)
    title = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    origltext = models.TextField(db_column='origLText', blank=True, null=True)
    # Field name made lowercase.
    olangkey = models.TextField(db_column='oLangKey', blank=True, null=True)
    # Field name made lowercase.
    obvicon = models.TextField(db_column='obvIcon', blank=True, null=True)
    # Field name made lowercase.
    revicon = models.TextField(db_column='revIcon', blank=True, null=True)
    diameter = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    datewords = models.TextField(db_column='dateWords', blank=True, null=True)
    # Field name made lowercase.
    obvtypekey = models.IntegerField(db_column='obvTypeKey')
    # Field name made lowercase.
    revtypekey = models.CharField(db_column='revTypeKey', max_length=100)
    # Field name made lowercase.
    scdatekey = models.IntegerField(db_column='scDateKey')
    # Field name made lowercase.
    hasimage = models.IntegerField(db_column='hasImage', blank=True, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'Boulloterion'


class Boulloterionfigure(models.Model):
    # Field name made lowercase.
    boulloterionfigurekey = models.IntegerField(
        db_column='boulloterionFigureKey')
    # Field name made lowercase.
    boulloterionkey = models.IntegerField(db_column='boulloterionKey')
    # Field name made lowercase.
    figurekey = models.IntegerField(db_column='figureKey')

    class Meta:
        db_table = 'BoulloterionFigure'


class Chronitem(models.Model):
    # Field name made lowercase.
    chronitemkey = models.SmallIntegerField(
        db_column='chronItemKey', primary_key=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    parent = models.SmallIntegerField(blank=True, null=True)
    # Field name made lowercase.
    chronorder = models.SmallIntegerField(
        db_column='chronOrder', blank=True, null=True)
    lft = models.SmallIntegerField()
    rgt = models.SmallIntegerField()
    chrontreekey = models.SmallIntegerField(db_column='chronTreeKey', blank=True,
                                            null=True)  # Field name made lowercase.
    year = models.SmallIntegerField(blank=True, null=True)
    datingelement = models.CharField(
        db_column='datingElement',
        max_length=100,
        blank=True,
        null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'ChronItem'


class Chronitemfactoid(models.Model):
    # Field name made lowercase.
    factoidkey = models.SmallIntegerField(
        db_column='factoidKey', blank=True, null=True)
    chronitemkey = models.SmallIntegerField(db_column='ChronItemKey', blank=True,
                                            null=True)  # Field name made lowercase.
    # Field name made lowercase.
    chronorder = models.SmallIntegerField(
        db_column='chronOrder', blank=True, null=True)

    class Meta:
        db_table = 'ChronItemFactoid'


class Chronsource(models.Model):
    # Field name made lowercase.
    chronsourcekey = models.SmallIntegerField(
        db_column='chronSourceKey', primary_key=True)
    sourceref = models.CharField(db_column='sourceRef', max_length=100, blank=True,
                                 null=True)  # Field name made lowercase.
    chronitemkey = models.SmallIntegerField(db_column='chronItemKey', blank=True,
                                            null=True)  # Field name made lowercase.
    # Field name made lowercase.
    sourcekey = models.SmallIntegerField(
        db_column='sourceKey', blank=True, null=True)
    # Field name made lowercase.
    datetypekey = models.SmallIntegerField(
        db_column='dateTypeKey', blank=True, null=True)

    class Meta:
        db_table = 'ChronSource'


class Chrontree(models.Model):
    # Field name made lowercase.
    chrontreekey = models.SmallIntegerField(
        db_column='chronTreeKey', primary_key=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'ChronTree'


class Colldb(models.Model):
    # Field name made lowercase.
    colldbkey = models.SmallIntegerField(
        db_column='collDBKey', primary_key=True)
    # Field name made lowercase.
    colldbid = models.CharField(db_column='collDBID', max_length=200)
    researcher = models.CharField(max_length=50)
    corrector = models.CharField(max_length=50)
    cdbcreationdate = models.DateTimeField(db_column='cdbCreationDate', blank=True,
                                           null=True)  # Field name made lowercase.
    # Field name made lowercase.
    cdbimportdate = models.DateTimeField(
        db_column='cdbImportDate', blank=True, null=True)
    # Field name made lowercase.
    sourcekey = models.SmallIntegerField(db_column='sourceKey')
    notes = models.TextField()
    # Field name made lowercase.
    creationdate = models.DateTimeField(
        db_column='creationDate', blank=True, null=True)
    tstamp = models.DateTimeField()

    class Meta:
        db_table = 'CollDB'


class Collection(models.Model):
    id = models.AutoField(primary_key=True)
    # Field name made lowercase.
    collectionkey = models.IntegerField(db_column='collectionKey')
    # Field name made lowercase.
    collectionname = models.TextField(db_column='collectionName')
    red = models.IntegerField()
    # Field name made lowercase.
    shortname = models.TextField(db_column='shortName')
    suppress = models.IntegerField()

    def __unicode__(self):
        return self.shortname

    class Meta:
        db_table = 'Collection'


class Country(models.Model):
    # Field name made lowercase.
    countrykey = models.AutoField(db_column='countryKey', primary_key=True)
    # Field name made lowercase.
    countryname = models.TextField(db_column='countryName')

    class Meta:
        db_table = 'Country'


class Cursus(models.Model):
    # Field name made lowercase.
    cursuskey = models.AutoField(db_column='cursusKey', primary_key=True)
    # Field name made lowercase.
    personkey = models.IntegerField(db_column='personKey')
    # Field name made lowercase.
    scdatekey = models.IntegerField(db_column='scDateKey')
    # Field name made lowercase.
    cursusorder = models.SmallIntegerField(db_column='cursusOrder')

    class Meta:
        db_table = 'Cursus'


class Datetypes(models.Model):
    # Field name made lowercase.
    datetypekey = models.SmallIntegerField(
        db_column='dateTypeKey', primary_key=True)
    datetype = models.CharField(db_column='dateType', max_length=200, blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'DateTypes'


class Deathfactoid(models.Model):
    # Field name made lowercase.
    factoidkey = models.IntegerField(db_column='factoidKey', primary_key=True)
    # Field name made lowercase.
    sourcedate = models.TextField(
        db_column='sourceDate', blank=True, null=True)
    # Field name made lowercase.
    olangkey = models.IntegerField(db_column='oLangKey')
    # Field name made lowercase.
    sourcedateol = models.TextField(
        db_column='SourceDateOL', blank=True, null=True)
    # Field name made lowercase.
    tstamp = models.DateTimeField(db_column='tStamp')

    class Meta:
        db_table = 'DeathFactoid'


class Dignityfactoid(models.Model):
    # factoidkey = models.IntegerField(db_column='factoidKey',
    # primary_key=True)  # Field name made lowercase.
    factoid = models.ForeignKey('Factoid', db_column='factoidKey')
    # Field name made lowercase.
    stdname = models.CharField(db_column='stdName', max_length=100)
    # dokey = models.SmallIntegerField(db_column='doKey')  # Field name made
    # lowercase.
    # Field name made lowercase.
    dotkey = models.IntegerField(db_column='dotKey')
    tstamp = models.DateTimeField()
    # Field name made lowercase.
    cursusorder = models.SmallIntegerField(db_column='cursusOrder')
    # Field name made lowercase.
    appointedby = models.TextField(
        db_column='AppointedBy', blank=True, null=True)
    dignityoffice = models.ForeignKey('Dignityoffice')

    class Meta:
        db_table = 'DignityFactoid'


class Dignityoffice(models.Model):
    # Field name made lowercase.
    id = models.SmallIntegerField(db_column='doKey', primary_key=True)
    # Field name made lowercase.
    stdname = models.CharField(db_column='stdName', max_length=100)
    # Field name made lowercase.
    olangkey = models.IntegerField(db_column='oLangKey')
    # Field name made lowercase.
    stdnameol = models.CharField(db_column='stdNameOL', max_length=100)
    # Field name made lowercase.
    stdshortol = models.CharField(db_column='stdShortOL', max_length=50)
    # Field name made lowercase.
    dotkey = models.IntegerField(db_column='dotKey')
    lft = models.SmallIntegerField()
    rgt = models.SmallIntegerField()
    # Field name made lowercase.
    parentkey = models.SmallIntegerField(db_column='parentKey')
    # Field name made lowercase.
    creationdate = models.DateTimeField(
        db_column='creationDate', blank=True, null=True)
    tstamp = models.DateTimeField()

    class Meta:
        db_table = 'DignityOffice'
        ordering = ['stdname']

    def __unicode__(self):
        return self.stdname



class Dignityofficetype(models.Model):
    # Field name made lowercase.
    dotkey = models.IntegerField(db_column='dotKey', primary_key=True)
    # Field name made lowercase.
    dotname = models.CharField(db_column='dotName', max_length=20)

    class Meta:
        db_table = 'DignityOfficeType'


class Dvsqlauth(models.Model):
    # Field name made lowercase.
    authkey = models.AutoField(db_column='authKey', primary_key=True)
    # Field name made lowercase.
    tablekey = models.SmallIntegerField(db_column='tableKey')
    # Field name made lowercase.
    keyvalue = models.IntegerField(db_column='keyValue')
    # Field name made lowercase.
    namevalue = models.CharField(db_column='nameValue', max_length=50)
    tstamp = models.DateTimeField()

    class Meta:
        db_table = 'DvSqlAuth'


class Dvsqlindex(models.Model):
    # Field name made lowercase.
    indexkey = models.AutoField(db_column='indexKey', primary_key=True)
    # Field name made lowercase.
    tablekey = models.SmallIntegerField(db_column='tableKey')
    # Field name made lowercase.
    indexname = models.CharField(db_column='indexName', max_length=100)
    # Field name made lowercase.
    isunique = models.IntegerField(db_column='isUnique')
    notes = models.TextField(blank=True, null=True)
    tstamp = models.DateTimeField()

    class Meta:
        db_table = 'DvSqlIndex'


class Dvsqlindxattr(models.Model):
    # Field name made lowercase.
    indexkey = models.IntegerField(db_column='indexKey')
    # Field name made lowercase.
    attrkey = models.IntegerField(db_column='attrKey')
    len = models.SmallIntegerField(blank=True, null=True)
    tstamp = models.DateTimeField()

    class Meta:
        db_table = 'DvSqlIndxAttr'
        unique_together = (('indexkey', 'attrkey'),)


class Ethnicity(models.Model):
    # Field name made lowercase.
    id = models.SmallIntegerField(db_column='ethnicityKey', primary_key=True)
    # Field name made lowercase.
    ethname = models.CharField(db_column='ethName', max_length=100)
    # Field name made lowercase.
    olangkey = models.IntegerField(db_column='oLangKey')
    # Field name made lowercase.
    ethnameol = models.CharField(db_column='ethNameOL', max_length=100)
    # Field name made lowercase.
    creationdate = models.DateTimeField(
        db_column='creationDate', blank=True, null=True)
    tstamp = models.DateTimeField()

    class Meta:
        db_table = 'Ethnicity'
        ordering = ['ethname']

    def __unicode__(self):
        return self.ethname


class Ethnicityfactoid(models.Model):
    # factoidkey = models.IntegerField(db_column='factoidKey',
    # primary_key=True)  # Field name made lowercase.
    factoid = models.ForeignKey('Factoid', db_column='factoidKey')
    ethnicity = models.ForeignKey('Ethnicity', db_column='ethnicityKey')
    # ethnicitykey = models.SmallIntegerField(db_column='ethnicityKey')  #
    # Field name made lowercase.
    # Field name made lowercase.
    isdoubtful = models.IntegerField(db_column='isDoubtful')
    tstamp = models.DateTimeField()

    class Meta:
        db_table = 'EthnicityFactoid'


class Factoid(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='factoidKey', primary_key=True)
    source = models.ForeignKey('Source', db_column='sourceKey', blank=True, null=True)
    # Field name made lowercase.
    sourceref = models.CharField(db_column='sourceRef', max_length=250)
    factoidtype = models.ForeignKey(
        'Factoidtype',
        blank=False,
        null=False,
        default=1,
        db_column='factoidTypeKey')  # Field name made lowercase.
    # Field name made lowercase.
    engdesc = models.TextField(db_column='engDesc')
    # Field name made lowercase.
    olangkey = models.IntegerField(db_column='oLangKey')
    # Field name made lowercase.
    origldesc = models.TextField(db_column='origLDesc', blank=True)
    # Field name made lowercase.
    needsattn = models.IntegerField(db_column='needsAttn')
    notes = models.TextField(blank=True)
    # Field name made lowercase.
    colldbkey = models.SmallIntegerField(db_column='collDBKey')
    # Field name made lowercase.
    creationdate = models.DateTimeField(
        db_column='creationDate', blank=True, null=True)
    # Field name made lowercase.
    boulloterionkey = models.IntegerField(db_column='boulloterionKey')
    tstamp = models.DateTimeField()

    @cached_property
    def person(self):
        fp = Person.objects.filter(
            factoidperson__factoid=self,
            factoidperson__factoidpersontype__fptypename="Primary")
        if fp.count() > 0:
            return fp[0]
        else:
            return None

    def getScDates(self):
        return Scdate.objects.filter(factoid=self)


    def __unicode__(self):
        return self.engdesc

    class Meta:

        db_table = 'Factoid'


class Factoidcursus(models.Model):
    # Field name made lowercase.
    cursuskey = models.IntegerField(db_column='cursusKey')
    # Field name made lowercase.
    factoidkey = models.IntegerField(db_column='factoidKey')

    class Meta:
        db_table = 'FactoidCursus'


class Factoidlocation(models.Model):
    id = models.AutoField(primary_key=True)
    factoid = models.ForeignKey('Factoid', db_column='factoidKey')
    # locationkey = models.IntegerField(db_column='locationKey')  # Field name
    # made lowercase.
    location = models.ForeignKey('Location', db_column='locationKey')
    # Field name made lowercase.
    olangkey = models.IntegerField(db_column='oLangKey')
    # Field name made lowercase.
    srcname = models.CharField(db_column='srcName', max_length=50)
    notes = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    siginfo = models.TextField(db_column='sigInfo')
    tstamp = models.DateTimeField()

    class Meta:
        db_table = 'FactoidLocation'


class Factoidperson(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='fpKey', primary_key=True)
    factoid = models.ForeignKey(
        'Factoid',
        blank=False,
        null=False,
        default=1,
        db_column='factoidkey')  # Field name made lowercase.
    factoidpersontype = models.ForeignKey(
        'Factoidpersontype',
        blank=False,
        null=False,
        default=1,
        db_column='fpTypeKey')  # Field name made lowercase.
    person = models.ForeignKey('Person', blank=False, null=False, default=1,
                               db_column='personKey')  # Field name made lowercase.

    class Meta:
        db_table = 'FactoidPerson'


class Factoidpersontype(models.Model):
    # Field name made lowercase.
    fptypekey = models.AutoField(db_column='fpTypeKey', primary_key=True)
    # Field name made lowercase.
    fptypename = models.CharField(db_column='fpTypeName', max_length=15)

    class Meta:
        db_table = 'FactoidPersonType'


class Factoidtype(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='factoidTypeKey', primary_key=True)
    # Field name made lowercase.
    typename = models.CharField(db_column='typeName', max_length=20)
    orderno = models.IntegerField(null=False, default=99)

    def __str__(self):
        return self.typename

    class Meta:
        db_table = 'FactoidType'


# class Famnamefactoid(models.Model):
#     # Field name made lowercase.
#
#     factoidKey = models.SmallIntegerField(db_column='factoidKey')  # Field name made
#     # Field name made lowercase.
#     familyname = models.ForeignKey('Factoid', related_name='familyname',null=True)
#     famnamekey = models.SmallIntegerField(db_column='famNameKey')  # Field name made
#     tstamp = models.DateTimeField()
#
#     class Meta:
#         db_table = 'FamNameFactoid'

class Famnamefactoid(models.Model):
    factoidkey = models.IntegerField(db_column='factoidKey', primary_key=True)  # Field name made lowercase.
    factoid = models.ForeignKey('Factoid', null=True)
    familyname = models.ForeignKey('Factoid', related_name='familyname', null=True)
    famnamekey = models.SmallIntegerField(db_column='famNameKey')  # Field name made lowercase.
    tstamp = models.DateTimeField()

    class Meta:
        db_table = 'FamNameFactoid'


class Familyname(models.Model):
    # Field name made lowercase.
    famnamekey = models.SmallIntegerField(
        db_column='famNameKey', primary_key=True)
    # Field name made lowercase.
    famname = models.CharField(db_column='famName', max_length=40)
    # Field name made lowercase.
    olangkey = models.IntegerField(db_column='oLangKey')
    # Field name made lowercase.
    famnameol = models.CharField(db_column='famNameOL', max_length=40)
    # Field name made lowercase.
    creationdate = models.DateTimeField(
        db_column='creationDate', blank=True, null=True)
    tstamp = models.DateTimeField()

    class Meta:
        db_table = 'FamilyName'


class Figure(models.Model):
    # Field name made lowercase.
    figurekey = models.IntegerField(db_column='figureKey', primary_key=True)
    # Field name made lowercase.
    figurename = models.TextField(db_column='figureName')

    class Meta:
        db_table = 'Figure'


class Found(models.Model):
    # Field name made lowercase.
    foundkey = models.AutoField(db_column='foundKey', primary_key=True)
    # Field name made lowercase.
    founddesc = models.TextField(db_column='foundDesc', blank=True, null=True)
    # Field name made lowercase.
    countrykey = models.IntegerField(
        db_column='countryKey', blank=True, null=True)
    boulloterionkey = models.IntegerField(db_column='boulloterionKey', blank=True,
                                          null=True)  # Field name made lowercase.
    # Field name made lowercase.
    bibkey = models.TextField(db_column='bibKey', blank=True, null=True)
    # Field name made lowercase.
    bibref = models.TextField(db_column='bibRef', blank=True, null=True)

    class Meta:
        db_table = 'Found'


class Hierarchyunit(models.Model):
    # Field name made lowercase.
    hierarchyunitid = models.AutoField(
        db_column='hierarchyUnitID', primary_key=True)
    # Field name made lowercase.
    narrativeunitid = models.IntegerField(db_column='narrativeUnitID')
    lft = models.IntegerField()
    rgt = models.IntegerField()
    # Field name made lowercase.
    parentid = models.IntegerField(db_column='parentID', blank=True, null=True)
    # Field name made lowercase.
    chronorder = models.IntegerField(db_column='Chronorder')
    # Field name made lowercase.
    treeid = models.IntegerField(db_column='treeID', blank=True, null=True)

    class Meta:
        db_table = 'HierarchyUnit'


class Kinfactoid(models.Model):
    factoid = models.ForeignKey('Factoid', db_column='factoid_id')
    # kinkey = models.SmallIntegerField(db_column='kinKey')  # Field name made
    # lowercase.
    kinship = models.ForeignKey('Kinshiptype', db_column='kinKey')
    tstamp = models.DateTimeField()

    class Meta:
        db_table = 'KinFactoid'


class Kinshiptype(models.Model):
    # Field name made lowercase.
    id = models.SmallIntegerField(db_column='kinKey', primary_key=True)
    # Field name made lowercase.
    gspecrelat = models.CharField(db_column='gspecRelat', max_length=30)
    # Field name made lowercase.
    gunspecrelat = models.CharField(db_column='gunspecRelat', max_length=30)
    # Field name made lowercase.
    creationdate = models.DateTimeField(
        db_column='creationDate', blank=True, null=True)
    tstamp = models.DateTimeField()
    kinorder = models.SmallIntegerField(default=1)

    class Meta:
        db_table = 'KinshipType'
        ordering = ['kinorder','gspecrelat']

    def __unicode__(self):
        return self.gspecrelat



class Langfactoid(models.Model):
    factoid = models.ForeignKey('Factoid', db_column='factoidKey')
    # factoidkey = models.IntegerField(db_column='factoidKey',
    # primary_key=True)  # Field name made lowercase.
    languageskill = models.ForeignKey('Languageskill', db_column='langkey')

    # langkey = models.SmallIntegerField(db_column='langKey')  # Field name
    # made lowercase.

    class Meta:
        db_table = 'LangFactoid'


class Languageskill(models.Model):
    # Field name made lowercase.
    langkey = models.SmallIntegerField(db_column='langKey', primary_key=True)
    # Field name made lowercase.
    languagename = models.CharField(db_column='languageName', max_length=100)

    class Meta:
        db_table = 'LanguageSkill'

    def __unicode__(self):
        return self.languagename


class Location(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='locationKey', primary_key=True)
    # factoidlocation = models.ForeignKey('Factoidlocation',db_column='locationKey')
    # Field name made lowercase.
    locname = models.CharField(db_column='locName', max_length=100)
    # Field name made lowercase.
    olangkey = models.IntegerField(db_column='oLangKey')
    locnameol = models.CharField(db_column='locNameOL', max_length=100, blank=True,
                                 null=True)  # Field name made lowercase.
    extrainfo = models.CharField(db_column='extraInfo', max_length=100, blank=True,
                                 null=True)  # Field name made lowercase.
    notes = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    creationdate = models.DateTimeField(
        db_column='creationDate', blank=True, null=True)
    tstamp = models.DateTimeField()
    pleiades_id = models.IntegerField(blank=True, null=True)
    geonames_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Location'

    def __unicode__(self):
        return self.locname


class Locationselector(models.Model):
    # Field name made lowercase.
    locselkey = models.SmallIntegerField(
        db_column='locSelKey', primary_key=True)
    # Field name made lowercase.
    locationkey = models.IntegerField(db_column='locationKey')
    # Field name made lowercase.
    locselname = models.CharField(db_column='locSelName', max_length=100)

    class Meta:
        db_table = 'LocationSelector'


class Narrativefactoid(models.Model):
    id = models.AutoField(primary_key=True)
    # Field name made lowercase.
    factoidkey = models.IntegerField(db_column='factoidKey')
    # Field name made lowercase.
    narrativeunitid = models.IntegerField(db_column='narrativeUnitID')
    hide = models.IntegerField()
    # Field name made lowercase.
    chronorder = models.SmallIntegerField(
        db_column='chronOrder', blank=True, null=True)
    # Field name made lowercase.
    fmkey = models.IntegerField(db_column='fmKey')
    factoid = models.ForeignKey(
        'Factoid',
        blank=True,
        null=True,
    )
    narrativeunit = models.ForeignKey(
        'Narrativeunit',
        blank=True,
        null=True,
    )  #

    class Meta:
        db_table = 'NarrativeFactoid'



class Narrativeunit(models.Model):
    # Field name made lowercase.
    narrativeunitid = models.AutoField(
        db_column='narrativeUnitID', primary_key=True)
    description = models.TextField(blank=True, null=True)
    primaryattestation = models.CharField(
        db_column='primaryAttestation',
        max_length=200,
        blank=True,
        null=True)  # Field name made lowercase.
    secondaryattestation = models.CharField(
        db_column='secondaryAttestation',
        max_length=200,
        blank=True,
        null=True)  # Field name made lowercase.
    dates = models.CharField(max_length=200, blank=True, null=True)
    # Field name made lowercase.
    datetypekey = models.IntegerField(
        db_column='dateTypeKey', blank=True, null=True)
    summary = models.TextField()
    # Field name made lowercase.
    fmkey = models.IntegerField(db_column='fmKey')
    notes = models.TextField(blank=True, null=True)
    number = models.IntegerField()
    # yearorder will be used for narrative view
    yearorder = models.IntegerField(blank=True, null=True)
    # These are old nested set trees from hierarchy unit.
    # Should be delete.
    year = models.IntegerField()
    reign = models.IntegerField()
    event = models.IntegerField()
    problem = models.IntegerField()
    heading = models.IntegerField()

    class Meta:
        db_table = 'NarrativeUnit'
        ordering = ['yearorder']


class Occupation(models.Model):
    # Field name made lowercase.
    occupationkey = models.SmallIntegerField(
        db_column='occupationKey', primary_key=True)
    # Field name made lowercase.
    occupationname = models.CharField(
        db_column='occupationName', max_length=50)

    class Meta:
        db_table = 'Occupation'
        ordering = ['occupationname']

    def __unicode__(self):
        return self.occupationname


class Occupationfactoid(models.Model):
    factoid = models.ForeignKey('Factoid', db_column='factoidKey')
    occupation = models.ForeignKey('Occupation', db_column='OccupationKey')

    class Meta:
        db_table = 'OccupationFactoid'


class Origlangauth(models.Model):
    # Field name made lowercase.
    olangkey = models.AutoField(db_column='oLangKey', primary_key=True)
    olanguage = models.CharField(db_column='oLanguage', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'OrigLangAuth'


class Person(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='personKey', primary_key=True)
    name = models.CharField(max_length=30)
    # Field name made lowercase.
    mdbcode = models.IntegerField(db_column='mdbCode')
    # Field name made lowercase.
    descname = models.CharField(db_column='descName', max_length=100)
    floruit = models.CharField(max_length=15, blank=True)
    # Field name made lowercase.
    firstdate = models.SmallIntegerField(db_column='firstDate')
    # Field name made lowercase.
    firstdatetype = models.IntegerField(db_column='firstDateType')
    # Field name made lowercase.
    lastdate = models.SmallIntegerField(db_column='lastDate')
    # Field name made lowercase.
    lastdatetype = models.IntegerField(db_column='lastDateType')
    # Field name made lowercase.
    sex = models.ForeignKey('Sexauth', db_column='sexKey')
    # Field name made lowercase.
    nameol = models.CharField(db_column='nameOL', max_length=100, blank=True)
    # Field name made lowercase.
    olangkey = models.IntegerField(db_column='oLangKey')
    bibliography = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    creationdate = models.DateTimeField(
        db_column='creationDate', blank=True, null=True)
    tstamp = models.DateTimeField(db_column='tstamp')

    class Meta:

        db_table = 'Person'
        ordering = ['name', 'mdbcode']

    def __unicode__(self):
        return '{} {}'.format(self.name, self.mdbcode)

    def __str__(self):
        return '%s %s' % (self.name, self.mdbcode)

    # These are factoids with a PRIMARY fp type, which the person "owns"
    def getPrimaryFactoids(self):
        return Factoid.objects.filter(
            factoidperson__person=self,
            factoidperson__factoidpersontype__fptypename="Primary")

    # This returns only factoid types listed in settings under
    # DISPLAYED_FACTOID_TYPES
    def getFilteredFactoids(self):
        factoidtypekeys = DISPLAYED_FACTOID_TYPES
        return self.factoids.filter(
            factoidtype__in=factoidtypekeys).order_by('factoidtype')

    # Make a complete "snapshot" of a person to use as a fixture
    # This serializes no only the person, but their relevant factoids and
    # their sub tables
    def serialize_to_fixture(self):
        person = self
        format = "json"
        Serializer = serializers.get_serializer(format)
        serializer = Serializer()
        fixture_path = os.path.join(BASE_DIR, 'pbw', 'fixtures')
        person_fixture = os.path.join(
            fixture_path, "person_" + str(person.id) + "." + format)
        with open(person_fixture, "w") as out:
            serializer.serialize(
                Person.objects.filter(
                    id=person.id),
                indent=2,
                stream=out)
            print "Serializing " + "person_" + str(person.id) + "." + format
        factoid_person_fixture = os.path.join(
            fixture_path, "factoids_person_" + str(person.id) + "." + format)
        with open(factoid_person_fixture, "w") as out:
            factoids_complete = self.collect_factoids()
            serializer.serialize(factoids_complete, indent=2, stream=out)
            print "Serializing " + "factoid_" + str(person.id) + "." + format

    # [8, 9, 10, 12, 13, 11, 15]
    def collect_factoids(self):
        factoids = self.getFilteredFactoids()
        factoids_complete = list(factoids)
        for f in factoids:
            main = None
            sub = None
            if f.factoidtype.id == 8:
                # Ethnicity
                eth = Ethnicityfactoid.objects.filter(factoid=f)
                if eth.count() > 0:
                    main = eth[0]
                    sub = main.ethnicity
                    # elif f.factoidtype.id == 9:
                    # Second Name
            elif f.factoidtype.id == 10:
                # Kinship
                kinFactoids = Kinfactoid.objects.filter(factoid=f)
                if kinFactoids.count() > 0:
                    kinFactoid = kinFactoids[0]
                    main = kinFactoid
                    sub = main.kinship
                    # elif f.factoidtype.id == 11:
                    # Language Skill
            elif f.factoidtype.id == 12:
                # Location
                fl = Factoidlocation.objects.filter(factoid=f)
                if fl.count() > 0:
                    main = fl[0]
                    sub = main.location
            elif f.factoidtype.id == 13:
                # Occupation
                ofs = Occupationfactoid.objects.filter(factoid=f)
                if ofs.count() > 0:
                    main = ofs[0]
                    sub = main.occupation
            elif f.factoidtype.id == 15:
                # Religion
                rs = Religion.objects.filter(factoid=f)
                if rs.count() > 0:
                    main = rs[0]
                    sub = main.religion

            if main is not None:
                factoids_complete.append(main)
                factoids_complete.append(sub)
        return factoids_complete


class Personcolldb(models.Model):
    # Field name made lowercase.
    personcolldbkey = models.AutoField(
        db_column='personCollDBKey', primary_key=True)
    # Field name made lowercase.
    personkey = models.IntegerField(db_column='personKey')
    # Field name made lowercase.
    colldbkey = models.SmallIntegerField(db_column='collDBKey')
    # Field name made lowercase.
    cdbcode = models.SmallIntegerField(db_column='cdbCode')
    name = models.CharField(max_length=30)
    # Field name made lowercase.
    olangkey = models.IntegerField(db_column='oLangKey')
    # Field name made lowercase.
    nameol = models.CharField(db_column='nameOL', max_length=60)
    notes = models.TextField()
    tstamp = models.DateTimeField()

    class Meta:
        db_table = 'PersonCollDB'


class Possessionfactoid(models.Model):
    # Field name made lowercase.
    factoidkey = models.IntegerField(db_column='factoidKey', primary_key=True)
    # Field name made lowercase.
    possessionname = models.CharField(
        db_column='possessionName', max_length=100)
    tstamp = models.DateTimeField()
    factoid = models.ForeignKey('Factoid',null=True,blank=True)

    class Meta:
        db_table = 'PossessionFactoid'
        ordering = ['possessionname']


class Published(models.Model):
    # Field name made lowercase.
    publishedkey = models.IntegerField(
        db_column='publishedKey', primary_key=True)
    # Field name made lowercase.
    bibkey = models.IntegerField(db_column='bibKey')
    # Field name made lowercase.
    bibliography = models.ForeignKey('Bibliography', default=1)
    # Field name made lowercase.
    publicationref = models.CharField(
        db_column='publicationRef', max_length=50)
    # Field name made lowercase.
    publicationpage = models.CharField(
        db_column='publicationPage', max_length=50)
    # Field name made lowercase.
    publishedorder = models.IntegerField(db_column='publishedOrder')
    # Field name made lowercase.
    boulloterionKey = models.IntegerField(db_column='boulloterionKey')
    # Field name made lowercase.
    boulloterion = models.ForeignKey('Boulloterion', default=1)

    def __unicode__(self):
        return self.bibliography.shortname + ' ' + self.publicationref

    class Meta:
        db_table = 'Published'


class Religion(models.Model):
    # Field name made lowercase.
    religionkey = models.AutoField(db_column='religionKey', primary_key=True)
    # Field name made lowercase.
    religionname = models.CharField(db_column='religionName', max_length=100)

    class Meta:
        db_table = 'Religion'


class Religionfactoid(models.Model):
    # factoidkey = models.IntegerField(db_column='factoidKey', primary_key=True)  # Field name made lowercase.
    # religionkey = models.SmallIntegerField(db_column='religionKey')  # Field
    # name made lowercase.
    factoid = models.ForeignKey('Factoid', db_column='factoidKey')
    religion = models.ForeignKey('Religion', db_column='religionKey')

    class Meta:
        db_table = 'ReligionFactoid'


class Scdate(models.Model):
    # Field name made lowercase.
    scdatekey = models.AutoField(db_column='scDateKey', primary_key=True)
    # Field name made lowercase.
    factoidkey = models.IntegerField(db_column='factoidKey')
    # Field name made lowercase.
    ssourcekey = models.IntegerField(db_column='sSourceKey')
    year = models.SmallIntegerField()
    # Field name made lowercase.
    yrorder = models.SmallIntegerField(db_column='yrOrder')
    ssref = models.TextField(db_column='ssRef')  # Field name made lowercase.
    priority = models.IntegerField()
    notes = models.TextField()
    # Field name made lowercase.
    creationdate = models.DateTimeField(
        db_column='creationDate', blank=True, null=True)
    tstamp = models.DateTimeField()
    # Field name made lowercase.
    acckey = models.IntegerField(db_column='accKey')
    certainty = models.IntegerField(default=1)
    yeargivenform = models.CharField(
        db_column='yearGivenForm',
        max_length=25,
        blank=True,
        null=True)  # Field name made lowercase.
    factoid = models.ForeignKey('Factoid', default=1)
    datetype = models.ForeignKey('Datetypes', default=7)

    def __unicode__(self):
        return unicode(self.year)

    class Meta:
        db_table = 'ScDate'
        ordering = ['year','yrorder']


class Scsource(models.Model):
    # Field name made lowercase.
    ssourcekey = models.AutoField(db_column='sSourceKey', primary_key=True)
    # Field name made lowercase.
    ssourceid = models.CharField(db_column='sSourceID', max_length=50)
    # Field name made lowercase.
    ssourcefullref = models.TextField(db_column='sSourceFullRef')
    notes = models.TextField()
    # Field name made lowercase.
    creationdate = models.DateTimeField(
        db_column='creationDate', blank=True, null=True)
    tstamp = models.DateTimeField()

    class Meta:
        db_table = 'ScSource'


class Seal(models.Model):
    # Field name made lowercase.
    sealkey = models.IntegerField(db_column='sealKey', primary_key=True)
    # Field name made lowercase.
    collectionKey = models.IntegerField(db_column='collectionKey')
    collection = models.ForeignKey('Collection')  # Field name made lowercase.
    # Field name made lowercase.
    collectionref = models.IntegerField(db_column='collectionRef')
    # Field name made lowercase.
    sealorder = models.IntegerField(db_column='sealOrder')
    # Field name made lowercase.
    boulloterionkey = models.IntegerField(db_column='boulloterionKey')
    # Field name made lowercase.
    boulloterion = models.ForeignKey('Boulloterion')

    def __unicode__(self):
        return self.boulloterion.title

    class Meta:
        db_table = 'Seal'


class Sexauth(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='sexKey', primary_key=True)
    # Field name made lowercase.
    sexvalue = models.CharField(db_column='sexValue', max_length=25)

    def __unicode__(self):
        return self.sexvalue

    class Meta:
        db_table = 'SexAuth'


class Source(models.Model):
    # Field name made lowercase.
    id = models.SmallIntegerField(db_column='sourceKey', primary_key=True)
    # Field name made lowercase.
    sourceid = models.CharField(db_column='sourceID', max_length=50)
    # Field name made lowercase.
    sourcebib = models.TextField(db_column='sourceBib')

    def __unicode__(self):
        return self.sourceid

    class Meta:
        ordering = ['sourceid']
        db_table = 'Source'


class Type(models.Model):
    # Field name made lowercase.
    typekey = models.IntegerField(db_column='typeKey', primary_key=True)
    # Field name made lowercase.
    typename = models.TextField(db_column='typeName')

    class Meta:
        db_table = 'Type'


class User(models.Model):
    # Field name made lowercase.
    userkey = models.AutoField(db_column='userKey', primary_key=True)
    # Field name made lowercase.
    username = models.CharField(db_column='userName', max_length=20)
    # Field name made lowercase.
    namedisplay = models.CharField(db_column='nameDisplay', max_length=100)
    passwd = models.CharField(max_length=100)
    initials = models.CharField(max_length=5)

    class Meta:
        db_table = 'User'


class Vnamefactoid(models.Model):
    # factoidkey = models.IntegerField(db_column='factoidKey', primary_key=True)  # Field name made lowercase.
    # vnamekey = models.IntegerField(db_column='vnameKey')  # Field name made
    # lowercase.
    factoid = models.ForeignKey('Factoid', db_column='factoidKey')
    variantname = models.ForeignKey('Variantname', db_column='vnamekey')

    class Meta:
        db_table = 'VNameFactoid'


class Variantname(models.Model):
    # Field name made lowercase.
    vnamekey = models.AutoField(db_column='vnameKey', primary_key=True)
    # Field name made lowercase.
    olangkey = models.IntegerField(db_column='oLangKey')
    name = models.CharField(max_length=50)
    # Field name made lowercase.
    creationdate = models.DateTimeField(
        db_column='creationDate', blank=True, null=True)
    tstamp = models.DateTimeField()

    class Meta:
        db_table = 'VariantName'


# Wagtail
class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full")
    ]


class IndexPage(Page):
    content = RichTextField(blank=True)

    search_name = 'Index Page'
    search_fields = Page.search_fields
    subpage_types = ['IndexPage', 'RichTextPage']

    content_panels = Page.content_panels + [
        FieldPanel('content', classname="full")
    ]


class RichTextPage(Page):
    content = RichTextField()

    search_fields = Page.search_fields
    search_name = 'Rich Text Page'
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel('content', classname="full")
    ]
