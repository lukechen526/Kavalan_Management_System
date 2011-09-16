"""
A common entry point for API handlers placed under other app directories
"""
from django.conf.urls.defaults import *
from piston.resource import Resource
from api.utils import SessionAuthenticationHandler
from api.emitters import *

#Import API module of other systems
from doc_engine.api import *
from stream.api import *


class CsrfExemptResource(Resource):
    """A Custom Resource that is csrf exempt"""
    def __init__(self, handler, authentication=None):
        super(CsrfExemptResource, self).__init__(handler, authentication)
        self.csrf_exempt = getattr(self.handler, 'csrf_exempt', True)

document_handler = Resource(DocumentHandler, authentication=SessionAuthenticationHandler())
batch_record_handler = Resource(BatchRecordHandler, authentication=SessionAuthenticationHandler())
stream_handler = CsrfExemptResource(StreamHandler, authentication=SessionAuthenticationHandler())
stream_comment_handler = CsrfExemptResource(StreamCommentHandler, authentication=SessionAuthenticationHandler())


#The Golden Rule of API URL: End points should NOT have a trailing slash. However, the url patterns are written so that
#even if the trailing slash is present, the reqeust will still get dispatched correctly without redirect, by putting '/?$' at the end.

urlpatterns = patterns('',
    #URLs for Doc Engine
    url(r'^documents/?$',document_handler, { 'emitter_format': 'page_json' }),
    url(r'^documents/(?P<document_id>\d+)/?$',document_handler, { 'emitter_format': 'page_json' }),
    
    url(r'^batchrecords/?$', batch_record_handler, { 'emitter_format': 'page_json' } ),
    url(r'^batchrecords/(?P<batchrecord_id>\d+)/?$', batch_record_handler, { 'emitter_format': 'page_json' } ),

    #URLs for Stream
    url(r'^stream/?$', stream_handler),
    url(r'^stream/(?P<post_id>\d+)/?$', stream_handler),
    url(r'stream/(?P<post_id>\d+)/comments/?$', stream_comment_handler),
    url(r'stream/(?P<post_id>\d+)/comments/(?P<comment_id>\d+)/?$', stream_comment_handler)

)


