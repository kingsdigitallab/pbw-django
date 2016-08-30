# from ddhldap.signal_handlers import register_signal_handlers as \
#     ddhldap_register_signal_handlers

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from views import PBWFacetedSearchView,PersonDetailView,PersonJsonView



admin.autodiscover()
# ddhldap_register_signal_handlers()


urlpatterns = [url(r'^grappelli/', include('grappelli.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^search/',
                           PBWFacetedSearchView.as_view(),
                           name='pbw_haystack_search'),
                       url(r'^person/(?P<pk>\d+)/$',
                            PersonDetailView.as_view(),
                            name='person-detail'),
                       url(r'^person/json/(?P<pk>\d+)/$',
                            PersonJsonView.as_view(),
                            name='person-json')
                       ]

# -----------------------------------------------------------------------------
# Django Debug Toolbar URLS
# -----------------------------------------------------------------------------
try:
    if settings.DEBUG:
        import debug_toolbar
        urlpatterns.append(url(r'^__debug__/',include(debug_toolbar.urls)),)

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
