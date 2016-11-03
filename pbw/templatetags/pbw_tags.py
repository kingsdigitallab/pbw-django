from django import template
from pbw.models import *
import re
from django.core.urlresolvers import reverse
import HTMLParser
register = template.Library()


@register.filter
def get_item(dictionary, key):
    if dictionary:
        return dictionary[key]

    return None

#Replaces the custom tags denoting a link to a person with a proper link.
@register.filter
def add_persref_links(desc):
    h = HTMLParser.HTMLParser()
    desc=h.unescape(desc)
    parsedDesc=desc
    m=re.findall("\<PERSREF ID=\"(\d+)\"\/\>",desc)
    if m:
        for tag in re.finditer("<PERSREF ID=\"(\d+)\"/>",desc):
            id=tag.group(1)
            fps=Factoidperson.objects.filter(id=id)
            if fps.count() > 0:
                fp=fps[0]
                person=fp.person
                personTag=u"<a href=\""+reverse('person-detail',args=[person.id])+"\">"+person.name+" "+unicode(person.mdbcode)+"</a>"
                parsedDesc=parsedDesc.replace(tag.group(0),personTag)
    return parsedDesc

#Get the authority label attached to the factoid
@register.filter
def get_authority_list(factoid):
    try:
        if factoid.factoidtype.typename == "Ethnic label":
            fes= Ethnicityfactoid.objects.filter(factoid=factoid)
            if fes.count() > 0:
                fe=fes[0]
                return fe.ethnicity.ethname
        elif factoid.factoidtype.typename == "Location":
            fls = Factoidlocation.objects.filter(factoid=factoid)
            if fls.count() > 0:
                fl=fls[0]
                return fl.location.locname
        elif factoid.factoidtype.typename == "Dignity/Office":
            dls = Dignityfactoid.objects.filter(factoid=factoid)
            if dls.count() > 0:
                dl=dls[0]
                return dl.dignityoffice.stdname
        elif factoid.factoidtype.typename == "Occupation":
            ols  = Occupationfactoid.objects.filter(factoid=factoid)
            if ols.count() > 0:
                ol = ols[0]
                return ol.occupation.occupationname
        elif factoid.factoidtype.typename == "Language Skill":
            lls = Langfactoid.objects.filter(factoid=factoid)
            if lls.count() > 0:
                ll=lls[0]
                return ll.languageskill.languagename
        elif factoid.factoidtype.typename == "Alternative Name":
            vls = Vnamefactoid.objects.filter(factoid=factoid)
            if vls.count() > 0:
                vl=vls[0]
                return vl.variantname.name
        elif factoid.factoidtype.typename == "Religion":
            rls = Religionfactoid.objects.filter(factoid=factoid)
            if rls.count() > 0:
                rl=rls[0]
                return rl.Religion.religionname
        elif factoid.factoidtype.typename == "Possession":
            pls = Possessionfactoid.objects.filter(factoid=factoid)
            if pls.count() > 0:
                pl=pls[0]
                return pl.possessionName
        elif factoid.factoidtype.typename == "Second Name":
            sls=Famnamefactoid.objects.filter(factoid=factoid)
            if sls.count() >0:
                sl=sls[0]
                fm=Familyname.objects.get(id=sl.famnamekey)
                return fm.famname

    except Exception:
        pass
    return factoid.engdesc

#Filter the selected facets by filter and return as query string
@register.filter(is_safe=True)
def filter_selected_facets(form,filter):
    selected_facets="?"
    for key,value in form.cleaned_data.iteritems():
         if key != filter and len(value) > 0:
             if len(selected_facets) > 1:
                 selected_facets+="&"
             selected_facets+=str(key)+"="+unicode(value)
    if len(selected_facets) > 1:
                 selected_facets+="&"
    return selected_facets


@register.assignment_tag(takes_context=True)
def get_site_root(context):
    """Returns the site root Page, not the implementation-specific model used.

    :rtype: `wagtail.wagtailcore.models.Page`
    """
    if 'BASE_URL' in context:
        return Page.objects.filter(slug=context['BASE_URL']).first()
    else:
        return context['request'].site.root_page

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