from django.conf.urls.defaults import *
from doc_engine.views import DocumentIndexView, DocumentListView, DocumentSearchView

urlpatterns = patterns('',
    url(r'^$', DocumentIndexView.as_view() ),
    url(r'^list/$', DocumentListView.as_view()),
    url(r'^search/$', DocumentSearchView),
)



