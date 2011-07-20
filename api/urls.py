"""
A common entry point for API handlers placed under other app directories
"""
from django.conf.urls.defaults import *
from piston.resource import Resource
from api.utils import DefaultAuthenticationHandler
from doc_engine.api import *
from hermes.api import *

document_handler = Resource(DocumentHandler, authentication=DefaultAuthenticationHandler())
batch_record_handler = Resource(BatchRecordHandler, authentication=DefaultAuthenticationHandler())
request_key_secret_pair_handler = Resource(RequestKeySecretPairHandler, authentication=DefaultAuthenticationHandler())
test_authentication_handler = Resource(TestAuthenticationHandler, authentication=HAuthenticationHandler())

urlpatterns = patterns('',
    url(r'^documents$',document_handler),
    url(r'^batchrecords$', batch_record_handler ),
    url(r'^hermes/request_key_secret_pair$', request_key_secret_pair_handler),
    url(r'^hermes/test_authentication$', test_authentication_handler),
)

  