from django import template
from pbw.models import *

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if dictionary:
        return dictionary[key]

    return None

#Replaces the custom tags denoting a link to a person with a proper link.
@register.filter
def add_persref_links(desc):

    return desc

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
    except Exception:
        pass
    return None

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