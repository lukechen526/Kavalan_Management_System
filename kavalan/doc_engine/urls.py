from django.conf.urls.defaults import *
from doc_engine.views import DocumentIndexView, document_access
from doc_engine.api import *
from django.contrib.auth.decorators import login_required
from piston_support.utils import SessionAuthenticationHandler
from piston.resource import Resource

document_handler = Resource(DocumentHandler, authentication=SessionAuthenticationHandler())
batch_record_handler = Resource(BatchRecordHandler, authentication=SessionAuthenticationHandler())

urlpatterns = patterns('',
    url(r'^$', login_required(DocumentIndexView.as_view())),
    url(r'^access/(?P<pk>\d+)/?$', login_required(document_access), name='document_access'),
    url(r'^api/documents/?$',document_handler, { 'emitter_format': 'page_json' }),
    url(r'^api/documents/(?P<document_id>\d+)/?$',document_handler, { 'emitter_format': 'page_json' }),
    url(r'^api/batchrecords/?$', batch_record_handler, { 'emitter_format': 'page_json' } ),
    url(r'^api/batchrecords/(?P<batchrecord_id>\d+)/?$', batch_record_handler, { 'emitter_format': 'page_json' } ),

    url(r'^search/', include('haystack.urls')),


)



