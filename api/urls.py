"""
A common entry point for API handlers placed under other app directories
"""
from django.conf.urls.defaults import *
from piston.resource import Resource
from api.utils import DefaultAuthenticationHandler
from doc_engine.api import *

document_handler = Resource(DocumentHandler, authentication=DefaultAuthenticationHandler())

urlpatterns = patterns('',
    url(r'^documents/',document_handler, {'emitter_format':'json'}),
)

  