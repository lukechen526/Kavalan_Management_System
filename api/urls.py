"""
A common entry point for API handlers placed under other app directories
"""
from django.conf.urls.defaults import *
from piston.resource import Resource
from api.utils import DefaultAuthenticationHandler
from doc_engine.api import *
from stream.api import *

class CsrfExemptResource(Resource):
    """A Custom Resource that is csrf exempt"""
    def __init__(self, handler, authentication=None):
        super(CsrfExemptResource, self).__init__(handler, authentication)
        self.csrf_exempt = getattr(self.handler, 'csrf_exempt', True)

document_handler = Resource(DocumentHandler, authentication=DefaultAuthenticationHandler())
batch_record_handler = Resource(BatchRecordHandler, authentication=DefaultAuthenticationHandler())
stream_handler = CsrfExemptResource(StreamHandler, authentication=DefaultAuthenticationHandler())

urlpatterns = patterns('',
    url(r'^documents$',document_handler),
    url(r'^batchrecords$', batch_record_handler ),
    url(r'^stream/(?P<post_id>\d*)$', stream_handler),
)

  