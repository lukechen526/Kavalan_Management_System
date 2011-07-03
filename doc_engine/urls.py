from django.conf.urls.defaults import *
from doc_engine.views import DocumentIndexView, DocumentListView, DocumentSearchView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', login_required(DocumentIndexView.as_view())),
    url(r'^list', login_required(DocumentListView.as_view())),
    url(r'^search', login_required(DocumentSearchView)),
)



