import html.parser
import re
from django import template
from django.urls import reverse
from django.utils.html import format_html
from haystack.utils import Highlighter
from wagtail.core.models import Page
from wagtail.core.models import Site
from pbw.models import Dignityfactoid, Occupationfactoid, Langfactoid, \
    Vnamefactoid, Religionfactoid, Possessionfactoid, Famnamefactoid, \
    Kinfactoid, Familyname, Scdate
from pbw.models import Factoidperson, Ethnicityfactoid, Factoidlocation, Location

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if dictionary and key in dictionary:
        return dictionary[key]

    return None


@register.filter
def get_item_count(floruits, floruit):
    for f in floruits:
        if floruit == f[0]:
            return f[1]
    return 0


# Replaces the custom tags denoting a link to a person with a proper link.
@register.filter
def add_persref_links(desc):
    h = html.parser.HTMLParser()
    desc = h.unescape(desc)
    parsedDesc = desc
    m = re.findall("\<PERSREF ID=\"(\d+)\"\/\>", desc)
    if m:
        for tag in re.finditer("<PERSREF ID=\"(\d+)\"/>", desc):
            id = tag.group(1)
            fps = Factoidperson.objects.filter(id=id)
            if fps.count() > 0:
                fp = fps[0]
                person = fp.person
                personTag = "<a href=\"" + \
                            reverse(
                                'person-detail', args=[person.id]) +\
                    "\">" + person.name + " " + \
                    str(person.mdbcode) + "</a>"
                parsedDesc = parsedDesc.replace(tag.group(0), personTag)
    return parsedDesc

# Add the Pleiades and Geonames links for a location factoid
# if present
# update Location set geonames_id=361885,pleiades_id=501325 where locname='Abydos';
@register.simple_tag()
def get_linked_location_uris(factoid):
    locations = Location.objects.filter(factoidlocation__factoid=factoid)
    linkdict = {}
    if locations.count() >0:
        location = locations[0]
        if location.geonames_id:
            linkdict['geonames'] = "http://sws.geonames.org/{}/".format(location.geonames_id)
        if location.pleiades_id:
            linkdict['pleiades'] = "https://pleiades.stoa.org/places/{}".format(location.pleiades_id)
    return linkdict


# A modification of the highlighter to make it play nice with add_persref


@register.simple_tag()
def highlighted_persref(text, query, **kwargs):
    highlight = Highlighter(
        query, html_tag='strong', css_class='found', max_length=120)
    phText = highlight.highlight(text)
    parsedText = add_persref_links(phText)
    return format_html(parsedText)


# Get the authority list label attached to the factoid
@register.simple_tag()
def get_authority_list(factoid):
    authority = ''
    try:
        if factoid.factoidtype.typename == "Ethnic label":
            fes = Ethnicityfactoid.objects.filter(factoid=factoid)
            if fes.count() > 0:
                fe = fes[0]
                authority = fe.ethnicity.ethname
        elif factoid.factoidtype.typename == "Location":
            fls = Factoidlocation.objects.filter(factoid=factoid)
            if fls.count() > 0:
                fl = fls[0]
                authority = fl.location.locname
        elif factoid.factoidtype.typename == "Dignity/Office":
            dls = Dignityfactoid.objects.filter(factoid=factoid)
            if dls.count() > 0:
                dl = dls[0]
                authority = dl.dignityoffice.stdname
        elif factoid.factoidtype.typename == "Occupation":
            ols = Occupationfactoid.objects.filter(factoid=factoid)
            if ols.count() > 0:
                ol = ols[0]
                authority = ol.occupation.occupationname
        elif factoid.factoidtype.typename == "Language Skill":
            lls = Langfactoid.objects.filter(factoid=factoid)
            if lls.count() > 0:
                ll = lls[0]
                authority = ll.languageskill.languagename
        # elif factoid.factoidtype.typename == "Alternative Name":
        #     vls = Vnamefactoid.objects.filter(factoid=factoid)
        #     if vls.count() > 0:
        #         vl = vls[0]
        #         authority = vl.variantname.name
        elif factoid.factoidtype.typename == "Religion":
            rls = Religionfactoid.objects.filter(factoid=factoid)
            if rls.count() > 0:
                rl = rls[0]
                authority = rl.Religion.religionname
        elif factoid.factoidtype.typename == "Possession":
            pls = Possessionfactoid.objects.filter(factoid=factoid)
            authority = ""
            if pls.count() > 0:
                pl = pls[0]
                authority = pl.possessionname
            if len(authority) == 0:
                authority = factoid.engdesc
        elif factoid.factoidtype.typename == "Second Name":
            sls = Famnamefactoid.objects.filter(factoid=factoid)
            if sls.count() > 0:
                sl = sls[0]
                fm = Familyname.objects.get(id=sl.famnamekey)
                authority = fm.famname
        elif "Narrative" in factoid.factoidtype.typename:
            scdates = Scdate.objects.filter(factoid=factoid).order_by("year")
            if scdates.count() > 0:
                scdate = scdates[0]
                authority = str(scdate.year)

        elif "Kinship" in factoid.factoidtype.typename:
            kfs = Kinfactoid.objects.filter(factoid=factoid)
            if kfs.count() > 0:
                kf = kfs[0]
                authority = kf.kinship.gspecrelat

        else:
            authority = factoid.engdesc
    except Exception:
        pass
        authority = factoid.engdesc
    return authority


# Test if the authority entry in factoid list is the same as the last


@register.simple_tag(takes_context=True)
def sameAsLast(context, authority):
    try:
        if authority != context['lastAuthority']:
            context['lastAuthority'] = authority
            return False
        else:
            return True
    except KeyError:
        context['lastAuthority'] = ''
        return False


# Filter the selected facets by filter and return as query string
@register.filter(is_safe=True)
def filter_selected_facets(form, filter):
    selected_facets = "?"
    if form.is_valid():
        for key, value in form.cleaned_data.items():
            if key != filter and len(value) > 0:
                if len(selected_facets) > 1:
                    selected_facets += "&"
                selected_facets += str(key) + "=" + str(value)
        if len(selected_facets) > 1:
            selected_facets += "&"
    return selected_facets


@register.simple_tag(takes_context=True)
def get_site_root(context):
    """Returns the site root Page, not the implementation-specific model used.

    :rtype: `wagtail.core.models.Page`
    """
    if 'BASE_URL' in context:
        return Page.objects.filter(slug=context['BASE_URL']).first()
    else:
        return Site.find_for_request(context["request"]).root_page


@register.inclusion_tag('pbw/tags/main_menu.html', takes_context=True)
def main_menu(context, root, current_page=None):
    """Returns the main menu items, the children of the root page. Only live
    pages that have the show_in_menus setting on are returned."""
    menu_pages = root.get_children().live().in_menu()

    root.active = (current_page.url == root.url
                   if current_page else False)

    for page in menu_pages:
        page.active = (current_page.url.startswith(page.url)
                       if current_page else False)

    return {'request': context['request'], 'root': root,
            'current_page': current_page, 'menu_pages': menu_pages}


@register.inclusion_tag('pbw/tags/footer_menu.html', takes_context=True)
def footer_menu(context, root, current_page=None):
    """Returns the main menu items, the children of the root page. Only live
    pages that have the show_in_menus setting on are returned."""
    menu_pages = root.get_children().live().in_menu()

    root.active = (current_page.url == root.url
                   if current_page else False)

    for page in menu_pages:
        page.active = (current_page.url.startswith(page.url)
                       if current_page else False)

    return {'request': context['request'], 'root': root,
            'current_page': current_page, 'menu_pages': menu_pages}
