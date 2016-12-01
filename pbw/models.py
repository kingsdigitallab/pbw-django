
from __future__ import unicode_literals
from settings import DISPLAYED_FACTOID_TYPES,BASE_DIR
from django.db import models
import os
from django.core import serializers
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsearch import index
from django.utils.functional import cached_property

class Accuracy(models.Model):
    acckey = models.AutoField(db_column='accKey', primary_key=True)  # Field name made lowercase.
    accuracyname = models.CharField(db_column='accuracyName', max_length=100)  # Field name made lowercase.

    class Meta:
        app_label = 'pbw'
        db_table = 'Accuracy'


class Activityfactoid(models.Model):
    factoidkey = models.IntegerField(db_column='factoidKey', primary_key=True)  # Field name made lowercase.
    sourcedate = models.TextField(db_column='sourceDate', blank=True, null=True)  # Field name made lowercase.
    olangkey = models.IntegerField(db_column='oLangKey')  # Field name made lowercase.
    sourcedateol = models.TextField(db_column='SourceDateOL', blank=True, null=True)  # Field name made lowercase.
    tstanp = models.DateTimeField()

    class Meta:
        
        db_table = 'ActivityFactoid'


class Attrdatetype(models.Model):
    attrdtkey = models.IntegerField(db_column='attrDTKey', primary_key=True)  # Field name made lowercase.
    adtname = models.CharField(db_column='aDTName', max_length=20)  # Field name made lowercase.

    class Meta:
        
        db_table = 'AttrDateType'


class Audit(models.Model):
    auditkey = models.SmallIntegerField(db_column='auditKey', primary_key=True)  # Field name made lowercase.
    colldbkey = models.IntegerField(db_column='CollDBKey')  # Field name made lowercase.
    factoidtypekey = models.SmallIntegerField(db_column='factoidTypeKey')  # Field name made lowercase.
    dcdcount = models.SmallIntegerField(db_column='DCDCount')  # Field name made lowercase.
    mdbcount = models.SmallIntegerField(db_column='MDBcount')  # Field name made lowercase.
    personcount = models.SmallIntegerField(db_column='personCount')  # Field name made lowercase.
    subcount = models.SmallIntegerField(db_column='subCount')  # Field name made lowercase.
    problem = models.IntegerField()

    class Meta:
        
        db_table = 'Audit'


