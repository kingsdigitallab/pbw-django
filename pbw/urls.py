# from ddhldap.signal_handlers import register_signal_handlers as \
# ddhldap_register_signal_handlers

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailsearch.urls import frontend as wagtailsearch_frontend_urls

from views import PBWFacetedSearchView, PersonDetailView, PersonJsonView, AutoCompleteView


admin.autodiscover()
# ddhldap_register_signal_handlers()


urlpatterns = [url(r'^grappelli/', include('grappelli.urls')),
               url(r'^admin/', include(admin.site.urls)),
               #url(r'^admin/', include(wagtailadmin_urls)),
               url(r'^wagtail/', include(wagtailadmin_urls)),
               url(r'^search/', include(wagtailsearch_frontend_urls)),
               url(r'^documents/', include(wagtaildocs_urls)),

               url(r'^browse/',
                   PBWFacetedSearchView.as_view(),
                   name='pbw_browse'),
               url(r'^person/(?P<pk>\d+)/$',
                   PersonDetailView.as_view(),
                   name='person-detail'),
               url(r'^person/json/(?P<pk>\d+)/$',
                   PersonJsonView.as_view(),
                   name='person-json'),

               url(r'^autocomplete/',
                   AutoCompleteView.as_view(),
                   name='pbw_autocomplete'),
               # For anything not caught by a more specific rule above, hand over to
               # Wagtail's serving mechanism
               url(r'^', include(wagtail_urls)),
]

# -----------------------------------------------------------------------------
# Django Debug Toolbar URLS
# -----------------------------------------------------------------------------
try:
    if settings.DEBUG:
        import debug_toolbar

        urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)), )

except ImportError:
    pass

# -----------------------------------------------------------------------------
# Static file DEBUGGING
# -----------------------------------------------------------------------------
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    import os.path

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL + 'images/',
                          document_root=os.path.join(settings.MEDIA_ROOT,
                                                     'images'))
