from django.conf.urls.defaults import *
from django.views.generic import ListView
from doc_engine.models import Document

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Document, context_object_name='document_list')),
)