class Bibliography(models.Model):
    bibkey = models.IntegerField(db_column='bibKey', primary_key=True)  # Field name made lowercase.
    latinbib = models.TextField(db_column='latinBib', blank=True, null=True)  # Field name made lowercase.
    greekbib = models.TextField(db_column='greekBib', blank=True, null=True)  # Field name made lowercase.
    reference = models.TextField(blank=True, null=True)
    date = models.SmallIntegerField()
    red = models.IntegerField()
    shortname = models.TextField(db_column='shortName', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'Bibliography'


class Boulloterion(models.Model):
    boulloterionkey = models.IntegerField(db_column='boulloterionKey', primary_key=True)  # Field name made lowercase.
    title = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    origltext = models.TextField(db_column='origLText', blank=True, null=True)  # Field name made lowercase.
    olangkey = models.TextField(db_column='oLangKey', blank=True, null=True)  # Field name made lowercase.
    obvicon = models.TextField(db_column='obvIcon', blank=True, null=True)  # Field name made lowercase.
    revicon = models.TextField(db_column='revIcon', blank=True, null=True)  # Field name made lowercase.
    diameter = models.TextField(blank=True, null=True)
    datewords = models.TextField(db_column='dateWords', blank=True, null=True)  # Field name made lowercase.
    obvtypekey = models.IntegerField(db_column='obvTypeKey')  # Field name made lowercase.
    revtypekey = models.CharField(db_column='revTypeKey', max_length=100)  # Field name made lowercase.
    scdatekey = models.IntegerField(db_column='scDateKey')  # Field name made lowercase.
    hasimage = models.IntegerField(db_column='hasImage', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'Boulloterion'


class Boulloterionfigure(models.Model):
    boulloterionfigurekey = models.IntegerField(db_column='boulloterionFigureKey')  # Field name made lowercase.
    boulloterionkey = models.IntegerField(db_column='boulloterionKey')  # Field name made lowercase.
    figurekey = models.IntegerField(db_column='figureKey')  # Field name made lowercase.

    class Meta:
        
        db_table = 'BoulloterionFigure'


class Chronitem(models.Model):
    chronitemkey = models.SmallIntegerField(db_column='chronItemKey', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    parent = models.SmallIntegerField(blank=True, null=True)
    chronorder = models.SmallIntegerField(db_column='chronOrder', blank=True, null=True)  # Field name made lowercase.
    lft = models.SmallIntegerField()
    rgt = models.SmallIntegerField()
    chrontreekey = models.SmallIntegerField(db_column='chronTreeKey', blank=True, null=True)  # Field name made lowercase.
    year = models.SmallIntegerField(blank=True, null=True)
    datingelement = models.CharField(db_column='datingElement', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'ChronItem'


class Chronitemfactoid(models.Model):
    factoidkey = models.SmallIntegerField(db_column='factoidKey', blank=True, null=True)  # Field name made lowercase.
    chronitemkey = models.SmallIntegerField(db_column='ChronItemKey', blank=True, null=True)  # Field name made lowercase.
    chronorder = models.SmallIntegerField(db_column='chronOrder', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'ChronItemFactoid'


class Chronsource(models.Model):
    chronsourcekey = models.SmallIntegerField(db_column='chronSourceKey', primary_key=True)  # Field name made lowercase.
    sourceref = models.CharField(db_column='sourceRef', max_length=100, blank=True, null=True)  # Field name made lowercase.
    chronitemkey = models.SmallIntegerField(db_column='chronItemKey', blank=True, null=True)  # Field name made lowercase.
    sourcekey = models.SmallIntegerField(db_column='sourceKey', blank=True, null=True)  # Field name made lowercase.
    datetypekey = models.SmallIntegerField(db_column='dateTypeKey', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'ChronSource'


class Chrontree(models.Model):
    chrontreekey = models.SmallIntegerField(db_column='chronTreeKey', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        
        db_table = 'ChronTree'


class Colldb(models.Model):
    colldbkey = models.SmallIntegerField(db_column='collDBKey', primary_key=True)  # Field name made lowercase.
    colldbid = models.CharField(db_column='collDBID', max_length=200)  # Field name made lowercase.
    researcher = models.CharField(max_length=50)
    corrector = models.CharField(max_length=50)
    cdbcreationdate = models.DateTimeField(db_column='cdbCreationDate', blank=True, null=True)  # Field name made lowercase.
    cdbimportdate = models.DateTimeField(db_column='cdbImportDate', blank=True, null=True)  # Field name made lowercase.
    sourcekey = models.SmallIntegerField(db_column='sourceKey')  # Field name made lowercase.
    notes = models.TextField()
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    tstamp = models.DateTimeField()

    class Meta:
        
        db_table = 'CollDB'


class Collection(models.Model):
    collectionkey = models.IntegerField(db_column='collectionKey')  # Field name made lowercase.
    collectionname = models.TextField(db_column='collectionName')  # Field name made lowercase.
    red = models.IntegerField()
    shortname = models.TextField(db_column='shortName')  # Field name made lowercase.
    suppress = models.IntegerField()

    class Meta:
        
        db_table = 'Collection'


class Country(models.Model):
    countrykey = models.AutoField(db_column='countryKey', primary_key=True)  # Field name made lowercase.
    countryname = models.TextField(db_column='countryName')  # Field name made lowercase.

    class Meta:
        
        db_table = 'Country'


class Cursus(models.Model):
    cursuskey = models.AutoField(db_column='cursusKey', primary_key=True)  # Field name made lowercase.
    personkey = models.IntegerField(db_column='personKey')  # Field name made lowercase.
    scdatekey = models.IntegerField(db_column='scDateKey')  # Field name made lowercase.
    cursusorder = models.SmallIntegerField(db_column='cursusOrder')  # Field name made lowercase.

    class Meta:
        
        db_table = 'Cursus'


class Datetypes(models.Model):
    datetypekey = models.SmallIntegerField(db_column='dateTypeKey', primary_key=True)  # Field name made lowercase.
    datetype = models.CharField(db_column='dateType', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'DateTypes'


class Deathfactoid(models.Model):
    factoidkey = models.IntegerField(db_column='factoidKey', primary_key=True)  # Field name made lowercase.
    sourcedate = models.TextField(db_column='sourceDate', blank=True, null=True)  # Field name made lowercase.
    olangkey = models.IntegerField(db_column='oLangKey')  # Field name made lowercase.
    sourcedateol = models.TextField(db_column='SourceDateOL', blank=True, null=True)  # Field name made lowercase.
    tstamp = models.DateTimeField(db_column='tStamp')  # Field name made lowercase.

    class Meta:
        
        db_table = 'DeathFactoid'


class Dignityfactoid(models.Model):
    #factoidkey = models.IntegerField(db_column='factoidKey', primary_key=True)  # Field name made lowercase.
    factoid = models.ForeignKey('Factoid',db_column='factoidKey')
    stdname = models.CharField(db_column='stdName', max_length=100)  # Field name made lowercase.
    #dokey = models.SmallIntegerField(db_column='doKey')  # Field name made lowercase.
    dotkey = models.IntegerField(db_column='dotKey')  # Field name made lowercase.
    tstamp = models.DateTimeField()
    cursusorder = models.SmallIntegerField(db_column='cursusOrder')  # Field name made lowercase.
    appointedby = models.TextField(db_column='AppointedBy', blank=True, null=True)  # Field name made lowercase.
    dignityoffice=models.ForeignKey('Dignityoffice')

    class Meta:
        
        db_table = 'DignityFactoid'


class Dignityoffice(models.Model):
    id = models.SmallIntegerField(db_column='doKey', primary_key=True)  # Field name made lowercase.
    stdname = models.CharField(db_column='stdName', max_length=100)  # Field name made lowercase.
    olangkey = models.IntegerField(db_column='oLangKey')  # Field name made lowercase.
    stdnameol = models.CharField(db_column='stdNameOL', max_length=100)  # Field name made lowercase.
    stdshortol = models.CharField(db_column='stdShortOL', max_length=50)  # Field name made lowercase.
    dotkey = models.IntegerField(db_column='dotKey')  # Field name made lowercase.
    lft = models.SmallIntegerField()
    rgt = models.SmallIntegerField()
    parentkey = models.SmallIntegerField(db_column='parentKey')  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    tstamp = models.DateTimeField()

    class Meta:
        
        db_table = 'DignityOffice'


class Dignityofficetype(models.Model):
    dotkey = models.IntegerField(db_column='dotKey', primary_key=True)  # Field name made lowercase.
    dotname = models.CharField(db_column='dotName', max_length=20)  # Field name made lowercase.

    class Meta:
        
        db_table = 'DignityOfficeType'


class Dvsqlauth(models.Model):
    authkey = models.AutoField(db_column='authKey', primary_key=True)  # Field name made lowercase.
    tablekey = models.SmallIntegerField(db_column='tableKey')  # Field name made lowercase.
    keyvalue = models.IntegerField(db_column='keyValue')  # Field name made lowercase.
    namevalue = models.CharField(db_column='nameValue', max_length=50)  # Field name made lowercase.
    tstamp = models.DateTimeField()

    class Meta:
        
        db_table = 'DvSqlAuth'


class Dvsqlindex(models.Model):
    indexkey = models.AutoField(db_column='indexKey', primary_key=True)  # Field name made lowercase.
    tablekey = models.SmallIntegerField(db_column='tableKey')  # Field name made lowercase.
    indexname = models.CharField(db_column='indexName', max_length=100)  # Field name made lowercase.
    isunique = models.IntegerField(db_column='isUnique')  # Field name made lowercase.
    notes = models.TextField(blank=True, null=True)
    tstamp = models.DateTimeField()

    class Meta:
        
        db_table = 'DvSqlIndex'


class Dvsqlindxattr(models.Model):
    indexkey = models.IntegerField(db_column='indexKey')  # Field name made lowercase.
    attrkey = models.IntegerField(db_column='attrKey')  # Field name made lowercase.
    len = models.SmallIntegerField(blank=True, null=True)
    tstamp = models.DateTimeField()

    class Meta:
        
        db_table = 'DvSqlIndxAttr'
        unique_together = (('indexkey', 'attrkey'),)


class Ethnicity(models.Model):
    id = models.SmallIntegerField(db_column='ethnicityKey',primary_key=True)  # Field name made lowercase.
    ethname = models.CharField(db_column='ethName', max_length=100)  # Field name made lowercase.
    olangkey = models.IntegerField(db_column='oLangKey')  # Field name made lowercase.
    ethnameol = models.CharField(db_column='ethNameOL', max_length=100)  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    tstamp = models.DateTimeField()

    class Meta:
        
        db_table = 'Ethnicity'


class Ethnicityfactoid(models.Model):
    #factoidkey = models.IntegerField(db_column='factoidKey', primary_key=True)  # Field name made lowercase.
    factoid = models.ForeignKey('Factoid',db_column='factoidKey')
    ethnicity = models.ForeignKey('Ethnicity',db_column='ethnicityKey')
    #ethnicitykey = models.SmallIntegerField(db_column='ethnicityKey')  # Field name made lowercase.
    isdoubtful = models.IntegerField(db_column='isDoubtful')  # Field name made lowercase.
    tstamp = models.DateTimeField()

    class Meta:
        
        db_table = 'EthnicityFactoid'


class Factoid(models.Model):
    id = models.AutoField(db_column='factoidKey', primary_key=True)  # Field name made lowercase.
    source = models.ForeignKey('Source',db_column='sourceKey')
    sourceref = models.CharField(db_column='sourceRef', max_length=250)  # Field name made lowercase.
    factoidtype = models.ForeignKey('Factoidtype', blank=False, null=False, default=1,db_column='factoidTypeKey' ) # Field name made lowercase.
    engdesc = models.TextField(db_column='engDesc')  # Field name made lowercase.
    olangkey = models.IntegerField(db_column='oLangKey')  # Field name made lowercase.
    origldesc = models.TextField(db_column='origLDesc')  # Field name made lowercase.
    needsattn = models.IntegerField(db_column='needsAttn')  # Field name made lowercase.
    notes = models.TextField()
    colldbkey = models.SmallIntegerField(db_column='collDBKey')  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    boulloterionkey = models.IntegerField(db_column='boulloterionKey')  # Field name made lowercase.
    tstamp = models.DateTimeField()

    @cached_property
    def person(self):
        fp=Person.objects.filter(factoidperson__factoid=self,factoidperson__factoidpersontype__fptypename="Primary")
        if fp.count() >0:
            return fp[0]
        else:
            return None

    def __unicode__(self):
        return self.engdesc

    class Meta:
        
        db_table = 'Factoid'


class Factoidcursus(models.Model):
    cursuskey = models.IntegerField(db_column='cursusKey')  # Field name made lowercase.
    factoidkey = models.IntegerField(db_column='factoidKey')  # Field name made lowercase.

    class Meta:
        
        db_table = 'FactoidCursus'



class Factoidlocation(models.Model):
    id = models.AutoField(primary_key=True)
    factoid = models.ForeignKey('Factoid',db_column='factoidKey')
    #locationkey = models.IntegerField(db_column='locationKey')  # Field name made lowercase.
    location = models.ForeignKey('Location',db_column='locationKey')
    olangkey = models.IntegerField(db_column='oLangKey')  # Field name made lowercase.
    srcname = models.CharField(db_column='srcName', max_length=50)  # Field name made lowercase.
    notes = models.TextField(blank=True, null=True)
    siginfo = models.TextField(db_column='sigInfo')  # Field name made lowercase.
    tstamp = models.DateTimeField()

    class Meta:
        
        db_table = 'FactoidLocation'



class Factoidperson(models.Model):
    id = models.AutoField(db_column='fpKey', primary_key=True)  # Field name made lowercase.
    factoid = models.ForeignKey('Factoid', blank=False, null=False, default=1,db_column='factoidkey' ) # Field name made lowercase.
    factoidpersontype = models.ForeignKey('Factoidpersontype', blank=False, null=False, default=1,db_column='fpTypeKey' ) # Field name made lowercase.
    person = models.ForeignKey('Person', blank=False, null=False, default=1,db_column='personKey' ) # Field name made lowercase.


    class Meta:
        
        db_table = 'FactoidPerson'


class Factoidpersontype(models.Model):
    fptypekey = models.AutoField(db_column='fpTypeKey', primary_key=True)  # Field name made lowercase.
    fptypename = models.CharField(db_column='fpTypeName', max_length=15)  # Field name made lowercase.

    class Meta:
        
        db_table = 'FactoidPersonType'


class Factoidtype(models.Model):
    id = models.AutoField(db_column='factoidTypeKey', primary_key=True)  # Field name made lowercase.
    typename = models.CharField(db_column='typeName', max_length=20)  # Field name made lowercase.
    orderno = models.IntegerField(null=False,default=99)

    def __str__(self):
        return self.typename

    class Meta:
        
        db_table = 'FactoidType'


class Famnamefactoid(models.Model):
    factoidkey = models.IntegerField(db_column='factoidKey', primary_key=True)  # Field name made lowercase.
    famnamekey = models.SmallIntegerField(db_column='famNameKey')  # Field name made lowercase.
    tstamp = models.DateTimeField()

    class Meta:
        
        db_table = 'FamNameFactoid'


class Familyname(models.Model):
    famnamekey = models.SmallIntegerField(db_column='famNameKey', primary_key=True)  # Field name made lowercase.
    famname = models.CharField(db_column='famName', max_length=40)  # Field name made lowercase.
    olangkey = models.IntegerField(db_column='oLangKey')  # Field name made lowercase.
    famnameol = models.CharField(db_column='famNameOL', max_length=40)  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    tstamp = models.DateTimeField()

    class Meta:
        
        db_table = 'FamilyName'


class Figure(models.Model):
    figurekey = models.IntegerField(db_column='figureKey', primary_key=True)  # Field name made lowercase.
    figurename = models.TextField(db_column='figureName')  # Field name made lowercase.

    class Meta:
        
        db_table = 'Figure'


class Found(models.Model):
    foundkey = models.AutoField(db_column='foundKey', primary_key=True)  # Field name made lowercase.
    founddesc = models.TextField(db_column='foundDesc', blank=True, null=True)  # Field name made lowercase.
    countrykey = models.IntegerField(db_column='countryKey', blank=True, null=True)  # Field name made lowercase.
    boulloterionkey = models.IntegerField(db_column='boulloterionKey', blank=True, null=True)  # Field name made lowercase.
    bibkey = models.TextField(db_column='bibKey', blank=True, null=True)  # Field name made lowercase.
    bibref = models.TextField(db_column='bibRef', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'Found'


class Hierarchyunit(models.Model):
    hierarchyunitid = models.AutoField(db_column='hierarchyUnitID', primary_key=True)  # Field name made lowercase.
    narrativeunitid = models.IntegerField(db_column='narrativeUnitID')  # Field name made lowercase.
    lft = models.IntegerField()
    rgt = models.IntegerField()
    parentid = models.IntegerField(db_column='parentID', blank=True, null=True)  # Field name made lowercase.
    chronorder = models.IntegerField(db_column='Chronorder')  # Field name made lowercase.
    treeid = models.IntegerField(db_column='treeID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'HierarchyUnit'


class Kinfactoid(models.Model):
    factoid = models.ForeignKey('Factoid',db_column='factoid_id')
    #kinkey = models.SmallIntegerField(db_column='kinKey')  # Field name made lowercase.
    kinship = models.ForeignKey('Kinshiptype',db_column='kinKey')
    tstamp = models.DateTimeField()

    class Meta:
        
        db_table = 'KinFactoid'


class Kinshiptype(models.Model):
    id = models.SmallIntegerField(db_column='kinKey', primary_key=True)  # Field name made lowercase.
    gspecrelat = models.CharField(db_column='gspecRelat', max_length=30)  # Field name made lowercase.
    gunspecrelat = models.CharField(db_column='gunspecRelat', max_length=30)  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    tstamp = models.DateTimeField()

    class Meta:
        
        db_table = 'KinshipType'


class Langfactoid(models.Model):
    factoid = models.ForeignKey('Factoid',db_column='factoidKey')
    #factoidkey = models.IntegerField(db_column='factoidKey', primary_key=True)  # Field name made lowercase.
    languageskill = models.ForeignKey('Languageskill',db_column='langkey')
    #langkey = models.SmallIntegerField(db_column='langKey')  # Field name made lowercase.

    class Meta:
        
        db_table = 'LangFactoid'


class Languageskill(models.Model):
    langkey = models.SmallIntegerField(db_column='langKey', primary_key=True)  # Field name made lowercase.
    languagename = models.CharField(db_column='languageName', max_length=100)  # Field name made lowercase.

    class Meta:
        
        db_table = 'LanguageSkill'


class Location(models.Model):
    id = models.AutoField(db_column='locationKey', primary_key=True)  # Field name made lowercase.
    #factoidlocation = models.ForeignKey('Factoidlocation',db_column='locationKey')
    locname = models.CharField(db_column='locName', max_length=100)  # Field name made lowercase.
    olangkey = models.IntegerField(db_column='oLangKey')  # Field name made lowercase.
    locnameol = models.CharField(db_column='locNameOL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    extrainfo = models.CharField(db_column='extraInfo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(blank=True, null=True)
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    tstamp = models.DateTimeField()

    class Meta:
        
        db_table = 'Location'


class Locationselector(models.Model):
    locselkey = models.SmallIntegerField(db_column='locSelKey', primary_key=True)  # Field name made lowercase.
    locationkey = models.IntegerField(db_column='locationKey')  # Field name made lowercase.
    locselname = models.CharField(db_column='locSelName', max_length=100)  # Field name made lowercase.

    class Meta:
        
        db_table = 'LocationSelector'


class Narrativefactoid(models.Model):
    factoidkey = models.IntegerField(db_column='factoidKey')  # Field name made lowercase.
    narrativeunitid = models.IntegerField(db_column='narrativeUnitID')  # Field name made lowercase.
    hide = models.IntegerField()
    chronorder = models.SmallIntegerField(db_column='chronOrder', blank=True, null=True)  # Field name made lowercase.
    fmkey = models.IntegerField(db_column='fmKey')  # Field name made lowercase.

    class Meta:
        
        db_table = 'NarrativeFactoid'
        unique_together = (('factoidkey', 'narrativeunitid'),)


class Narrativeunit(models.Model):
    narrativeunitid = models.AutoField(db_column='narrativeUnitID', primary_key=True)  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)
    primaryattestation = models.CharField(db_column='primaryAttestation', max_length=200, blank=True, null=True)  # Field name made lowercase.
    secondaryattestation = models.CharField(db_column='secondaryAttestation', max_length=200, blank=True, null=True)  # Field name made lowercase.
    dates = models.CharField(max_length=200, blank=True, null=True)
    datetypekey = models.IntegerField(db_column='dateTypeKey', blank=True, null=True)  # Field name made lowercase.
    summary = models.TextField()
    fmkey = models.IntegerField(db_column='fmKey')  # Field name made lowercase.
    notes = models.TextField(blank=True, null=True)
    number = models.IntegerField()
    year = models.IntegerField()
    reign = models.IntegerField()
    event = models.IntegerField()
    problem = models.IntegerField()
    heading = models.IntegerField()

    class Meta:
        
        db_table = 'NarrativeUnit'


class Occupation(models.Model):
    occupationkey = models.SmallIntegerField(db_column='occupationKey', primary_key=True)  # Field name made lowercase.
    occupationname = models.CharField(db_column='occupationName', max_length=50)  # Field name made lowercase.

    class Meta:
        
        db_table = 'Occupation'


class Occupationfactoid(models.Model):
    factoid = models.ForeignKey('Factoid',db_column='factoidKey')
    occupation = models.ForeignKey('Occupation',db_column='OccupationKey')

    class Meta:
        
        db_table = 'OccupationFactoid'


class Origlangauth(models.Model):
    olangkey = models.AutoField(db_column='oLangKey', primary_key=True)  # Field name made lowercase.
    olanguage = models.CharField(db_column='oLanguage', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'OrigLangAuth'


class Person(models.Model):
    id = models.AutoField(db_column='personKey', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=30)
    mdbcode = models.IntegerField(db_column='mdbCode')  # Field name made lowercase.
    descname = models.CharField(db_column='descName', max_length=100)  # Field name made lowercase.
    floruit = models.CharField(max_length=15)
    firstdate = models.SmallIntegerField(db_column='firstDate')  # Field name made lowercase.
    firstdatetype = models.IntegerField(db_column='firstDateType')  # Field name made lowercase.
    lastdate = models.SmallIntegerField(db_column='lastDate')  # Field name made lowercase.
    lastdatetype = models.IntegerField(db_column='lastDateType')  # Field name made lowercase.
    sex = models.ForeignKey('Sexauth',db_column='sexKey')  # Field name made lowercase.
    nameol = models.CharField(db_column='nameOL', max_length=100)  # Field name made lowercase.
    olangkey = models.IntegerField(db_column='oLangKey')  # Field name made lowercase.
    bibliography = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    tstamp = models.DateTimeField(db_column='tstamp')
    factoids = models.ManyToManyField(Factoid, through='Factoidperson',through_fields=('person','factoid'))

    class Meta:
        
        db_table = 'Person'
        ordering = ['name','mdbcode']

    def __str__(self):
        return '%s %s' % (self.name, self.mdbcode)

    #These are factoids with a PRIMARY fp type, which the person "owns"
    def getPrimaryFactoids(self):
        return Factoid.objects.filter(factoidperson__person=self,factoidperson__factoidpersontype__fptypename="Primary")



    #This returns only factoid types listed in settings under  DISPLAYED_FACTOID_TYPES
    def getFilteredFactoids(self):
        factoidtypekeys = DISPLAYED_FACTOID_TYPES
        return self.factoids.filter(factoidtype__in=factoidtypekeys).order_by('factoidtype')

    #Make a complete "snapshot" of a person to use as a fixture
    #This serializes no only the person, but their relevant factoids and their sub tables
    def serialize_to_fixture(self):
        person = self
        format="json"
        Serializer = serializers.get_serializer(format)
        serializer=Serializer()
        fixture_path=os.path.join(BASE_DIR,'pbw','fixtures')
        person_fixture=os.path.join(fixture_path,"person_"+str(person.id)+"."+format)
        with open(person_fixture, "w") as out:
            serializer.serialize(Person.objects.filter(id=person.id),indent=2, stream=out)
            print "Serializing "+"person_"+str(person.id)+"."+format
        factoid_person_fixture=os.path.join(fixture_path,"factoids_person_"+str(person.id)+"."+format)
        with open(factoid_person_fixture, "w") as out:
            factoids_complete=self.collect_factoids()
            serializer.serialize(factoids_complete, indent=2,stream=out)
            print "Serializing "+"factoid_"+str(person.id)+"."+format

    #[8, 9, 10, 12, 13, 11, 15]
    def collect_factoids(self):
        factoids = self.getFilteredFactoids()
        factoids_complete = list(factoids)
        for f in factoids:
            main = None
            sub = None
            if f.factoidtype.id == 8:
                #Ethnicity
                eth=Ethnicityfactoid.objects.filter(factoid=f)
                if eth.count() > 0:
                    main=eth[0]
                    sub=main.ethnicity
            #elif f.factoidtype.id == 9:
                #Second Name
            elif f.factoidtype.id == 10:
                #Kinship
                kinFactoids=Kinfactoid.objects.filter(factoid=f)
                if kinFactoids.count() > 0:
                    kinFactoid=kinFactoids[0]
                    main = kinFactoid
                    sub = main.kinship
            # elif f.factoidtype.id == 11:
                #Language Skill
            elif f.factoidtype.id == 12:
                #Location
                fl= Factoidlocation.objects.filter(factoid=f)
                if fl.count() > 0:
                    main=fl[0]
                    sub=main.location
            elif f.factoidtype.id == 13:
                #Occupation
                ofs = Occupationfactoid.objects.filter(factoid=f)
                if ofs.count() > 0:
                    main=ofs[0]
                    sub=main.occupation
            elif f.factoidtype.id == 15:
                #Religion
                rs = Religion.objects.filter(factoid=f)
                if rs.count() > 0:
                    main = rs[0]
                    sub = main.religion

            if main != None:
                factoids_complete.append(main)
                factoids_complete.append(sub)
        return factoids_complete





class Personcolldb(models.Model):
    personcolldbkey = models.AutoField(db_column='personCollDBKey', primary_key=True)  # Field name made lowercase.
    personkey = models.IntegerField(db_column='personKey')  # Field name made lowercase.
    colldbkey = models.SmallIntegerField(db_column='collDBKey')  # Field name made lowercase.
    cdbcode = models.SmallIntegerField(db_column='cdbCode')  # Field name made lowercase.
    name = models.CharField(max_length=30)
    olangkey = models.IntegerField(db_column='oLangKey')  # Field name made lowercase.
    nameol = models.CharField(db_column='nameOL', max_length=60)  # Field name made lowercase.
    notes = models.TextField()
    tstamp = models.DateTimeField()

    class Meta:
        
        db_table = 'PersonCollDB'


class Possessionfactoid(models.Model):
    factoidkey = models.IntegerField(db_column='factoidKey', primary_key=True)  # Field name made lowercase.
    possessionname = models.CharField(db_column='possessionName', max_length=100)  # Field name made lowercase.
    tstamp = models.DateTimeField()

    class Meta:
        
        db_table = 'PossessionFactoid'


class Published(models.Model):
    publishedkey = models.IntegerField(db_column='publishedKey', primary_key=True)  # Field name made lowercase.
    bibkey = models.IntegerField(db_column='bibKey')  # Field name made lowercase.
    publicationref = models.CharField(db_column='publicationRef', max_length=50)  # Field name made lowercase.
    publicationpage = models.CharField(db_column='publicationPage', max_length=50)  # Field name made lowercase.
    publishedorder = models.IntegerField(db_column='publishedOrder')  # Field name made lowercase.
    boulloterion = models.ForeignKey('Boulloterion',db_column='boulloterionKey')  # Field name made lowercase.

    class Meta:
        
        db_table = 'Published'


class Religion(models.Model):
    religionkey = models.AutoField(db_column='religionKey', primary_key=True)  # Field name made lowercase.
    religionname = models.CharField(db_column='religionName', max_length=100)  # Field name made lowercase.

    class Meta:
        
        db_table = 'Religion'


class Religionfactoid(models.Model):
    #factoidkey = models.IntegerField(db_column='factoidKey', primary_key=True)  # Field name made lowercase.
    #religionkey = models.SmallIntegerField(db_column='religionKey')  # Field name made lowercase.
    factoid = models.ForeignKey('Factoid',db_column='factoidKey')
    religion = models.ForeignKey('Religion',db_column='religionKey')

    class Meta:
        
        db_table = 'ReligionFactoid'


class Scdate(models.Model):
    scdatekey = models.AutoField(db_column='scDateKey', primary_key=True)  # Field name made lowercase.
    factoidkey = models.IntegerField(db_column='factoidKey')  # Field name made lowercase.
    ssourcekey = models.IntegerField(db_column='sSourceKey')  # Field name made lowercase.
    year = models.SmallIntegerField()
    yrorder = models.SmallIntegerField(db_column='yrOrder')  # Field name made lowercase.
    ssref = models.TextField(db_column='ssRef')  # Field name made lowercase.
    priority = models.IntegerField()
    notes = models.TextField()
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    tstamp = models.DateTimeField()
    acckey = models.IntegerField(db_column='accKey')  # Field name made lowercase.
    yeargivenform = models.CharField(db_column='yearGivenForm', max_length=25, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'ScDate'


class Scsource(models.Model):
    ssourcekey = models.AutoField(db_column='sSourceKey', primary_key=True)  # Field name made lowercase.
    ssourceid = models.CharField(db_column='sSourceID', max_length=50)  # Field name made lowercase.
    ssourcefullref = models.TextField(db_column='sSourceFullRef')  # Field name made lowercase.
    notes = models.TextField()
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    tstamp = models.DateTimeField()

    class Meta:
        
        db_table = 'ScSource'


class Seal(models.Model):
    sealkey = models.IntegerField(db_column='sealKey', primary_key=True)  # Field name made lowercase.
    collectionkey = models.IntegerField(db_column='collectionKey')  # Field name made lowercase.
    collectionref = models.IntegerField(db_column='collectionRef')  # Field name made lowercase.
    sealorder = models.IntegerField(db_column='sealOrder')  # Field name made lowercase.
    boulloterion = models.ForeignKey('Boulloterion',db_column='boulloterionKey')  # Field name made lowercase.

    class Meta:
        
        db_table = 'Seal'


class Sexauth(models.Model):
    id = models.AutoField(db_column='sexKey', primary_key=True)  # Field name made lowercase.
    sexvalue = models.CharField(db_column='sexValue', max_length=25)  # Field name made lowercase.

    def __unicode__(self):
        return self.sexvalue

    class Meta:
        
        db_table = 'SexAuth'


class Source(models.Model):
    id = models.SmallIntegerField(db_column='sourceKey', primary_key=True)  # Field name made lowercase.
    sourceid = models.CharField(db_column='sourceID', max_length=50)  # Field name made lowercase.
    sourcebib = models.TextField(db_column='sourceBib')  # Field name made lowercase.

    def __unicode__(self):
        return self.sourceid

    class Meta:
        
        db_table = 'Source'


class Type(models.Model):
    typekey = models.IntegerField(db_column='typeKey', primary_key=True)  # Field name made lowercase.
    typename = models.TextField(db_column='typeName')  # Field name made lowercase.

    class Meta:
        
        db_table = 'Type'


class User(models.Model):
    userkey = models.AutoField(db_column='userKey', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='userName', max_length=20)  # Field name made lowercase.
    namedisplay = models.CharField(db_column='nameDisplay', max_length=100)  # Field name made lowercase.
    passwd = models.CharField(max_length=100)
    initials = models.CharField(max_length=5)

    class Meta:
        
        db_table = 'User'


class Vnamefactoid(models.Model):
    #factoidkey = models.IntegerField(db_column='factoidKey', primary_key=True)  # Field name made lowercase.
    #vnamekey = models.IntegerField(db_column='vnameKey')  # Field name made lowercase.
    factoid = models.ForeignKey('Factoid',db_column='factoidKey')
    variantname = models.ForeignKey('Variantname',db_column='vnamekey')

    class Meta:
        
        db_table = 'VNameFactoid'


class Variantname(models.Model):
    vnamekey = models.AutoField(db_column='vnameKey', primary_key=True)  # Field name made lowercase.
    olangkey = models.IntegerField(db_column='oLangKey')  # Field name made lowercase.
    name = models.CharField(max_length=50)
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    tstamp = models.DateTimeField()

    class Meta:
        
        db_table = 'VariantName'

#Wagtail
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