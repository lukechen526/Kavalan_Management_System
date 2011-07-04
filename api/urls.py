from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import *

document_handler = Resource(DocumentHandler, authentication=DefaultAuthenticationHandler())

urlpatterns = patterns('',
    url(r'^documents/',document_handler, {'emitter_format':'json'}),
)

  