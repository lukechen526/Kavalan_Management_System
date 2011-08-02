from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from stream.views import StreamIndexView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', StreamIndexView.as_view() ),
    url(r'^doc_engine/', include('doc_engine.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^api/', include('api.urls')),
    
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.DOCUMENT_URL, document_root=settings.DOCUMENTATION_ROOT)

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('Kavalan_Management_System',),
}
urlpatterns += patterns('',
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
)