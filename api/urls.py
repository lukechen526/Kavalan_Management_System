"""
A common entry point for API handlers placed under other app directories
"""
from django.conf.urls.defaults import *
from piston.resource import Resource
from api.utils import DefaultAuthenticationHandler
from doc_engine.api import *
from stream.api import *

document_handler = Resource(DocumentHandler, authentication=DefaultAuthenticationHandler())
batch_record_handler = Resource(BatchRecordHandler, authentication=DefaultAuthenticationHandler())
stream_handler = Resource(StreamHandler, authentication=DefaultAuthenticationHandler())

urlpatterns = patterns('',
    url(r'^documents$',document_handler),
    url(r'^batchrecords$', batch_record_handler ),
    url(r'^stream$', stream_handler),
)

  