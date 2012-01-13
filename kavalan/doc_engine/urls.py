from django.conf.urls.defaults import *
from doc_engine.views import DocumentIndexView, document_access, autocomplete
from doc_engine.api import *
from django.contrib.auth.decorators import login_required
from piston_support.utils import SessionAuthenticationHandler
from piston.resource import Resource
from haystack.views import SearchView, search_view_factory
from haystack.forms import HighlightedSearchForm
from doc_engine.emitters import *

#document_handler = Resource(DocumentHandler, authentication=SessionAuthenticationHandler())
batch_record_handler = Resource(BatchRecordHandler, authentication=SessionAuthenticationHandler())

urlpatterns = patterns('',
    url(r'^$', login_required(DocumentIndexView.as_view()), name='index'),
    url(r'^access/(?P<pk>\d+)/?$', login_required(document_access), name='document_access'),
    url(r'^api/documents/?$',document_search_view),
    url(r'^api/documents/(?P<document_id>\d+)/?$',document_search_view),
    url(r'^api/batchrecords/?$', batch_record_handler, { 'emitter_format': 'page_json' } ),
    url(r'^api/batchrecords/(?P<batchrecord_id>\d+)/?$', batch_record_handler, { 'emitter_format': 'page_json' } ),
    url(r'^autocomplete/', autocomplete)

)

urlpatterns += patterns('haystack.views',
    url(r'^search/$',
        search_view_factory(view_class=SearchView,form_class= HighlightedSearchForm),
        name='search'
    ),


)

